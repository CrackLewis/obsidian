
基本概念：
- 状态（state）：某一时刻智能体所处环境的完整描述
- 行动（action）：智能体在某个状态下可执行的所有可能行为的集合
- 策略（policy）：智能体的行为准则，决定在给定状态下如何选择行动
	- 确定性策略：$\pi(a^*\mid s)=1, \forall a\in\mathcal A\backslash \{a^*\}, \pi(a\mid s)=0$
	- 随机性策略：$\forall a\in\mathcal A, 0<\pi(a\mid s)<1$
- 奖励（reward）：在某一状态$s\in\mathcal S$下，智能体执行某一动作$a\in\mathcal A$后，由环境给予的即时反馈
- 回报（return）：从某一时刻开始，未来所有奖励折扣后的累计总和
- 价值（value）：评估一个状态或一个状态行动对的长期价值
	- 状态价值函数（SVF）：$V^\pi(s)=E_\pi[G_t\mid S_t=s]$
	- 动作价值函数（AVF）：$Q^\pi(s,a)=E_\pi[G_t\mid S_t=s,A_t=a]$
	- SVF等于当前状态下所有动作的AVF总和

