
![[Pasted image 20260610191317.png]]

$$
\text{SiLU}(x)=\frac{x}{1+e^{-x}}
$$

梯度：
$$
\frac{\partial z}{\partial x}=z\cdot \left[1+x(1-z)\right]
$$

作用：
- 有梯度，非单调，总体平滑，可解决ReLU的神经元死亡问题
- 计算量低于GELU，常作为其替代

Google的成果称Swish为$\text{Swish}(x)=x\cdot \sigma(\beta x)$，当$\beta=1$时，Swish等价于SiLU。但更多时候这两者是混为一谈的