
# the `Composite` pattern allows complex tree structures to be built from simple
# components, often called `nodes`; A node with children will behave like a
# container; a node without children wil bahave like a single object;
# Traditionally, each node in a composite object must be either a `leaf` node
# (that cannot contain other objects) or a `composite` node;
# `ast` module: provides the classes that define the structure of Python code;
""" the `Composite` pattern """
#
import abc
from typing import Optional

class Folder:
    def __init__(
        self,
        name: str,
        children: Optional[dict[str, "Node"]] = None
    ) -> None:
        self.name = name
        self.children = children or {}
        self.parent: Optional["Folder"] = None

    def __repr__(self) -> str:
        return f"Folder({self.name!r}, {self.children!r})"

    def add_child(self, node: "Node") -> "Node":
        node.parent = self
        return self.children.setdefault(node.name, node)

    def move(self, new_folder: "Folder") -> None:
        pass

    def copy(self, new_folder: "Folder") -> None:
        pass

    def remove(self) -> None:
        pass


class File:
    def __init__(self, name: str) -> None:
        self.name = name
        self.parent: Optional[Folder] = None

    def __repr__(self) -> str:
        return f"File({self.name!r})"

    def move(self, new_path):
        pass

    def copy(self, new_path):
        pass

    def remove(self):
        pass
#
class Node(abc.ABC):
    def __init__(
        self,
        name: str,
    ) -> None:
        self.name = name
        self.parent: Optional["Folder"] = None

    def move(self, new_place: "Folder") -> None:
        previous = self.parent
        new_place.add_child(self)
        if previous:
            del previous.children[self.name]

    @abc.abstractmethod
    def copy(self, new_folder: "Folder") -> None:
        ...

    @abc.abstractmethod
    def remove(self) -> None:
        ...
#
class Folder(Node):
    def __init__(
        self,
        name: str,
        children: Optional[dict[str, "Node"]] = None
    ) -> None:
        super().__init__(name)
        self.children = children or {}

    def __repr__(self) -> str:
        return f"Folder({self.name!r}, {self.children!r})"

    def add_child(self, node: "Node") -> "Node":
        node.parent = self
        return self.children.setdefault(node.name, node)

    def copy(self, new_folder: "Folder") -> None:
        target = new_folder.add_child(Folder(self.name))
        for c in self.children:
            self.children[c].copy(target)

    def remove(self) -> None:
        names = list(self.children)
        for c in names:
            self.children[c].remove()
        if self.parent:
            del self.parent.children[self.name]


class File(Node):
    def __repr__(self) -> str:
        return f"File({self.name!r})"

    def copy(self, new_folder: "Folder") -> None:
        new_folder.add_child(File(self.name))

    def remove(self) -> None:
        if self.parent:
            del self.parent.children[self.name]
#
tree = Folder("Tree")

tree.add_child(Folder("src"))
tree.children["src"].add_child(File("ex1.py"))
tree.add_child(Folder("src"))
tree.children["src"].add_child(File("test1.py"))

print(tree)
#
