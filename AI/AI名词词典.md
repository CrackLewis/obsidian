
## A

- Adam：一种自适应优化算法，结合了RMSProp和Momentum算法的优点，通过对梯度的一阶矩估计（均值）和二阶矩估计（未中心化的方差）进行综合运用，实现自适应学习率调整
- AUC：Area Under (ROC) Curve，表示ROC曲线下的面积，等于将正样本排列在负样本前的概率。AUC=0.5等同于随机猜测，AUC=1等同于完美预测 ^1cb2ac

## B

- BatchNorm：批次内各通道归一化
- BERT：Bidirectional Encoder Representations from Transformer，由Google于2018年提出的一种革命性自然语言处理模型
- BP：gradient Back-Propagation, 梯度反向传播算法
- BPE：Byte-Pair Encoding

## C

- CF：Cross Filtering，协同过滤
- [CLIP](https://proceedings.mlr.press/v139/radford21a/radford21a.pdf)：Contrastive Language-Image Pre-training，图文对比预训练方法
- CNN：Convolutional Neural Network，卷积神经网络
- Confusion Matrix：混淆矩阵，分类问题中的一种评估方式，可用于计算准确率和召回率
- CoT：Chain of Thought，思维链，一个提示工程概念，用于向LLM展示如何逐步推理构造输出
- CRF：Conditional Random Field，条件随机场
- CrossEntropyLoss：交叉熵损失函数
- Cross Validation：交叉验证方法。一种模型评估方法，将数据集分为$k$份，轮流取其中一份作为验证集，其他作为训练集，取$k$次结果的平均值

## D

- DCG@K：Discounted Cummulative Gain，推荐系统指标，表示推荐列表中前K个物品的相关性得分加权和：$\text{DCG@K}=\sum_{i=1}^K \frac{\text{rel}_i}{\log_2(i+1)}$
- Decision Tree：决策树，一种基于树结构进行决策的算法，通过一系列规则对数据进行分类或回归，是随机森林和 GBDT 的基础
- DNN：深度神经网络
- Dropout：一种正则化技术。在训练过程中随机将部分神经元的输出置零（概率为$p$），防止神经元之间的共适应关系，有效缓解过拟合

## E

## F

- F1-score：精确率与召回率的调和平均数，用于综合评估一个分类模型的性能，特别适用于样本不平衡的场景。$F1=2\cdot \dfrac{P\cdot R}{P+R}$
- Faster R-CNN：一类两阶段的目标检测算法，先通过区域提议网络（RPN）生成候选区域，再对区域进行分类和边界框回归，检测精度高
- FlashAttention：一种高效的注意力算法，旨在减少内存读写量并提高计算速度
- FPR：False Positive Rate，假阳性率。$FPR=FP/(FP+TN)$

## G

- GBDT：Gradient Boosting Decision Tree，梯度提升决策树。一种迭代算法，每一棵树拟合前一棵树的残差，常用于结构化数据建模（如 XGBoost, LightGBM 的基础）
- GELU：Gaussian-Error Linear Unit，高斯误差线性单元。 $\text{GELU}(x)=x\Phi(x)\approx 0.5x(1+\tanh(\sqrt{2/\pi}\cdot (x+0.044715x^3)))$
- GNN：图神经网络
- GPT：Generative Pretrained Transformer，OpenAI于2018年提出的一类文本序列生成模型
- GroupNorm：一种小batch（一般低于8）时适用的归一化方法，将通道分组，组内归一化，可以解决BN对均值/方差估算不准的问题，但分组需要调参

## H

- Huber Loss：也称Smooth L1 Loss，一种融合了MSE和MAE特征的损失函数，$\delta$为超参数，在差距较低时为平方增长，差距较大时为线性增长：$\text{Huber}(y,\hat y)=(\min\{\delta,|y-\hat y|\})^2/2+\delta\cdot \max\{0,|y-\hat y|-\delta\}$ ^fc32ce

## I

## J

## K

- KL Divergence：Kullback-Leibler Divergence，KL散度，用于衡量使用一个近似概率分布$Q$模拟真实概率分布$P$时引入的信息损失。KL散度值越小，意味着$P,Q$越贴合

## L

- L1 Loss：也称[[#^c65b04|MAE]]
- L2 Loss：也称[[#^5d96e6|MSE]]
- LASSO：Least Absolute Shrinkage and Selection Operator，一种线性回归变体，能同时进行特征选择和模型正则化。目标函数为$\frac{1}{2}\sum_{i=1}^n (y_i-\sum_{j=1}^p x_{ij}\beta_j)^2+\lambda \sum_{j=1}^p |\beta_j|$
- LayerNorm：样本内特征值归一化
- LogSoftmax：一种防止softmax计算时指数溢出的技巧，$\text{LogSoftmax}(x_i)=x_i-x_m-\log \sum e^{x_j-x_m}$，其中$x_m=\max(x_j)$。
- LoRA：Low-Rank Adaption，低秩适应。一种LLM轻量微调技术，通过向模型的部分层添加可训练的低秩矩阵模块，实现模型在特定任务上的能力调整，同时保持原模型参数不变 ^e94b19

## M

- MAE：Mean Absolute Error，也称L1Loss，平均绝对误差，$\text{MAE}(y,\hat y)=1/n \cdot \sum|y_i-{\hat y}_i|$ ^c65b04
- MHA：Multi-Head Attention，多头注意力
- MLM：Masked Language Modeling，掩码语言建模，BERT架构采用的一种预训练任务，类似于让模型做“完形填空”
- MLP：Multi-Layer Perceptron，多层感知机
- MSE：Mean Squared Error，也称L2Loss，均方误差：$\text{MSE}(y,\hat{y})=1/n \cdot \sum (y_i-\hat{y}_i)^2$ ^5d96e6

## N

- NDCG@K
- NSP：Next Sentence Prediction，下句预测，BERT架构采用的一种预训练任务

## O

- Overfitting：过拟合，模型在训练集上表现很好但在测试集上表现较差的现象，通常因模型过于复杂或训练数据不足导致，可通过正则化、Dropout 等手段缓解。见[[#^193e15|Underfitting]] ^be82ea

## P

- PCA：Principal Component Analysis，主成分分析。一种无监督降维技术，通过正交变换将数据投影到方差最大的方向，保留主要信息
- Precision：精确率/准确率，预测为正的样本中，实际为正的比率。$\text{Precision}=TP/(TP+FP)$
- Prompt Engineering：提示工程，一门研究如何开发、优化LLM提示词，帮助用户更好应用LLM的新兴学科
- [[模型量化#PTQ static|PTQ]]：Post-Training Quantization，先训练后量化的模型量化方法。根据激活的量化时机不同分为动态和静态PTQ

## Q

- QLoRA：Quantized [[#^e94b19|LoRA]], LoRA的量化版本
- [[模型量化#QAT|QAT]]：Quantization-Aware Training。一种边训练边量化的模型量化方法，在模型中添加伪量化节点模拟量化，微调模型

## R

- Random Forest：随机森林。一种集成学习算法，通过构建多个决策树并综合它们的输出（投票或平均）来提高预测精度和稳定性
- RBM：Restricted Boltzmann Machine，受限玻尔兹曼机。
- ResNet：Residual deep neural Network，带残差连接的深层网络
- ReLU：一种非饱和激活函数，满足$\text{ReLU}(x)=\max(0,x)$。
- RNN：recurrent neural network，循环神经网络
- ROC：Receiver Operating Characteristic Curve，接收者操作特征曲线。以FPR为横轴，TPR为纵轴绘制的曲线，曲线下面积即为[[#^1cb2ac|AUC]]。

## S

- SGD：Stochastic Gradient Descent，随机梯度下降。每次更新参数仅使用一个样本或一个小批量样本，相比批量梯度下降收敛更快但波动较大
- Sigmoid：一种饱和激活函数，满足$\text{Sigmoid}(x)=1/(1+e^{-x})$.
- Smooth L1：也称[[#^fc32ce|Huber Loss]]，一种L1/L2 Loss的制衡手段
- Softmax：柔性最大传递函数，满足$\text{Softmax}(x_1,\cdots,x_n)=1/\sum_{i=1}^n e^{x_i} \cdot(e^{x_1},\cdots,e^{x_n})$
- SVM：support vector machine，支持向量机。核心思想是找到一个超平面，使得不同类别样本之间的间隔（margin）最大化

## T

- tanh：双曲正切函数，作为一种饱和激活函数
- TPR：True Positive Rate，真阳性率，也称*灵敏度、召回率*，表示模型找全正例的能力。$TPR=TP/(TP+FN)$。
- Transformer：2017年提出的一种仅依赖注意力机制的序列转录模型

## U

- Underfitting：欠拟合，模型在训练集和测试集上表现均不佳，通常因模型过于简单无法捕捉数据特征导致。见[[#^be82ea|Overfitting]] ^193e15

## V

## W

## X

- Xavier Initialization：Xavier初始化方法，一种模型权重初始化方法。要求对于全连接层，权重方差$\delta^2=2/(m+n)$，其中$n,m$分别为输入和输出的维度数

## Y

- YOLO：You Look Only Once，一类图像目标检测框架，目标为通过仅一次前向传播完成目标检测

## Z

## 非英文开头

