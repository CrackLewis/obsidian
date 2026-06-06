
## 函数调用

无脑`inline`。尽管`inline`在C++中有不同的含义，但内联思想很重要。

## 内存布局

尽量使用连续内存，相同时间段访问的内存尽量相邻，降低缓存的刷新率。

一维数组\>二维表

如果事先知道STL容器（`std::vector`等）的最大容量，可以用`reserve`预分配空间，避免内存反复申请/释放

如果程序时间要求比较极端，且确定STL不会重新分配内存，使用`data`方法访问裸地址，但可能不安全

bitset适合：
- 记录有限个元素是否存在
- 快速计算两个有限集合的交集

## 指令

加减法耗时\<乘法耗时\<除法/取模耗时

现代编译器一般会将乘除法优化为位运算+加减法，但仍无法改变它们耗时的本质

普通计算\<访存\<函数调用\<系统调用/中断

SIMD

并行化（OpemMP/pthread/CUDA）

分支预测判定

### 分支预测提示

现代CPU采用动态分支预测（Branch Prediction Unit）技术对条件跳转指令的走向预测。预测失败将清空流水线，产生约10-20 cycles的性能损失

GCC的`__builtin_expect(cond, val)`内建函数可以：
- 提示GCC`cond`更可能是什么（`val`取0或1）
- GCC将：
	- 执行概率更高的路径放在顺序分支（冷路径）
	- 执行概率更低的路径放在跳转分支（热路径）

```asm
cmp ...  ;被比较的条件
je  L1   ;相等则跳转至L1。先验认为，两个比较值相等概率低，因此将不相等分支放在顺序分支

;likely路径（比较值不相等，执行概率更高）
...
jmp L2

;unlikely路径（比较值相等，执行概率更低）
L1:
...

L2:
...
```

*作用*：对于错误判断等必要但不常触发的冷路径，可以通过提示GCC错误条件成立概率低，来规避热路径跳转的情况

```cpp
#define LIKELY(c) __builtin_expect(c,1)
#define UNLIKELY(c) __builtin_expect(c,0)

void foo(int x) {
	if (UNLIKELY(x < 0)) {
		// print error or something
	}
}
```

## I/O

C方式输入输出\<C++方式输入输出

`fread/fwrite`\<`fscanf/fprintf`

