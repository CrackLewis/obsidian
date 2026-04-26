
## 已知性质

设全图为$G$，k-plex为$g$，其规模为$l=|V_g|$，松弛度$k$。

（KPlexS论文）

两个非邻居节点必有至少$l-2k+1$个公共邻居。

规模满足$l\ge 2k-1$的k-plex必定连通。

任意节点的邻居集合的导出子图规模不小于$l-2k$。

（学长论文）

任何一个k-plex可分解为一个(k-1)-plex和一个clique

设对松弛度$2\le k\le 5$，最大k-plex规模$v_k$。则：
- $v_{k+1}\le 2v_k$。
- 向$G$任加一边：$v_k\le v_k'\le v_k+1$。
- 从$G$任删一边：$v_k-1\le v_k'\le v_k$。

## KPlexS

一个根据指定松弛度$k$，求解最大k-plex的算法

> [!note] k-plex的包含性质
> 一个k-plex的任意子图仍是k-plex。

> [!note] 引理1
> 一个规模为$l$的$k$-plex中，任意两个非邻居节点至少具有$l-2k+2$个公共邻居。
> - 可通过容斥原理简单证明。
> - 进一步，若$l\ge 2k-1$，则k-plex必为连通子图。

> [!note] 引理2
> 对规模为$l$的k-plex$P$中一点$u\in V_P$，若$l\ge 2k+1$，则其邻居集合$N_P(u)$的导出子图$g$的度数满足：$\deg g\ge l-2k$。
> - 证明：根据k-plex的包含性质，$N_P(u)$也是k-plex。由于$|N_P(u)|\ge l-k$，所以$\deg N_P(u)\ge (l-k)-k=l-2k$。

> [!note] k-plex的core和truss性质
> - **core性质**：规模为$l$的k-plex内任一顶点的度数不低于$l-k$。
> - **truss性质**：规模为$l$的k-plex内任意一对顶点的公共邻居数不少于$l-2k$。

^4928c4

算法框架：
- 先用`kPlex-Degen`方法启发式计算一个k-plex，并估计当前图中的最大k-plex上界
- 运用`CTCP`方法移除一些显然不可能在最大k-plex中的节点
- 从剩余的图中，选取一个度数最小的节点（最大k-plex必受制于全图度数最小的节点）。在该节点附近，通过`BBMatrix`方法寻求一个最大k-plex
- 将最小度数节点移除，从剩余节点中重复上述步骤，直到图为空或当前最大k-plex达到规模上界

![[Pasted image 20250614124310.png]]

### kPlex-Degen

kPlexS算法首先调用该算法，用于在图中启发式计算一个k-plex，并返回全图最大k-plex的规模上限。

大致流程：依次移除度数最小的节点，根据移除各节点$v_i$时的全图规模$l_i$估算最大k-plex规模的上界：
$$
ub=\min\left(\min(\deg(v_i)+k, l_i)\right),\forall i=1,2,\cdots,n
$$
在不断移除顶点的同时，维护并更新最大k-plex。

![[Pasted image 20250618085857.png]]

### Core-Truss Co-Pruning (CTCP)

^ed1c3e

*算法思想*：

