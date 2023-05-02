from __future__ import annotations
from typing import Protocol
from collections import Counter
from math import hypot
import time

""" Common Design Patterns """

class Distance(Protocol):

    def distance(
        self,
        s1: TrainingKnownSample,
        s2: AnySample
    ) -> float:
        ...

class Euclidean(Distance):
    def distance(self, s1: TrainingKnownSample, s2: AnySample) -> float:
        return hypot(
            (s1.sample.sample.sepal_length - s2.sample.sepal_length)**2,
            (s1.sample.sample.sepal_width - s2.sample.sepal_width)**2,
            (s1.sample.sample.petal_length - s2.sample.petal_length)**2,
            (s1.sample.sample.petal_width - s2.sample.petal_width)**2,
        )

class Manhattan(Distance):
    def distance(self, s1: TrainingKnownSample, s2: AnySample) -> float:
        return sum(
            [
                abs(s1.sample.sample.sepal_length - s2.sample.sepal_length),
                abs(s1.sample.sample.sepal_width - s2.sample.sepal_width),
                abs(s1.sample.sample.petal_length - s2.sample.petal_length),
                abs(s1.sample.sample.petal_width - s2.sample.petal_width),
            ]
        )

class Chebyshev(Distance):
    def distance(self, s1: TrainingKnownSample, s2: AnySample) -> float:
        return max(
            [
                abs(s1.sample.sample.sepal_length - s2.sample.sepal_length),
                abs(s1.sample.sample.sepal_width - s2.sample.sepal_width),
                abs(s1.sample.sample.petal_length - s2.sample.petal_length),
                abs(s1.sample.sample.petal_width - s2.sample.petal_width),
            ]
        )

def k_nn_1(
    k: int,
    dist: DistanceFunc,
    training_data: TrainingList,
    unknown: AnySample
) -> str:
    distances = sorted(
        map(lambda t: Measured(dist(t, unknown), t), training_data))
    k_nearest = distances[:k]
    k_frequencies: Counter[str] = Counter(
        s.sample.sample.species for s in k_nearest
    )
    mode, fq = k_frequencies.most_common(1)[0]
    return mode

class Hyperparameter(NamedTuple):
    k: int
    distance: Distance
    training_data: TrainingList
    classifier: Classifier

    def classify(self, unknown: AnySample) -> str:
        classifier = self.classifier
        distance = self.distance
        return classifier(
            self.k, distance.distance, self.training_data, unknown)

    def test(self, testing: TestingList) -> float:
        classifier = self.classifier
        distance = self.distance
        test_results = (
            ClassifiedKnownSample(
                t.sample,
                classifier(
                    self.k, distance.distance,
                    self.training_data, t.sample),
            )
            for t in testing
        )
        pass_fail = map(
            lambda t: (1 if t.sample.species == t.classification else 0),
            test_results
        )
        return sum(pass_fail) / len(testing)

class Timing(NamedTuple):
    k: int
    distance_name: str
    classifier_name: str
    quality: float
    time: float # Milliseconds

class TestCommand:
    def __init__(
        self,
        hyper_param: Hyperparameter,
        testing: TestingList,
    ) -> None:
        self.hyperparameter = hyper_param
        self.testing_samples = testing

    def test(self) -> Timing:
        start = time.perf_counter()
        recall_score = self.hyperparameter.test(self.testing_samples)
        end = time.perf_counter()
        timing = Timing(
            k=self.hyperparameter.k,
            distance_name=
                self.hyperparameter.distance.__class__.__name__,
            classifier_name=
                self.hyperparameter.classifier.__name__,
            quality=recall_score,
            time=round((end - start) * 1000.0, 3),
        )
        return timing

    def tuning(source: Path) -> None:
        train, test = load(source)
        scenarios = [
            TestCommand(Hyperparameter(k, df, train, cl), test)
            for k in range(3, 33, 2)
            for df in (euclidean, manhattan, chebyshev)
            for cl in (k_nn_1, k_nn_b, k_nn_q)
        ]
        timings = [s.test() for s in scenarios]
        for t in timings:
            if t.quality >= 1.0:
                print(t)
####
####
data = [
    KnownSample(sample=Sample(1, 2, 3, 4), species="a"),
    KnownSample(sample=Sample(2, 3, 4, 5), species="b"),
    KnownSample(sample=Sample(3, 4, 5, 6), species="c"),
    KnownSample(sample=Sample(4, 5, 6, 7), species="d"),
]
manhattan = Manhattan().distance
training_data = [TrainingKnownSample(s) for s in data]
h = Hyperparameter(1, manhattan, training_data, k_nn_1)
h.classify(UnknownSample(Sample(2, 3, 4, 5)))








#
