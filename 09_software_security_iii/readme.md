# Exercises: Software Security III -- Finding Bugs

Today we are talking about different classes of bugs and how we can use tools
to find them.



## 1. Classes of Vulnerabilities

During the course, we have seen many different kinds of vulnerabilities in software.
For [assignment 3](https://github.com/dfaranha/au-syssec-f24-assignments/edit/main/software/readme.md), you will be asked to reproduce an exploit for a notorious software vulnerability.

1. Think about what *classes of bugs* you can think of, e.g., what you have
   encountered in this course or in other context and collect them on a text file.

2. Think about whether they are security relevant, i.e., could an attacker exploit them?

3. Take a look at the [Common Weakness
   Enumeration](https://cwe.mitre.org/index.html) -- a project that lists and
   categorizes security-related problems and their relationships in software
   and hardware.

   Try to find some of the vulnerability classes you though of in CWE.

   You can for example use the following views to navigate CWE:

    - [CWE VIEW: Software Development](https://cwe.mitre.org/data/definitions/699.html)
    - [CWE VIEW: Research Concepts](https://cwe.mitre.org/data/definitions/1000.html)
    - [CWE VIEW: Weaknesses in the 2021 CWE Top 25 Most Dangerous Software Weaknesses](https://cwe.mitre.org/data/definitions/1337.html)



## 2. Using Sanitizers

C is a widely used programming language.  It is, however, easy to make mistakes
that often lead to security problems behavior.  Fortunately, the available
tooling has improved in recent years.

Very helpful are the so-called *sanitizers* available in the GCC and Clang
compilers.  When enabled, these sanitizers instrument the resulting binary
program with additional checks.  At run-time, the inserted checks are able to
detect certain classes of errors and provider information to the developer
where/how the error occurred.  Hence, it is compile programs (or test suites)
with sanitizers to detect bugs that otherwise would not have had directly
observable consequences.

You are given three programs `address.c`, `thread.c`, and `undefined.c` which
contain very questionable code and different kinds of bugs to demonstrate the
powers of the different sanitizers.  Run `make` to compile them.


### 2.1 AddressSanitizer (ASan)

The manual memory management and the absence of automatic bounds checking in C
are major sources of trouble.  The AddressSanitizer, enabled with
`-fsanitize=address`, is able to detect such mistakes.

Consider the program `address.c` which is obviously buggy.
```
$ ./address AAAAAAAAAAAAAAA BBBBBBBBBBBBBBB
What's your name?
lennart
============== Moin lennart ==============
Do you like pointers?
YES!
WTF???
free(): invalid pointer
[1]    2385487 abort (core dumped)  ./address AAAAAAAAAAAAAAA BBBBBBBBBBBBBBB
```
Run it with ASan and see what kind of errors it detects.


### 2.2 ThreadSanitizer (TSan)

Multi-threading and synchronization is not trivial either.  The
ThreadSanitizer, enabled with `-fsanitize=thread`, is able to detect data races
and other threading-related issues.

Consider the program `thread.c` (some of you might find it familiar) and
observe the inconsistent output:
```
$ ./thread 10000 40
there are 1220 primes up to 10000
$ ./thread 10000 40
there are 1202 primes up to 10000
$ ./thread 10000 40
there are 1209 primes up to 10000
```
Use TSan to detect the problems in the code.


### 2.3 UndefinedBehaviorSanitizer (UBSan)

Undefined behavior can occur when a C program violates a rule given by the C
language standard and the standard does not specify what should happen in this
cases.
Then the compiler as allowed to do as it pleases.

This can be used to generate faster code: The compiler is allowed to assume
that certain invalid things do not happen and can then optimize the code based
on these assumptions

Consider the program `undefined.c` and follow the comments in the file.  Use
UBSan, enabled with `-fsanitize=undefined`, to detect possible issues.
```
$ ./undefined 36 6
36
6
no overflow happened :)
42
success
p = 0x7ffd33643991
s = 328350
```

The following articles give a good introduction to the concept of undefined behavior:

- [John Regehr, A Guide to Undefined Behavior in C and C++](https://blog.regehr.org/archives/213)
- [Chris Lattner, What Every C Programmer Should Know About Undefined Behavior](https://blog.llvm.org/2011/05/what-every-c-programmer-should-know.html)



## 3. Fuzzing

Install [American Fuzzy Lop (AFL)](https://lcamtuf.coredump.cx/afl/) (or its
successor project [AFL++](https://aflplus.plus/)) and `gcc-multilib`:
```
$ sudo apt install afl gcc-multilib
```

In the directories `random_password` and `broken_register` you find two
programs with corresponding Makefiles.  Use AFL to find crashing inputs.  E.g.,
you can use `afl-gcc` (instead of `gcc`) to compile executables with
instrumentation and `afl-fuzz` to perform the actual fuzzing.


### Bonus: Exploit the Programs

If you are ~~bored~~want a challenge, you can try to exploit the two programs
at home.  These are non-trivial, though, and at least `random_password`
requires concepts that we did not discuss in class.  Goal is to print
`flag.txt` or to get a shell.
