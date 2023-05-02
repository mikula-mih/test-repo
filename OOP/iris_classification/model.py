from typing import Optional, Iterable, Iterator, TypedDict, overload
from typing import Set, List, Tuple
import abc
from enum import Enum, IntEnum
from pathlib import Path
import datetime
import random

class Sample:

    def __init__(
        self,
        sepal_length: float,
        sepal_width: float,
        petal_length: float,
        petal_width: float,
        species: Optional[str] = None,
    ) -> None:
        self.sepal_length = sepal_length
        self.sepal_width = sepal_width
        self.petal_length = petal_length
        self.petal_width = petal_width
        self.species = species
        self.classification: Optional[str] = None

    def __repr__(self) -> str:
        if self.species is None:
            known_unknown = "UnknownSample"
        else:
            known_unknown = "KnownSample"
        if self.classification is None:
            classification = ""
        else:
            classification = f", {self.classification}"

        return (
            f"{known_unknown}("
            f"sepal_length={self.sepal_length}, "
            f"sepal_width={self.sepal_width}, "
            f"petal_length={self.petal_length}, "
            f"petal_width={self.petal_width}, "
            f"species={self.species!r}"
            f"{classification}"
            f")"
        )

    def classify(self, classification: str) -> None:
        self.classification = classification

    def matches(self) -> bool:
        return self.species == self.classification

# Input valisdation
class SampleReader:
    """
    See iris.names for attribute ordering in bezdekIris.data file
    """

    target_class = Sample
    header = [
        "sepal_length", "sepal_width",
        "petal_length", "petal_width", "class"
    ]

    def __init__(self, source: Path) -> None:
        self.source = source

    def sample_iter(self) -> Iterator[Sample]:
        target_class = self.target_class
        with self.source.open() as source_file:
            reader = csv.DictReader(source_file, self.header)
            for row in reader:
                try:
                    sample = target_class(
                        sepal_length=float(row["sepal_length"]),
                        sepal_width=float(row["sepal_width"]),
                        petal_length=float(row["petal_length"]),
                        petal_width=float(row["petal_width"]),
                    )
                except ValueError as ex:
                    raise BadSampleRow(f"Invalid {row!r}") from ex
                yield sample


class BadSampleRow(ValueError):
    pass

# Input partitioning

# purpose enumeration
class Purpose(IntEnum):
    Classification = 0
    Testing = 1
    Training = 2


class Hyperparameter:
    """A hyperparameter value and the overall quality of the classification."""

    def __init__(self, k: int, training: "TrainingData") -> None:
        self.k = k
        self.data: weakref.ReferenceType["TrainingData"] = weakref.ref(training)
        self.quality: float

    def test(self) -> None:
        """Run the entire test suite."""
        training_data: Optional["TrainingData"] = self.data()
        if not training_data:
            raise RuntimeError("Broken Weak Reference")
        pass_count, fail_count = 0, 0
        for sample in training_data.testing:
            sample.classification = self.classify(sample)
            if sample.matches():
                pass_count += 1
            else:
                fail_count += 1
        self.quality = pass_count / (pass_count + fail_count)

    """ the classify algorithm of the Hyperparameter class """
    class Distance:
        """Definition of a distance computation"""
        def distance(self, s1: Sample, s2: Sample) -> float:
            pass

    """ the "Euclidean" distance """
    class ED(Distance):
        def distance(self, s1: Sample, s2: Sample) -> float:
            return hypot(
                s1.sepal_length - s2.sepal_length,
                s1.sepal_width - s2.sepal_width,
                s1.petal_length - s2.petal_length,
                s1.petal_width - s2.petal_width,
            )

    """ Manhattan distance """
    # the distance you would walk in a city with square blocks
    class MD(Distance):
        def distance(self, s1: Sample, s2: Sample) -> float:
            return sum(
                [
                    abs(s1.sepal_length - s2.sepal_length),
                    abs(s1.sepal_width - s2.sepal_width),
                    abs(s1.petal_length - s2.petal_length),
                    abs(s1.petal_width - s2.petal_width),
                ]
            )

    """ Chebyshev distance """
    # counts a diagonal step as 1
    # Manhattan computation would rank this as 2
    # the Euclidean distance would be 1.41
    class CD(Distance):
        def distance(self, s1: Sample, s2: Sample) -> float:
            return max(
                [
                    abs(s1.sepal_length - s2.sepal_length),
                    abs(s1.sepal_width - s2.sepal_width),
                    abs(s1.petal_length - s2.petal_length),
                    abs(s1.petal_width - s2.petal_width),
                ]
            )
    # Our examples are collectively identified as `Minkowski` measures because
    # they're similar and measure each axis equally. Each alternative distance
    # strategy yields different results in the model's ability to classify
    # unknown samples given a set of training data.
    class SD(Distance):
        def distance(self, s1: Sample, s2: Sample) -> float:
            return sum(
                [
                    abs(s1.sepal_length - s2.sepal_length),
                    abs(s1.sepal_width - s2.sepal_width),
                    abs(s1.petal_length - s2.petal_length),
                    abs(s1.petal_width - s2.petal_width),
                ]
            ) / sum(
                [
                    abs(s1.sepal_length + s2.sepal_length),
                    abs(s1.sepal_width + s2.sepal_width),
                    abs(s1.petal_length + s2.petal_length),
                    abs(s1.petal_width + s2.petal_width),
                ]
            )
    # `Manhattan distance` applies no matter how far from the origin we are
    # `Sorensen distance` reduces the importance of measures that are further
    # from the origin so they don't dominate the k-NN by virtue of being
    # large-valued outliers


