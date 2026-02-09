
## ch01-NLP基础

NLP基础-发展历程

NLP任务：
- 中文分词：jieba
- 子词切分：BPE、WordPiece、Unigram、SentencePiece
- 词性标注：HMM、CRF等机器学习模型
- 文本分类：BERT
- 实体识别：从文中寻找特定元素，如人名、地名等
- 关系抽取：从文本中识别实体之间的语义关系
- 文本摘要
- 机器翻译
- 自动问答

文本表示：
- 词向量
- N-gram模型
- Word2Vec
- ELMo（Embeddings for Language Models）

## ch02-Transformer架构

### 2.1-注意力机制

*注意力机制*：本质是对训练数据的加权
- Query：查询值，训练时为文本自身，推理时为输入文本
- Key：键值，为模型已存储的训练数据
- Value：真值，训练数据对应的真实数据

$$
\text{Attention}(Q_{n\times d},K_{m\times d},V_{m\times d})=\text{softmax}\left(\frac{Q_{n\times d}K_{m\times d}^T}{\sqrt{d}}\right) V_{m\times d}
$$
其中：$n,m,d$分别为查询数、键值对数、隐向量维数

*自注意力*：用于计算一段文本内两个token间的相关关系

*掩码自注意力*：给输出加一个mask，只允许模型使用当前位置之前的信息

*多头注意力*：
- why：一次注意力计算只能拟合一种相关关系，单一注意力难以全面拟合语句序列的完整关系

$$
\begin{split}
\mathrm{MultiHead}(Q, K, V) &= \mathrm{Concat}(\mathrm{head_1}, ...,

\mathrm{head_h})W^O    \\

    \text{where}~\mathrm{head_i} &= \mathrm{Attention}(QW^Q_i, KW^K_i, VW^V_i)
\end{split}
$$

### 2.2-Encoder/Decoder

Seq2Seq模型：编码再解码
- 编码：输入的自然语言序列-->转换为能够表征语义的向量
- 解码：向量-->自然语言序列

![[Pasted image 20260131141242.png]]

前馈神经网络（FFN）：
$$
o=\text{Dropout}\left(W_2\cdot \text{ReLU}(W_1\cdot x)\right)
$$

*LayerNorm*：对序列的每个样本计算其所有通道的均值和方差，并执行归一化操作

*残差连接*：由于transformer层数较深，防止模型退化
$$
\begin{split}
x'&=x+\text{MultiHeadSelfAttention}\left(\text{LayerNorm}(x)\right) \\
o&=x'+\text{FNN}\left(\text{LayerNorm}(x)\right)
\end{split}
$$

*单个Encoder结构*=注意力层+FFN
$$
\begin{split}
x'&=\text{LayerNorm}(x) \\
h&=x'+\text{MultiHeadAttention}(x',x',x') \\
o&=h+\text{FFN}(h)
\end{split}
$$

*单个Decoder结构*=两部分
- 前置LayerNorm
- 第一部分：多头注意力层+LN
- 第二部分：多头注意力层+LN
- 第三部分：MLP

