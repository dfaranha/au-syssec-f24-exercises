#!/usr/bin/env python3

from hashlib import sha256


# Pretend that you don't know anything about the secret key apart from its length.
secret_key = b'VERY_SECRET_KEY_'
secret_key_len = len(secret_key)


def authenticate(message: bytes) -> bytes:
    """Authenticate a given message."""
    global secret_key
    h = sha256()
    h.update(secret_key)
    h.update(message)
    return h.digest()


def verify(message: bytes, tag: bytes) -> bool:
    """Verify a given message and authentication tag."""
    t = authenticate(message)
    return t == tag


def main():
    print(f'length of secret key: {secret_key_len} bytes')
    message = b'This is a test message.'
    tag = authenticate(message)
    print(f'message = {message} ({len(message)} bytes)')
    print(f'tag = {tag.hex()}')
    assert tag.hex() == 'a587c96990b5d6ea1ba9dbec664bb7aa0df1a7176a2b87a590f87ae9600d2c30'
    assert verify(message, tag)


if __name__ == '__main__':
    main()
