

# Nested Loops
# whenever possible, flat the iteration to a single for loop;
def search_nested_bad(array, desired_value):
    coords = None
    for i, row in enumerate(array):
        for j, cell in enumerate(row):
            if cell == desired_value:
                coords = (i, j)
                break

        if coords is not None:
            break

    if coords is None:
        raise ValueError(f"{desired_value} not found")

    logger.info("value %r found at [%i, %i]", desired_value, *coords)
    return coords

# the auxiliary generator that was created works as an abstraction
# for the iteration that's required
def _iterate_array2d(array2d):
    for i, row in enumerate(array2d):
        for j, cell in enumerate(row):
            yield (i, j), cell

def search_nested(array, desired_value):
    try:
        coord = next(
            coord
            for (coord, cell) in _iterate_array2d(array)
            if cell == desired_value
        )
    except StopIteration:
        raise ValueError("{desired_value} not found")

    logger.info("value %r found at [%i, %i]", desired_value, *coords)
    return coords

# Try to simplify the iteration as much as possible with as many
# abstractions as are required, flatting the loops whenever possible.
