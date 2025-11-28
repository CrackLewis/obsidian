
![[Pasted image 20230430154510.png]]

History:
- 1986: BP-Algorithm
- 1998: BP->LeNet5
- 2006: Deep Learning
- 2012: DL model dominates ImageNet

## 全连接层

### 神经元

![[Pasted image 20230430160547.png]]

$$
y=f(x_1\cdot \omega_1 + x_2\cdot \omega_2+x_3\cdot \omega_3-1)
$$

### BP算法

- 信号的前向传播
- 误差的反向传播

## 卷积层

卷积：一个在像素图上滑动的窗口矩阵。

特性：
- 局部感知机制
- 权值共享

![[Pasted image 20230430162310.png]]

卷积层：
- 卷积核个数=输出特征矩阵的深度（channel）
- 卷积核的channel=输入特征层的channel
![[Pasted image 20230430162639.png]]

### 激活函数

激活函数：非线性因素，引入非线性问题的解决能力。

Sigmoid激活函数：
$$
f(x)=\frac{1}{1+e^{-x}}
$$

ReLU激活函数：
$$
f(x)=\max(0,x)
$$

实际更常用ReLU。

对比：
- Sigmoid：饱和时梯度太小，网络层数较深时出现梯度消失。
- ReLU：反向传播时，如果梯度过大，更新后权重分布中心小于零，导致导数始终为0，反向传播无法更新权重，从而失活。

### 越界问题

卷积操作可能遇到：像素图的最后几列凑不齐一次卷积，所以通过padding手段增加几列。

设输入为$W*W$，滤波器为$F*F$，步长为$S$，padding宽度为$P$，则卷积后矩阵尺寸满足
$$
N=\frac{W-F+2P}{S}+1
$$

![[Pasted image 20230430163850.png]]

$W=4,F=3,S=2$，由于上面的例子只补一侧，所以取
$$
N=\frac{W-F+P}{S}+1=\frac{4-3+1}{2}+1=2
$$
本例中$P=1$。

## 池化层

目的：对特征图进行稀疏处理，减少数据运算量。

![[Pasted image 20230430201638.png]]

- 最大池化：max-pooling，取每个池的最大值
- 平均池化：avg-pooling，取每个池的平均值

特点：
- 没有训练参数
- 只改变特征矩阵的$w$和$h$，并不会改变channel
- 一般poolsize和stride相同

## 误差计算

![[Pasted image 20230430203015.png]]

原始输出满足：
$$
y_i=\sum_{k=1}^3 w_{ki}^{(2)} \sigma(w_{1k}^{(1)}x_1+w_{2k}^{(1)}x_2+b_{k}^{(1)})+b_{i}^{(2)}
$$

softmax输出满足：
$$
o_i=\frac{e^{y_i}}{\sum_{j} e^{y_j}}
$$

计算损失一般使用交叉熵损失。针对多分类问题（softmax输出），有：
$$
H=-\sum_i o_i^**\log(o_i)
$$

针对二分类问题（sigmoid输出），有：
$$
H=-\frac{1}{N}\sum_{i=1}^{N}\left[o_i^* \log(o_i)+(1-o_i^*) \log(1-o_i)\right]
$$

其中$o_i^*$为真实标签值，$o_i$为预测值。

### 误差的反向传播

![[Pasted image 20230430210208.png]]

![[Pasted image 20230430210710.png]]

化简结果：
$$
\dfrac{\partial Loss}{\partial w_{11}^{(2)}}=a_1(o_2^*o_1-o_1^*o_2)
$$

### 权重更新

实际应用中，训练都是分批次（batch），因为不可能一次性载入所有数据。

![[Pasted image 20230430211446.png]]

### 优化器

##### SGD优化器（Stochastic Gradient Descent）：

$$
w_{t+1}=w_t-\alpha g(w_t)
$$

缺点：样本噪声、可能陷入局部最优解

##### SGD+Momentum优化器

$$
v_t=\eta v_{t-1}+\alpha g(w_t)
$$
$$
w_{t+1}=w_t-v_t
$$
原理：动量机制，将上一次的变化量按比例参与计算。

$\alpha$：学习率，$\eta(0.9)$：动量系数。

##### Adagrad

$$
\begin{aligned}
&s_t = s_{t-1}+g^2(w_t) \\
&w_{t+1}=w_t-\frac{\alpha}{\sqrt{s_t+\varepsilon}}g(w_i)
\end{aligned}
$$

$\alpha$：学习率，$g(w_t)$：$t$时刻对参数$w_t$的损失梯度，$\varepsilon(10^{-7})$为防止分母为零的小数。

缺点：学习率下降比较快。

##### RMSProp

$$
\begin{aligned}
&s_t=\eta s_{t-1}+(1-\eta)g^2(w_t) \\
&w_{t+1}=w_t-\frac{\alpha}{s_t+\varepsilon} g(w_t)
\end{aligned}
$$

在Adagrad基础上：
$\eta(0.9)$：控制学习率衰减速度的系数。

特点：自适应学习率。

##### Adam

特点：二阶动量机制。

![[Pasted image 20230430213126.png]]

$\alpha$：学习率
$g(w_t)$：$t$时刻对参数$w_t$的损失梯度
$\beta_1=0.9, \beta_2=0.999$：控制衰减速度的系数
$\varepsilon(10^{-7})$：同上

##### 比较

综合最好：Adam

迭代最快：Adagrad/RMSProp

最准确：SGD+Momentum

