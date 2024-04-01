# Exercises: Software Security II -- Return-Oriented Programming


Today we will use return-oriented programming (ROP) to exploit a stack-based
buffer overflow in the vulnerable program `rop_me`.


## 1. Finding ROP Gadgets

Use [`objdump`](https://man.archlinux.org/man/objdump.1) with the `-d` flag to
disassemble the binary (`-M intel` selects the Intel assembly syntax).
```
objdump -M intel -d rop_me
```
For convenience, you can use the [`less`](https://man.archlinux.org/man/less.1)
pager, which, e.g., enables nicer scrolling (you can quit it with `q`):
```
objdump -M intel -d rop_me | less
```
Now look for ROP gadgets, i.e., sequences of instructions ending with `ret`.
Copy gadgets you found into [this
Etherpad](https://ep.mafiasi.de/p/6cb4cdb5c1bed526-syssec_rop_gadgets) and
remember to include the address of the gadget.



## 2. Composing a ROP Chain


Use the provided ROP gadgets to compose a chain that will spawn a shell with
the `execve` syscall.
```c
execve("/bin/sh", {NULL}, {NULL});
```
For this you have to set the registers in the following way:

| Register | Value                             |
| -------- | --------------------------------- |
| rax      | 0x3b (syscall number of execve)   |
| rdi      | "/bin/sh" (pointer to the string) |
| rsi      | NULL (pointer to a NULL pointer)  |
| rdx      | NULL (pointer to a NULL pointer)  |



## 3. Implementing the Exploit (Bonus)

The binary is also running on a server, and you can talk to it via
[`netcat`](https://man.archlinux.org/man/netcat.1):
```
$ nc rop.syssec.dk 1337
to execute a program (e.g., a shell), you can use the execve syscall
[...]
ROP me!
```

Write a program that outputs your ROP chain and feed it to the the remotely running program.
(The `cat` trick is used again to keep the input open and allow commands to be entered.)
```
$ (python exploit.py; cat) | nc rop.syssec.dk 1337
to execute a program (e.g., a shell), you can use the execve syscall
- rax = 0x3b (syscall number)
- rdi = <pointer to the command> (e.g., "/bin/sh")
- rsi = <pointer to a NULL-terminated array of arguments> (e.g., pointer to a NULL pointer for no arguments)
- rdx = <pointer to a NULL-terminated array of environment variables> (e.g., pointer to a NULL pointer for no arguments)
useful values:
- string "/bin/sh" at address 0x402012
- pointer "(nil)" at address 0x404080
- readable/writable 1024 B array at address  0x4040a0
ROP me!
read 160 bytes from standard input
cat flag.txt
flag{this_is_not_the_flag}
```
