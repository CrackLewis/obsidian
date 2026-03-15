
## 向量和矩阵微分复习

*微分结果布局*：
- 分子布局（Jacobian式）：微分的维度与分子（因变量）对齐，行对应分子，列对应分母。例：$\partial y/\partial x$，$x\in \mathbb{R}^n,y\in\mathbb{R}^m$，则$\partial y/\partial x\in \mathbb{R}^{n\times m}$。
- *分母布局*（Hessian式，*默认布局*）：微分的维度与分母（自变量）完全一致。例：$\partial y/\partial x$，$x\in \mathbb{R}^n,y\in\mathbb{R}^m$，则$\partial y/\partial x\in \mathbb{R}^{m\times n}$。

*求向量/矩阵微分的一般步骤*：先求全微分，再计算梯度
- 先计算全微分：假设要计算$\partial f/\partial X$，则先计算$df$
- 利用迹的性质将$df$整理为：$df=\text{tr}(A^TdX)$
- 直接写出：$\partial f/\partial X=A$

迹技巧：
- 标量的迹等于自身，矩阵的迹等于主对角线元素之和
- $df=\text{tr}((\partial f/\partial X)^TdX)$
- 性质：
	- 转置不变性、加性、数乘性质
	- *置换不变性*：$\text{tr}(AB)=\text{tr}(BA)$

向量/矩阵微分的基本恒等式：假设需要计算$\partial f/\partial x$或者$\partial f/\partial X$。
- *线性项*：
	- $f(x)=a^T x \Rightarrow df=a^Tdx=\text{tr}(a^Tdx)\Rightarrow \partial f/\partial x=a$
	- $f(x)=\text{tr}(A^T X)\Rightarrow \partial f/\partial X=A$
- *二次型*（重要）：$f(x)=x^T Ax$
	- 微分：$df = (dx)^T A x + x^T A (dx) = x^T A^T dx + x^T A dx = x^T (A^T + A) dx$
	- 迹表示：$df = \text{tr}(x^T (A^T + A) dx) = \text{tr}(((A^T + A)x)^T dx)$
	- 结果：$\partial f/\partial x=\nabla_x (x^T A x) = (A + A^T)x$
		- 特例：当$A=A^T$（对称）时，$\partial f/\partial x=2Ax$
- 行列式与逆：
	- $f(x)=\ln |X|\Rightarrow \partial f/\partial X=(X^{-1})^T$
	- $f(x)=|X|\Rightarrow \partial f/\partial X=|X|(X^{-1})^T$
- 链式法则：矩阵链式法则不像标量那样简单直接写成乘积，通常需要通过微分形式传递，然后通过迹的变换将微元移动到最右侧提取梯度
	- 例：$df=\text{tr}(A^TdY),dY=\mathcal{L}(dX)\Rightarrow df=\text{tr}(A^T \mathcal{L}(dX))$

## GD

Gradient Descent = 梯度下降

参数依据所有样本损失函数的平均值更新，直至收敛（梯度归零）

$$
\theta'\leftarrow \theta-\eta\cdot \underset{1\le i\le n}{\text{mean}}\left(\frac{\partial L(y_i,\hat{y}_i)}{\partial \theta}\right)
$$

## SGD

Stochastic Gradient Descent = 随机梯度下降

对于参数$\theta$、目标函数$L$和*超参数学习率*$\eta$，更新规则为：
$$
\theta'\leftarrow \theta-\eta\cdot\frac{\partial L(y_i,\hat{y}_i)}{\partial \theta}
$$

其中：$\partial L(y_i,\hat{y}_i)$是随机某个样本的损失

所有可学习的参数根据SGD更新参数，梯度由链式法则确定

## 动量法

