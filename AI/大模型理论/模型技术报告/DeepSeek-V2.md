
2405.04434

refs:
- [arxiv](https://arxiv.org/pdf/2405.04434)
- [zhihu1](https://zhuanlan.zhihu.com/p/696292840)

基本信息：
- 总参数236B，每个token激活2.1B
- 上下文128K
- 节省42.5%训练成本，减少93.3%的KV cache，将最大生成量从10K提升至50K+
- 

技术要点：
- Multi-head Latent Attention
- 低秩KV联合压缩
- 解耦RoPE位置编码
- DeepSeekMoE

## 模型架构

### 架构细节

```
DeepseekForCausalLM(
  (model): DeepseekModel(
    (embed_tokens): Embedding(102400, 5120)
    (layers): ModuleList(
      (0): DeepseekDecoderLayer(
        (self_attn): DeepseekAttention(
          (q_a_proj): Linear(in_features=5120, out_features=1536, bias=False)
          (q_a_layernorm): DeepseekRMSNorm()
          (q_b_proj): Linear(in_features=1536, out_features=24576, bias=False)
          (kv_a_proj_with_mqa): Linear(in_features=5120, out_features=576, bias=False)
          (kv_a_layernorm): DeepseekRMSNorm()
          (kv_b_proj): Linear(in_features=512, out_features=32768, bias=False)
          (o_proj): Linear(in_features=16384, out_features=5120, bias=False)
          (rotary_emb): DeepseekYarnRotaryEmbedding()
        )
        (mlp): DeepseekMLP(
          (gate_proj): Linear(in_features=5120, out_features=12288, bias=False)
          (up_proj): Linear(in_features=5120, out_features=12288, bias=False)
          (down_proj): Linear(in_features=12288, out_features=5120, bias=False)
          (act_fn): SiLU()
        )
        (input_layernorm): DeepseekRMSNorm()
        (post_attention_layernorm): DeepseekRMSNorm()
      )
      (1-59): 59 x DeepseekDecoderLayer(
        (self_attn): DeepseekAttention(
          (q_a_proj): Linear(in_features=5120, out_features=1536, bias=False)
          (q_a_layernorm): DeepseekRMSNorm()
          (q_b_proj): Linear(in_features=1536, out_features=24576, bias=False)
          (kv_a_proj_with_mqa): Linear(in_features=5120, out_features=576, bias=False)
          (kv_a_layernorm): DeepseekRMSNorm()
          (kv_b_proj): Linear(in_features=512, out_features=32768, bias=False)
          (o_proj): Linear(in_features=16384, out_features=5120, bias=False)
          (rotary_emb): DeepseekYarnRotaryEmbedding()
        )
        (mlp): DeepseekMoE(
          (experts): ModuleList(
            (0-159): 160 x DeepseekMLP(
              (gate_proj): Linear(in_features=5120, out_features=1536, bias=False)
              (up_proj): Linear(in_features=5120, out_features=1536, bias=False)
              (down_proj): Linear(in_features=1536, out_features=5120, bias=False)
              (act_fn): SiLU()
            )
          )
          (gate): MoEGate()
          (shared_experts): DeepseekMLP(
            (gate_proj): Linear(in_features=5120, out_features=3072, bias=False)
            (up_proj): Linear(in_features=5120, out_features=3072, bias=False)
            (down_proj): Linear(in_features=3072, out_features=5120, bias=False)
            (act_fn): SiLU()
          )
        )
        (input_layernorm): DeepseekRMSNorm()
        (post_attention_layernorm): DeepseekRMSNorm()
      )
    )
    (norm): DeepseekRMSNorm()
  )
  (lm_head): Linear(in_features=5120, out_features=102400, bias=False)
)
```

### 架构图

![[Pasted image 20260717110629.png]]

## 读论文

- ch01-intro
- ch02-arch
- ch03-pretrain
- ch04-alignment
- ch05-conclusion, limitation, future work

### ch01-intro

methods:
- MLA
	- other approaches to KV-cache problems: GQA, MQA
- DeepSeekMoE
	- conventional MoE methods: GShard
- supplementary mechanisms

corpus: 8.1t tokens
- extended Chinese corpus, higher quality

training:
- pretrain: with full corpus
- SFT: 1.5m conversational sessions of various domains
- GRPO

### ch02-arch

Transformer = Attention + FFN

Attention -> MLA

FFN -> DeepSeekMoE

#### 2.1-MLA

MLA = Multi-Latent Attention

why: 
- vanilla MHA has heavy KV-cache and becomes the bottleneck of inference efficiency
- MQA/GQA reduces KV-cache but are less efficient

*low-rank KV joint compression*:

| Multi-Head Attention                                                    | low-rank JV joint compression                                                                           |
| ----------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| $$\begin{split}q_t&=W^Q h_t\\ k_t&=W^K h_t\\ v_t&= W^V h_t\end{split}$$ | $$\begin{split}c_t^{KV}&= W^{DKV} h_t\\ k_t^C&= W^{UK} c_t^{KV}\\ v_t^C &= W^{UV} c_t^{KV}\end{split}$$ |
|                                                                         |                                                                                                         |

where:
- $n_h$: attention heads; 
- $d$: dimension of hidden vectors; 
- $d_h$: dimension of each attention head;
- $d_c$: dimension of compressed *latent vectors*, s.t. $d_c\ll n_h\cdot d_h$
- $W^Q,W^K,W^V\in \mathbb{R}^{d_h n_h\times d}$: MHA input matrices, `d -> n_h * d_h`
- $W^{DKV}\in \mathbb{R}^{d_c\times d}$: conversion matrix from input hidden to latent vectors
- $W^{UK},W^{UV}\in \mathbb{R}^{d_h n_h\times d_c}$: conversion from latent vectors to KVs

*low-rank query compressions*:
$$
\begin{split}
c_t^Q &= W^{DQ} h_t \\
q_t^C &= W^{UQ} c_t^Q
\end{split}
$$
where $c_t^Q\in \mathbb{R}^{d_c'}$ and $d_c'\ll d_h n_h$.

*decoupled RoPE*:
- why: [[RoPE]] is incompatible with low-rank KV compression
	- applying naive RoPE for $k_t^C$ will fuse position information into latent vectors and undermine the semantic integrity
	- GEMM optimizations and caches are disabled
- how: split RoPE vectors from latent vectors; calculate MLA and RoPE respectively, and concatenate them later

![[Pasted image 20260720175328.png]]

where:
- $d_h^R$: num' of dimensions of RoPE queries/keys
- $q_t^R,k_t^R\in \mathbb{R}^{d_h^R n_h}$: RoPE queries/keys, decoupled from latent vectors
- $W^{QR}\in \mathbb{R}^{d_h^R n_h\times d_c'}$: conversion matrix from latent query vectors to RoPE queries of various headers
- $W^{KR}\in \mathbb{R}^{d_h^R \times d}$: conversion matrix from hidden states to RoPE key
- RoPE queries of various heads $q_{t,i}^R$ are matched to one RoPE key of that specific position $k_t^R$

*comparision of KV cache*:
- MLA requires a KV cache of ~$4.5d_h l$ per token, equiv' to GQA where $n_g=2.25$
- MLA is stronger in inference efficiency than all other variants

![[Pasted image 20260717181840.png]]

#### 2.2-DeepSeekMoE

two key ideas:
- 