
ref：
- [zhihu1](https://zhuanlan.zhihu.com/p/2064151280365330830)

## tl;dr

高频系统的系列原则
- 大部分的时候，不使用基于节点的容器，包括但不限于：红黑树、AVL、B+树等
- 通过观察数据理解代码出现的问题
- 手工定制（特化）的算法是通往极致性能的关键
- 简单是终极的复杂
- 机械共情（庖丁解牛）
- 

## 用于展开故事的背景

Optiver本身是写高频交易程序的，所以会涉及对买盘（bids）和卖盘（asks）信息的高频查询

挑战有两个：
- 算法必须以最快的速度处理价格更新，因为决策准确性和信息获取速度、时效性直接挂钩
- 每秒会有数万至数十万次价格更新，程序处理得稍慢，网卡缓冲区便会溢出从而导致数据丢失，甚至系统中断

假设策略操作这三个函数（只是假设，实际远更复杂）：

```cpp
void AddOrder(OrderId orderId, Side side, Price price, Volume volume);
void ModifyOrder(OrderId orderId, Volume newVolume);
void DeleteOrder(OrderId orderId);
```

算法涉及一个问题：维护价格有序性的数据结构选择什么？

## std::map

很浅显，买盘卖盘各一个：

```cpp
std::map<Price, Volume, std::greater<Price>> mBidLevels; // 买盘，价格从高到低
std::map<Price, Volume, std::less<Price>> mAskLevels;    // 卖盘，价格从低到高
```

`std::map`是红黑树实现，`AddOrder`是logN级别，`Modify/Delete`几乎是O(1)。在*不受干扰*的环境下，随机操作的benchmark表现也不错。

但一旦在操作间进行随机内存分配，benchmark表现中的延迟便掉了一倍：

![[Pasted image 20260818183223.png]]

导致这种现象的原因是：内存碎片化、缓存局部性差、指针解引用开销

尽管这些数据结构的理论复杂度很优秀，但硬件中缓存是按块存取的。高度局部性的结构可以弥补时间复杂度的不足，而节点数据结构的局部性则会很差

## std::vector

换用`std::vector`+`std::lower_bound`。

```cpp
// 使用 vector 实现
std::vector<std::pair<Price, Volume>> mBidLevels;
std::vector<std::pair<Price, Volume>> mAskLevels;

template <classT, classCompare>
void AddOrder(T& levels, Price price, Volume volume, Compare comp)
{
    // 使用 lower_bound 进行二分查找 O(logN)
    auto it = std::lower_bound(levels.begin(), levels.end(), price,
        [comp](constauto& p, Price price) { returncomp(p.first, price); });

    if (it != levels.end() && it->first == price) // 找到现有层级
        it->second += volume; // O(1)
    else// 需要插入新层级
        levels.insert(it, {price, volume}); // O(N)
}
```

平均耗时好了一些，但尾巴还是很长：

![[Pasted image 20260818184433.png]]

代码本身能说明的事情有限，得看数据，查看操作订单簿各个位置的频率：

**![[Pasted image 20260818184632.png]]

level指代的是订单簿操作索引。有趣但符合直觉的是，越接近订单簿头部，操作越频繁，也就是在最佳价格附近。

这样便引入了一个问题。`AddOrder`会在订单簿头部插入一个新订单，从而让其余元素集体后移一位，代价过高，因此考虑反转vector：

```cpp
// 伪代码逻辑
// 以前：bids = {92, 90, 85} -> 最佳价格在头部
// 现在：bids = {85, 90, 92} -> 最佳价格在尾部
// 获取最佳价格时，使用 rbegin() 即可
auto GetBestPrices() const {
    return {mBidLevels.rbegin()->first, mAskLevels.rbegin()->first};
}
```

考虑到大部分操作现在发生在vector尾部，现在只有深入订单簿的操作才会需要O(N)的高昂移动，所以最新的benchmark中，尾巴消失了：

![[Pasted image 20260818185018.png]]

## 深入到CPU

Linux perf工具可以以较低的开销追踪程序的底层行为，从而分析程序的性能瓶颈

使用`perf stat -I 10000 -M Frontend_Bound,Backend_Bound,Bad_Speculation,Retiring`发现，`vector+reverse`程序存在25%的*错误分支预测*。分支预测是现代流水线CPU通用的一种策略，但一旦分支预测出了错，流水线需要清空+重建，损失数至十数个周期，因此不可接受。

![[Pasted image 20260819141451.png]]

`perf record`可以进一步定位到，程序中大部分的分支预测错误来自`std::lower_bound`内的二分查找。

考虑到标准库的二分解决不了问题，最好的方法是定制一个算法，规避分支预测错误的问题：

```cpp
template <classForwardIt, classT, classCompare>
ForwardIt branchless_lower_bound(ForwardIt first, ForwardIt last, const T& value, Compare comp)
{
    auto length = last - first;
    while (length > 0)
    {
        auto half = length / 2;
        // 关键：用计算代替分支
        // comp(...) 返回 0 或 1，结果要么是 first += 0，要么 first += (length-half)
        first += comp(first[half], value) * (length - half);
        length = half;
    }
    return first;
}
```

这种做法的原理是：`cmov`指令会计算条件值，用计算规避分支预测失败。收益也是显著的，平均耗时又降了3ns：

![[Pasted image 20260819142325.png]]

## 线性搜索（？）

目前的进展是：`vector+reverse+定制二分算法`

目前算法还有个问题：内存访问还是太过跳跃了，内存局部性比较差。所以尝试线性搜索平替二分，结果是出人意料的：线性比二分快

![[Pasted image 20260819142537.png]]

为什么：
- 线性搜索会顺序访问内存，局部性更强，对缓存和数据prefetcher也极为友好
- 线性搜索的分支操作极少，只有比较和递增
- 对于足够小的N，低常数O(N)会赢过高常数O(logN)。在现代计算机的缓存系统中，N可能很大

不要迷信理论复杂度；简单可预测的内存访问模式更可以发挥硬件的威力

越简单有效的解法，越接近问题的本质

## 共情机械

> [!note]
> Mechanical Sympathy. 庖丁解牛。

软件运行在物理硬件上。CPU 有多级缓存、指令流水线、分支预测器、预取器、SIMD 单元等。理解这些硬件特性并利用它们，是实现极致性能的关键。

在前面的事情都做完了之后，如果还不够，这些事情是值得一做的：
- 分支预测提示（[[Cpp优化小记#分支预测提示]]）
- 冷代码分离（`[[noinline]]`、`[[cold]]`）：将一大块核心代码中，执行频次较低的部分移出核心代码段，给代码瘦身
- lambda over `std::function`

## 从内核到用户态

*内核旁路*（kernel bypass）：绕过OS+层层协议栈，让应用程序直接和网卡对接

![[Pasted image 20260819143700.png]]

或者更进一步，用EF\_VI/DPDK，直接让应用程序控制数据包收发+缓冲区管理，高风险高回报

这些技术不仅省去了从内核到用户态的一次数据拷贝，还规避了协议栈可能引入的其他复杂细节

![[Pasted image 20260819143930.png]]

Linux内核很精美，但对于我们纯粹的需求（尽可能快地收发+处理数据包），它可能会引入不必要的开销

## 共享内存与消息分发

WIP

## 性能监控

WIP

## 系统是一个整体

WIP

## 与他人合作

WIP