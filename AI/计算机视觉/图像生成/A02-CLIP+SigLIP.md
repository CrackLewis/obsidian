
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


## SigLIP

SigLIP = **Sig**moid loss for **L**anguage-**I**mage **P**re-training

功能与CLIP类似，将图像和文本进行对比训练，但规避了CLIP中的softmax计算

![|150%](https://pic1.zhimg.com/v2-de06bab657398b3e7ee52c736577cf9e_1440w.jpg)

CLIP损失函数：

![[Pasted image 20260331153254.png]]

（注意两项分母的向量点积有区别）

## 模型结构

CLIP/SigLIP均采用双塔式图文对齐模型的结构

![[Drawing 2026-05-19 11.42.09.excalidraw|1000x300]]

投影层：将编码器输出的图文特征投影到一个较低且相等维度的向量空间
$$
z_i=W_I f_I(x_i),\qquad z_t=W_T f_T(x_t)
$$

L2正则化：转换为单位向量
$$
\hat{z_i}=z_i/\lVert z_i\rVert,\qquad \hat{z_t}=z_t/\lVert z_t\rVert
$$

