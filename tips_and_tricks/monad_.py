
""" Manad in Python """
# The simplest definition of a `Monad` is a context attached to a value that
# allows that value to be sequenced;
# allows sequential and procedural programming in functional languages
# that don't have it by default;

# used to attach a failure context to a value, like .error() in JS or maybe
# similar to a try-catch. This failiure context is passed down to the end of
# the execution and can be obtained at the end so we don't call a method on the value.
class Maybe:

  def __init__(self, value):
    self.value = value

  def __repr__(self):
    return f"Maybe({self.value})"

  def unwrap(self):
    return self.value

  def bind(self, func):
    if self.value == None:
      return Maybe(None)
    return Maybe(func(self.value))

  @staticmethod
  def wrap(value):
    return Maybe(value)


maybe = Maybe(4).bind(lambda x: 2*x).bind(lambda y: y+1)
print(maybe)
print(maybe.unwrap())


def this_could_fail(x):
  return None if x < 10 else x

maybe = Maybe(4).bind(this_could_fail).bind(lambda x: 2*x).bind(lambda y: y+1)
print(maybe)
print(maybe.unwrap())

def do_something_with_response(res):
    if res is not None:
        print(res.text)

Maybe(requests.get("http://somesite.com/")).bind(do_something_with_response)


# the `List monad`. The list monad is similar to map or list comprehensions,
# except it can do more than just mapping a function to a list.

class List:

    def __init__(self, value):
        self.value = list(value)

    def __repr__(self):
        return f"List({self.value})"

    def unwrap(self):
        return self.value

    def concat(self, list_lists):
        return [item for sublist in list_lists for item in sublist]

    def bind(self, func):
        ls = self.concat([func(x) for x in self.value])
        return List(ls)

    @staticmethod
    def wrap(value):
        return List(value)

ls = List([1,2,3,4,5]).bind(lambda x: [x, -x])
print(ls)
print(ls.unwrap())

ls = List(["Dog", "Kitty"]).bind(lambda x: ["Smelly " + x, "Good " + x])
print(ls.unwrap())
# The output of this is a list of all the combinations from the two lists
# in the monadic chain.
#
# We can do something similar with list comprehensions like this:
ls = [y + " " + x for x in ["Dog", "Kitty"] for y in ["Smelly", "Good"]]
# Monads already kind of exist in Javascript with promises;
# doComputation().then(doThisIfSuceeded).error(doThisIfFailed)
# This sort of functional chain is already a monad; can be used to determine
# when a failure occurs instead of using complicated exception handling routines
# or null pointer checks;
#
# Monads aren't that difficult to understand when you understand them in the
# context of things we already know like function chaining, promises, and
# list comprehensions.
# They are simply values with an added context that lets us do more complicated
# computations with the value.
