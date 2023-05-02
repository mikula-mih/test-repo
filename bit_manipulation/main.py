
""" Python Bitwise Operators """
# <<    : shift to the left (replace with 0) == multiplying by 2^num
# >>    : shift to the right == division by 2^num == // operator
#   also called `arithmetic right shift`, fills in iwth the value of the sign bit;
# &     : bitwise AND;
# |     : bitwise OR;
# ~     : bitwise NOT;
# ^     : bitwise XOR;
'''XOR examples:
a^b=c
c^b=a

n^n=0
n^0=n
'''
# `Logical right shift`
# after shifting puts a 0 in the most significant bit
# in Python, there is no such operator; can implement using `bitstring` module
# padding with zeros using >>= operator;

""" Python Built-in Functions """
# take an integer -> return binary string | TypeError;
# doesn't return binary string bits that applies the two's complement rule;
a = bin(88)
print(a)    # 0b1011000
a1 = bin(-88)
print(a1)    # -0b1011000
# takes sting -> integer with corresponding base (2, 10, 16)
b = ord('01011000', 2)
c = ord('88', 10)
print(b, c)    # 88 88
# takes integer -> character(string) whose Unicode integer | ValueError
d = chr(88)
print(d)    # X
# takes string -> integer
e = ord('a')
print(e)    # 97
#
""" Twos-compliment Binary """
# Twos-compliment binary is used for representing the signed number;
# get Two'c Complement Binary Representation
bits = 8
ans = (1 << bits) -2
print(ans)  # 0b11111110
# One's Complement: inverting the bits of n and +1;
def twos_complement(val, bits):
    # first flip implemented with XOR of val with all 1's
    flip_val = val ^ (1 << bits - 1)
    # flip_val = ~val we only give 3 bits
    return bin(flip_val + 1)

def twos_complement_result(x):
    ans1 = -x
    ans2 = ~x + 1
    print(ans1, ans2)
    print(bin(ans1), bin(ans2))
    return ans1
#
""" Useful Combined Bit Operations """
# mask = 1 << i
# set bits to 1 and other to 0
#
# Get ith Bit
def get_bit(x, i):
    mask = 1 << i
    if x & mask:
        return 1
    return 0
print(get_bit(5,1)) # 0

def get_bit2(x, i):
    return x >> i & 1
print(get_bit2(5,1)) # 0
#
# Set ith Bit
# set it to 1
# x = x | mask
# set it to 0
# x = x & (~mask)
#
# Toggle ith Bit
# x = x ^ mask
#
# Clear Bits
# base mask
# i = 5
# mask = 1 << i
# mask = mask -1
# print(bin(mask)) # 0b11111
def clear_bits_left_right(val, i):
    print('val', bin(val))
    mask = (1 << i) -1
    print('mask', bin(mask))
    return bin(val & (mask))

def clear_bits_right_left(val, i):
    print('val', bin(val))
    mask = (1 << i) -1
    print('mask', bin(~mask))
    return bin(val & (~mask))
#
# Get the lowest set bit
def get_lowest_set_bit(val):
    return bin(val & (-val))
print(get_lowest_set_bit(5)) # 0b1
#
# Clear the lowest set bit
def strip_last_set_bit(val):
    print(bin(val))             # 0b101
    return bin(val & (val - 1))
print(strip_last_set_bit(5))    # 0b100
