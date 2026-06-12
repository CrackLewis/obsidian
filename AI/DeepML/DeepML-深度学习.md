
## 22-Sigmoid

```python
import math

def sigmoid(z: float) -> float:
	#Your code here
	return 1.0 / (1 + math.exp(-z))
```

## 23-Softmax

$$
\text{Softmax}(X)=\frac{e^X}{\sum_{x\in X} e^x}
$$

*注意*：如果直接用原始值计算，会溢出

更稳妥的方法是对每一项减最大值，过小负数做指数运算会直接取0，不会溢出

```python
import math

def softmax(scores: list[float]) -> list[float]:
    if not scores:
        return []
    max_score = max(scores)
    exp_scores = [math.exp(x - max_score) for x in scores]
    sum_exp = sum(exp_scores)
    return [e / sum_exp for e in exp_scores]
```

PyTorch：`torch.nn.Softmax`或`torch.nn.functional.softmax`

## 24-单神经元模拟

