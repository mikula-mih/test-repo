from __future__ import annotations
from typing import TYPE_CHECKING
from module_b import func_b1

# 2nd solution: import directly
# import module_b

# 3rd solution: merge two files

if TYPE_CHECKING:
    from module_b import B

def func_a():
    # first resolution to put it inside function
    # from module_b import func_b1
    b: B = func_b1()
    # 2nd solution
    # b = module_b.func_b1()
    ...


class A:
    def __init__(self, b: B):
        self.b = b
