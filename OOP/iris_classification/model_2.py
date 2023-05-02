from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Optional

@dataclass(frozen=True)
class Sample:
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

@dataclass(frozen=True)
class KnownSample(Sample):
    species: str

@dataclass
class TrainingKnownSample:
    sample: KnownSample

class TestingKnownSample:
    def __init__(
        self, sample: KnownSample, classification: Optional[str] = None
    ) -> None:
        self.sample = sample
        self.classification = classification

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(sample={self.sample!r},"
            f"classification={self.classification!r})"
        )

@dataclass
class Hyperparameter:
    """A spcific tuning parameter set with k and a distance algorith"""

    k: int
    algorithm: Distance
    data: weakref.ReferenceType["TrainingData"]

    def classify(self, sample: Sample) -> str:
        """The k-NN algorithm"""
        ...
