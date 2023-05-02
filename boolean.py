
def true_things():
    literal_true = True
    nonzero_nums = [1, -7, 0.5, 0.2+2j, float('nan')]
    nonempty_containers = [{1, 2, 3}, {"a":1}, [1, 2, 3], "hello"]
    some_obj = object()

def false_things():
    literal_false = False
    literal_none = None
    zeros = [0, 0.0, 0.0 + 0.0j]
    empty_containers = [set(), {}, [], ""]

# 2 way to opt out of a default True conversion
class MyClass:
    def __bool__(self):
        # your logic here
        return False

    def __len__(self):
        return 0

def main():
    if "":
        print("True")
    else:
        print("False")

if __name__ == "__main__":
    main()
