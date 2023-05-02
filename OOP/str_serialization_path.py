
""" Strings, Serialization, & File Paths """
# persistence – the ability to write data to a file and retrieve it
# at an arbitrary later date;
#
# in Python3 strings are all represented in Unicode;
#
# the important rule is this:
# we `encode` our characters to create bytes; we `decode` bytes to recover
# the characters;
bytes = b'Flamb\xc3\xa9'
# the b' prefix tells us these are bytes, and the letters are really only ASCII code;
'''string manipulation'''
isalpha(), isupper(), islower(), startswith(), endswith(), isspace() methods
help(str.isalpha)
istitle()
isdigit(), isdecimal(), isnumeric() methods
# the period character that we use to construct floats from strings is not considered
# a decimal character, so '45.2' .isdecimal() returns False; the real decimal
# character is represented by the Unicode value 0660, as in 45.2 (or 45\u06602);
isdecimal()
count()
find(), index(), rfind(), rindex() methods
split(), rsplit() method
partition(), rpartition() methods
join()
replace()
upper(), lower(), capitalize(), title() methods
translate() method
'''string formatting'''
# A format string (also called an `f-string`)
# Escaping braces
template = f"""
public class {var} {{
    public static void main(String[] args) {{
        System.out.println("{{var2}}");
    }}
}}
"""
print(f"{[2*a+1 for a in range(5)]}")
for n in range(1, 5):
    print(f"{'fizz' if n % 3 == 0 else n}")
a, b = 5, 7
print(f"{a=}, {b=}, {31*a//42*b + b=}")
#
def distance(
    lat1: float, lon1: float, lat2: float, lon2: float,
) -> float:

    d_lat = radians(lat2) - radians(lat1)
    d_lon = min(
        (radians(lon2) - radians(lon1)) % (2 * pi),
        (radians(lon1) - radians(lon2)) % (2 * pi),
    )
    R = 60 * 180 / pi
    d = hypot(R * d_lat, R * cos(radians(lat1)) * d_lon)
    return d

annapolis = (38.9784, 76.4922)
saint_michaels = (38.7854, 76.2233)
round(distance(*annapolis, *saint_michaels), 9)
#
print(f"{'leg':16s} {'dist':5s} {'time':4s} {'fuel':4s}") # :16s == takes 16 char
print(f"{name:16s} {d:5.2f} {d/speed:4.1f} ") # :5.2f == .decimal point, f == flaoting-point numeric value
print(f"{d/speed*fuel_per_hr:4.0f}")
# A filler character (space if nothing is provided) that's used to pad out the number to fill in the specified size.
#
# The alignment rule. By default, numbers are right-aligned and strings are
#left-aligned. Characters like <, ^, and > can force left, centered, or right alignment.
#
# How to handle the sign (default is – for negative, nothing for positive.) You
# can use + to show all signs. Also, " " (a space) leaves a space for positive
# numbers and - for negative numbers to assure proper alignment.
#
# A 0 if you want leading zeroes to fill in the front of the number.
#
# The overall size of the field. This should include signs, decimal places,
# commas, and the period itself for floating-point numbers.
#
# A , if you want 1,000 groups separated by ",". Use _ to separate groups with
# an "_". If you have a locale where grouping is done with ".", and the decimal
# separator is ",", you'll want to use the n format to use all of the locale settings.
# The f format is biased toward locales that use "," for grouping.
#
# The . if it's a float (f) or general (g) number, followed by the number of digits
# to the right of the decimal point.
#
# The type. Common types are s for strings, d for decimal integers, and f for
# floating-point. The default is s for string. Most of the other format specifiers
# are alternative versions of these; for example, o represents octal format
# and X represents hexadecimal format for integers. The n type specifier can be
# useful for formatting any kind of number in the current locale's format. For
# floating-point numbers, the % type will multiply by 100 and format a float as
# a percentage.

"""Custom formatters"""
import datetime
important = datetime.datetime(2019, 10, 26, 13, 14)
f"{important:%Y-%m-%d %I:%M%p}"
# Look into overriding the __format__() special method if you need to do this in your code.

""" the format() method """
# the `format()` method behaves similarly to an f-string with one important
# distinction: you can access values provided as the arguments to the `format()`
# method only;
from decimal import Decimal
subtotal = Decimal('2.95') * Decimal('1.0625')
template = "{label}: {number:*^{size}.2f}"
template.format(label="Amount", size=10, number=subtotal)
>>> 'Amount: ***3.13***'
grand_total = subtotal + Decimal('12.34')
template.format(label="Total", size=12, number=grand_total)
>>> 'Total: ***15.47****'

