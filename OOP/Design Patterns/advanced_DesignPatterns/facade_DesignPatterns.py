from __future__ import annotations
# the `Facade` pattern is designed to provide a simple interface to a complex
# system of components; it allows us to define a new class that encapsulates a
# typical usage of the system, thereby avoiding a design that exposes the many
# implementation details hiding among multiple object interactions;
""" the `Facade` pattern """
# the `Facade` pattern is, in many ways, like the `Adapter` pattern; the primary
# difference is that a Facade tries to abstract a simpler interface out of a
# complex one, while an `Adapter` only tries to map one existing interface to
# another;
import re
from pathlib import Path
from typing import Iterator, Tuple

class FindUML:
    def __init__(self, base: Path) -> None:
        self.base = base
        self.start_pattern = re.compile(r"@startuml *(.*)")

    def uml_file_iter(self) -> Iterator[tuple[Path, Path]]:
        for source in self.base.glob("**/*.uml"):
            if any(n.startswith(".") for n in source.parts):
                continue
            body = source.read_text()
            for output_name in self.start_pattern.findall(body):
                if output_name:
                    target = source.parent / output_name
                else:
                    target = source.with_suffix(".png")
                yield (
                    source.relative_to(self.base),
                    target.relative_to(self.base)
                )
#
import subprocess

class PlantUML:

    conda_env_name = "CaseStudy"
    base_env = Path.home() / "miniconda3" / "envs" / conda_env_name

    def __init__(
        self,
        graphviz: Path = Path("bin") / "dot",
        plantjar: Path = Path("share") / "plantuml.jar",
    ) -> None:
        self.graphviz = self.base_env / graphviz
        self.plantjar = self.base_env / plantjar

    def process(self, source: Path) -> None:
        env = {
            "GRAPHVIZ_DOT": str(self.graphviz),
        }
        command = [
            "java", "-jar",
        str(self.plantjar), "-progress",
        str(source)
        ]
        subprocess.run(command, env=env, check=True)
        print()


class GenerateImages:
    def __init__(self, base: Path) -> None:
        self.finder = FindUML(base)
        self.painter = PlantUML()

    def make_all_images(self) -> None:
        for source, target in self.finder.uml_file_iter():
            if (
                not target.exists()
                or source.stat().st_mtime > target.stat().st_mtime
            ):
                print(f"Processing {source} -> {target}")
                self.painter.process(source)
            else:
                print(f"Skipping {source} -> {target}")


if __name__ == "__main__":
    g = GenerateImages(Path.cwd())
    g.make_all_images()
#
