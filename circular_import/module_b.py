from __future__ import annotations
from typing import TYPE_CHECKING
from module_a import func_a

# import module_a

if TYPE_CHECKING:
    from module_a import A

    
def func_b1():
    ...

def func_b2():
    a = func_a()
    # a = module_a.func_a()
    ...


class B:
    def __init__(self, a: A):
        self.a = a
