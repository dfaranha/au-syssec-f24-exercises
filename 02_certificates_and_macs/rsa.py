import sys
import Crypto.Util.number
from Crypto.Util.number import getPrime, GCD, inverse


def main(bits, message):

    # key generation
    while True:
        # sample two different primes
        p = getPrime(bits // 2)
        q = getPrime(bits // 2)
        if p == q:
            continue
        N = p * q
        phi = (p - 1) * (q - 1)
        e = 65537
        # e needs to be invertible modulo phi(N)
        if GCD(e, phi) > 1:
            continue
        d = inverse(e,phi)

        print(f"Random Prime p = {p}")
        print(f"Random Prime q = {q}")
        print()
        print(f"Modulus N = {N}")
        print(f"Public exponent e = {e}")
        print(f"Private exponent d = {d}")
        break

    # encryption

    m = message % N
    enc = pow(m, e, N)
    dec = pow(enc, d, N)
    print()
    print(f"RSA ciphertext c = m ^ e mod N = {enc}")
    print(f"RSA plaintext c ^ d mod N = {dec}")
    assert dec == m


if __name__ == '__main__':
    if (len(sys.argv) < 3):
        print(f'usage: {sys.argv[0]} <bits> <message>', file=sys.stderr)
        exit(1)
    main(int(sys.argv[1]), int(sys.argv[2]))