class TrainingData:
    """A set of training data and testing data with methods to load and
        test the samples."""

    def __init__(self, name: str) -> None:
        self.name = name
        self.uploaded: datetime.datetime
        self.tested: datetime.datetime
        self.training: List[TrainingKnownSample] = []
        self.testing: List[TrainingKnownSample] = []
        self.tuning: List[Hyperparameter] = []

    def load(
        self, raw_data_iter: Iterable[dict[str, str]]
    ) -> None:
        bad_count = 0
        """Load and partition the raw data"""
        for n, row in enumerate(raw_data_iter):
            try:
                if n % 5 == 0:
                    test = TestingKnownSample.from_dict(row)
                    self.testing.append(test)
                else:
                    train = TrainingKnownSample.from_dict(row)
                    self.training.append(train)
            except InvalidSampleError as ex:
                print(f"Row {n+1}: {ex}")
                bad_count += 1
        if bad_count != 0:
            print(f"{bad_count} invalid rows")
            return
        self.uploaded = datetime.datetime.now(tz=datetime.timezone.utc)

    def test(
            self,
            parameter: Hyperparameter) -> None:
        """Test this Hyperparameter value."""
        parameter.test()
        self.tuning.append(parameter)
        self.tested = datetime.datetime.now(tz=datetime.timezone.utc)

    def classify(
            self,
            parameter: Hyperparameter,
            sample: Sample) -> Sample:
        """Classify this Sample."""
        classification = parameter.classify(sample)
        sample.classify(classification)
        return sample


class InvalidSampleError(ValueError):
    """Source data file has invalid data representation"""


class KnownSample(Sample):

    def __init__(
        self,
        species: str,
        sepal_length: float,
        sepal_width: float,
        petal_length: float,
        petal_width: float,
        purpose: int,
    ) -> None:
        purpose_enum = Purpose(purpose)
        if purpose_enum not in {Purpose.Training, Purpose.Testing}:
            raise ValueError(
                f"Invalid purpose: {purpose!r}: {purpose_enum}"
            )
        super().__init__(
            sepal_length=sepal_length,
            sepal_width=sepal_width,
            petal_length=petal_length,
            petal_width=petal_width,
        )
        self.purpose = purpose_enum
        self.species = species
        self._classification: Optional[str] = None

    def matches(self) -> bool:
        return self.species == self.classification

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"sepal_length={self.sepal_length}, "
            f"sepal_width={self.sepal_width}, "
            f"petal_length={self.petal_length}, "
            f"petal_width={self.petal_width}, "
            f"species={self.species!r}, "
            f")",
        )

    # this method is defined with the @classmethod decoration.
    @classmethod
    # any subclass that inherits this will have the method tailored for that subclass
    def from_dict(cls, row: dict[str, str]) -> "KnownSample":
        # the actual class object becomes the first parameter, `cls`
        if row["species"] not in {
                "Iris-setosa", "Iris-versicolour", "Iris-virginica"}:
            raise InvalidSampleError(f"invalid species in {row!r}")
        try:
            return cls(
                species=row["species"],
                sepal_length=float(row["sepal_length"]),
                sepal_width=float(row["sepal_width"]),
                petal_length=float(row["petal_length"]),
                petal_width=float(row["petal_width"]),
            )
        except ValueError as ex:
            raise InvalidSampleError(f"invalid {row!r}")
    # Property setters
    @property
    def classification(self) -> Optional[str]:
        if self.purpose == Purpose.Testing:
            return self._classification
        else:
            raise AttributeError(f"Training samples have no classification")

    @classification.setter
    def classification(self, value: str) -> None:
        if self.purpose == Purpose.Testing:
            self._classification = value
        else:
            raise AttributeError(
                f"Training samples cannot be classified")


