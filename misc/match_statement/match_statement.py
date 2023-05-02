
""" Match statement """
# is not a `switch/case` statement;


def match_int_example(x):
    match x:
        case 0:
            pass
        case 1 | 2:
            pass
        case 3:
            pass
        case _:
            pass


def match_int_elif_example(x):
    if x == 0:
        pass
    elif x in (1, 2):
        pass
    elif x == 3:
        pass
    else:
        pass


def f(): pass
def g(): pass
def default(): pass

_switch_dict = {0: f, 1: g, 2: g, 3: f,}

def switch_dict_example(x):
    don_next = _switch_dict.get(x, default=default)
    don_next()

# `Structural Pattern Matching`

# `Abstract Syntax Trees`
import ast
import libcst as cst
from libcst.tool import dump
import textwrap

code = textwrap.dedent("""
    a = 'hello' # some comment
    b = 'another one'
""")

def dump_ast_example():
    node = ast.parse(code)
    print(ast.dump(node, indent=4))


# match statement tips

def match_case_reserved_softkws():
    match = 6
    case = "case"

    match 6:
        case 6:
            print("6")
    print("no problem")

    # don't do this
    match case:
        case match:
            print(f'{match=} {case=}')

def underscore_is_a_wildcard():
    match 0:
        case x:
            print("x bound")
    print(f'{x=}')

    _ = "case _ is a wildcard, not a var name"
    match 0:
        case _:
            print("wildcard")
    print(f'{_=}')

def name_binding_scope():
    match 1, 2:
        case 1, x:
            pass
    print(f'{x=}')

    x = 0
    match 0, 1, 2:
        case 0, x, 1:
            pass
        case 0, y, 2:
            pass

    print(f'{y=} is well-defined')
    print(f'{x=} is undefined/implementation dependent behavior')

def name_binding_already_bound():
    x = 0
    match 1:
        case 2:
            print('case 2')
        case x:
            print(f'You didnt match against 0, you just bound x!, {x=}')

def name_binding_dynamic():
    class dummy:
        x = sum(i**2 for i in range(5))

    y = sum(i**2 for i in range(5))
    match y:
        case dummy.x:
            print(f'{y=} {dummy.x=}')

def class_matching_getattr():
    class Person:
        def __init__(self, fullname):
            self.names = fullname.split(" ")

    p1 = Person(fullname="Mike")
    match p1:
        case Person(fullname="Mike"):
            print("wrong! not a constructor")
        case Person(names=["Mike", "Mike"]):
            print("found me!")


def main():
    pass


if __name__ == '__main__':
    main()
