
refs:
- 面试鸭

## 索引

- 基本问题
	- [[#架构和基本原理]]
- 对比
	- [[#解决了RNN什么问题]]

## 架构和基本原理

- encoder-decoder
- Multi-Head self-Attention
- positional encoding
- FFNs
- LayerNorm
- Masking

## 解决了RNN什么问题

- 并行计算效率：RNN必须依赖时序，Transformer基于自注意力，可并行计算序列内所有元素
- 长距离依赖：RNN难以捕捉到长距离关系，但Transformer可以通过自注意力处理长距离关系
- 模型训练速度：Transformer可以有效并行化
- 前向和反向传播：Transformer可以不考虑时序关系，高效简洁实现反向传播

## 哪个部分最占用显存

模型参数：FFN；推理计算：注意力模块

设注意力头数为`H`，embedding维数为`E`，特征维数为`D`，最大序列长度为`N`，则：
- 偏置矩阵`Wq,Wk,Wv`：各`E * H * D`
- 输出偏置`Wo`：`H * D * H * D`
- （可选）mask：`N * N`

注意力模块总共参数约为：
$$
N^2+H^2D^2 + 3EHD
$$

FFN的参数为两个全连接层，总参数：$2H^2D^2$ 