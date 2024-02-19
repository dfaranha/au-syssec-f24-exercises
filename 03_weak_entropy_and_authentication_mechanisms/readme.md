# Exercises: Weak Entropy and Authentication Mechanisms

## Exercise 1: Authentication Mechanisms

We will classify authentication mechanisms described in a set of printed slides according to the taxonomy we saw on class, and rank from the least secure to the most secure. The class will be split in at most 8 groups, each with its own set of slides. There will be two activities in the exercise:

1. First, classify all different authentication solutions into the 4 types given. Use the diagram below as a reference example. Consider that a user is authenticating against some service provider, and the classification should be performed from the point of view of the service provider and what authentication factors must be managed by it.

<p align="center">
  <img src="https://user-images.githubusercontent.com/5369810/134070931-a702ac64-8d96-45e1-a1fb-bc8846e572b9.png" />
</p>

2. After all solutions are classified, organize each column from **least** secure (on bottom) to **most** secure (on top).

**Observation:** _There is no single correct solution, the point is exactly to discuss the trade-offs. Assume a realistic implementation (not horrible or perfect) working in realistic conditions._

### Sample Solution (most to least secure)

Ownership Factors
* Cryptographic Token or challenge-response
* Authenticator App (most people often have their phones, good as a second factor)
* One-time Password Device (more likely to be lost than a phone with authenticator app)
* Credit Card with NFC (more secure than magnetic stripe)
* Microchip beneath the skin (cannot be stolen, but very invasive and new technology)
* Password Book (could be copied or stolen)
* Government-issued ID card (relatively easy to forge or steal)
* Credit Card (Magnetic stripe) (easy to copy or steal)

Multiple Factors
* Credit Card with PIN and fingerprint (all 3: knowledge, ownership & inherent)
* NemID (password and app/number card)
* Credit card with chip and PIN (ownership & knowledge)
* University Access Card (ownership & knowledge)

Inherent Factors (raking depends on criteria, one possibility is easeness of capture and replay signal)
* Keystroke Rhythm (hard to clone if deeply embedded in the OS)
* Fingerprint Scanning (we leave fingerprints around, but sensors measure liveness too)
* Gait/Palm/Iris Recognition
* Voice Recognition (easy to capture and replay)
* Face Recognition (easy to fool current face recognition)
* DNA Sample (we leave traces everywhere)
* Handwritten Signature (relatively easy to forge)

Knowledge Factors
* Password Manager (Master Password)
* Passphrase (sometimes easy to guess)
* Username/Password (many people use the same password for many accounts)
* Personal Identification Number (PIN) (sometimes short and easy to guess)
* Security Question (information could be easy to find or guess)

## Exercise 2: Weak Entropy

I have a big problem: When preparing this exercise last Monday, I encrypted a
very important file.  Unfortunately, I forgot to save the key, and now I cannot
access the data anymore.  Can you help me decrypt it?

This is the command that I used:
```
$ python encrypt.py plain.txt ciphertext.bin
```


### Solution

See [`decrypt.py`](decrypt.py) for a brute force attack over possible keys.
Use it like this:
```
$ python decrypt.py 2021-09-20 ciphertext.bin decrypted.txt
```
