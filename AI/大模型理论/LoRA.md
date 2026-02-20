
LoRA = Low-Rank Adaption

## 原理



## QLoRA

量化版本的LoRA
- 4-bit量化：将预训练权重量化为NF4（Normalized Float4）格式，减少显存占用
- 分页优化器：将优化器状态卸载至CPU内存，避免OOM
- 双重量化：对量化常数二次量化，进一步压缩
