
# the `Strategy` pattern is a common demonstration of abstraction in object-oriented
# programming. The pattern implements different solutions to a single problem,
# each in a different object. The core class can then choose the most appropriate
# implementation dynamically at runtime;
""" the `Strategy` pattern """
# common example of the `Strategy` pattern is sort routines;
import abc
from pathlib import Path
from PIL import Image   # type: ignore [import]
from typing import Tuple

Size = Tuple[int, int]

class FillAlgorithm(abc.ABC):
    @abc.abstractmethod
    def make_background(
        self,
        img_file: Path,
        desktop_size: Size
    ) -> Image:
        pass

class TiledStrategy(FillAlgorithm):
    def make_background(
        self,
        img_file: Path,
        desktop_size: Size
    ) -> Image:
        in_img  = Image.open(img_file)
        out_img =  Image.new("RGB", desktop_size)
        num_tiles = [
            o // i + 1 for o, i in zip(out_img.size, in_img.size)]
        for x  in range(num_tiles[0]):
            for y in range(num_tiles[1]):
                out_img.paste(
                    in_img,
                    (
                        in_img.size[0] * x,
                        in_img.size[1] * y,
                        in_img.size[0] * (x + 1),
                        in_img.size[1] * (y + 1),
                    ),
                )
        return out_img


class CenteredStrategy(FillAlgorithm):
    def make_background(
        self,
        img_file: Path,
        desktop_size: Size
    ) -> Image:
        in_img = Image.open(img_file)
        out_img = Image.new("RGB", desktop_size)
        left = (out_img.size[0] - in_img.size[0]) // 2
        top = (out_img.size[1] - in_img.size[1]) // 2
        out_img.paste(
            in_img,
            (left, top, left + in_img.size[0], top + in_img.size[1]),
        )
        return out_img


class ScaledStrategy(FillAlgorithm):
    def make_background(
        self,
        img_file: Path,
        desktop_size: Size
    ) -> Image:
        in_img = Image.open(img_file)
        out_img = in_img.resize(desktop_size)
        return out_img


class Resizer:
    def __init__(self, algorithm: FillAlgorithm) -> None:
        self.algorithm = algorithm

    def resize(self, image_file: Path, size: Size) -> Image:
        result = self.algorithm.make_background(image_file, size)
        return result


def main() -> None:
    image_file = Path.cwd() / "boat.png"
    tiled_desktop = Resizer(TiledStrategy())
    tiled_image = tiled_desktop.resize(image_file, (1920, 1080))
    tiled_image.show()
# the  preceding canonical implementation of the `Strategy` pattern, while very
# common in most object-oriented libraries, isn't ideal in Python;
# we could just as easily call that function __call__() and make the object
# callable directly;
# because we have a choice between an abstract class and a type hint, the
# `Strategy` design pattern seems superfluous;
# "Because Python has first-class functions, the Strategy pattern is unnecessary"
# In truth, Python's first-class functions allow us to implement the Strategy
# pattern in a more straightforward way, without the overhead of class definitions.
#
# The Strategy pattern, whether a class or a top-level function, should be used when we
# need to allow client code or the end user to select from multiple implementations of
# the same interface at runtime.
#
# Overloading, mixin class definitions are created in the source code, and cannot 
# easily be tweaked at runtime. A plug-in strategy object, however, is filled in
# at runtime, allowing late binding of the strategy. The code tends to be very
# similar between them, and it helps to have clear docstrings on each class to
# explain how the various classes fit together.
#
