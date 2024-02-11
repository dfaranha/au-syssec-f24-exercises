"""
Simple, pure Python implementation of SHA-256.
Adapted from the pseudocode given at https://en.wikipedia.org/wiki/SHA-2#Pseudocode
"""

import struct


def sha256(message: bytes) -> bytes:
    """ Calculate SHA-256 sum of the given string.

    We first pad the message to be a multiple of 512 bits and split it into
    512 bit chunks. Then we apply the compression function according to the
    Merkle-Darmgard scheme:
    http://en.wikipedia.org/wiki/Merkle%E2%80%93Damg%C3%A5rd_construction

    message: bytes-like object
        input to be hashed
    returns: bytes of size 32
        digest
    """

    # initial value of the internal state
    internal_state = b'j\t\xe6g\xbbg\xae\x85<n\xf3r\xa5O\xf5:Q\x0eR\x7f\x9b\x05h\x8c\x1f\x83\xd9\xab[\xe0\xcd\x19'

    # TODO implement this
    pass


def sha256_extend(given_hash: bytes, prefix_length: int, message_suffix: bytes) -> bytes:
    """ Perform a length extension attack on SHA-256

    given_hash: bytes-like object of size 32
        given SHA-256 hash to be extended
    prefix_length: int
        length of the unknown prefix inclusive padding
    message_suffix: bytes-like object
        input to be appended
    returns: bytes of size 32
        digest, SHA-256(unknown_prefix || pad(unknown_prefix) || message_suffix)
    """
    assert len(given_hash) == 32
    assert prefix_length % 64 == 0

    # TODO implement this
    pass


def padded_size(message_len: int) -> int:
    """ Compute the resulting size when a message of length message_len is
    padded.
    """
    num_zero_bytes = (64 - (message_len + 1 + 8)) % 64
    return message_len + 1 + num_zero_bytes + 8


def build_padding(message_len: int) -> bytes:
    """ Build padding to pad a message to a multiple of 512 bits. The
    padding will be a 1 bit and as many 0 bits followed by 8 byte length
    so that message + padding (incl. length) is a multiple of 512 bit
    """
    num_zero_bytes = (64 - (message_len + 1 + 8)) % 64
    length = struct.pack('>Q', message_len * 8)
    return b'\x80' + b'\x00' * num_zero_bytes + length


def split_chunks(message: bytes) -> list[bytes]:
    """ Split a message into chunks of 256 bits each."""
    assert len(message) % 64 == 0
    chunks = []
    for i in range(len(message) // 64):
        chunks.append(message[i * 64:(i + 1) * 64])
    return chunks


def compress(input_chunk: bytes, state: bytes) -> bytes:
    """ The SHA-256 compression function.

    Map a 512 bit input chunk and a 256 bit state to a new 256 bit state.

    input_chunk: bytes-like object of size 64
        input chunk to be processed
    state: bytes-like object of size 32
        current internal state
    returns: bytes of size 32
        new internal state

    You don't have to look at the details, it's not important for us how it
    works.
    """

    def rightrotate(n: int, k: int) -> int:
        """ Rotate a 32 bit integer n by k positions to the right."""
        return ((n >> k) | (n << (32 - k))) & 0xffffffff

    # some constants
    k = [0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1,
         0x923f82a4, 0xab1c5ed5, 0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3,
         0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174, 0xe49b69c1, 0xefbe4786,
         0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
         0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147,
         0x06ca6351, 0x14292967, 0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13,
         0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85, 0xa2bfe8a1, 0xa81a664b,
         0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
         0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a,
         0x5b9cca4f, 0x682e6ff3, 0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
         0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2]

    # create a 64-entry message schedule array w[0..63] of 32-bit words
    w = [0] * 64

    # copy chunk into first 16 words w[0..15] of the message schedule array
    for i, val in enumerate(struct.unpack('>IIIIIIIIIIIIIIII', input_chunk)):
        w[i] = val

    # Extend the first 16 words into the remaining 48 words w[16..63] of the
    # message schedule array
    for i in range(16, 64):
        s0 = rightrotate(w[i - 15], 7) ^ rightrotate(w[i - 15], 18) ^ (
            w[i - 15] >> 3)
        s1 = rightrotate(w[i - 2], 17) ^ rightrotate(w[i - 2], 19) ^ (
            w[i - 2] >> 10)
        w[i] = (w[i - 16] + s0 + w[i - 7] + s1) & 0xffffffff

    h0, h1, h2, h3, h4, h5, h6, h7 = struct.unpack('>IIIIIIII', state)
    a, b, c, d, e, f, g, h = h0, h1, h2, h3, h4, h5, h6, h7

    # compression function main loop
    for i in range(64):
        S1 = rightrotate(e, 6) ^ rightrotate(e, 11) ^ rightrotate(e, 25)
        ch = (e & f) ^ ((~e) & g)
        temp1 = (h + S1 + ch + k[i] + w[i]) & 0xffffffff
        S0 = rightrotate(a, 2) ^ rightrotate(a, 13) ^ rightrotate(a, 22)
        maj = (a & b) ^ (a & c) ^ (b & c)
        temp2 = (S0 + maj) & 0xffffffff

        h = g
        g = f
        f = e
        e = (d + temp1) & 0xffffffff
        d = c
        c = b
        b = a
        a = (temp1 + temp2) & 0xffffffff

    h0 = (h0 + a) & 0xffffffff
    h1 = (h1 + b) & 0xffffffff
    h2 = (h2 + c) & 0xffffffff
    h3 = (h3 + d) & 0xffffffff
    h4 = (h4 + e) & 0xffffffff
    h5 = (h5 + f) & 0xffffffff
    h6 = (h6 + g) & 0xffffffff
    h7 = (h7 + h) & 0xffffffff

    return struct.pack('>IIIIIIII', h0, h1, h2, h3, h4, h5, h6, h7)


def main():
    # check that the SHA-256 implementation is correct
    assert sha256(b"").hex() == \
        'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'
    assert sha256(b'The quick brown fox jumps over the lazy dog').hex() == \
        'd7a8fbb307d7809469ca9abcb0082e4f8d5651e46d3cdb762d02d0bf37c9e592'

    # check that length extension works
    given_hash = bytes.fromhex('fcb1b3142d1a0176f66f5901deef70df82ac0ee8860ef960cb99e4a525c9e427')
    prefix_length = padded_size(16 + len(b'This is a test message for MAC computation.'))
    message_suffix = b'???'
    new_hash = sha256_extend(given_hash, prefix_length, message_suffix)
    assert new_hash.hex() == 'bd7f1410e7e16fc34efb9d4efbcb702a7ce9860cf2c3033d7ea03c06f7237b6e'


if __name__ == '__main__':
    main()
