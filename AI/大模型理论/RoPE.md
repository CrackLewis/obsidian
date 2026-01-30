---
tags:
  - encoding
  - 位置编码
---


RoPE = Rotary Position Encoding = 旋转位置编码

RoPE用于将*相对位置信息*集成到*自注意力机制*中

假设输入序列$W$有$N$个token，每个token记作$w_i$（$i=1,2,\cdots,N$），对应一个$d$维嵌入$x_i$：
$$
x_i\in \mathbb{R}^{d}
$$
在做自注意力前，会用词嵌入向量$x_i$计算$q,k,v$，在其中加入位置信息：
$$
q_m,k_n,v_n\leftarrow f_q(x_m,m),f_k(x_n,n),f_v(x_n,n)
$$
其中$q_m$表示$x_m$集成了位置信息$m$形成的query向量；$k_n,v_n$表示$x_n$集成了位置$n$形成的key/value向量

而计算$x_m$对应的自注意力输出结果$o_m$，则需要将其与其他词嵌入依次加权求和：
$$
\begin{split}
a_{m,n}&= \frac{\exp\left(q_m^T\cdot k_n/\sqrt{d}\right)}{\displaystyle\sum_{n=1}^N \exp\left(q_m^T\cdot k_n/\sqrt{d}\right)}\\
o_m&=\sum_{n=1}^N a_{m,n}\cdot v_n
\end{split}
$$

## 绝对位置编码

以$f_q$为例：
$$
f_{q}(x_m,m)=W_{q}^{m\times m}\cdot (x_m+p_m)
$$
其中$p_m$即为$m$对应的位置偏移向量：
$$
p_{m,i}=\left\{\begin{matrix}
\sin(k/10000^{i/d}), & i\bmod 2=0,\\
\cos(k/10000^{(i-1)/d}), & i\bmod 2=1.
\end{matrix}\right.
$$

## 二维旋转位置编码

我们希望$p$能够存储相对位置信息，即

## RoPE实现