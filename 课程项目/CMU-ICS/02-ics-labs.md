
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

