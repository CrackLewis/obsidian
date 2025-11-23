
框架思路：
- 先启发式获取一个$k$-plex及其规模上界
- 根据获得的上界，减去不符合core性质的顶点和不符合truss性质的边
- 对剩余的子图内结点逐一进行分支限界

![[Pasted image 20251101091451.png]]

## kPlex-Degen

一个启发式k-plex求解算法。

依照退化序剥离结点，若被剥离结点度数满足k-plex要求，就根据其更新解集$S$和上界$ub$。

![[Pasted image 20251101005144.png]]

## CTCP

预处理算法，剥离一些明显不符合条件的点和边。

步骤：
- 首先需要计算度数和support数组。（support数组的计算比较费时，compact-forward算法或者定向计数算法可用）
- 将不符合边约束，即$\Delta(u,v)<\tau_e$的边加入$Q_e$
- 重复执行truss-peeling子过程，直至没有结点满足$\deg(v)<\tau_v$：
	- 将$Q_e$中所有边移除，并对应修改端点的度数、端点公共邻居与其连边的support
	- 若上述操作引发更多的边或结点不满足约束，则将对应节点加入$Q_v$，对应边加入$Q_e$

![[Pasted image 20251101005700.png]]

## BBMatrix

![[Pasted image 20251101013748.png]]

搜索实例为$(g,S,C,k)$

2个分支规则：决定哪些顶点优先加入$S$内
- BR1：在$g$中邻居极多（只有不超过一个非邻居）
- BR2：在$S$中恰好有$k-1$个非邻居。

5个归约规则：
- RR1：$v$有至少$k$个非邻居在$S$内。
- RR2：$v$有一个$u\in S$为非邻居，且$|S-N_S(u)|=k$。
- RR3：$\deg_g(v)+k\le lb$。
- RR4：对于$v\in C$，存在$u\in S$，满足：$|S|+1+r_{S\cup \{v\}}(u)+r_{S\cup \{u\}}(v)+\text{cn}_{\overline S} (u,v)\le lb$。
- RR5：对于$(u,v)\in E_g$，满足：$|S|+2+r_{S\cup \{u,v\}}(u)+r_{S\cup \{u,v\}}(v)+\text{cn}_{\overline S} (u,v)\le lb$。

2个$k$-plex规模上界：
- UB1（度数上界）：$\min_{u\in S} \{\deg_{g}(u)\}+k$。
- UB2（支撑上界）：$\min_{u,v\in S, u\neq v}\{r_S(u)+r_S(v)+\text{cn}_{\overline S}(u,v)\} + |S|$。

![[Pasted image 20251101015205.png]]

## et cetera

