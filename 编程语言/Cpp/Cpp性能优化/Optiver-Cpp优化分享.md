
ref：
- [zhihu1](https://zhuanlan.zhihu.com/p/2064151280365330830)

## tl;dr

高频系统的系列原则
- 大部分的时候，不使用基于节点的容器，包括但不限于：红黑树、AVL、B+树等
- 通过观察数据理解代码出现的问题

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

