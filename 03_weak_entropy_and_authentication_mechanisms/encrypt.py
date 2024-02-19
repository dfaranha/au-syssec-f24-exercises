#!/usr/bin/env python3

import random
import sys
import time
from Crypto.Cipher import AES


def encrypt(input_file, output_file):
    random.seed(int(time.time()))
    key = random.randbytes(16)
    aes = AES.new(key, AES.MODE_GCM)

    with open(input_file, 'rb') as f_in:
        data = f_in.read()
    ciphertext, tag = aes.encrypt_and_digest(data)

    with open(output_file, 'wb') as f_out:
        f_out.write(aes.nonce)  # 16 bytes
        f_out.write(tag)        # 16 bytes
        f_out.write(ciphertext) # len(data) bytes


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(f'usage: {sys.argv[0]} <src-file> <dst-file>', file=sys.stderr)
        exit(1)
    encrypt(sys.argv[1], sys.argv[2])
