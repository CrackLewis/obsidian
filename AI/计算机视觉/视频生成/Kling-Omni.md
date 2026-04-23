
![[Pasted image 20260326120122.png]]

## 结构

- MVL：多模态视觉语言，包含一组确定的视频生成指令
- Prompt Enhancer：用于理解复杂输入并推断意图
- Omni-Generator：在共享嵌入空间中处理视觉和文本令牌，允许深层次跨模态交互
- Multimodal Super-Resolution：细化高频细节

## 训练：Omni-Generator

- 预训练：
	- 大量且全面的文本-视频对，注入基于指令的文生视频能力
	- 融合图生视频任务，增加模态间敏感度
- SFT：
	- continue-training：通过让模型接触大量且全面的任务，增强模型解读复杂指令和推理的能力
	- quality-tuning：构建一个高质量数据集并在上面微调，优化模型的输出分布
- RL：DPO，比GRPO复杂度低
- 蒸馏：
	- 为什么蒸馏：原始模型很厉害，画质也好，但推理慢；需要训练一个新模型加快推理流程
	- **轨迹匹配蒸馏**：老师模型生成视频需要150次NFE（从纯噪声迭代至清晰视频），学生模型需要学习老师模型的迭代轨迹，在大幅压缩步骤（150->10）的前提下遵循正确的去噪方向
	- **分布匹配蒸馏**：确保学生和老师生成视频的结果分布（纹理、光影、色泽等）一致。DMD/SiD等使用随机微分方程（SDE）建模，本文为ODE建模，便于在少步数的情况下生成确定结果

## Prompt Enhancer



## Multimodal Super-Resolution

级联扩散框架：在不牺牲视频质量的前提下，大幅提高视频生成模型的训练和推理效率

## 数据系统

数据收集：
- 目标：多样，一致，可控
- real-world data acquisition：
- synthetic data construction：