
```python
import numpy as np
```

## 类型

`numpy.ndarray`

## 数组定义

- `np.array(list)`
- `np.zeros(shape)`
- `np.ones(shape)`
- `np.random.random(shape)`

## 基本运算

- `np.add`：数组叠加/数组加数
	- `np.add(arr1, arr2)`
	- `np.add(arr, num)`
- `np.transpose(arr)`：转置
- `np.all`：所有元素非零
- `np.any`：任意元素非零
- `np.max`
- `np.min`

## 变形

- `np.stack(elements,axis)`：按照一个方向堆积元素
	- 对二维空间：`axis=0`为逐行堆积（每行一个元素），`axis=1`为逐列
	- `np.vstack(elements)`：等价于`np.stack(elements,axis=0)`
- `np.reshape(elements,shape)`
- 