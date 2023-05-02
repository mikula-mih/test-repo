
""" Mutable/Immutable """
# An immutable object is an object whose state cannot be modified after it is
# created; This is in contrast to a mutable object, which can be modified after
# it is created;

a = 'strings are immutable!!!'
print('Address of a is: {}'.format(id(a)))

a = 'CHANGED'
print('Address of a is: {}'.format(id(a)))

try:
    a[0] = 'C'
    print("Address of a is: {}".format(id(a)))
except TypeError:
    print('Opps')

Lists_Mutable = list()

###
employees = ['a', 'a', 'a', 'a', 'a', 'a', 'a']
output = '<ul>\n'

for employees in employees:
    output += '\t<li>{}</li>\n'.format(employees)
    print("Address of output is: {}".format(id(output)))

output += '</ul>'
print(output)
print('\n')
