
## outline

- 机试简介：机试分析、编程语言、输入输出技巧、复杂度
- 入门经典问题：排版类、日期类、字符串类、排序类

## E01-机试分析

### Python输入输出

Python的stdin：

```python
import sys

for i in range(n):
	line = sys.stdin.readline()
```

一行读多个数据：

```python
int_list = list(map(int, input().split(' ')))
str_list = list(map(str, input().split(' ')))
```

### Java输入输出

Java的Scanner：

```java
Scanner sc = new Scanner(System.in);
while (sc.hasNext()) {
	String s = stdin.next();
	int n = stdin.nextInt();
	double b = stdin.nextDouble();
}
```

### 主定理

主定理是一种复杂度分析工具

设：
- $n$是问题规模
- $a$是子问题个数
- $b$是原问题和子问题的规模比例
- $f(n)$是原问题分解为子问题，以及子问题解合并为原问题解的成本

主定理：对于如下递归式算法的渐进时间复杂度
$$
T(n)=aT\left(\dfrac{n}{b}\right)+f(n)
$$
设$N=\log_n f(n$)，则：
- 若$N<\log_b a$，则$T(n)=O(n^{\log_b a})$。
- 若$N=\log_b a$，则$T(n)=O(n^{\log_b a}\cdot \log n)$。
- 若$N>\log_b a$，则$T(n)=O(f(n))$。

例如：
- $T(n)=T(3n/4)+n$：$N=1,\log_b a=0\Rightarrow T(n)=O(n)$。
- $T(n)=4T(n/2)+n^2$：$N=2,\log_b a=2\Rightarrow T(n)=O(n^2\log n)$。

## E02-机试上

各语言的字符串API：

![[Pasted image 20240127210724.png]]

字符串题型：统计字符、大小写转换、字符加解密、统计子串出现次数、无重复字符的最长子串