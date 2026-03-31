
SigLIP = **Sig**moid loss for **L**anguage-**I**mage **P**re-training

功能与CLIP类似，将图像和文本进行对比训练，但规避了CLIP中的softmax计算

![|150%](https://pic1.zhimg.com/v2-de06bab657398b3e7ee52c736577cf9e_1440w.jpg)

CLIP损失函数：

![[Pasted image 20260331153254.png]]

（注意两项分母的向量点积有区别）

