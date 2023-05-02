
''' Salting, peppering, and hashing '''
import base64
import hashlib
import hmac
import secrets
from dataclasses import dataclass
from typing import Callable

import pytest

# Password storage best practices:
# https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html
# Crypto.SE on peppering:
# https://security.stackexchange.com/questions/3272/password-hashing-add-salt-pepper-or-is-salt-enough

class AuthenticationError(Exception):
    pass

''' Plaintext '''

def update_password_plaintext(db, user, password: str) -> None:
    user.password = password
    db.store(user)


def verify_password_plaintext(user, password: str) -> None:
    pw = user.password
    if not hmac.compare_digest(pw, password):
        raise AuthenticationError

''' Hashed '''

def hash_name(hash_fn: Callable[[bytes], bytes]) -> str:
    if hash_fn.name == "blake2b":
        return "blake2b"
    raise ValueError

def hash_from_name(name: str) -> Callable[[bytes], bytes]:
    if name == "blake2b":
        def hash_fn(b: bytes) -> bytes:
            return hashlib.blake2b(b).digest()

        hash_fn.name = "blake2b"
        return hash_fn
    raise ValueError

# base 64encoding
# the $ sign is not used in base 64 encoding; that makes it safe to use as a
# separator for the name and hash;
def hash_str_and_b64_encode(hash_fn: Callable[[bytes], bytes], password: str) -> str:
    pw_bytes = password.encode("utf-8")
    hash_bytes = hash_fn(pw_bytes)
    hash_bytes = base64.b64encode(hash_bytes)
    hashed_password = hash_bytes.decode("ascii")
    return hashed_password

def update_password_hashed(db, user, hash_fn: Callable[[bytes], bytes], password: str) -> None:
    hashed_password = hash_str_and_b64_encode(hash_fn, password)
    name = hash_name(hash_fn)
    user.password = f"{name}${hashed_password}"
    db.store(user)

def verify_password_hashed(user, password: str) -> None:
    hash_fn_name, hashed_password = user.password.split("$")
    hash_fn = hash_from_name(hash_fn_name)
    h = hash_str_and_b64_encode(hash_fn, password)

    if not hmac.compare_digest(hashed_password, h):
        raise AuthenticationError

# database of hashed passwords is leaked;
# Bad stuff attacker can do:
# 1. Recognize and break common passwords, because these hashes could be precomputed;
# 2. Try many guesses offline (GPU) for those that aren't precomputed since they know
#   which hash functions were used; (this is a big win since the server won't ban them
#   for too many wrong attempts, potentially allowing them to break weak passwords,
#   even if they haven't been precomputed);
# 3. Also if they are able to crack a password that multiple users have used, they
#   crack the password for everyone that used that password all at once;
# 4. See if two users have same pass

''' Hashed and salted '''

# A salt is just a little of extra randomness that we sprinkle in  with a user's password;
# A salt should be unique for each user;
def gen_salt() -> str:
    return secrets.token_urlsafe(20)

# hash the salt together with the password;
def update_password_hashed_salted(db, user, hash_fn: Callable[[bytes], bytes], password: str) -> None:
    salt = gen_salt()
    hashed_password = hash_str_and_b64_encode(hash_fn, salt + password)
    name = hash_name(hash_fn)
    user.password = f"{name}${salt}${hashed_password}"
    db.store(user)

def verify_password_hashed_salted(user, password: str) -> None:
    hash_fn_name, salt, hashed_password = user.password.split("$")
    hash_fn = hash_from_name(hash_fn_name)
    h = hash_str_and_b64_encode(hash_fn, salt + password)

    if not hmac.compare_digest(hashed_password, h):
        raise AuthenticationError

''' Hashed, salted, and peppered '''
# A pepper is specifically something that you do not store in the database;
# In application code, or in a secure memory enclave;
def get_global_pepper() -> str:
    """
    Get the global secret pepper from secure memory.
    The important thing is that it is NOT stored in the database.
    """
    return "some hashed string YSkkYFGRzdqNLCy68z0uT0kjZQgxh6-vzTH_dw7NirYPqDhcU3ykSlG0O-AAx65ivIbx1FPrukM3K4rNSFbcpg"

def update_password_hashed_salted_peppered(db, user, hash_fn: Callable[[bytes], bytes], password: str) -> None:
    salt = gen_salt()
    pepper = get_global_pepper()
    hashed_password = hash_str_and_b64_encode(hash_fn, pepper + salt + password)
    name = hash_name(hash_fn)
    user.password = f"{name}${salt}${hashed_password}"
    db.store(user)

def verify_password_hashed_salted_peppered(user, password: str) -> None:
    hash_fn_name, salt, hashed_password = user.password.split("$")
    pepper = get_global_pepper()
    hash_fn = hash_from_name(hash_fn_name)
    h = hash_str_and_b64_encode(hash_fn, pepper + salt + password)

    if not hmac.compare_digest(hashed_password, h):
        raise AuthenticationError


def main():
    class LolDB:
        def __init__(self):
            self.user = None

        def store(self, user):
            self.user = user
            print("storing user:")
            print(f"{user.email=}")
            print(f"{user.password=}")
            print()

    @dataclass
    class User:
        email: str
        password: str

    user = User(email="user@example.com", password="")
    db = LolDB()
    hash_fn = hash_from_name("blake2b")

    print("plaintext")
    update_password_plaintext(db, user, "v3ry s3cur3")
    verify_password_plaintext(user, "v3ry s3cur3")
    with pytest.raises(AuthenticationError):
        verify_password_plaintext(user, "incorrect pass")

    print("hashed")
    update_password_hashed(db, user, hash_fn, "v3ry s3cur3")
    verify_password_hashed(user, "v3ry s3cur3")
    with pytest.raises(AuthenticationError):
        verify_password_hashed(user, "incorrect pass")

    print("hashed+salted")
    update_password_hashed_salted(db, user, hash_fn, "v3ry s3cur3")
    verify_password_hashed_salted(user, "v3ry s3cur3")
    with pytest.raises(AuthenticationError):
        verify_password_hashed_salted(user, "incorrect pass")

    print("hashed+salted+peppered")
    update_password_hashed_salted_peppered(db, user, hash_fn, "v3ry s3cur3")
    verify_password_hashed_salted_peppered(user, "v3ry s3cur3")
    with pytest.raises(AuthenticationError):
        verify_password_hashed_salted_peppered(user, "incorrect pass")


if __name__ == '__main__':
    main()
