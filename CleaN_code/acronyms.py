
""" DRY principle """
# a principle of software development, aimed at reducing repetition of
# information of all kinds;

""" OAOO Once and Only Once """
# bad example
def process_students_list(students):
    # do some processing...

    students_ranking = sorted(
        students, key=lambda s: s.passed * 11 - s.failed * 5 - s.years * 2
    )
    # more processing
    for student in students_ranking:
        print(
            "Name: {0}, Score: {1}".format(
                student.name,
                (student.passed * 11 - student.failed * 5 - student.years * 2),
            )
        )

# good refactoring
def score_for_student(student):
    return student.passed * 11 - student.failed * 5 - student.years * 2

def process_students_list(students):
    # do some processing...
    students_ranking = sorted(students, key=score_for_student)
    # more processing
    for student in students_ranking:
        print(
            "Name: {0}, Score: {1}".format(
                student.name, score_for_student(student)
            )
        )

""" YAGNI You Ain't Gonna Need It """
# Having maintainable software is not about anticipating future requirements;
# writing software that only addresses current requirements in such a way that
# it will be possible (and easy) to change later on;

""" KIS Keep It Simple """
# when designing a software component, avoid over-engineering it;
# implement minimal functionality that correctly solves the problem &
# doesn't complicate the solution;
# simpler the design, the more maintainable it will be;
#
# it terms of code, keeping it simple usually means using the smallest
# data structure that fits the problem;
class ComplicatedNamespace:
    """An convoluted example of initializing an object with some properties."""

    ACCEPTED_VALUES = ("id_", "user", "location")

    @classmethod
    def init_with_data(cls, **data):
        # having an extra class method for initializing the object
        # doesn't seem really necessary
        instance = cls()
        for key, value in data.items():
            if key in cls.ACCEPTED_VALUES:
                setattr(instance, key, value)
        return instance

cn = ComplicatedNamespace.init_with_data(
    id_=42, user="root", location="127.0.0.1", extra="excluded"
)
print(cn.id_, cn.user, cn.location)
print(hasattr(cn, "extra"))
# initialize the object as we initialize any other object in Python
class Namespace:
    """Create an object from keyword arguments."""

    ACCEPTED_VALUES = ("id_", "user", "location")

    def __init__(self, **data):
        accepted_data = {
            k: v for k, v in data.items() if k in self.ACCEPTED_VALUES
        }
        self.__dict__.update(accepted_data)

# the zen of Python: simple is better than complex

""" EAFP Easier to Ask Forgiveness than Permission
    LBYL Look Before You Leap """
# `EAFP` write code so that it performs an action directly, and then take care
# of the consequences later in case it doesn't work;
#
# This is the opposite of `LBYL`;
# in the look before you leap approach, we first check what we are about to use;
if os.path.exists('filename'):
    with open('filename') as f:
        ...
# not the Pythonic way of writing code
try:
    with open('filename') as f:
        ...
except FileNotFoundError as e:
    logger.error(e)

# Prefer EAFP over LBYL
