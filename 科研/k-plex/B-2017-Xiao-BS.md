
repo: [link](https://github.com/Lweb/KPLEX)

novelties:
- constrained MKPP: given $F$, return a maximum $k$-plex that contains $F$
- diameter property (prop3)
- F-reducible and D-reducible
- exchanging-related branching rules

## MKPP complexities by k

branching factor upperbound

![[Pasted image 20251119153319.png]]

## lemma(s)

lemma 1-3 are trivial

considering instance $(G=(V,E),k,F)$, denoting $U=V-F$

($F$-*constrained*) a k-plex $S$ is F-constrained iff $F\subseteq S$

(*$F$-reducible*) at least one maximum $F$-constrained $k$-plex contains $v$

(*$D$-reducible*) no maximum $F$-constrained $k$-plex contains $v$

(*Lemma 4*) if $v\in U$ and all non-neighbors of $v$ in $G$ satisfies that $\deg_G(\cdot)\ge |V|-k$, then $v$ is F-reducible

(*exchangeable*) we say $v$ is exchangeable with $u$ iff the maximum k-plex $S$ contains $v$, and $S-\{v\}\cup \{u\}$ is also a k-plex

(*Lemma 5*) assume $v$ is exchangeable with $u$. there is a sol'n either:
- containing $u,v$
- or containing $u$ but not $v$

(*dominate*) $u$ dominates $v$ iff $v$'s neighbors are $u$ or $u$'s neighbors

(*Lemma 6*) if $u$ dominates $v$, then $u,v$ are exchangeable

lemma 7 is deg'-based, lemma 8 is distance-based

## branching rules

instance $(G=(V,E),F)$

notations:
- candidate sets: $U=V\backslash F$.
- maximum leaves in search tree of $(G,F)$ with $|U|\le n_0$: $C(n_0)$
- *branching factor*: suppose the $i$-th branch decreases $U$ by at least $a_i$ vertices, and branch count is $l$. the largest root of $f(x)=1-\sum_{i=1}^l x^{-a_i}$, denoted by $1<\gamma\le 2$ is the branching factor

recurr' relation of $C(n_0)$:
$$
C(n_0)\le \sum_{i=1}^l C(n_0-a_i)
$$
the total complexity is $C(n_0)=O(\gamma^{n_0})$.

(*BR1*: on dominated vtx's) if there're $u,v\in U$ such that $v$ is dominated by $u$, then we consider two branches for $u,v$ based on Lemma 5,6:
- include both: $(G,F\cup \{u,v\})$
- delete $v$: $(G\backslash \{v\},F)$

the recurr' rel' is: $C(n_0)\le C(n_0-2)+C(n_0-1)$, the branching factor is $\gamma_1=1.6181$.

(*BR2*: on $F$-vtx's) consider one of $k$-unsatisfied vtx's $v\in F$, i.e.:
$$
|\overline{N_G}(v)|=|V|-\deg_G(v)\ge k+1
$$