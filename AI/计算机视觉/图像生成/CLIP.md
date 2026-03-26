
ref's:
- [paper](https://proceedings.mlr.press/v139/radford21a/radford21a.pdf)
- [vid1](https://www.bilibili.com/video/BV1xM4m1m7vA/?spm_id_from=333.999.0.0&vd_source=4b806a5b4fc9caaf6e7e0cb9bd5da2a0)

CLIP = Contrastive Language-Image Pre-training, 对比式文图预训练

可学习自定义任务（OCR/定位/识别动作等）

核心思想：使用大量图像和文本的配对数据进行预训练，以学习图像和文本之间的对齐关系

结构：image encoder + text encoder

![[Pasted image 20260326171308.png]]![[Pasted image 20260326172013.png]]

## image encoder

架构A：ResNet50 + 抗锯齿rect-2模糊池子 + 平均池化替换为注意力池化

架构B：Vision Transformer + 对combined patch和PE添加额外的层归一化

![[Pasted image 20260326173535.png]]
## text encoder

Transformer架构：
- 12层encoder + d=512 + heads=8
- 对文本的小写字节对编码（BPE）表示

## 训练和推理方法

构造数据集：
- 参考数据集：MS-COCO、Visual Genome、YFCC100M
- 4亿个图像-文本对

预训练：取$N$个图像-文本对打乱，让模型对每个图像找出最匹配的文本，最大化正例的余弦相似度，最小化负例的余弦相似度

训练：
- 预训练两个encoder
- $N$个图像和文本的embedding正交，得到$N\times N$的矩阵$Q$。令实际概率分布中，$P$的对角线$P_{ii}=1$，其他元素$P_{ij}=-1$。通过交叉熵计算损失函数：
$$
H(P,Q)=-\sum_{(i,j)} P_{ij}\log Q_{ij}
$$

更具体地，损失为InfoNCE Loss，其中$z=x\cdot y^T$:
$$
\mathcal L=-\log \dfrac{e^{z_{pos}}}{\sum_j e^{z_j}}
$$