class TrainingKnownSample(KnownSample):
    @classmethod
    def from_dict(cls, row: dict[str, str]) -> "TrainingKnownSample":
        return cast(TrainingKnownSample, super().from_dict(row))

class TestingKnownSample():
    pass


class OutlierError(ValueError):
    """Value lies outside the expected range."""


"""Validating enumerated values"""

class Species(Enum):
    Setosa = "Iris-setosa"
    Versicolour = "Iris-versicolour"
    Viginica = "Iris-viginica"


class Domain(Set[str]):
    def validate(self, value: str) -> str:
        if value in self:
            return value
        raise ValueError(f"invalid {value!r}")


""" extending the list class with two sublists """
class SampleDict(TypedDict):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float
    species: str


class SamplePartition(List[SampleDict], abc.ABC):
    @overload
    def __init__(self, *, training_subset: float = 0.80) -> None:
        ...

    @overload
    def __init__(
        self,
        iterable: Optional[Iterable[SampleDict]] = None,
        # the lonely `*` separates parameters where the argument value can be
        # provided positionally from parameters where the argument value must be
        # provided as a keyword;
        *,
        training_subset: float = 0.80,
    ) -> None:
        ...

    def __init__(
        self,
        iterable: Optional[Iterable[SampleDict]] = None,
        *,
        training_subset: float = 0.80,
    ) -> None:
        self.training_subset = training_subset
        if iterable:
            super().__init__(iterable)
        else:
            super().__init__()

    @abc.abstractproperty
    @property
    def training(self) -> List[TrainingKnownSample]:
        ...

    @abc.abstractproperty
    @property
    def testing(self) -> List[TestingKnownSample]:
        ...


""" suffling strategy for partitioning """

class ShufflingSamplePartition(SamplePartition):
    def __init__(
        self,
        iterable: Optional[Iterable[SampleDict]] = None,
        *,
        training_subset: float = 0.80,
    ) -> None:
        super().__init__(iterable, training_subset=training_subset)
        self.split: Optional[int] = None

    def shuffle(self) -> None:
        if not self.split:
            random.shuffle(self)
            self.split = int(len(self) * self.training_subset)

    @property
    def training(self) -> List[TrainingKnownSample]:
        self.shuffle()
        return [TrainingKnownSample(**sd) for sd in self[: self.split]]

    @property
    def testing(self) -> List[TestingKnownSample]:
        self.shuffle()
        return [TestingKnownSample(**sd) for sd in self[self.split :]]


""" incremental strategy for partitioning """

class DealingPartition(abc.ABC):
    @abc.abstractmethod
    def __init__(
        self,
        items: Optional[Iterable[SampleDict]],
        *,
        training_subset: Tuple[int, int] = (8, 10),
    ) -> None:
        ...

    @abc.abstractmethod
    def extend(self, items: Iterable[SampleDict]) -> None:
        ...

    @abc.abstractmethod
    def append(self, items: SampleDict) -> None:
        ...

    @property
    @abc.abstractmethod
    def training(self) -> List[TrainingKnownSample]:
        ...

    @property
    @abc.abstractmethod
    def testing(self) -> List[TestingKnownSample]:
        ...


class CountingDealingPartition(DealingPartition):
    def __init__(
        self,
        items: Optional[Iterable[SampleDict]],
        *,
        training_subset: Tuple[int, int] = (8, 10),
    ) -> None:
        self.training_subset = training_subset
        self.counter = 0
        self._training: List[TrainingKnownSample] = []
        self._testing: List[TestingKnownSample] = []
        if items:
            self.extend(items)

    def extend(self, items: Iterable[SampleDict]) -> None:
        for item in items:
            self.append(item)

    def append(self, item: SampleDict) -> None:
        n, d = self.training_subset
        if self.counter % d < n:
            self._training.append(TrainingKnownSample(**item))
        else:
            self._testing.append(TestingKnownSample(**item))
        self.counter += 1

    @property
    def training(self) -> List[TrainingKnownSample]:
        return self._training

    @property
    def testing(self) -> List[TestingKnownSample]:
        return self._testing
