#!/usr/bin/env python3

from datetime import datetime
import random
import sys
import time
from tqdm import tqdm # install the tqdm package for a fancy progress bar
from Crypto.Cipher import AES


def decrypt(date, input_file, output_file):

    date = datetime.strptime(date, '%Y-%m-%d')
    t_start = int(date.timestamp())

    with open(input_file, 'rb') as f_in:
        nonce = f_in.read(16)
        tag = f_in.read(16)
        ciphertext = f_in.read()

    #  for t in range(t_start, t_start + (60 * 60 * 24)):  # <- use this instead of the following line if you don't have tqdm
    for t in tqdm(range(t_start, t_start + (60 * 60 * 24))):
        random.seed(t)
        key = random.randbytes(16)
        try:
            aes = AES.new(key, AES.MODE_GCM, nonce=nonce)
            plaintext = aes.decrypt_and_verify(ciphertext, tag)
            break
        except:
            continue
    else:
        print('decryption failed')

    with open(output_file, 'wb') as f_out:
        f_out.write(plaintext)


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print(f'usage: {sys.argv[0]} <date> <src-file> <dst-file>', file=sys.stderr)
        exit(1)
    decrypt(sys.argv[1], sys.argv[2], sys.argv[3])
