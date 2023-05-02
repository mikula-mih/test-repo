from __future__ import annotations
import itertools
from typing import Iterable, DefaultDict
from collections import defaultdict, Counter


# Splitting the data
def training(s: Sample, i: int) -> bool:
    pass

training_samples = [
    TrainingKnownSample(s)
    for i, s in enumerate(samples)
    if training(s, i)]

test_samples = [
    TestingKnownSample(s)
    for i, s in enumerate(samples)
    if not training(s, i)]

# the `partition()` function
def training_80(s: KnownSample, i: int) -> bool:
    return i % 5 != 0

def training_75(s: KnownSample, i: int) -> bool:
    return i % 4 != 0

def training_67(s: KnownSample, i: int) -> bool:
    return i % 3 != 0
#
def partition(
    samples: Iterable[KnownSample],
    rule: Callable[[KnownSample, int], bool]
) -> Tuple[TrainingList, TestingList]:

    training_samples = [
        TrainingKnownSample(s)
        for i, s in enumerate(samples) if rule(s, i)
    ]

    test_samples = [
        TestingKnownSample(s)
        for i, s in enumerate(samples) if not rule(s, i)
    ]

    return training_samples, test_samples

# One-pass partition
def partition_1(
    samples: Iterable[KnownSample],
    rule: Callable[[KnownSample, int], bool]
) -> Tuple[TrainingList, TestingList]:

    training: TrainingList = []
    testing: TestingList = []

    for i, s in enumerate(samples):
        training_use = rule(s, i)
        if training_use:
            training.append(TrainingKnownSample(s))
        else:
            testing.append(TestingKnownSample(s))

    return training, testing

def partition_1p(
    samples: Iterable[KnownSample],
    rule: Callable[[KnownSample], int], bool]
) -> tuple[TrainingList, TestingList]:

    pools: defaultdict[bool, list[KnownSample]] = dafaultdict(list)
    partition = ((rule(s, i), s) for i, s in enumerate(samples))
    for usage_pool, sample in partition:
        pools[usage_pool].append(sample)

    training = [TrainingKnownSample(s) for s in pools[True]]
    testing = [TestingKnownSample(s) for s in pools[False]]
    return training, testing


"""CSV format designs"""
#
test = TestingKnownSample(
    species=row["species"],
    sepal_length=float(row["sepal_length"]),
    sepal_width=float(row["sepal_width"]),
    petal_length=float(row["petal_length"]),
    petal_width=float(row["petal_width"]),
)
# CSV dictionary reader
class CSVIrisReader:
    """
    Attribute Information:
        1. sepal length in cm
        2. sepal width in cm
        3. petal length in cm
        4. petal width in cm
        5. class:
            -- Iris Setosa
            -- Iris Versicolour
            -- Iris Virginica
    """

    header = [
        "sepal_length", # in cm
        "sepal_width", # in cm
        "petal_length", # in cm
        "petal_width", # in cm
        "species", # Iris-setosa, Iris-versicolour, Iris-virginica
    ]

    def __init__(self, source: Path) -> None:
        self.source = source

    def data_iter(self) -> Iterator[dict[str, str]]:
        with self.source.open() as source_file:
            reader = csv.DictReader(source_file, self.header)
            yield from reader

JSON = Union[
    None, bool, int, float, str, List['JSON'], Dict[str, 'JSON']
]

JSON_Samples = List[Dict[str, Union[float, str]]]

class JSONIrisReader:
    def __init__(self, source: Path) -> None:
        self.source = source

    def data_iter(self) -> Iterator[SampleDict]:
        with self.source.open() as source_file:
            sample_list = json.load(source_file)
        yield from iter(sample_list)

class NDJSONIrisReader:
    def __init__(self, source: Path) -> None:
        self.source = source

    def data_iter(self) -> Iterator[SampleDict]:
        with self.source.open() as source_file:
            for line in source_file:
                sample = json.loads(line)
                yield sample
# >>> python -m pip install jsonschema
class ValidatingNDJSONIrisReader:
    def __init__(self, source: Path, schema: dict[str, Any]) -> None:
        self.source = source
        self.validator = jsonschema.Draft7Validator(schema)

    def data_iter(self) -> Iterator[Sampledict]:
        with self.source.open() as source_file:
            for line in source_file:
                sample = json.loads(line)
                if self.validator.is_valid(sample):
                    yield sample
                else:
                    print(f"Invalid: {sample}")
#
""" the `Iterator pattern` """
ModuloDict = DefaultDict[int, List[KnownSample]]

def partition_2(
    samples: Iterable[KnownSample],
    training_rule: Callable[[int], bool]
) -> tuple[TrainingList, TestingList]:

    rule_multiple = 60
    partitions: ModuloDict = collections.defaultdict(list)
    for s in samples:
        partitions[hash(s) % rule_multiple].append(s)

    training_partitions: list[Iterator[TrainingKnownSample]] = []
    testing_partitions: list[Iterator[TestingKnownSample]] = []
    for i, p in enumerate(partitions.values()):
        if training_rule(i):
            training_partitions.append(
                TrainingKnownSample(s) for s in p)
        else:
            testing_partitions.append(
                TestingKnownSample(s) for s in p)

    training = list(itertools.chain(*training_partitons))
    resting = list(itertools.chain(*testing_partitions))
    return training, testing
#
# Testing
Classifier = Callable[
    [int, DistanceFunc, TrainingList, AnySample], str]

class Hyperparameter(NamedTuple):
    k: int
    distance_function: DistanceFunc
    training_data: TrainingList
    classifier: Classifier

    def classify(self, unknown: AnySample) -> str:
        classifier = self.classifier
        return classifier(
            self.k, self.distance_function,
            self.training_data,
            unknown
        )

    def test(self, testing: TestingList) -> int:
        classifier = self.classifier
        test_results = (
            ClassifiedKnownSample(
                t.sample,
                classifier(
                    self.k, self.distance_function,
                    self.training_data, t.sample
                ),
            )
            for t in testing
        )
        pass_fail = map(
            lambda t: (
                1 if t.sample.species == t.classification else 0),
            test_results
        )
        return sum(pass_fail))
####
