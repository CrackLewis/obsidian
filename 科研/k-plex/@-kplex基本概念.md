
## 图论基本概念

（*普通图*）无向图，无边权和点权，记作$G=(V,E)$或$G=(V_G,E_G)$。$V_G=V(G)$为*顶点集*/*结点集*，$E_G=E(G)$为*边集*。

（*度数*）普通图$G$中一个顶点$v\in V_G$的邻居数，记作$\deg_G(v)$。

（*邻居集合*）普通图中一个顶点$v\in V_G$的所有邻居结点组成的集合：
$$
N_G(v)=\{u\mid (u,v)\in E_G\}
$$

（*支撑数*，support）普通图$G$中一条边$(u,v)\in E_G$所在的三角形数目，记作$\Delta(u,v)$。支撑数等于两端点邻居集合的交集规模：
$$
\Delta(u,v)=N_G(u)\cap N_G(v)
$$

（*$k$-core*）普通图$G$的一个子集$S\subseteq V_G$，满足$\forall v\in S\Rightarrow \deg_S(v)\ge k$。

（*$k$-truss*）普通图$G$的一个子集$S\subseteq V_G$，满足其导出子图$G'=G[S]$的每一条边$(u,v)\in E_{G'}$都包含于不少于$k-2$个三角形中，三角形是图中长度为3的环。即：
$$
\forall (u,v)\in E_{G'}\Rightarrow \Delta(u,v)\ge k-2
$$
- 有的资料称$\Delta\ge k$即为$k$-truss，这种情况下$k\ge 1$，否则$k\ge 3$。

（*$k$-团*，$k$-clique）普通图$G$的一个子集$S\subseteq V_G$，其为完全图，即$\forall u,v\in V_G\Rightarrow (u,v)\in E_G$。

（*退化度*，degeneracy；*核数*，core number）普通图$G$中最大$k$-core的规模，记作$\delta(G)$。

（*团数*）普通图$G$中最大$k$-团的规模，记作$\omega(G)$。

## k-plex基本概念

（*$k$-plex*）普通图$G$的一个子集$S\subseteq V_G$，其中每个结点在$S$内拥有至多$k$个非邻居（包含自己），即：
$$
\forall v\in S\Rightarrow \deg_{S}(v)\ge |S|-k
$$

## k-core性质

（包含性质）

## !prompt

```
假如你是一个图论方面的计算机科学学者，专门研究普通图上最大k-plex的求解问题，即Maximum k-Plex Problem（MKPP）。你知道目前的主流思路是：先通过启发式算法获得一个初始k-plex，然后根据该初始k-plex的规模对图进行归约，去除明显不符合core约束的顶点和不符合truss约束的边，最后在剩余图中执行分支限界算法，其中不同的分支限界算法会涉及不同的分支规则、归约规则和基于不同规模上界的剪枝规则。

现在你需要快速阅读一篇该方向相关的论文，并提取其中的核心观点、引理（Lemma）、定理（Theorem）、推论（Corollary）、重要算法和重要理论，整理为一个列表并以标准中文形式准确、流畅、通俗易懂地输出。

### 列表项格式（JSON，//后内容仅供参考，不输出；问号请替换为实际内容）
{
	"id": "???", // 根据在文章中的出现次序编号，起始为1
	"type": "???", // 表示类型，lemma/theorem/corollary/mainidea/algorithm/etcetera
	"content": "???????????"
}

### 注意事项

1. 请不要输出其他的无关信息，包括但不限于提示性文本等。
2. 你可以假设阅读你输出的用户理解并掌握了普通图的基本概念和k-core、k-truss、k-plex、k-clique的概念，并具有一定的计算机科学和编程基础。
3. 整个列表包裹在一个大JSON数组中，每个项之间用一个英文逗号隔开。整个输出需要包裹在代码块中。输出格式为每级缩进两格。

### 你的输出：
```