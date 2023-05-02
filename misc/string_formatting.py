
person = {'name': 'Jenn', 'age': 23}

# String Concatenation
# NOT THE BEST practice
str = 'My name is ' + person['name'] + ' and I am ' + str(person['age']) + ' years old.'

# String Formatting
str = 'My name is {} and I am {} years old.'.format(person['name'], person['age'])
str = 'My name is {0} and I am {1} years old.'.format(person['name'], person['age'])
str = 'My name is {0[name]} and I am {0[age]} years old.'.format(person)

tag = 'h1'
text = 'This is a headline'

str = '<{0}>{1}</{0}>'.format(tag, text)

# Access Attributes
class Person():
    def __init__(self, name, age):
        self.name = name
        self.age = age

p1 = Person('Jack', '33')

str = 'My name is {0.name} and I am {0.age} years old.'.format(p1)

# passing KeyWord args to format
str = 'My name is {name} and I am {age} years old.'.format(name='Jenn', age='30')

# unpacking lists & dicts
person = {'name': 'Jenn', 'age': 23}
str = 'My name is {name} and I am {age} years old.'.format(**person)

# formatting Numbers
pi = 3.14159265
str = 'The value is {:.3f}'.format(pi) # three decimanl
for i in range(1, 11):
    str = 'The value is {:02}'.format(i) # two digits padding
