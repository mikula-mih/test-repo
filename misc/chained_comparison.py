
def rules_of_thumb(x, y, z):
    ...

def main():
    x, y, z = 0, 1, 2

    if x < y < z < 5 <= 10:
        """x < y and y < z and z < 5 and 5 <= 10"""
        print(True)
    else:
        print(False)

    comparisons = ['<', '>', '<=', '>=', '==', '!=', 'is', 'is not', 'in', 'not in']

if __name__ == '__main__':
    main()
