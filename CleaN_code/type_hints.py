
# Type-driven Development
# this is very subjective
# 1.type hints reduces need for documentation
# 2.improve editing experience
# 3.makes coupling more explicit
# 4.force being explicit with data structures
# 5.simplifies your code

def luhn_checksum(number: str) -> bool:
    """
    documentation
    """
    def digits_of(nr: str) -> list[int]:
        return [int(d) for d in nr]

    digits = digits_of(number)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum = 0
    checksum += sum(odd_digits)
    for digit in even_digits:
        checksum += sum(digits_of(str(digit * 2)))
    return checksum % 10 == 0

def is_eligible_for_bonus(
    contracts_landed: int, hours_worked: int, is_family: bool
) -> bool:
    if is_family:
        return True
    return contracts_landed > 0 and hours_worked > 40
