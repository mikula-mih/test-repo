
""" Software Testing Theory """
#  Software Testing is the process of verifying that a software application is
# working as expected; tests are never a guarantee that your program is correct;
#
# Edsger Dijkstra dutch computer scientist;
# "Program testing can be used to show the presence of bugs, never to show
# their absence!"
import random

'''A simple testing example.'''
def add_three(x: int) -> int:
    return x + 3

def remove_three(x: int) -> int:
    return x - 3

def add_three_alt(x: int) -> int:
    if x == 1:
        return 4
    elif x == 2:
        return 5
    elif x == 3:
        return 6
    else:
        return 0

def main():
    # testing the function add_three
    assert add_three(1) == 4
    assert add_three(2) == 5
    assert add_three(3) == 6

    assert add_three_alt(1) == 4
    assert add_three_alt(2) == 5
    assert add_three_alt(3) == 6
    # Property-Based Testing
    for x in range(100):
        assert add_three(remove_three(x)) == x
    # property-based testing where you are applying a transformation on a number
    # and then applying the reverse and verifying that you get the original
    # input is also called `Bilbo testing` | "there and back again";
    for _ in range(100):
        x = random.randint(-1000, 1000)
        assert add_three(remove_three(x)) == x
    print("All tests pass!")


if __name__ == "__main__":
    main()

# `Hoare logic`
# Hoare triple: {P}C{Q} precondition, computation, postcondition
#
# Unit Tests & any other testing approach where you run your code with a
# collection of predefined use cases, test cases is called `dynamic testing`;
# `static testing` doesn't require writing test cases but involves things like
# code reviews and even syntax and type checking by IDE;
# `passive testing` which doesn't even look at the code but looks more at the
# side effects of the code so; log files...
#
# `White Box` & `Black Box` testing: white box testing assumes knowledge about
# the inner workings of the code (Unit testing);
#
# `mutation testing` slightly modifies the source code of your program basically
# introducing mutants and see whether your tests pick these minor changes up;
# "mutmut" - python mutation tester;
#
# `Snapshot testing` take a snapshot of the system before and after a command is
# executed and then compare;
# "Jest library React" - snapshot testing
#
# `Invariant` is a logical assertion that is always held to be true during a
# certain phase of computation;
#
# `Property-Based testing`; "Hypothesis" for python property-based testing;
# measuring whether a property holds; with Unit Tests you provide a particular
# input;
