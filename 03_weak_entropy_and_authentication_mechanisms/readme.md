# Exercises: Weak Entropy and Authentication Mechanisms

## Exercise 1: Authentication Mechanisms

We will strengthen your authentication mechanisms by adopting a password manager and hardening its default configuration.

1. First, find a password manager that is compatible with your personal choices of operating system and mobile device. There are many options here, and some popular suggestions are LastPass, 1Password, Dashlane and BitWarden. An open-source solution with somewhat lower usability is KeePass. You should favor any options that support multi-factor authentication as a free option, not requiring a paid subscription.

**Note**: If you already are a user of a password manager, use this exercise to _harden_ your setup instead.

3. Install and create an account in your password manager software. Pick a long passphrase containing at least 6 words by using the [Diceware](https://diceware.dmuth.org/) (or a similar) method.

4. Use the [have i been pwned](https://haveibeenpwned.com/) service to detect if any of your credentials was observed in a data breach included in their database.

5. Migrate some accounts to your new password manager by resetting their passwords and picking the random replacements suggested by the password manager. We do not suggest migrating your e-mail account, since that will be needed to recover your password manager account itself in case the passphrase is lost.

6. Find what options are supported for multi-factor authentication in your password manager, and pick one to setup.

7. Attempt to harden your password manager configuration by finding out what is the current choice of iterations for the password hashing function -- typically [PBKDF2](https://en.wikipedia.org/wiki/PBKDF2) -- and what the recommended best practices are.

8. Think of other ways to harden your account further, for example using it strictly in offline mode (to reduce attack surface) or a secure backup policy for the unlikely case of losing access to your passphrase.

## Exercise 2: Weak Entropy

I have a big problem: When preparing this exercise last Monday, I encrypted a
very important file.  Unfortunately, I forgot to save the key, and now I cannot
access the data anymore.  Can you help me decrypt it?

This is the command that I used:
```
$ python encrypt.py plain.txt ciphertext.bin

