
网上有数个版本的lab，每版题目都不尽相同。这里以CS:APP 3e官网的lab为准，做一份属于自己的踩坑记录。

## datalab

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

## bomblab

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

`phase_1`函数的源码如下：

```asm
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

