
## A

- Adam：一种自适应优化算法，结合了RMSProp和Momentum算法的优点，通过对梯度的一阶矩估计（均值）和二阶矩估计（未中心化的方差）进行综合运用，实现自适应学习率调整
- AUC：Area Under (ROC) Curve，表示ROC曲线下的面积，等于将正样本排列在负样本前的概率。AUC=0.5等同于随机猜测，AUC=1等同于完美预测

## B

- BatchNorm：批次内各通道归一化
- BP：梯度反向传播算法

## C

- [CLIP](https://proceedings.mlr.press/v139/radford21a/radford21a.pdf)：Contrastive Language-Image Pre-training，图文对比预训练方法
- CNN：Convolutional Neural Network，卷积神经网络
- CoT：Chain of Thought，思维链，一个提示工程概念，用于向LLM展示如何逐步推理构造输出
- CRF：Conditional Random Field，条件随机场
- CrossEntropyLoss：交叉熵损失函数

## D

## E

## F

- Faster R-CNN：一类两阶段的目标检测算法，先通过区域提议网络（RPN）生成候选区域，再对区域进行分类和边界框回归，检测精度高
- FlashAttention：一种高效的注意力算法，旨在减少内存读写量并提高计算速度
- FPR：False Positive Rate，假阳性率。$FPR=FP/(FP+TN)$

## G

- GNN：图神经网络
- GroupNorm：一种小batch（一般低于8）时适用的归一化方法，将通道分组，组内归一化，可以解决BN对均值/方差估算不准的问题，但分组需要调参

## H

- Huber Loss：也称Smooth L1 Loss，一种融合了MSE和MAE特征的损失函数，$\delta$为超参数，在差距较低时为平方增长，差距较大时为线性增长：$\text{Huber}(y,\hat y)=(\min\{\delta,|y-\hat y|\})^2/2+\delta\cdot \max\{0,|y-\hat y|-\delta\}$ ^fc32ce

## I

## J

## K

## L

- L1 Loss：也称[[#^c65b04|MAE]]
- L2 Loss：也称[[#^5d96e6|MSE]]
- LASSO：Least Absolute Shrinkage and Selection Operator，一种线性回归变体，能同时进行特征选择和模型正则化。目标函数为$\frac{1}{2}\sum_{i=1}^n (y_i-\sum_{j=1}^p x_{ij}\beta_j)^2+\lambda \sum_{j=1}^p |\beta_j|$
- LayerNorm：样本内特征值归一化
- LogSoftmax：一种防止softmax计算时指数溢出的技巧，$\text{LogSoftmax}(x_i)=x_i-x_m-\log \sum e^{x_j-x_m}$，其中$x_m=\max(x_j)$。

## M

- MAE：Mean Absolute Error，也称L1Loss，平均绝对误差，$\text{MAE}(y,\hat y)=1/n \cdot \sum|y_i-{\hat y}_i|$ ^c65b04
- MLP：Multi-Layer Perceptron，多层感知机
- MSE：Mean Squared Error，也称L2Loss，均方误差：$\text{MSE}(y,\hat{y})=1/n \cdot \sum (y_i-\hat{y}_i)^2$ ^5d96e6

## N

## O

## P

- Prompt Engineering：提示工程，一门研究如何开发、优化LLM提示词，帮助用户更好应用LLM的新兴学科

## Q

## R

- ResNet：Residual deep neural Network，带残差连接的深层网络
- ReLU：一种非饱和激活函数，满足$\text{ReLU}(x)=\max(0,x)$.
- RNN：recurrent neural network，循环神经网络
- ROC：

## S

- Sigmoid：一种饱和激活函数，满足$\text{Sigmoid}(x)=1/(1+e^{-x})$.
- SmoothL1：也称[[#^fc32ce|Huber Loss]]，一种L1/L2 Loss的制衡手段
- Softmax：柔性最大传递函数，满足$\text{Softmax}(x_1,\cdots,x_n)=1/\sum_{i=1}^n e^{x_i} \cdot(e^{x_1},\cdots,e^{x_n})$
- SVM：support vector machine，支持向量机

## T

- tanh：双曲正切函数，作为一种饱和激活函数
- TPR：True Positive Rate，真阳性率，也称*灵敏度、召回率*，表示模型找全正例的能力。$TPR=TP/(TP+FN)$。
- Transformer：2017年提出的一种仅依赖注意力机制的序列转录模型

## U

## V

## W

## X

## Y

- YOLO：You Look Only Once，一类图像目标检测框架，目标为通过仅一次前向传播完成目标检测

## Z