# >>> parameter variable
# >>> operands
# >>> operator
# >>> assignment statements
# >>> parameters to functions & methods

# `syntactic sugar`: [] is a call to the list() constructor

the % operator:
- for strings does interpolation: "a=%d" % 113 computes a string 'a=113';
- for numbers computes the remainder after division, the `modulo`

# *Object-Oriented Design*
>>>Object-oriented analysis (OOA) is the process of looking at a problem, system,
>>> or task (that somebody wants to turn into a working software application) and
>>> identifying the objects and interactions between those objects.

>>>Object-oriented design (OOD) is the process of converting such requirements
>>> into an implementation specification.

>>>Object-oriented programming (OOP) is the process of converting a design into a
>>> working program that does what the product owner originally requested.
# `Don't Repeat Yourself (DRY) principle`
#
# #############################################################################
# `SOLID` principles:
# `Single Responsibility Principle` >>> a class should have one responsibility
# `Open/Closed` >>> a class open to extensions, closed to modification
# `Liskov Substitution` >>> any subclass can be substituted for its superclass
# `Interface Segregation` >>> a class should have the smallest interface possible
# `Dependency Inversion` >>> pragmatically, we'd like classes to be independent,
#  so a Liskov Substitution doesn't involve a lot of code changes.
# We need to know what a bad dependency relationship is so we know how to
# invert it to have a good relationship.
# In Python, this often means referring to superclasses in type hints to be sure
# we have the flexibility to make changes. In some cases, it also means
# providing parameters so that we can make global class changes without
# revising any of the code.
# ############################################################################
#
# >>> `magic numbers`: numbers that seem to come out of thin air with no
# apparent meaning within the code
