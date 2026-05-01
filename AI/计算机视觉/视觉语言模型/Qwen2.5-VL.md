---
tags:
  - VLM
  - 多模态
---


refs:
- [arxiv](https://arxiv.org/abs/2502.13923)
- [zhihu1](https://arxiv.org/abs/2502.13923)
- [cnblogs1](https://www.cnblogs.com/yangykaifa/p/19251300)

![[Pasted image 20260427173728.png]]

outline:
- intro
- approach
	- model arch
	- pre-training
	- post-training
- experiments
	- v.s. SotA
	- pure text tasks
	- quantitative results
		- general visual Q&A
		- document understanding & OCR
		- spatial understanding
		- video understanding & grounding
		- agent capabilities
- conclusion

## sec01-intro

VLM的夹心饼干 = 底层（精细视觉感知）+中层（多模态视觉能力）+高层（多模态推理）

