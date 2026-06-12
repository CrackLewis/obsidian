
GELU = Gaussian Error Linear Unit, 高斯误差线性单元

$$
\text{GELU}(x)=x\cdot \Phi(x)
$$
其中：
$$
\Phi(x)=\int_{-\infty}^{x} \frac{1}{\sqrt{2\pi}} e^{-t^2/2}dt=\frac{1}{2}\left(1+\text{erf}\left(\frac{x}{\sqrt{2}}\right)\right)
$$

代入后的*定义表达式*：
$$
\text{GELU}(x)=\frac{x}{2}\left[1+\text{erf}\left(\frac{x}{\sqrt{2}}\right)\right]
$$

*常用近似计算式*：
$$
\text{GELU}_2(x)\approx 0.5x\cdot \left[1+\tanh\left(\sqrt{\frac{2}{\pi}} (x+0.044715x^3)\right)\right]
$$
一个更快的近似是$\beta=1.702$的Swish函数：
$$
\text{GELU}_3(x)\approx x\cdot \sigma(1.702x)
$$

以上三者的误差在0.01以内，可以忽略

## 梯度

WIP

## PyTorch实现

PyTorch官方提供`torch.nn.functional.gelu`作为实现

工程实现用第二个用的多一些

```python
import torch.nn as nn

class GELUTanh(nn.Module):
    def __init__(self):
        super().__init__()

    def forward(self, x):
        c = math.sqrt(2 / math.pi)
        return 0.5 * x * (1 + torch.tanh(c * (x + 0.044715 * x ** 3)))
```