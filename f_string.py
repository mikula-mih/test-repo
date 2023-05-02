from datetime import datetime

name = 'jane'
birthday = datetime(1990, 1, 1)
str = f'{name.upper()} has a birthday on {birthday:%B %d, %Y}'

def equals_debugging():
    str_value = "other dog"
    num_value = 123
    print(f'the value is {str_value}'
          f'{str_value=}'
          f'{num_value % 2 = }')

def condersions():
    str_value = "other dog"
    print(f'{str_value!a}') # ASCII
    print(f'{str_value!r}') # repr()
    print(f'{str_value!s}') # string conversion

class MyClass:
    def __format__(self, format_spec) -> str:
        print(f'MyClass __format__ called with {format_spec=!r}')
        return "MyClass()"

def formatting():
    num_value = 123.456
    now = datetime.datetime.utcnow()
    print(f'{now=:%Y-%m-%d}')
    print(f'{num_value:.2f}')
    print(f'{MyClass():blah blah %%MYFORMAT%%}')

    nested_format = ".2f"
    print(f'{num_value:{nested_format}}')


def main():
    greet = "Hi"

    # Adding spaces to the left
    print(f"{greet:>10}")

    # Various alignment options
    print(f"{greet:_^10}")
    print(f"{greet:_<10}")
    print(f"{greet:_>10}")

    print(f"{3.4:10}") # numbers are right alignment
    print(f"{3820.45:2}") # value can be larger

    print(f"{100.345736:.2f}") # .2f is the number

    print(f"{1000000:,.2f}") # grouping thousand
    print(f"{1000000:_.2f}")

    print(f"{0.34576:%}") # percentage
    print(f"{0.34576:.2%}")

    print(f"{34:o}") # octal
    print(f"{34:x}") # hexadecimal
    print(f"{34:b}") # binary
    print(f"{345.345:e}") # scientific representation


if __name__ == '__main__':
    main()
