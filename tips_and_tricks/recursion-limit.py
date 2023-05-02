
import sys

# traversing a tree
class Node:
    def __init__(self, *children: 'Node', data=None):
        self.children = list(children)
        self.data = data

    def __repr__(self):
        return f'({self.data})'


def print_parent_then_children(node: Node):
    print(node)
    # pre-order traversal
    for child in node.children:
        print_parent_then_children(child)


def print_stack(node: Node):
    # turning recursive funciton into iterative
    stack = [node]

    while stack:
        node = stack.pop()

        print(node)
        for child in reversed(node.children):
            stack.append(child)


def print_stack_complex(node: Node, max_depth=-1):
    stack = [(node, max_depth)]

    while stack:
        node, max_depth = stack.pop()

        print(node)
        if max_depth == 0:
            continue
        for child in reversed(node.children):
            stack.append((child, max_depth - 1))

# both recursive and iterative solutions have high coupling

def walk_stack_complex(node: Node, max_depth=-1):
    stack = [(node, max_depth)]

    while stack:
        node, max_depth = stack.pop()

        yield node
        if max_depth == 0:
            continue
        for child in reversed(node.children):
            stack.append((child, max_depth - 1))


def print_stack_yield(node: Node, max_depth=-1):
    for node in walk_stack_complex(node, max_depth):
        print(node)


def small_example():
    root = Node(
        Node(
            Node(data="child 0-0"),
            Node(data="child 0-1"),
            Node(data="child 0-2"),
            data="child 0",
        ),
        Node(data="child 1"),
        data="root",
    )

    # print_parent_then_children(root)
    print_stack(root)
    print_stack_complex(root, max_depth=1)


def long_tree_example():
    sys.setrecursionlimit(2_000)
    root = Node(data="root")
    node = root
    for n in range(1000):
        new = Node(data=f"child {n}")
        node.children.append(new)
        node = new

    # print_parent_then_children(root)
    print_stack(root)


if __name__ == "__main__":
    small_example()
    # long_tree_example()
