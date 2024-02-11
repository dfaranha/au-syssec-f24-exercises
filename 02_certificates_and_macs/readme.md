# Exercises: Certificates and MACs


## Exercise 1: Textbook RSA in Python

For this exercise, you must again need the PyCryptodome library we used last week.

1. Run the Python program `rsa.py` attached by passing two arguments: (i) the key size
   in bits (size of the modulus N); (ii) an integer to be encrypted (modulo N):

```
$ python3 rsa.py 1024 <plaintext>
```

2. Take a look at the implementation to see a direct translation from the
   textbook RSA version we saw on class. Try to encrypt different messages, and especially very short ones.

Remember that textbook RSA is insecure and serves only for illustration, use a
standardized version instead.



## Exercise 2: Verifying a Public-Key Certificate Chain

To illustrate how public-key certificates work, in this task we will manually
verify an X.509 web server certificate using the issuer's public key. You will
need OpenSSL installed, which is already the case for Ubuntu.
You can find details about the `openssl` command line tool on its
[manpages](https://man.archlinux.org/man/core/openssl/openssl.1ssl.en).
It contains a lot of functionality and in this exercise, we will
use the subcommands
[`s_client`](https://man.archlinux.org/man/s_client.1ssl.en),
[`verify`](https://man.archlinux.org/man/verify.1ssl.en),
[`x509`](https://man.archlinux.org/man/x509.1ssl.en), and
[`asn1parse`](https://man.archlinux.org/man/asn1parse.1ssl.en)
as described below.
The exercise is heavily inspired on [SEED Project's PKI
Lab](https://seedsecuritylabs.org/Labs_20.04/Crypto/Crypto_PKI/).

1. Choose a hostname using only RSA in their certificate chain and download the server certificate. We suggest `www.facebook.com`, since it has a simple chain of 3 RSA certificates. You
   can use a browser or command-line OpenSSL:

```
$ openssl s_client -connect <hostname>:443 -showcerts
```

2. The command will show you the certificate chain from a root certificate
   installed in your system to the web server certificate. This typically
   contains n = 2 certificates when an
   intermediate CA is involved. Copy the i-th certificate in the chain (lines
   between and including `BEGIN_CERTIFICATE` and `END_CERTIFICATE`) and save it
   in the format `cert_i.pem`, so that you get files `cert_0.pem`, ...,
   `cert_(n-1).pem`.

3. Find the CA from the output above and search the root certificate in the
   local trusted storage `/etc/ssl/certs`. Copy it to the local folder you are
   working on under the name `cert_n.pem`.

   Note that the Let's Encrypt chain used to verify many hosts (e.g. twitter.com and cs.au.dk) is [a bit more complicated](https://letsencrypt.org/certificates/).

4. Verify the certificate chains by specifying the root CA and the server
   certificate in the `openssl verify` command. For example, with 2
   certificates (`cert_2.pem` is the root, `cert_1.pem` is the intermediate and
   `cert_0.pem` is the server) you can use the command below:

```
$ openssl verify -no-CAstore -no-CApath -show_chain -verbose -trusted cert_2.pem -untrusted cert_1.pem cert_0.pem
```

5. We will now see what is exactly being performed in this verification
   procedure by extracting the signatures and verifying manually. We can
   extract both the RSA modulus and public exponent from the issuer or
   intermediate certificate with the command below:

```
$ openssl x509 -in cert_1.pem -noout -text -modulus
```

6. We can also extract a signature of a certificate by running the command
   above over `cert_0.pem` and looking for both the Signature Algorithm and the
   field that comes right below. With high probability it will be a
   `sha256withRSAEncryption`, but adjust what follows if this is not the case.
   Save the resulting signature without spaces or : to a file `sign_0.txt`

7. Now let us extract and hash the contents of the certificate that end up
   being signed:

```
$ openssl asn1parse -i -in cert_0.pem -strparse 4 -out cert0_body.bin -noout
$ sha256sum cert0_body.bin
```

8. Now let us use Python to verify the signature by defining Exponent, Modulus,
   Signature and the Hash as big integers and performing the computation. See
   example below:

```
>>> Modulus=0xB6E02FC22406C86D045FD7EF0A6406B27D22266516AE42409BCEDC9F9F76073EC330558719B94F940E5A941F5556B4C2022AAFD098EE0B40D7C4...

>>> Exponent = 65537
>>> Hash = 0x135c2a2d9142359d8a00fdb500c145d61badee5f32cf4b362d9aa54296a85c57
>>> Signature = 0x49b920e76237dc1d9e757078f0a465707fa28a0703d73d6b3696bfb8e482836050d6b6473d08ceb937c85a1316a4f9493f9e9451ff495cd26c5922c31397f69c49849c1...
```

9. The computation below should reveal the Hash in the lowest significant bytes
   of the result (the rest is padding):

```
>>> hex(pow(Signature, Exponent, Modulus))
```

10. Now repeat the same procedure for the next certificate in the chain until
    you reach the root. What changes for the self-signed root certificate?



## Exercise 3: Length Extension Attacks

Given a cryptographic hash function `H`, a simple (but insecure) Message
Authentication Code (MAC) construction is hashing a secret key `K` concatenated
with a message `M` as `H(K || M)`. Depending on how the hash function is
constructed, this allows an adversary to compute a valid MAC for a message `M'`
from the MAC of a message `M` which is a prefix of `M'`. This is particularly
feasible if the hash function is constructed using the Merkle-Damgård paradigm,
but the usage of padding can complicate matters a little bit.

The attached Python program implements this simple idea and computes the MAC of
message `M = 'This is a test message'` using the `K = 'VERY_SECRET_KEY_'` (without
quotes) using the SHA-256 implementation of Python's standard `hashlib` module.
You run the program with the command line below:

```
$ python mac.py
```

The result should be the same as running the following command in your terminal:

```
$ echo -n "VERY_SECRET_KEY_This is a test message." | sha256sum
0e3542399804e2ddc76f80c59858f82a41d21280cff7b64ded86edbb0bab191a  -
```

Notice that the padding is handled internally in a transparent way.  The block
size of SHA-256 is 64 bytes, so a message `M` will be padded to the multiple of
64 bytes during the hash calculation.  According to RFC 6234, the padding for
SHA-256 consist of one byte of 0x80, followed by a many 0’s, followed by a
64-bit (8 bytes) length field (the length is the number of bits in `M`).

The total length of the hash input is 39 bytes, so the padding is then 64 - 39
= 25 bytes, including 8 bytes for the length field (in big endian format). The
length will be 39 * 8 = 312 = 0x138. The padded message looks as follows:

```
padded_message = b'VERY_SECRET_KEY_This is a test message.' \  # message
               + b'\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
               + b'\x00\x00\x00\x00\x00\x00\x01\x38'  # length
```

Your task is to:

1. Complete the implementation of `sha256` function given in `sha256.py`. The
   file contains a couple of building blocks you can use, e.g., for padding and
   the compression function.  With these, only a handfull of lines are missing.

2. Study the Merkle-Damgård paradigm and think about how the MAC for one
   message (plus padding) can be extended to another message containing the
   first message (plus padding?) as a prefix.

3. Complete the implementation of `sha256_extend` and use it to extend the
   computed MAC tag
   `fcb1b3142d1a0176f66f5901deef70df82ac0ee8860ef960cb99e4a525c9e427` under an
   unknown 16 byte key for the message
   `b'This is a test message for MAC computation.'`
   to a longer message. You can use any programming language you would like.
