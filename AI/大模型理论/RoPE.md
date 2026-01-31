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

我们希望$p$能够存储相对位置信息，从而使得query/key的内积可以捕捉这一层关系：
$$
f_q(x_m,m)\cdot f_k(x_n,n)=g(x_m,x_n,m-n)
$$

一种设计是利用复数运算机制实现：
$$
f_q(x_m,m)=W_q x_m e^{im\theta},\quad f_k(x_n,n)=W_k x_n e^{in\theta}
$$
从而有：
$$
g(x_m,x_n,m-n)=\mathbb{Re}\left[x_m^T (W_q^TW_k) x_n\cdot e^{i(m-n)\theta}\right]
$$
$f_q,f_k,g$转化为矩阵表示即为：
![[Pasted image 20260131011659.png]]

注意到它们本质是左乘了一个旋转矩阵，因此称作*旋转位置编码*

## RoPE实现


```python
import torch
import torch.nn as nn

class RoPE(nn.Module):
    """
    RoPE 是旋转位置编码，它通过将输入的稠密向量旋转来稳定训练。
    公式是：
    out = x * cos(theta * position) - x * sin(theta * position)
    Args:
        theta (float): 底数超参数
        d_k (int): 输入的维度，也就是d_model
        max_seq_len (int): 最大序列长度
        device (torch.device): 设备
    input:
        x: (batch_size, seq_len, d_model) 输入的稠密向量
        token_positions: (batch_size, seq_len) 每个token的位置信息
    output:
        out: (batch_size, seq_len, d_model) 输出的稠密向量
    """
    def __init__(self, theta: float, d_k: int, max_seq_len: int, device=None):
        super().__init__()
        if d_k % 2 != 0:
            raise ValueError("d_k must be even")
        # 这个是RoPE的底数超参数，不是直接的角度
        self.theta = theta 
        # d_k就是d_model,即嵌入之后的稠密向量，它必须为偶数
        self.d_k = d_k
        self.max_seq_len = max_seq_len
        self.device = device
        # 计算频率
        freqs = 1.0 / (self.theta ** (torch.arange(0, self.d_k, 2).float() / self.d_k))
        # 记录每个token的位置信息
        positions = torch.arange(self.max_seq_len)
        
        # 计算正弦和余弦：outer是外积，即每个位置都与每个频率相乘，shape: [max_seq_len, d_k//2]
        sinusoids = torch.outer(positions, freqs)
        self.register_buffer("cos_cache", sinusoids.cos(), persistent=False) #利用register_buffer表示这是固定的，不需要学习
        self.register_buffer("sin_cache", sinusoids.sin(), persistent=False)

    def forward(self, x: torch.Tensor, token_positions: torch.Tensor) -> torch.Tensor:
        # 这里的x是输入的稠密向量，token_positions是token的位置信息
        cos = self.cos_cache[token_positions]
        sin = self.sin_cache[token_positions]

        cos = cos.unsqueeze(0) # shape: [1, max_seq_len, d_k//2] 对应 [batch, max_seq_len, d_k//2]
        sin = sin.unsqueeze(0) # shape: [1, max_seq_len, d_k//2] 对应 [batch, max_seq_len, d_k//2]

        #  这里还是分奇偶数写容易理解
        x_part1 = x[..., 0::2]
        x_part2 = x[..., 1::2]
		# 偶数位置乘以cos，奇数位置乘以sin
        output1 = x_part1 * cos - x_part2 * sin 
        # 偶数位置乘以sin，奇数位置乘以cos
        output2 = x_part1 * sin + x_part2 * cos 

        # out = torch.cat([output1, output2], dim=-1) # shape: [batch,  max_seq_len, d_k]
        out = torch.stack([output1, output2], dim=-1)  # [batch, seq_len, d_k//2, 2] #用stack能巧妙的把奇数和偶数交叉在一起，cat就不行
        out = out.flatten(-2)  # [batch, seq_len, d_k]
        return out
```