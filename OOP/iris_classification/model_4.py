



""" the essential k-NN algorithm """

class Measured(NamedTuple):
    distance: float
    sample: TrainingKnownSample

def k_nn_1(
    k: int, dist: DistanceFunc, training_data: TrainingList,
    unknown: AnySample
) -> str:
    distances = sorted(
        map(
            lambda t: Measured(dist(t, unknown), t), training_data
        )
    )
    k_nearest = distances[:k]
    k_frequencies: Counter[str] = collections.Counter(
        s.sample.sample.species for s in k_nearest
    )
    mode, fq = k_frequencies.most_common(1)[0]
    return mode

# k-NN using the `bisect module`

def k_nn_b(
    k: int, dist: DistanceFunc, training_data: TrainingList,
    unknown: AnySample
) -> str:
    k_nearest = [
        Measured(float("inf"), cast(TrainingKnownSample, None))
        for _ in range(k)
    ]
    for t in training_data:
        t_dist = dist(t, unknown)
        if t_dist > k_nearest[-1].distance:
            continue
        new = Measured(t_dist, t)
        k_nearest.insert(bisect.bisect_left(k_nearest, new), new)
        k_nearest.pop(-1)
    k_frequencies: Counter[str] = collections.Counter(
        s.sample.sample.species for s in k_nearest
    )
    mode, fq = k_frequencies.most_common(1)[0]
    return mode

# k-NN using the `heapq module`

def k_nn_q(
    k: int, dist: DistanceFunc, training_data: TrainingList,
    unknown: AnySample
) -> str:
    measured_iter = (
        Measured(dist(t, unknown), t) for t in training_data)
    k_nearest = heapq.nsmallest(k, measured_iter)
    k_frequencies: Counter[str] = collections.Counter(
        s.sample.sample.species for s in k_nearest
    )
    mode, fq = k_frequencies.most_common(1)[0]
    return mode
###

def test_classifier(
        training_data: List[TrainingKnownSample],
        testing_data: List[TestingKnownSample],
        classifier: Classifier) -> None:
    h = Hyperparameter(
        k=5,
        distance_function=manhattan,
        training_data=training_data,
        classifier=classifier)
    start = time.perf_counter()
    q = h.test(testing_data)
    end = time.perf_counter()
    print(
        f'| {classifier.__name__:10s} '
        f'| q={q:5}/{len(testing_data):5} '
        f'| {end-start:6.3f}s |')


def main() -> None:
    test, train = a_lot_of_data(5_000)
    print("| algorithm | test quality | time |")
    print("|------------|---------------|---------|")
    test_classifier(test, train, k_nn_1)
    test_classifier(test, train, k_nn_b)
    test_classifier(test, train, k_nn_q)
















#
