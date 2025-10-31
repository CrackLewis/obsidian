
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

## k-core性质

（包含性质）