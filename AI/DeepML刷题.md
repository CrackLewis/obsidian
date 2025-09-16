
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

## 4