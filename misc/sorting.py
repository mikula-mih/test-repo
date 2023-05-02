# LISTS
li = [9,1,8,2,7,3,6,4,5]

s_li = sorted(li) # returns a new sorted list
li.sort() # sorts the given list

s_li = sorted(li, reverse=True)
# TUPLES
tup = (9,1,8,2,7,3,6,4,5)
s_tup = sorted(tup) # sorting by creating a new tuple
# Dictionary
di = {'name': 'Mike', 'age': None, 'os': 'Linux'}
s_di = sorted(di) # sorting Keys

# Sorting on Different Criteria
li = [9,-1,8,2,-7,3,-6,4,-5]
s_li = sorted(li, key=abs) # sorting absolute values

from operator import attrgetter
class Employee():
    def __init__(self, name, age, salary):
        self.name = name
        self.age = age
        self.salary = salary

    def __repr__(self):
        return '({},{},${})'.format(self.name, self.age, self.salary)

e1 = Employee('mike1', 37, 70000)
e2 = Employee('mike2', 29, 80000)
e3 = Employee('mike3', 43, 90000)

employees = [e1, e2, e3]

def e_sort(emp):
    return emp.salary

s_employees = sorted(employees, key=e.sort, reverse=True)
s_employees = sorted(employees, key=lambda e: e.name)
s_employees = sorted(employees, key=attrgetter('age'))
