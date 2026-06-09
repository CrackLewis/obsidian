
official: [site](https://www.deep-ml.com/)

## 1-矩阵与向量乘积

[src](https://www.deep-ml.com/problems/1)

给定矩阵与向量，求”矩阵每一行与向量的内积“组成的序列。若存在与向量长度不等的行，返回-1。

```python
def matrix_dot_vector(a: list[list[int|float]], b: list[int|float]) -> list[int|float]:
	# Return a list where each element is the dot product of a row of 'a' with 'b'.
	# If the number of columns in 'a' does not match the length of 'b', return -1.
	if len(a) == 0: return 0
	if len(a[0]) != len(b): return -1
	try:
		cols, prod = len(b), []
		for row in a:
			if len(row) != len(b): raise Exception('wtf')
			prod_l = 0
			for col in range(cols):
				prod_l += row[col] * b[col]
			prod.append(prod_l)
	except Exception as e:
		return -1
	return prod
```

## 2-转置矩阵

[src](https://www.deep-ml.com/problems/2)

```python
def transpose_matrix(a: list[list[int|float]]) -> list[list[int|float]]:
    rs, cs = len(a), len(a[0])
    b = [[a[rx][cx] for rx in range(rs)] for cx in range(cs)]
	return b
```

## 3-矩阵变形

[src](https://www.deep-ml.com/problems/3)

非NumPy做法：

```python
def reshape_matrix(a: list[list[int|float]], new_shape: tuple[int, int]) -> list[list[int|float]]:
    rs_n, cs_n = new_shape
    rs, cs = len(a), len(a[0])
    if rs_n * cs_n != rs * cs: return []

    b = [sum(a, [])]
    return [b[rx*cs_n:(rx+1)*cs_n].copy() for rx in range(rs_n)]
```

NumPy做法：

```python
import numpy as np

def reshape_matrix(a: list[list[int|float]], new_shape: tuple[int, int]) -> list[list[int|float]]:
    try:
        return np.array(a).flatten().reshape(new_shape).tolist()
    except ValueError:
        return []
```

## 4-矩阵按行或按列求平均值

```python
def calculate_matrix_mean(matrix: list[list[float]], mode: str) -> list[float]:
	if mode == 'column':
        matrix = list(map(list, zip(*matrix)))
        
    return [sum(row) / len(row) for row in matrix]
```

NumPy:

```python
def calculate_matrix_mean(matrix: list[list[float]], mode: str) -> list[float]:
	import numpy as np
	matrix = np.array(matrix)
	if mode == 'column':
        matrix = matrix.T
        
    return [sum(row) / len(row) for row in matrix]
```

## 5-矩阵数乘

```python
def scalar_multiply(matrix: list[list[int|float]], scalar: int|float) -> list[list[int|float]]:
	return [[i * scalar for i in row] for row in matrix]
```

NumPy:

```python
import numpy as np
def scalar_multiply(matrix: list[list[int|float]], scalar: int|float) -> list[list[int|float]]:
	return (np.array(matrix) * scalar).tolist()
```

## 6-2x2矩阵特征值

NumPy：

```python
import numpy as np

def calculate_eigenvalues(matrix: list[list[float|int]]) -> list[float]:
	# [[a, b], [c, d]]
	# (a-l)(d-l)-bc=0
	# l^2-(a+d)l+(ad-bc)=0
	a, b = matrix[0]
	c, d = matrix[1]
	A = (a + d) / 2
	B = np.sqrt((a + d) ** 2 - 4 * (a * d - b * c)) / 2
	return [A + B, A - B]
```

PyTorch：

```python
import torch

def calculate_eigenvalues(matrix: torch.Tensor) -> torch.Tensor:
    # Your implementation here
    a = torch.linalg.eig(matrix).eigenvalues.real
    return torch.sort(a, descending=True).values
```

## 7-矩阵变换

题意：给定$2\times 2$矩阵$A,T,S$，判断$T,S$是否可逆并计算$T^{-1}AS$

```python
import numpy as np

def transform_matrix(A: list[list[int|float]], T: list[list[int|float]], S: list[list[int|float]]) -> list[list[int|float]]:
	if np.linalg.det(T) == 0 or np.linalg.det(S) == 0:
		return -1
	Ti = np.linalg.inv(T)
	return ((Ti @ np.array(A)) @ np.array(S)).tolist()
```

torch：

```python
import torch
import torch.linalg as la

def transform_matrix(A, T, S) -> torch.Tensor:
    A_t = torch.as_tensor(A, dtype=torch.float)
    T_t = torch.as_tensor(T, dtype=torch.float)
    S_t = torch.as_tensor(S, dtype=torch.float)
    # Your implementation here
    if la.det(T_t) == 0 or la.det(S_t) == 0: return -1

    return (la.inv(T_t) @ A_t) @ S_t
```

## 8-2x2矩阵的逆

numpy下调用`np.linalg.inv`，torch下是`torch.linalg.inv`

转置矩阵算法：先计算转置矩阵（代数余子式矩阵转置），再除以行列式值

```python
def inverse_2x2(matrix: list[list[float]]) -> list[list[float]] | None:
    a, b = matrix[0]
    c, d = matrix[1]
    if a * d == b * c: return None 

    # adj_matrix = [[d, -c], [-b, a]]
    det_val = a * d - b * c 
    return [[d / det_val, -b / det_val], [-c / det_val, a / det_val]]
```

## 9-矩阵乘法

torch/numpy里可以使用`matmul`或者`@`运算符

```python
def matrixmul(a:list[list[int|float]],
              b:list[list[int|float]])-> list[list[int|float]]:
    m = len(a) 
    n = len(a[0]) 
    p = len(b[0]) 
    if n != len(b): return -1 

    return [[sum(a[r][x] * b[x][c] for x in range(n)) for c in range(p)] for r in range(m)]
```

## 10-