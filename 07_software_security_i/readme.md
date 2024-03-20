# Exercises: Software Security I


## Preliminaries

For today's exercises, you need a Linux environment installed either directly
on your hardware, or in a virtual machine.
Moreover, you need a C compiler to build the challenge executables.

```
sudo apt install build-essential    # on Debian, Ubuntu, etc.
sudo pacman -S base-devel           # on Arch Linux, Manjaro, etc.
```

To compile the programs, you can run the command `make` in this directory.
Some of the operations require root permissions using `sudo` (so check the
`Makefile` if you do not trust us).


## Exercise 1: Time-of-check to Time-of-use (TOCTOU)

In this exercise, we explore so-called TOCTOU vulnerabilities.
Quoting from the [Common Weakness Enumeration (CWE) 367](https://cwe.mitre.org/data/definitions/367.html):

> The software checks the state of a resource before using that resource, but
> the resource's state can change between the check and the use in a way that
> invalidates the results of the check. This can cause the software to perform
> invalid actions when the resource is in an unexpected state.
>
> This weakness can be security-relevant when an attacker can influence the
> state of the resource between check and use. This can happen with shared
> resources such as files, memory, or even variables in multithreaded programs.

In our case we will exploit such a vulnerability to print the contents of a file
that should only be accessible by the root user.


### Background: User IDs in Unix

In Unix systems each user has a user id, a number that identifies this user.
The id of a user can be retrieved using the `id` command:
```
$ id --user alice
1000
$ id --user root
0
```
Moreover, each file is owned by a user. For example, the file `print_user_id`
is owned by the user `alice` with the user id `1000` (see above):
```
$ ls -l print_user_id
-rwxr-xr-x 1 alice users 16K 18. Okt 14:43 print_user_id
```
When a user executes a program, then user ids are associated with the process.
```
$ ./print_user_id
Real user id: 1000
Effective user id: 1000
```
One distinguishes between the *real* and the *effective* user id.
The *real* user id is always the id of the user that executes the program.
The *effective* user id specifies which permissions the program actually has,
and might be different.

Consider the following example, where a program needs more permissions than the
user executing it has:
The `passwd` program can change a users password, and, therefore, needs to
update the operating systems user database.
Normal users, however, do not have permissions to do this.

If the SUID bit of a program is set, then the *effective* user id is set to the
id of the *owner* of the file.
```
$ sudo chown root print_user_id
$ sudo chmod u+s print_user_id
$ ls -l print_user_id
-rwsr-xr-x 1 root users 16K 18. Okt 14:43 print_user_id
$ ./print_user_id
Real user id: 1000
Effective user id: 0
```


### Exploiting a TOCTOU Vulnerability

You are given the program `toctou` and the corresponding source code `toctou.c`.
The program accepts a file name as command line parameter, displays some
information about that file and prints its content.

```
$ ./toctou dummy_file.txt
Real user id: 1000
Effective user id: 0
Selected file: dummy_file.txt
Testing access
File has size 7
Printing file now:
--------------------------------------------------------------------------------
foobar
```

Your goal is to use the program to read the content of the file `flag.txt`,
which belongs to the `root` user and is not readable by other users:
```
$ ls -l flag.txt
-rw------- 1 root root 15 17. Okt 09:43 flag.txt
```

Luckily, the `toctou` program is owned by the `root` user and has the SUID bit
set.
Hence, when run, the *effective* user id is set to `0` and it has the
permission to access the file `flag.txt`.
```
$ ls -l toctou
-rwsr-sr-x 1 root root 17K 18. Okt 14:43 toctou
```

Unfortunately, `toctou` uses the function
[`access`](https://man.archlinux.org/man/access.2) to verify that the executing
user, i.e., the user belonging to the *real* user id, has permissions to view
the file.

**Your task**: Trick the `toctou` program into printing the file `flag.txt`
even though the check should prevent it.

First, generate the `flag.txt` file that contains the string "flag{success!}" and change permissions as follows:
``` 
chmod go-rw flag.txt
sudo chown root:root flag.txt 
```
Also change the following:
``` 
sudo sysctl -w fs.protected_regular=0
sudo sysctl -w fs.protected_symlinks=0
```

<details>
<summary>Hint 1</summary>

Use the time windows between the calls to
[`access`](https://man.archlinux.org/man/access.2) and
[`open`](https://man.archlinux.org/man/open.2) to change the file that `toctou`
is accessing. You can also add a call to `sleep(1);` to help with debugging.

</details>

<details>
<summary>Hint 2</summary>

You can use the command [`ln -s <name of file> <name of
link>`](https://man.archlinux.org/man/ln.1) to create symbolic links to
arbitrary files.

</details>



## Exercise 2: Buffer Overflows

In the C programming language, an array is basically a pointer to the first
element of the array.
In particular, no information about the length is stored and it is not checked
that an accessed index lies within the bounds of the buffer.
If more data is written into a buffer than it has capacity, then the additional
data overwrites whatever is stored behind the buffer in memory.

In this exercise we explore the concept of a
[Stack-based Buffer Overflow (CWE-121)](https://cwe.mitre.org/data/definitions/121.html),
where the buffer is an array that has been statically allocated on the stack.


### Background: Stack Layout

To remind you of the typical stack layout, consider the following two functions:

```c
void foo() {
    char blubb[8];
    int answer;
    answer = bar();
    printf("The answer is %d\n", answer);
    return 42;
}

int bar() {
    int six = 6;
    int seven = 7;
    return six * seven;
}
```

The function `foo` has two local variables `blubb` and `answer` which are stored on the stack.
Then it makes a call to the other function `bar` and creates a new stack frame:
In order to remember where to continue the execution of the program after `bar`
has returned, the return address, i.e., the address of the next instruction
after the call, is stored on the stack.
Then the current base pointer (`rbp`, also called frame pointer) is saved to
the stack, and `rbp` is updated to point to the current top of the stack.
Finally, the stack pointer (`rsp`) is advanced to allocate space for the local
variables of the function `bar`.

The following drawing illustrates the stack layout:

```
.                                 .  0xff...ff (high addresses)
.                                 .                                                   .
.                                 .                                                   .
.                                 .                                                   .
|                                 |                                                   |
+---------------------------------+ <--+                                              |
|                                 |    |                                              | Stack Frame of the
|  Local Variables of the Caller: |    |                                              |
|                                 |    |                                              | function `foo`
|    char[8] blubb;               |    |                                              |
|    int answer;                  |    |                                              |
|                                 |    |                                              |
+---------------------------------+    |                                            --+--
|         Return Address          |    |                                              |
|  (address of the printf call)   |    |                                              |
+---------------------------------+    |                                              |
|     Saved Base Pointer (rbp)    |----+                                              |
+---------------------------------+ <--- current rbp (Base Pointer)                   | Stack Frame of the
|                                 |                                                   |
|  Local Variables of the Callee  |                                                   | function `bar`
|                                 |                                                   |
|    int six;                     |                                                   |
|    int seven;                   |                                                   |
|                                 |                                                   |
+---------------------------------+ <--- rsp (Stack Pointer)                        --+--
.                                 .
.                                 .
.     Unallocated Stack Space     .
.                                 .
.                                 .  0x00...00 (low addresses)
```



### Part 1: Overflowing a Buffer

Now consider the following program `overflow1.c`:

```c
#include <stdio.h>
#include <stdint.h>
#include <unistd.h>


void win() {
    printf("Success!\n");
}

void vuln() {
    uint64_t x = 0x42;
    char name[32];

    printf("Please enter your name: ");
    read(0, name, 320);
    printf("Hello %s!\n", name);

    printf("x == %lx\n", x);
    if (x == 0x1337) {
        win();
    }
}

int main() {
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    vuln();
}
```

The `vuln` function asks you to input your name and then prints a greeting.
There is also a local variable `x` which is initialized with the value 0x42 and
never modified.
At the end of the function, the program checks whether `x` has obtained the
value 0x1337, which clearly should never happen.
If the check would pass, then the function `win` would be executed.

**Your task**: Find a way to change the variable and execute `win`. When compiling, be sure to add the `-fno-stack-protector` flag.

To feed raw bytes to the program you can use, e.g., `python` or `echo` and
connect its output with a pipe to the program's input:
```
python -c "import os; os.write(1, b'foobar_\xc0\xff\xee')" | ./overflow1
echo -en "foobar_\xc0\xff\xee" | ./overflow1
```


### Part 2: Changing the Control Flow

Now we have modified the program a bit (`overflow2.c`):
```c
#include <stdio.h>
#include <stdint.h>
#include <unistd.h>


void win() {
    printf("Success!\n");
}

void vuln() {
    char name[32];

    printf("win is located at %p\n", win);
    printf("Please enter your name: ");
    read(0, name, 320);
    printf("Hello %s!\n", name);
}

int main() {
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    vuln();
}
```

The goal is still to execute the `win` function, but the program does not
contain a call to `win` anymore.
Hence, instead of overwriting a local variable, you need to overwrite the
program's return address with the address of the function `win`.

**Your tasks**:
1. Find the address of the function `win` in the binary program.
2. Find the offset of the return address relative to the beginning of the
   buffer `name`.
3. Exploit the buffer overflow with a payload that overwrites the return
   address with the address of `win`.

<details>
<summary>Hint</summary>

You can use the command [`objdump -M intel -d <name of
executable>`](https://man.archlinux.org/man/objdump.1) to disassemble binaries.
In the disassembly you can find the required address and the location of the
buffer `name` relative to the base pointer.

</details>


### Bonus Part 3: Executing Shellcode

In `overflow3.c` the `win` function has disappeared.
Luckily, the stack is now executable, so we can inject our own code into the `name` buffer and execute it.

We want to use the syscall `execve` to spawn a shell so that we can execute arbitrary commands.
```c
execve("/bin/sh", {NULL}, {NULL});
```
You can find information on `execve` on its [manpage of the C wrapper
function](https://man.archlinux.org/man/execve.2) and in the [syscall
reference](https://filippo.io/linux-syscall-table/).

Try to understand the following shellcode which executes the systemcall:
```nasm
# store b'/bin/sh\0' on the stack
mov rax, 0x68732f6e69622f
push rax
# load a pointer to the string into rdi
mov rdi, rsp
# store a NULL pointer on the stack
xor rax, rax
push rax
# load a pointer to the null pointer into rsi and rdx
mov rsi, rsp
mov rdx, rsp
# load the syscall number of execve into rax
mov rax, 0x3b
# execute the syscall
syscall
```
You can for example use the [Online
Assembler](https://defuse.ca/online-x86-assembler.htm) (remember to select
"x64") to assemble the shellcode to obtain executable machine code.

To complete the exploit, we still need the address where we want to jump, i.e.,
the address of the shellcode inside the `name` buffer.
The program is nice enough to print the address of `name` to us, and if you run
it with the command `setarch $(uname -m) -R ./overflow3`, then ASLR is disabled
and the address stays the same in each execution.

```
(python -c "import os, struct; os.write(1, b'<write your payload here>)"; cat) | setarch $(uname -m) -R ./overflow3
```
If everything works, you should land in a newly spawned shell (the `cat` is
necessary to prevent the shell from getting immediately closed again).
Try executing commands.



## Solutions

See [here](solutions.md) for example solutions.
