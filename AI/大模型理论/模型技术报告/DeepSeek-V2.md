
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

### 