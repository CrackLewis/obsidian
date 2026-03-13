
## 向量和矩阵微分复习

*微分结果布局*：
- 分子布局（Jacobian式）：微分的维度与分子（因变量）对齐，行对应分子，列对应分母。例：$\partial y/\partial x$，$x\in \mathbb{R}^n,y\in\mathbb{R}^m$，则$\partial y/\partial x\in \mathbb{R}^{n\times m}$。
- *分母布局*（Hessian式，*默认布局*）：微分的维度与分母（自变量）完全一致。例：$\partial y/\partial x$，$x\in \mathbb{R}^n,y\in\mathbb{R}^m$，则$\partial y/\partial x\in \mathbb{R}^{m\times n}$。



关于标量的微分：广播机制

关于向量的微分：
- 标量：梯度计算
- 向量：Hessian矩阵
- 矩阵：

## 