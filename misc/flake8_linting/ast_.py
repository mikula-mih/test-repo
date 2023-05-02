import ast # Abstract Syntax Tree

""" Python AST Parsing and Custom Linting """
# >>> pip install flake8

# >>> python -m ast cool_module.py

class Visitor(ast.NodeVisitor):

    def visit(self, node: ast.AST):
        print(node)
        self.generic_visit(node)


def main():
    with open('misc/the_Sieve_of_Eratosthenes.py') as f:
        code = f.read()

    node = ast.parse(code)
    # print(node)
    # print(node._fields)
    # print(node.body)
    # print(node.body[0]._fields)
    Visitor().visit(node)


if __name__ == '__main__':
    main()
