
$$
\text{ReLU}(x)=\max(0,x)
$$

该激活函数比较常用，但容易出现神经元死亡的情况。其变种可以规避这个问题，其中$a\in (0,1)$是超参数：

$$
\text{LeakyReLU}(x)=\max(ax,x)
$$

