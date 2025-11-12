
研究MKPP的首篇论文，首次形式化定义MKPP，并提出整数规划方法

k-plex是NP完全问题

## 基本问题

设普通图$G=(V_G,E_G)$的每个结点$v_i\in V_G$各对应一个离散变量$x_i\in \{0,1\}$，其中$1\le i\le |V_G|$。则MKPP可转化为如下整数线性规划问题：
$$
\begin{split}
\omega_k(G)&=\max \sum_{v_i\in V_G} x_i \\
s.t.\quad \sum_{j\in V-N_G(v_i)} x_j&\le (k-1)x_i + \overline{d_i}(1-x_i), \quad \forall 1\le i\le |V_G|, \\
x_i&\in \{0,1\}, \quad \forall 1\le i\le |V_G|.
\end{split}
$$

(*co-k-plex*) 补图上$S$是一个$k$-plex，在原图上$S$就是一个co-$k$-plex，任意结点$v\in S$满足：
$$
\deg_{G[S]}(v)\le k-1
$$

## 实用结论

(*图中clique/club/plex的规模关系*) 设$\omega,\omega_k,\overline{\omega}_k,\tilde{\omega}_k$分别为：最大团规模、最大$k$-plex规模、最大$k$-club规模、最大$k$-clique规模。
$$
\omega(G)\le \omega_k(G)\le \overline{\omega}_k(G)\le \tilde{\omega}_k(G)
$$

(*独立集不等式*) 对独立集$I\subseteq V_G$，其内结点$v_i\in I$满足：
$$
\sum_{v_i\in I} x_i\le k,\quad \forall I\in \mathcal I_{k+1}.
$$

(*环不等式*) 对于一个长度不低于$k+3$的无重复环路$H\subseteq V_G$，其不可能是一个$k$-plex，且其满足