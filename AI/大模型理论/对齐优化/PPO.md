---
tags:
  - 对齐优化
  - 后训练
---

refs:
- [zhihu1](https://zhuanlan.zhihu.com/p/614115887)

PPO = Proximal Policy Optimization 近端策略优化

## 背景

![[Pasted image 20260803150517.png]]

基于值函数的强化学习：通过递归求解Bellman方程维护Q函数

*基于策略的强化学习*：不通过价值函数确定动作的选择策略，而是直接学习策略$\pi(a\mid s)$本身；通过一组参数$\theta$对策略进行参数化，然后优化$\theta$

*目标函数定义*：
$$
\max_\theta J(\theta)=\max_\theta E_{\tau\sim\pi_\theta} R(\tau)=\max_\theta \sum_\tau P(\tau;\theta)R(\tau)
$$
其中：
- $\theta$是策略参数；$\tau$是状态-动作轨迹：$(s_1,a_1,s_2,a_2,\cdots,s_T,a_T)$
- 对$\tau$求和代表的是和环境交互产生的所有情况
- 轨迹$\tau$在策略$\pi_\theta(a\mid s)$下发生的概率定义为：$$P(\tau;\theta)=\left[\prod_{t=0}^T P(s_{t+1}\mid s_t,a_t)\cdot \pi_\theta(a_t\mid s_t)\right]$$

*策略梯度计算*：即$J(\theta)$对$\theta$的梯度
$$
\begin{split}
\nabla_\theta J(\theta)&=\sum_{\tau} \nabla_\theta P(\tau;\theta) R(\tau) \\
&=\sum_{\tau} P(\tau;\theta)\cdot \frac{\nabla_\theta P(\tau;\theta)}{P(\tau;\theta)} R(\tau)\\
&=\sum_{\tau} P(\tau;\theta)\nabla_\theta \log P(\tau;\theta) R(\tau)\\
&= E_{\tau\sim\pi_\theta} \nabla_\theta \log P(\tau;\theta) R(\tau)
\end{split}
$$
其中$\nabla_\theta \log P(\tau;\theta)$的计算使用了对数导数技巧：
$$
\begin{split}
\nabla_\theta \log P(\tau;\theta)&= \nabla_\theta\left[ \sum_{t=0}^T \log P(s_{t+1}\mid s_t,a_t) + \sum_{t=0}^T \log \pi_\theta(a_t\mid s_t) \right]\\
&=\sum_{t=0}^T \nabla_\theta \log \pi_\theta(a_t\mid s_t)
\end{split}
$$
其中首项和策略、策略参数无关，梯度为0。

到这一步，策略梯度计算转化为轨迹$\tau$的求和问题。由于真实环境难以精确测算，只能通过样本进行近似：
![[Pasted image 20260803155044.png]]

其中：$m$为采样次数，$n$为最长步数。

通过采样计算得到$\nabla_\theta J(\theta)$，根据其反向更新$\theta$，直至最优策略：
$$
\theta\leftarrow \theta+\alpha\cdot \nabla_\theta J(\theta)
$$

### 策略建模

*Softmax策略*：多用于离散动作空间
$$
\pi_\theta(s,a)=\frac{e^{\phi(s,a)^T \theta}}{\sum_{a'\in A} e^{\phi(s,a')^T \theta}}
$$
策略梯度：
$$
\nabla_\theta \log \pi_\theta(a\mid s)=\phi(s,a)-\sum_{a'\in A} \phi(s,a')\pi_\theta (a\mid s)
$$
解释：观察到的特征向量$\phi(s,a)$，减去所有动作的平均特征向量；远离均值的动作会触发强烈的更新梯度信号

*高斯策略*：多用于连续动作空间
$$
\pi_\theta(a\mid s)=\frac{1}{\sqrt{2\pi}\cdot \sigma_\theta} e^{-\frac{a-\mu_\theta}{2\sigma_\theta^2}}
$$
其中：$\mu_\theta=\phi(s,a)^T \theta$为正态分布均值

策略梯度：
$$
\nabla_\theta \log \pi_\theta (a\mid s)=\frac{(a-\mu_\theta)\phi(s)}{\sigma_\theta^2}
$$

### 自然策略梯度算法

*传统策略梯度算法的不足*：
- 可能出现过冲或下冲：
	- 过冲：更新错过了奖励峰值，落入了次优策略区域
	- 下冲：更新步长过小，导致收敛缓慢