""" Strings are Unicode """
list(map(hex, b'abc'))
>>> ['0x61', '0x62', '0x63']
list(map(bin, b'abc'))
>>> ['0b1100001', '0b1100010', '0b1100011']
bytes([137, 80, 78, 71, 13, 10, 26, 10])
>>> b'\x89PNG\r\n\x1a\n'
# bytes must be decoded using the same character set with which they were encoded
#
# If we have an array of bytes, we can convert it to Unicode using the `.decode()`
# method on the `bytes` class;
characters = b'\x63\x6c\x69\x63\x68\xc3\xa9'
>>> b'clich\xc3\xa9'
characters.decode("utf-8")
>>> 'cliché'
characters.decode("iso8859-5")
>>> 'clichÓŠ'
characters.decode("cp037")
>>> 'Ä%ÑÄÇZ'
#
characters = "cliché"
characters.encode("UTF-8")
>>> b'clich\xc3\xa9'
characters.encode("latin-1")
>>> b'clich\xe9'
characters.encode("cp1252")
>>> b'clich\xe9'
characters.encode("CP437")
>>> b'clich\x82'
characters.encode("ascii")  # returns ERROR
# the `encode` method takes an optional string argument named `errors` that can
# define how such characters should be handled; this string can be one of the
# following: "strict", "replace", "ignore", "xmlcharrefreplace";
#
# The ignore strategy simply discards any bytes it doesn't understand, while
# the xmlcharrefreplace strategy creates an xml entity representing the Unicode
# character.
characters = "cliché"
characters.encode("ascii", "replace")
>>> b'clich?'
characters.encode("ascii", "ignore")
>>> b'clich'
characters.encode("ascii", "xmlcharrefreplace")
>>> b'clich&#233;'
# It is possible to call the `str.encode()` and `bytes.decode()` methods without passing
# an encoding name. The encoding will be set to the default encoding for the current
# platform. This will depend on the current operating system and locale or regional
# settings; you can look it up using the `sys.getdefaultencoding()` function.
#
# The UTF-8 encoding uses one byte to represent ASCII and other common characters,
# and up to four bytes for other characters.
""" Mutable byte strings """
# the bytes type, like str, is immutable;
ba = bytearray(b"abcdefgh")
ba[4:6] = b"\x15\xa3"
>>> bytearray(b'abcd\x15\xa3gh')
# the bytearray built-in comes in. This type behaves something like a
# list, except it only holds bytes
# The extend method can be used to append another bytes object to
# the existing array (for example, when more data comes from a socket or other I/O
# channel).
ba = bytearray(b"abcdefgh")
ba[3] = ord(b'g')
ba[4] = 68
>>> bytearray(b'abcgDfgh')
# A single byte character can be converted to an integer using the ord() (short
# for ordinal) function. This function returns the integer representation of a single
# character;
#
# The bytearray type has methods that allow it to behave like a list (we can append
# integer bytes to it, for example). It can also behave like a bytes object (we can use
# methods such as `count()` and `find()`).

""" Regular expressions """
# Regular expressions don't describe languages with recursive structures;
# the XML parsers in the Python standard library can handle these more complex constructs;
# Matching patterns
import re

search_string = "hello world"
pattern = r"hello world"
if match := re.match(pattern, search_string):
    print(match)
>>> <re.Match object; span=(0, 11), match='hello world'>
# A successful match returns a `re.Match` object describing what – exactly – matched. A
# failing match returns None, which is equivalent to False in the Boolean context of an
# if-statement.
#
# the "walrus" operator (:=) to compute the results of re.match() and
# save those results in a variable all as part of an if-statement. This is one of the most
# common ways to use the walrus operator to compute a result and then test the result
# to see if it's truthy. This is a little optimization that can help clarify how the results
# of the matching operation will be used if they are not None.
#
# We'll almost always use "raw" strings with the r prefix for regular expressions. Raw
# strings do not have the backslash escapes processed by Python into other letters
from typing import Pattern, Match

def matchy(pattern: Pattern[str], text: str) -> None:
    if match := re.match(pattern, text):
        print(f"{pattern=!r} matches at {match=!r}")
    else:
        print(f"{pattern=!r} not found in {text=!r}")