$$
\begin{split}
x_n &= \text{LN}_1(x) \\
x'&= x_n+\text{MaskedMultiHeadAttention}(x_n,x_n,x_n) \\
x_n'&= \text{LN}_2(x') \\
h&= x + \text{MultiHeadAttention}(x_n',o_e,o_e) \\
o_d&= h+\text{MLP}(\text{LN}_3(h)) \\
\end{split}
$$

### 2.2a-Transformer链路

![](https://i-blog.csdnimg.cn/img_convert/8eaa61e136c492a201b0756c6a2c10ea.png)

Encoder单片:

![[Drawing 2026-01-31 16.09.42.excalidraw]]

Decoder单片：

![[Drawing 2026-01-31 18.01.59.excalidraw|100%]]

### 2.3-手搓Transformer

基本步骤：
- 先写注意力机制、LayerNorm、MLP、位置编码
- 再写Encoder/Decoder单片
- 最后组装为一个Transformer

```python
import torch
import math
from torch import nn
from dataclasses import dataclass
from transformers import BertTokenizer
import torch.nn.functional as F

@dataclass
class ModelArgs:
    n_embd: int # 嵌入维度
    n_heads: int # 头数
    dim: int # 模型维度
    dropout: float
    max_seq_len: int
    vocab_size: int
    block_size: int
    n_layer: int

    

class MultiHeadAttention(nn.Module):
    """
    Multi-Head Attention 模块
    公式：
    MultiHead(Q, K, V) = Concat(head_1, ..., head_h)W^O
    where head_i = Attention(QW_i^Q, KW_i^K, VW_i^V)
    """

    def __init__(self, args: ModelArgs, is_causal=False):
        # 构造函数
        # args: 配置对象
        super().__init__()
        # 隐藏层维度必须是头数的整数倍，因为后面我们会将输入拆成头数个矩阵
        assert args.dim % args.n_heads == 0
        # 每个头的维度，等于模型维度除以头的总数。
        self.head_dim = args.dim // args.n_heads
        self.n_heads = args.n_heads

        # Wq, Wk, Wv 参数矩阵，每个参数矩阵为 n_embd x dim
        # 这里通过三个组合矩阵来代替了n个参数矩阵的组合，其逻辑在于矩阵内积再拼接其实等同于拼接矩阵再内积，
        # 不理解的读者可以自行模拟一下，每一个线性层其实相当于n个参数矩阵的拼接
        self.wq = nn.Linear(args.n_embd, self.n_heads * self.head_dim, bias=False)
        self.wk = nn.Linear(args.n_embd, self.n_heads * self.head_dim, bias=False)
        self.wv = nn.Linear(args.n_embd, self.n_heads * self.head_dim, bias=False)
        # 输出权重矩阵，维度为 dim x dim（head_dim = dim / n_heads）
        self.wo = nn.Linear(self.n_heads * self.head_dim, args.dim, bias=False)
        # 注意力的 dropout
        self.attn_dropout = nn.Dropout(args.dropout)
        # 残差连接的 dropout
        self.resid_dropout = nn.Dropout(args.dropout)
        self.is_causal = is_causal

        # 创建一个上三角矩阵，用于遮蔽未来信息
        # 注意，因为是多头注意力，Mask 矩阵比之前我们定义的多一个维度
        if is_causal:
            mask = torch.full((1, 1, args.max_seq_len, args.max_seq_len), float("-inf"))
            mask = torch.triu(mask, diagonal=1)
            # 注册为模型的缓冲区
            self.register_buffer("mask", mask)

    def forward(self, q: torch.Tensor, k: torch.Tensor, v: torch.Tensor):

        # 获取批次大小和序列长度，[batch_size, seq_len, dim]
        bsz, seqlen, _ = q.shape

        # 计算查询（Q）、键（K）、值（V）,输入通过参数矩阵层，维度为 (B, T, n_embed) x (n_embed, dim) -> (B, T, dim)
        xq, xk, xv = self.wq(q), self.wk(k), self.wv(v)

        # 将 Q、K、V 拆分成多头，维度为 (B, T, n_head, dim // n_head)，然后交换维度，变成 (B, n_head, T, dim // n_head)
        # 因为在注意力计算中我们是取了后两个维度参与计算
        # 为什么要先按B*T*n_head*C//n_head展开再互换1、2维度而不是直接按注意力输入展开，是因为view的展开方式是直接把输入全部排开，
        # 然后按要求构造，可以发现只有上述操作能够实现我们将每个头对应部分取出来的目标
        xq = xq.view(bsz, seqlen, self.n_heads, self.head_dim)
        xk = xk.view(bsz, seqlen, self.n_heads, self.head_dim)
        xv = xv.view(bsz, seqlen, self.n_heads, self.head_dim)
        xq = xq.transpose(1, 2)
        xk = xk.transpose(1, 2)
        xv = xv.transpose(1, 2)

        # 注意力计算
        # 计算 QK^T / sqrt(d_k)，维度为 (B, nh, T, hs) x (B, nh, hs, T) -> (B, nh, T, T)
        scores = torch.matmul(xq, xk.transpose(2, 3)) / math.sqrt(self.head_dim)
        # 掩码自注意力必须有注意力掩码
        if self.is_causal:
            assert hasattr(self, 'mask')
            # 这里截取到序列长度，因为有些序列可能比 max_seq_len 短
            scores = scores + self.mask[:, :, :seqlen, :seqlen]
        # 计算 softmax，维度为 (B, nh, T, T)
        scores = F.softmax(scores.float(), dim=-1).type_as(xq)
        # 做 Dropout
        scores = self.attn_dropout(scores)
        # V * Score，维度为(B, nh, T, T) x (B, nh, T, hs) -> (B, nh, T, hs)
        output = torch.matmul(scores, xv)

        # 恢复时间维度并合并头。
        # 将多头的结果拼接起来, 先交换维度为 (B, T, n_head, dim // n_head)，再拼接成 (B, T, n_head * dim // n_head)
        # contiguous 函数用于重新开辟一块新内存存储，因为Pytorch设置先transpose再view会报错，
        # 因为view直接基于底层存储得到，然而transpose并不会改变底层存储，因此需要额外存储
        output = output.transpose(1, 2).contiguous().view(bsz, seqlen, -1)

        # 最终投影回残差流。
        output = self.wo(output)
        output = self.resid_dropout(output)
        return output

class LayerNorm(nn.Module):
    """
    LayerNorm层：对单个样本的所有特征维度进行归一化
    公式：LN(x) = a * (x - mean) / (std + eps) + b
    其中，mean和std是对最后一个维度进行计算的均值和标准差，a和b是可学习的参数
    该实现与PyTorch内置的LayerNorm略有不同，PyTorch的LayerNorm可以指定归一化的维度，而这里固定为最后一个维度
    适用于Transformer中的LayerNorm
    """
    def __init__(self, features, eps=1e-6):
        super().__init__()
        # 线性矩阵做映射
        self.a_2 = nn.Parameter(torch.ones(features))
        self.b_2 = nn.Parameter(torch.zeros(features))
        self.eps = eps
        
    def forward(self, x):
        # 在统计每个样本所有维度的值，求均值和方差
        mean = x.mean(-1, keepdim=True) # mean: [bsz, max_len, 1]
        std = x.std(-1, keepdim=True) # std: [bsz, max_len, 1]
        # 注意这里也在最后一个维度发生了广播
        return self.a_2 * (x - mean) / (std + self.eps) + self.b_2

class MLP(nn.Module):
    """
    前馈神经网络模块
    
    z1 = W1 * x
    a1 = ReLU(z1)
    z2 = W2 * a1
    output = Dropout(z2)
    """
    def __init__(self, dim: int, hidden_dim: int, dropout: float):
        super().__init__()
        # 定义第一层线性变换，从输入维度到隐藏维度
        self.w1 = nn.Linear(dim, hidden_dim, bias=False)
        # 定义第二层线性变换，从隐藏维度到输入维度
        self.w2 = nn.Linear(hidden_dim, dim, bias=False)
        # 定义dropout层，用于防止过拟合
        self.dropout = nn.Dropout(dropout)

    def forward(self, x):
        # 前向传播函数
        # 首先，输入x通过第一层线性变换和RELU激活函数
        # 最后，通过第二层线性变换和dropout层
        return self.dropout(self.w2(F.relu(self.w1(x))))
    

class EncoderLayer(nn.Module):
    def __init__(self, args):
        super().__init__()
        # 一个 Layer 中有两个 LayerNorm，分别在 Attention 之前和 MLP 之前
        self.attention_norm = LayerNorm(args.n_embd)
        # Encoder 不需要掩码，传入 is_causal=False
        self.attention = MultiHeadAttention(args, is_causal=False)
        self.fnn_norm = LayerNorm(args.n_embd)
        self.feed_forward = MLP(args.dim, args.dim, args.dropout)

    def forward(self, x):
        # Layer Norm
        x = self.attention_norm(x)
        # 自注意力
        h = x + self.attention.forward(x, x, x)
        # 经过前馈神经网络
        out = h + self.feed_forward.forward(self.fnn_norm(h))
        return out

class Encoder(nn.Module):
    '''Encoder 块'''
    def __init__(self, args):
        super(Encoder, self).__init__() 
        # 一个 Encoder 由 N 个 Encoder Layer 组成
        self.layers = nn.ModuleList([EncoderLayer(args) for _ in range(args.n_layer)])
        self.norm = LayerNorm(args.n_embd)

    def forward(self, x):
        "分别通过 N 层 Encoder Layer"
        for layer in self.layers:
            x = layer(x)
        return self.norm(x)
    
class DecoderLayer(nn.Module):
    '''Decoder 层'''
    def __init__(self, args):
        super().__init__()
        # 一个 Layer 中有三个 LayerNorm，分别在 Mask Attention 之前、Self Attention 之前和 MLP 之前
        self.attention_norm_1 = LayerNorm(args.n_embd)
        # Decoder 的第一个部分是 Mask Attention，传入 is_causal=True
        self.mask_attention = MultiHeadAttention(args, is_causal=True)
        self.attention_norm_2 = LayerNorm(args.n_embd)
        # Decoder 的第二个部分是 类似于 Encoder 的 Attention，传入 is_causal=False
        self.attention = MultiHeadAttention(args, is_causal=False)
        self.ffn_norm = LayerNorm(args.n_embd)
        # 第三个部分是 MLP
        self.feed_forward = MLP(args.dim, args.dim, args.dropout)

    def forward(self, x, enc_out):
        # Layer Norm
        x = self.attention_norm_1(x)
        # 掩码自注意力
        x = x + self.mask_attention.forward(x, x, x)
        # 多头注意力
        x = self.attention_norm_2(x)
        h = x + self.attention.forward(x, enc_out, enc_out)
        # 经过前馈神经网络
        out = h + self.feed_forward.forward(self.ffn_norm(h))
        return out

class Decoder(nn.Module):
    '''解码器'''
    def __init__(self, args):
        super(Decoder, self).__init__() 
        # 一个 Decoder 由 N 个 Decoder Layer 组成
        self.layers = nn.ModuleList([DecoderLayer(args) for _ in range(args.n_layer)])
        self.norm = LayerNorm(args.n_embd)

    def forward(self, x, enc_out):
        "Pass the input (and mask) through each layer in turn."
        for layer in self.layers:
            x = layer(x, enc_out)
        return self.norm(x)

class PositionalEncoding(nn.Module):
    """
    位置编码模块
    公式：
    PE(pos, 2i) = sin(pos / 10000^(2i/d_model))
    PE(pos, 2i+1) = cos(pos / 10000^(2i/d_model))
    其中 pos 是位置，i 是维度索引，d_model 是嵌入维度
    
    这里仍然使用Sinusoidal编码，如果需要相对位置，可改用LoRA等
    """

    def __init__(self, args):
        super(PositionalEncoding, self).__init__()
        # Dropout 层
        # self.dropout = nn.Dropout(p=args.dropout)

        # block size 是序列的最大长度
        pe = torch.zeros(args.block_size, args.n_embd)
        position = torch.arange(0, args.block_size).unsqueeze(1)
        # 计算 theta
        div_term = torch.exp(
            torch.arange(0, args.n_embd, 2) * -(math.log(10000.0) / args.n_embd)
        )
        # 分别计算 sin、cos 结果
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        pe = pe.unsqueeze(0)
        self.register_buffer("pe", pe)

    def forward(self, x):
        # 将位置编码加到 Embedding 结果上
        x = x + self.pe[:, : x.size(1)].requires_grad_(False)
        return x


class Transformer(nn.Module):
    '''整体模型'''

    def __init__(self, args):
        super().__init__()
        # 必须输入词表大小和 block size
        assert args.vocab_size is not None
        assert args.block_size is not None
        self.args = args
        self.transformer = nn.ModuleDict(dict(
            wte=nn.Embedding(args.vocab_size, args.n_embd),
            wpe=PositionalEncoding(args),
            drop=nn.Dropout(args.dropout),
            encoder=Encoder(args),
            decoder=Decoder(args),
        ))
        # 最后的线性层，输入是 n_embd，输出是词表大小
        self.lm_head = nn.Linear(args.n_embd, args.vocab_size, bias=False)

        # 初始化所有的权重
        self.apply(self._init_weights)

        # 查看所有参数的数量
        print("number of parameters: %.2fM" % (self.get_num_params() / 1e6,))

    '''统计所有参数的数量'''

    def get_num_params(self, non_embedding=False):
        # non_embedding: 是否统计 embedding 的参数
        n_params = sum(p.numel() for p in self.parameters())
        # 如果不统计 embedding 的参数，就减去
        if non_embedding:
            n_params -= self.transformer.wte.weight.numel()
        return n_params

    '''初始化权重'''

    def _init_weights(self, module):
        # 线性层和 Embedding 层初始化为正则分布
        if isinstance(module, nn.Linear):
            torch.nn.init.normal_(module.weight, mean=0.0, std=0.02)
            if module.bias is not None:
                torch.nn.init.zeros_(module.bias)
        elif isinstance(module, nn.Embedding):
            torch.nn.init.normal_(module.weight, mean=0.0, std=0.02)

    '''前向计算函数'''

    def forward(self, idx, targets=None):
        # 输入为 idx，维度为 (batch size, sequence length, 1)；targets 为目标序列，用于计算 loss
        device = idx.device
        b, t = idx.size()
        assert t <= self.args.block_size, f"不能计算该序列，该序列长度为 {t}, 最大序列长度只有 {self.args.block_size}"

        # 通过 self.transformer
        # 首先将输入 idx 通过 Embedding 层，得到维度为 (batch size, sequence length, n_embd)
        print("idx", idx.size())
        # 通过 Embedding 层
        tok_emb = self.transformer.wte(idx)
        print("tok_emb", tok_emb.size())
        # 然后通过位置编码
        pos_emb = self.transformer.wpe(tok_emb)
        # 再进行 Dropout
        x = self.transformer.drop(pos_emb)
        # 然后通过 Encoder
        print("x after wpe:", x.size())
        enc_out = self.transformer.encoder(x)
        print("enc_out:", enc_out.size())
        # 再通过 Decoder
        x = self.transformer.decoder(x, enc_out)
        print("x after decoder:", x.size())

        if targets is not None:
            # 训练阶段，如果我们给了 targets，就计算 loss
            # 先通过最后的 Linear 层，得到维度为 (batch size, sequence length, vocab size)
            logits = self.lm_head(x)
            # 再跟 targets 计算交叉熵
            loss = F.cross_entropy(logits.view(-1, logits.size(-1)), targets.view(-1), ignore_index=-1)
        else:
            # 推理阶段，我们只需要 logits，loss 为 None
            # 取 -1 是只取序列中的最后一个作为输出
            logits = self.lm_head(x[:, [-1], :])  # note: using list [-1] to preserve the time dim
            loss = None

        return logits, loss


def main():
    args = ModelArgs(100, 10, 100, 0.1, 512, 1000, 1000, 2)
    text = "我喜欢快乐地学习大模型"
    tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')
    inputs_token = tokenizer(
        text,
        return_tensors='pt', # PyTorch tensor
        max_length=args.max_seq_len, # 512
        truncation=True,
        padding='max_length'
    )
    args.vocab_size = tokenizer.vocab_size
    transformer = Transformer(args)
    inputs_id = inputs_token['input_ids']
    logits, loss = transformer.forward(inputs_id)
    print(logits)
    predicted_ids = torch.argmax(logits, dim=-1).item()
    output = tokenizer.decode(predicted_ids)
    print(output)

if __name__ == "__main__":
    print("开始")
    main()
```

## ch03-预训练语言模型

PLM=pretrained language model

- Encoder-only PLMs
	- BERT
	- RoBERTa
	- ALBERT
- Encoder-Decoder PLMs
	- T5
- Decoder-only PLMs
	- GPT
	- LLaMa
	- GLM

### 3.1-BERT

核心思想：
- Transformer架构：堆叠Encoder
- 预训练+微调

*BERT架构*：
- 将decoder部分替换成了一个分类头（prediction_heads），将多维度的隐藏状态转换为分类维度
- tokenizer -> embedding -> encoder(s) -> predictioin_heads

![图片描述](https://raw.githubusercontent.com/datawhalechina/happy-llm/main/docs/images/3-figures/1-0.png)

BERT内使用GELU作为激活函数，核心思想是通过输入自身的概率分布，来决定抛弃还是保留自身的神经元：
$$GELU(x) = 0.5x(1 + tanh(\sqrt{\frac{2}{\pi}})(x + 0.044715x^3))$$

预训练-微调范式：分离预训练和微调，预训练学习语法语义等知识，微调学习领域知识

*BERT预训练*：MLM+NSP
- *掩码语言模型*（MLM, masked language model）：一种预训练任务类型，让模型做“完形填空”
	- 策略：语料中随机选取15%的token，这些token中：80%替换为MASK，10%随机替换，10%不变
- *下句预测*（NSP, next sentence prediction）：另一种任务，针对句级NLU任务。从语料库中抽两句话，判断它们是否为上下句

BERT微调：训练时参数更新的策略一致，但
- 特定的任务、更少的训练数据、更小的 batch_size 上进行训练
- 更新参数的幅度更小

### 3.2-RoBERTa

相对BERT的优化：
- 去掉NSP任务，将MLM的掩码策略修改为*动态遮蔽策略*
- 更大规模的预训练数据、训练步长（batch size）
- 更大的BPE词表：BERT为30k，RoBERTa为50k

### 3.3-ALBERT

相对BERT的优化：
- 