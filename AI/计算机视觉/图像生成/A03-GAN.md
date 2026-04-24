
refs:
- [csdn1](https://blog.csdn.net/lzm12278828/article/details/147905139)
- [zhihu1](https://zhuanlan.zhihu.com/p/628915533)

Generative Adversarial Network

一对无监督模型：
- *生成器*（generator）：生成尽可能和原始数据相像的新数据
- *判别器*（discriminator）：判定一个样本是真实数据还是生成数据

![[Pasted image 20260424152921.png]]

## 博弈均衡

真实分布设为$p_{data}(x)$，生成器分布设为$p_g(x;\theta_g)$，则二者差异可通过*KL散度*衡量：
$$
\text{KL}(p_{data}||p_g)=\int p_{data}(x)\cdot \log\dfrac{p_{data}(x)}{p_g(x)} dx
$$
*GAN目标函数*：极小极大博弈
$$
\begin{gather}
\mathcal L(D,G)=\min_G \max_D V(D,G) \\
V(D,G)=E_{x\sim p_{data}(x)} [\log D(x)]+E_{z\sim p_g(z)}[\log(1-D(G(z)))]
\end{gather}
$$
其中：$x$为真实数据，$z$为随机噪声，$G(\cdot):z\rightarrow \overset{\sim}{x}$为生成器函数，$D(\cdot):x\rightarrow score$为判别器函数

最理想的情况：$p_{data}=p_g$，生成分布和数据分布一致，此时$D(x)=0.5$，损失函数达到最小值$-\log 4$。

## 模型结构

经典结构：
- 生成器为反卷积网络，将噪声转化为数据
- 判别器为卷积网络，将数据转化为一个判别值

![[Pasted image 20260424172552.png]]

*对损失函数的改进*：
- WGAN-GP（带梯度惩罚的Wasserstein GAN）：在损失函数后加一个梯度惩罚项，控制参数稳定性
- LSGAN（最小二乘GAN）：对数损失 --> 最小二乘损失
- CGAN（条件GAN）：在某一类别/特征下的损失是多少

*高级GAN结构*：
- DCGAN：生成器/判别器中：
	- 全连接层 --> 卷积层
	- 池化层 --> 步长卷积
	- 引入BN实现稳定训练
- StyleGAN：引入风格注入机制
- TransformerGAN：
	- 生成器使用Transformer decoder
	- 判别器使用ViT

*特殊GAN*：CycleGAN/StarGAN/3DGAN

## 模式崩溃问题