结合[[#^4928c4|core和truss性质]]得知：对于规模为$l$的k-plex：
- k-plex中所有顶点$v$满足$\deg(v)\ge l-k$。
- k-plex中所有边$(u,v)$满足$\Delta(u,v)\ge l-2k$。

`kPlex-Degen`已经获得了一个规模为$lb$的k-plex。如果需要更新，则至少需要找到一个规模为$lb+1$的k-plex。这样在新k-plex中，所有的顶点必须满足$\deg(v)\ge lb+1-k$，所有的边必须满足$\Delta(u,v)\ge lb+1-2k$。

基于这种思想，我们移除所有不符合这两条约束的顶点和边。如果规模至少为$lb+1$的k-plex存在，它一定是剩余顶点和边的一个子图。

这个过程会在kPlexS内重复多次。当CTCP完成后，下游的`BBMatrix`会在图内搜索一个最大k-plex，如果搜索成功，则$lb$会变更为新k-plex的规模。

![[Pasted image 20250619131705.png]]

*算法流程*：
- 参数：
	- $G$：待剪枝的图
	- $Q_v$：待移除顶点队列。作为参数时不超过一个元素
	- $lb\_changed$：标记最大k-plex的下界是否发生了变化。
	- $\tau_v,\tau_e$：顶点度数阈值和边三角数阈值。$\deg(v)<\tau_v$的顶点和$\Delta(u,v)<\tau_e$的边都会被移除
	- $\deg,\Delta$：度数和边三角数
- 总体步骤：
	- 若$lb\_changed$为`true`，则将所有$\Delta(u,v)<\tau_e$的边收集至队列$Q_e$
	- 调用`truss_peeling`方法移除所有$Q_e$内的边和$Q_v$内的顶点，同时更新$\deg$和$\Delta$
	- 若存在顶点满足$\deg(v)<\tau_v$，则将其加入$Q_v$并重复调用`truss-peeling`，直到图同时满足$\tau_v$-core和$\tau_e$-truss

*truss-peeling过程*：
- 依次移除$Q_e$中的所有边，并更新$\deg,\Delta$。若出现新的边满足$\Delta(u,v)=\tau_e-1$，则将其加入$Q_e$
- 从$Q_v$中移除一个顶点及其关联边，更新$\deg,\Delta$。同时重复上述检查+加边操作

*时间复杂度*：$O(\delta(G)\times |E|)$，其中$\delta(G)$是图的退化度（$\delta(G)\ll \sqrt{|E|}$）。
- Maplex为$O(r\cdot |E|^{1.5})$，KpLeX为$O(r\cdot |V|\cdot |E|)$。

### BBMatrix

在`CTCP`算法得到一个相对稠密的子图后，可以对每个节点进行分支限界，搜索出子图中的最大k-plex。

搜索实例的数学描述为$I=(g,k,S,lb)$，其中$g$为稠密子图，$k$为松弛度，$S$为候选顶点集，$lb$为当前k-plex规模下界。

#### 2条分支规则

分支规则决定哪些节点必定在$S$内

*分支规则*：判断哪些顶点必定在$S$内
- BR1（优先处理非邻居少的顶点）：
	- 白话：若一个顶点和图中几乎所有其他顶点均为邻居，只有不超过一个非邻居，则其肯定在最大k-plex中
	- 数学表达：若$\exists u\in V(g)-S$，使得$\deg_g(u)\ge |V(g)|-2$，则$u$必须加入$S$。（不生成排除分支）
- BR2（处理剩余顶点）：
	- 白话：候选集$S$会随着搜索深入不断扩大。适合加入候选集的顶点应当确保$S$中仅有不超过$k-1$个顶点不是该顶点的邻居，这样才不会违背k-plex性质
	- 数学表达：选择$V_0=\{v\not\in S\mid |S-N_S(v)|=k-1\}$中的顶点。若$V_0=\varnothing$，则选择$V(g)-S$中度数最高的顶点
	- 目的：度数较低、非邻居数较高的节点是k-plex的瓶颈。处理这些约束强的顶点可以加速剪枝

#### 5条归约规则

归约规则决定哪些节点不会加入$S$

> [!note] 引理5.2
> 给定一个图$g$、一个k-plex$S\subset V(g)$和其中两个顶点$u,v\in S$，则包含$S$中所有顶点的最大k-plex的规模不会超过：
> $$
> |S|+r_S(u)+r_S(v)+\text{cn}_{\overline{S}}(u,v) 
> $$
> 其中，$r_S(u)=k-|S-N_S(u)|$表示$u$在$S$外最多允许存在多少个非邻居；$\text{cn}_{\overline{S}}(u,v)=|N_{\overline{S}}(u)\cap N_{\overline{S}}(v)|$表示$u,v$在$S$外的公共邻居数。
> **证明**：考虑一个包含$S$的k-plex $P\supseteq S$，则$P-S$可以划分为四个不相交的子集（见下图），分别为：
> - $N^{cn}$：$u,v$的公共邻居
> - $N^e(u)$：与$u$相邻但不与$v$相邻的顶点集合，即$N^e(u)=N_{P-S}(u)-N^{cn}$
> - $N^e(v)$：类上
> - $N^{cnon}$：$u,v$的公共非邻居
> 根据$r_S(u),r_S(v)$的定义，我们有：
> $$
> |N^e(v)|+|N^{cnon}|\le r_S(u), |N^e(u)|+|N^{cnon}|\le r_S(v), 
> $$
> 因为$P-S\subseteq V(g)-S$，所以$P-S$中允许的$u,v$的非邻居数量不能超过$V(g)-S$中的对应数量。同理：
> $$
> |N^{cn}|\le \text{cn}_{\overline{S}}(u,v)
> $$
> 因此$|P|$满足：
> $$
> \begin{split}
> |P|&=|S|+|N^e(u)|+|N^e(v)|+|N^{cnon}|+|N^{cn}|\\
> &\le |S|+r_S(u)+r_S(v)+\text{cn}_{\overline{S}}(u,v)
> \end{split}
> $$

![[Pasted image 20250629123348.png]]

*归约规则*：判断哪些顶点必定不在$S$内
- RR1-RR3（基于度数的规则）：
	- RR1：
		- 白话：如果顶点在$S$内有至少$k$个非邻居，则认为其不可能加入$S$
		- 数学表达：若$v\not\in S$满足$|S-N_S(v)|\ge k$，则排除$v$
	- RR2：
		- 白话：$S$中会存在一些瓶颈顶点，它们的非邻居数恰为$k-1$。如果顶点与它不为邻居，则认为顶点不可能加入$S$
		- 数学表达：对于$u\not\in S$，若$\exists v\in S$且$|S-N_S(v)|=k$，使得$u,v$非邻居，则排除$u$
	- RR3：
		- 白话：如果$v$在原图$g$中都无法满足k-core性质，则其在$S$中更不可能满足
		- 数学表达：若$\deg_g(v)+k\le lb$，则排除$v$
- RR4-RR5（基于三角数的规则）：参考引理5.2及其证明
	- RR4：
		- 白话：若往$S$中加入一个顶点，会导致任何包含$S$的k-plex规模上限不超过已知最大k-plex的规模下限，则排除此顶点
		- 数学表达：对$v\not\in S$，若存在$u\in S$满足$|S|+1+r_{S\cup \{v\}}(u)+r_{S\cup \{v\}}(v)+\text{cn}_{\overline{S}}(u,v)\le lb$，则排除$v$
	- RR5：
		- 白话：若$S$中同时包含互为邻居的两个顶点，会导致任何包含$S$的k-plex规模上限不超过已知最大k-plex的规模下限，则排除连接这两个顶点的边
		- 数学表达：对$(u,v)\in E(g)$（其中$u,v\not\in S$），若$|S|+2+r_{S\cup \{u,v\}}(u)+r_{S\cup \{u,v\}}(v)+\text{cn}_{\overline{S}}(u,v)\le lb$，则排除$(u,v)$

#### 上界计算

根据当前的$S$估计一个k-plex规模上界，可以排除大量的无用分支

*UB1*（度数上界）：
$$
\min_{u\in S} \deg_g(u)+k
$$

*UB2*（二阶上界）：$u,v$不需要为邻居
$$
\min_{u,v\in S,u\neq v} \left\{r_S(u)+r_S(v)+\text{cn}_{\overline{S}}(u,v)\right\}+|S|
$$

上界在算法中的具体应用：
- RR3：根据$S$外的顶点估算k-plex规模上界（见下文UB1），基于该上界排除顶点
- RR4：根据$S$内外顶点间的连接关系估算k-plex规模上界（见下文UB2），基于该上界排除顶点
- RR5：根据$V(g)-S$内顶点连接关系计算上界，基于该上界排除边

#### BBMatrix算法内容

![[Pasted image 20250630175603.png]]

总体步骤：
- 1-6：在$g$中启发式寻找一个k-plex，并根据该k-plex确定的上下界实施CTCP
- 9-23：BBSearch过程
	- 9-10（特判）：如果$S$已经包含了所有顶点，则直接返回$S$
	- 12-17（包含分支）：从$V(g)-S$中选取一个可加入的顶点$u$，尝试将其加入$S$，通过归约规则对$g$归约，如果满足上界限制则继续搜索，最后回溯
	- 19-23（排除分支）：从$g$中尝试移除$u$并对$g$归约，然后如果满足上界限制则继续搜索，最后回溯

## kPEX

![[Pasted image 20250706080111.png]]

*核心思想*：提出一种交替式归约-定界框架（Alternated Reduction-and-Bound, AltRB），结合高效的预处理技术，显著提升最大k-plex搜索的效率。

设搜索实例$I=(S,C)$。$S$为部分解集（partial solution，确定加入k-plex的顶点集合），$C$为候选集（candidate set，有可能但尚未加入k-plex的顶点集合）。传统的归约定界法对每个$u\in C$尝试两个分支：
- $I_1=(S\cup \{u\},C-\{u\})$：接受$u$作为$S$的新成员
- $I_2=(S,C-\{u\})$：从候选集排除$u$

框架组成：
- CF-CTCP：改进版的[[#^ed1c3e|CTCP]]归约算法
- KPHeuris：启发式算法
- AltRB（*核心*）：交替式缩减-定界框架

### AltRB

![[Pasted image 20250707172933.png]]

大致流程：
- 先分别划分解集$S$和候选集$C$为两部分
- 若根据$S_L,C_L$推算的上界大于$UB_L$（$UB_L$未收敛），则更新上下界，并运用[[#AltRB归约规则]]，排除不可能的顶点
- 若$UB_L$已收敛，则合并$C_L,C_R$并返回

#### 分支划分与理论基础

给定$I=(S,C)$，将其划为两部分：
$$
S=S_L\cup S_R, C=C_L\cup C_R
$$
考虑将候选解$H$（满足$|H|\ge |S^*|+1$的k-plex）拆分为：
$$
H=S\cup (C_L\cap H)\cup (C_R\cap H)
$$

> [!note] 引理4.1
> 设左右两侧集合$C_L,C_R$的规模上下界为$UB_L,LB_L,UB_R,LB_R$。则上界满足：
> $$
> \begin{split}
> |C_L\cap H|&\ge (|S^*|+1)-|S|-UB_R, \\
> |C_R\cap H|&\ge (|S^*|+1)-|S|-UB_L.
> \end{split}
> $$
> 以第一个不等式为例，通过反证法证明，假设$|C_L\cap H|< (|S^*|+1)-|S|-UB_R$，则：
> $$
> |H|=|S|+|C_L\cap H|+|C_R\cap H|<|S|+\left((|S^*|+1)-|S|-UB_R\right)+UB_R=|S^*|+1
> $$
> 与假设矛盾。因此第一个不等式成立，第二个同理。

若规定候选集两侧的下界如下：
$$
\begin{split}
(|S^*|+1)-|S|-UB_R&\le LB_L\le |C_L\cap H|\\
(|S^*|+1)-|S|-UB_L&\le LB_R\le |C_R\cap H|
\end{split}
$$
则候选集一侧的上/下界与另一侧下/上界相互约束。因此可以考虑，通过交替“更新一侧上界-更新另一侧下界”的步骤，实现上下界逐渐收敛。

*AltRB的大致步骤*：
- 计算$UB_L$（计算过程详见上界计算），根据$UB_L$更新$LB_R$
- 根据归约规则（详见归约规则）和$UB_R,LB_R$更新$C_R$
- 计算$UB_R$，根据其更新$LB_L$
- 根据归约规则和$UB_L,LB_L$更新$C_L$
- 重复上述四步，直到$UB_L$在一轮内未变更

上界越紧，下界一般也越紧

#### AltRB归约规则

归约规则应用在AltRB算法伪代码的第5、7行

> [!note] 归约规则RR1
> 给定$I=(S,C)$和下界$LB_L,LB_R$，若$v\in C$满足下列条件之一，则将$v$从$C$中排除：
> - $v\in C_L$，且$|N(v,S\cup C_L)|<LB_L+|S|-k$或$|N(v,S\cup C_R)|<LB_R+|S|-k+1$成立。
> - $v\in C_R$，且$|N(v,S\cup C_L)|<LB_L+|S|-k+1$或$|N(v,S\cup C_R)|<LB_R+|S|-k$成立。

大意是：若$C$中的顶点在任意一边缺乏足够凑成k-plex的邻居数，则认为其不可能包含在$S$内。

> [!note] 归约规则RR2
> 给定$I=(S,C)$和上界$UB_L,UB_R$：
> - 当$UB_L+UB_R+|S|=|S^*|+1$且$UB_L=|C_L|$时，若$G[S\cup C_L]$是一个k-plex，则$S\leftarrow S\cup C_L$，否则终结分支。
> - 当$UB_L+UB_R+|S|=|S^*|+1$且$UB_R=|C_R|$时，若$G[S\cup C_R]$是一个k-plex，则$S\leftarrow S\cup C_R$，否则终结分支。

大意是：若当前候选集的规模上界刚刚超过最优解，则判断规模完全贴合上界的一侧是否可以与$S$组成k-plex，若可以，则将这一侧并入$S$。

#### 上界计算（ComputeUB）

以计算$UB_L=\text{ComputeUB}(S_L,C_L)$为例。

`ComputeUB`首先将$C_L$划分为$|S_L|+1$个互斥子集，其中第$i$个子集$\Pi_i(S_L,C_L)$包含集合$C_L^i$中节点$u_i\in S_L$的所有非邻居节点。公式表述：
$$
\Pi_i(S_L,C_L)=\overline{N}(u_i,C_L^i), C_L^i=C_L-\bigcup_{j=1}^{i-1} \Pi_j(S_L,C_L)
$$

其中：
- $C_L^i$：从$C_L$中排除前$i-1$个互斥子集后，形成的剩余集合。特别地，$C_L^1=C_L$，$C_L^{|S_L|+1}=\Pi_i(S_L,C_L)$。
- $u_i$：递归定义得到，为$S_L-\{u_1,\cdots,u_{i-1}\}$中比值$\dfrac{\overline{N}(u_i,C_L^i)}{k-|\overline{N}(u_i,C_L^i)|}$最大的节点（可以理解为，这个比值越大，结点$u_i$和$C$中结点越难共存）

特别地：
$$
\Pi_0(S_L,C_L)=C_L-\bigcup_{i=1}^{|S_L|} \Pi_i(S_L,C_L)
$$
表示与$S_L$中所有节点相邻的节点子集。

大白话：$\Pi_i(S_L,C_L)$中的任一节点$v$满足$v$与所有的$u_j$（$1\le j\le i-1$）相邻，但$v,u_j$不相邻。$\Pi_0(S_L,C_L)$则与$S_L$的所有节点相邻。

*注意到*：对于分支$H$内的一个k-plex $G[H]$，对于子集$\Pi_i(S_L,C_L)$（$1\le i\le |S_L|$），$C_L\cap H$包含其中的顶点数不超过：
$$
\min\{|\Pi_i(S_L,C_L)|, k-|\overline{N}(u_i,S)|\}
$$
可以通过反证简单证明：如果超过这个值，$u_i$在$H$中就有超过$k$个非邻居，从而不构成一个合法的k-plex。因此$\text{ComputeUB}$结果（$UB_L$的估计值）等于$\Pi_0$以及各子集与$C_L\cap H$交集上限的总和：
$$
\text{ComputeUB}(S_L,C_L)=\Pi_0(S_L,C_L)+ \sum_{i=1}^{|S_L|} \min\{|\Pi_i(S_L,C_L)|,k-|\overline{N}(u_i,S)|\}
$$

在SeqRB中，使用ComputeUB的上界计算可以获得目前（2025）已知的最紧k-plex规模上界：$|S|+\text{ComputeUB}(S,C)$。*在AltRB中*，分别对$(S_L,C_L),(S_R,C_R)$各运用一次上界计算，分别得到$UB_L,LB_L$的估计值。

#### 基于贪心策略的左右划分

从ComputeUB的部分注意到，$\Pi_0$的所有节点都对上界计算产生了贡献，因为它们和$S_L$（或$S_R$）中的所有节点相邻，所以有资格加入$S_L$（或$S_R$）。

同理，满足$|\overline{N}(u_i,C_L^i)|\le k-|\overline{N}(u_i,S)|$（$1\le i\le |S_L|$）的$\Pi_i(S_L,C_L)$也有资格加入，因为它们与$S_L$间缺失的边数更少。

基于上述观察，可以考虑将$S,C$划分为缺失边更多的一组（$S_L,C_L$）和缺失边更少的一组（$S_R,C_R$）。具体实施方面，从$S$开始将比值$\dfrac{|\overline{N}(v,C)|}{k-\overline{N}(v,S)}$最大的结点加入$S_L$并移出$S$，直至剩余的所有节点比值都小于1，或$S$为空。$S$中剩余结点统一归入$S_R$。$C$中则同步加入$S$中对应节点的非邻居。

![[Pasted image 20250803081506.png]]

这样划分的好处：
- `ComputeUB(S_L, C_L)`会返回一个更紧的上界：因为$S_L$任意节点$v$都满足$\overline{N}(v,C)>k-\overline{N}(v,S)$，所以加入它们都有可能破坏k-plex
- `ComputeUB(S_R, C_R)`始终等于$|C_R|$，因为$C_R$所有节点均有资格加入$S_R$

不难证明AltRB计算出的上界比单独应用SeqRB计算的上界更紧

*贪心划分与随机划分相比的优点*：
- $C_L$的缺失边更多，上界更紧（$UB_L$更小），使得$LB_R$更大，从而使归约规则RR1更有效
- $UB_R=|C_R|$始终成立，意味着只要$UB_L+UB_R+|S|=|S^*|+1$，RR2便可生效；同时计算成本更低

#### 时间复杂度分析

![[Pasted image 20250707172933.png]]

回顾上述算法代码：
- 首先调用Partition进行子集划分
- 执行r若干轮归约-定界流程
- 合并结果并返回

其中，Partition算法中的节点选择流程最多进行$|S|$轮，每轮需要为$v\in S$计算$|\overline{N}(v,C)|$，一轮时间成本为$O(|S|\times |C|)$。因此Partition算法的时间复杂度为$O(|S|^2|C|)$。

归约-定界计算（AltRB的第3-7行）包含两次上界计算、两次下界计算和两次归约。上界计算的时间复杂度是$O(|S|^2C)$；RR1迭代移除$|N(v,S\cup C_{L/R})|$最小的$v\in C_{R/L}$，RR2则检查$S\cup C_R$是否为k-plex，时间复杂度均为$O(|C|\times (|S|+|C|))$。

注意到$|S|\le \delta(G)+k$（$\delta(G)$为图退化度）；$|C|\le \delta(G)\cdot d$（kPEX框架中，$V(g)$由$v$的二跳内邻居子图构成，其规模受制于最大度数和退化度）。

设AltRB中归约-定界的迭代轮数为$r$。$r$在实践中很小，多数情况下一轮即可收敛（论文指出期望为1.13），且必定小于$|C|$（因为每轮必定排除至少一个节点）。

因此AltRB的时间复杂度为：
$$
\begin{split}
T_{\text{AltRB}}(G,k,d)&=T_{\text{Partition}}(G,k,d)+T_{\text{RB}}(G,k,d)\\
&=O(|S|^2|C|)+O(r\times (|S|\times |C|+|C|^2)) \\
&=O((\delta+k)^2 \delta d)+O(\delta d\cdot ((\delta+k)\delta d+\delta^2 d^2))\\
&= O(\delta^3 d+2k\delta^2d+k^2\delta d)+O()
\end{split}
$$

![[Pasted image 20250806144727.png]]

上述例子基于：$S=\{v_1,v_2\}$，$C=\{v_3,v_4,v_5,v_6,v_7,v_8\}$，$k=2$，$|S^*|=5$。

*第一轮*：
- 计算$C_L$上界$UB_L$：

WIP

## Fast Enumeration of Large k-Plexes

基本思想：
- 