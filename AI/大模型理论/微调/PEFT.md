---
tags:
  - 微调
  - fine-tuning
  - PEFT
---

ref(s):
- [Huggingface PEFT](https://hugging-face.cn/docs/peft/index)

PEFT = parameter-efficient fine-tuning

PEFT不是一个特定的微调方法，而是一类微调方法的统称。此类方法倾向于对模型的较少参数（而非全量参数）进行微调，使模型更适用于特定任务

PEFT方法：
- Prompt-tuning
- Prefix-tuning
- P-tuning
- [[LoRA|LoRA/QLoRA]]
- IA3

## Prompt-tuning

只在输入层添加可训练的连续提示向量（软提示向量）$e$：
$$
x'\leftarrow x+e
$$

✔：实现简单，参数量最少，不修改原模型参数
❌：小模型上效果有限

## Prefix-tuning

在输入前拼接一个前缀向量$p\in \mathbb{R}^r$，模型内对应的$d$维调整为$d+r$维

$$
x'\leftarrow \text{Concat}(p,x)
$$

训练过程中，预训练部分冻结，只训练因前缀向量增加的参数部分

## P-tuning

核心思想：
- P-tuning v1：使用可训练的连续提示，通过LSTM/MLP编码器生成提示向量
- P-tuning v2：在每一层都添加可训练提示，类似Prefix-tuning但更通用

实现方式：
- v1: 提示向量通过一个编码器网络生成，增加连续性约束
- v2: 深层提示+增强编码器，解决小模型性能问题

特点：
- 比Prompt-tuning更灵活
- P-tuning v2在理解和生成任务上都有好表现
- 对小模型更友好

适用场景： 自然语言理解（NLU）和生成任务（NLG）

## IA3

Infused Adapter by Inhibiting and Amplifying Inner Activations

基于抑制和放大内部激活值的注入适应

*核心思想*：
- 通过可学习的缩放向量来抑制或放大模型内部的激活值
- 不添加新矩阵，只是对现有激活进行缩放

$\odot(\cdot,\cdot)$为缩放函数，$h,l$分别为激活值和缩放向量
$$
h'=(l\odot h)
$$

✔：实现简单，参数量极少，不影响推理速度
❌：表达能力有限

## 微调方法对比

LoRA赢麻了，哈哈哈

| 维度      | Prefix-tuning | Prompt-tuning | P-tuning v2 | LoRA     | IA3          |
| ------- | ------------- | ------------- | ----------- | -------- | ------------ |
| 参数位置    | 每层K/V前缀       | 仅输入层          | 每层提示        | 权重旁路矩阵   | 激活缩放向量       |
| 可训练参数占比 | ~0.1-1%       | *~0.01-0.1%*  | ~0.1-1%     | ~0.1-1%  | *~0.01-0.1%* |
| 推理开销    | 轻微增加          | *无*           | 轻微增加        | *可合并无开销* | 无            |
| 小模型效果   | 中等            | 较差            | 较好          | *好*      | 中等           |
| 大模型效果   | 好             | 好             | 好           | 好        | 好            |
| 实现复杂度   | 中             | 低             | 中           | 低        | 低            |
| 适用任务    | 生成            | 分类/生成         | 理解/生成       | *通用*     | *通用*         |
| 生态支持    | 一般            | 一般            | 一般          | *非常好*    | 较好           |
