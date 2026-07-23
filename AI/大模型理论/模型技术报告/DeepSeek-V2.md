
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
- Multi-head Latent Attention:
	- 既降低总参数量，又提升推理效率
	- 低秩KV联合压缩：对输入分别压缩为等长latent向量再复原为q和kv
	- 解耦RoPE位置编码：位置信息latent与内容信息分离
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
- segmenting experts into finer granularity for higher expert specialization and more accurate knowledge acquisition
- isolating some *shared experts* for mitigating knowledge redundancy among *routed experts*

![[Pasted image 20260721182303.png]]
![[Pasted image 20260721182720.png]]

where:
- $N_s,N_r\ge 1$: num's of shared and routed experts
- $\text{FFN}_i^{(s)}$, $\text{FFN}_j^{(r)}$: shared and routed expert FFNs, where $1\le i\le N_s,1\le j\le N_r$
- $g_{i,t}\in \{0,1\}$: for $i$-th routed expert, whether to activate it or not
	- $s_{i,t}$: the token-to-expert affinity score
	- $e_i \in \mathbb{R}^{d}$: the centroid of the $i$-th routed expert in this layer
- $u_t,h_t'\in \mathbb{R}^{d}$: input and output hidden

*device-limited routing*:
- why: when expert parallelism is applied, routed experts are distributed to multi devices; MoE-related communication cost can be large if the expert count is large
- DS-v2 ensures that target experts of each token will be distributed on at most $M$ devices: select $M$ devices with highest affinity experts, and perform top-$K$ expert selecton on experts from those devices

*auxiliary loss for load balance*: ^2fdae3
- why: unbalanced load will: 1. raise the risk of routing collapse, preventing some experts from being fully trained and utilized; 2. diminish the computation efficiency when expert parallelism is employed
- three types of aux' losses:
	- *expert-level balance loss*: mitigate the routing collapse risk ![[Pasted image 20260721194135.png]]
	- *device-level balance loss*: suppose all experts are on $D$ groups and each group exclusively takes one device. $D=\{\mathcal E_1,\mathcal E_2,\ldots,\mathcal E_D\}$. ![[Pasted image 20260721194450.png]]
	- *communication balance loss*: balance the received token amount among devices ![[Pasted image 20260721194745.png]]

*token dropping*:
- why: balance losses only encourage load balancing, not ensuring it
- first calc' the avg' computation budgets for each devices; then drop tokens with lowest affinity scores on each device until the budget is reached
- tokens belonging to ~10% of the training sequences will never be dropped

### ch03-pre-training

#### 3.1-experimental-setups

*data construction*:
- quantity:
	- recover deleted corpus data
	- incorporate more Chinese data
- quality:
	- improve the quality-based filtering algorithm
	- filter out contentious content to mitigate data bias introduced from specific regional cultures
- tokenizer: based on *byte-level byte-pair encoding* (BBPE) and have a voc' of size 100K (102400)
	- full corpus: ~8.1T tokens

*hyper-parameters*:
- model param's:
	- transformer layers: 60
	- hidden dim's: $d=5120$
	- initial parameters standard deviation: $\sigma=0.006$
	- MLA:
		- num' of attention heads: $n_h=128$
		- per-head dim': $d_h=128$
		- KV compression dim': $d_c=512$
		- Q compression dim': $d_c'=1536$
		- per-head dim' for decoupled q/k: $d_h^R=64$
	- DeepSeekMoE:
		- each MoE layer has 2 shared experts and 160 routed experts
		- intermediate hidden dim' of each expert: 1536
		- 6 routed experts + 2 shared experts activated for each token
	- additional RMSNorm layers after compressed latent vectors
- training param's:
	- AdamW: $\beta_1=0.9,\beta_2=0.95, weight\_decay=0.1$
	- learning rate scheduling: a *warmup-and-step-decay* strategy
		- maximum lr: $2.4\times 10^{-4}$
		- warmup: increase lr from 0 to maximum lr linearly during first 2K steps
		- step decay:
			- on 60%/90% tokens trained: multiply lr by 0.316
		- gradient clipping norm: 1.0
	- batch size scheduling:
		- first 225B tokens: increase gradually from 2304 to 9216
		- the rest: keep 9216 as is
	- maximum seq' len: 4K
	- pipeline parallelism leveraging: 
		- device count for routed experts in each layer: $D=8$
		- device count for each token: $M=3$
		- load balancing factors: [[#^2fdae3|see this]]
			- $\alpha_1=0.003,\alpha_2=0.05,\alpha_3=0.02$
		- drop tokens during training, but not during evaluation

*infrastructures*:
- HAI-LLM framework:
	- 16-way zero-bubble pipeline parallelism
	- 8-way expert parallelism
	- ZeRO-1 data parallelism
- less activated param's -> less requirements for tensor parallelism
- overlap the shared expert computations w/ the expert parallel all-to-all communication
- customize faster CUDA kernels
- optimize MLA based on FlashAttention-2
- NVIDIA H800 GPU clusters, each node with 8 GPUs and interconnected using NVLink + NVSwitch + InfiniBand

*long context extension*:
- *YaRN* (*Y*et *a*nother *R*oPE extensio*N* method)