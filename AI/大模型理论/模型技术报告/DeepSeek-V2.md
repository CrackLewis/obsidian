
2405.04434

refs:
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

