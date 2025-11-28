
![[Pasted image 20230502162412.png]]

since: 2012
inventor: Hinton & Alex Krizhevsky

## highlights

- GPU utilized for the first time
- ReLU applied instead of sigmoid or tanh
- LRN局部响应归一化
- 前两层应用Dropout随机失活神经元，减少过拟合

## 过拟合现象

原因：
- 特征过多，模型过复杂，参数过多
- 训练过少
- 噪声过多

### 解决方案之一：dropout

![[Pasted image 20230502165945.png]]

## 模型详解

![[Pasted image 20230502170614.png]]

![[Pasted image 20230502170817.png]]