#
matchy(pattern=r"hello wo", text="hello world")
>>> pattern='hello wo' matches at match=<re.Match object; span=(0, 8), match='hello wo'>
matchy(pattern=r"ello world", text="hello world")
>>> pattern='ello world' not found in text='hello world'
# the ^ and $ characters to represent the start and end of the string respectively;
matchy(pattern=r"^hello world$", text="hello world")
>>> pattern='^hello world$' matches at match=<re.Match object; span=(0, 11), match='hello world'>
matchy(pattern=r"^hello world$", text="hello worl")
>>> pattern='^hello world$' not found in text='hello worl'
# We call the ^ and $ characters "anchors." They anchor the match to the beginning
# or end of the string. What's important is that they don't literally match themselves;
# they're also called meta-characters. If we were doing fancy math typesetting, we'd
# use a different font to distinguish between ^ meaning anchored at the beginning and
# ^ meaning the actual "^" character. Since we don't have fancy math typesetting in
# Python code, we use \ to distinguish between meta-character and ordinary character.
# In this case, ^ is a meta-character, and \^ is the ordinary character.
#
# Note that we used r"\^hello…" to create a raw
# string. Python's canonical display came back as '\\^hello…'.
#
# As with ^ and $, the characters ., [ and ] are meta-characters. Meta-characters define
# a more complex feature of a regular expression
#
# These square bracket sets could be named character sets, but they are more often
# referred to as character classes
#
# The dash character, in a character set, will create a range. This is especially useful if
# you want to match all lowercase letters, all letters, or all numbers;
#
# \d is digits, \s is whitespace, and \w is "word" characters. Instead of
# [0-9], use \d. Instead of trying to enumerate all the Unicode whitespace characters,
# use \s. Instead of [a-z0-9_], use \w.
#
# Without the defined sets, this pattern would start out as [0-9][0-9][ \t\n\r\f\v]
# [A-Za-z0-9_][A-Za-z0-9_][A-Za-z0-9_]. It gets quite long as we repeat the
# [ \t\n\r\f\v] class and the [0-9] class four more times.
# When defining a class with []'s, the – becomes a meta-character
#
# [A-Z-] means any character between A and Z, and the -, also.
def email_domain(text: str) -> Optional[str]:
    email_pattern = r"[a-z0-9._%+-]+@([a-z0-9.-]+\.[a-z]{2,})"
    if match := re.match(email_pattern, text, re.IGNORECASE):
        return match.group(1)
    else:
        return None
#
def email_domain_2(text: str) -> Optional[str]:
    email_pattern = r"(?P<name>[a-z0-9._%+-]+)@(?P<domain>[a-z0-9.-]+\.[a-z]{2,})"
    if match := re.match(email_pattern, text, re.IGNORECASE):
        return match.groupdict()["domain"]
    else:
        return None
#
# The `search()` function finds the first instance
# of a matching pattern, relaxing the restriction that the pattern should be implicitly
# anchored to the first letter of the string. Note that you can get a similar effect by
# using match() and putting a .* character at the front of the pattern to match any
# characters between the start of the string and the pattern you are looking for.
# The `findall()` function behaves similarly to search(), except that it finds all nonoverlapping
# instances of the matching pattern, not just the first one. Think of it
# searching for the first match, then continuing the search after the end of the first
# matching to find the next one.
#
# If there are no groups in the pattern, re.findall() will return a list of strings,
# where each value is a complete substring from the source string that matches
# the pattern
# If there is exactly one group in the pattern, re.findall() will return a list of
# strings where each value is the contents of that group
# If there are multiple groups in the pattern, re.findall() will return a list of
# tuples where each tuple contains a value from a matching group, in order
re.findall(r"\d+[hms]", "3h 2m 45s")
>>> ['3h', '2m', '45s']
re.findall(r"(\d+)[hms]", "3h:2m:45s")
>>> ['3', '2', '45']
re.findall(r"(\d+)([hms])", "3h, 2m, 45s")
>>> [('3', 'h'), ('2', 'm'), ('45', 's')]
re.findall(r"((\d+)([hms]))", "3h - 2m - 45s")
>>> [('3h', '3', 'h'), ('2m', '2', 'm'), ('45s', '45', 's')]
# the `re.compile()` method. It returns an object-oriented version
# of the regular expression that has been compiled down and has the methods we've
# explored (match(), search(), and findall()), among others. The changes to what
# we've seen are minor.
duration_pattern = re.compile(r"\d+[hms]")
duration_pattern.findall("3h 2m 45s")
>>> ['3h', '2m', '45s']
duration_pattern.findall("3h:2m:45s")
>>> ['3h', '2m', '45s']
#
