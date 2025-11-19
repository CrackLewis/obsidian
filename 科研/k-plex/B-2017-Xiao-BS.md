
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

(*$F$-reducible*) at least one maximum $F$-constrained $k$-plex contains $v$

(*$D$-reducible*) no maximum $F$-constrained $k$-plex contains $v$

(*Lemma 4*) if $v\in U$ and all non-neighbors of $v$ in $G$ satisfies that $\deg_G(\cdot)\ge |V|-k$, then $v$ is F-reducible

(*exchangeable*) we say $u,v$ are exchangeable iff the maximum k-plex $S$ contains $v$, and $S-\{v\}\cup \{u\}$ is also a k-plex

(*Lemma 5*) assume $u,v$ are exchangeable. there is a sol'n either:
- containing $u,v$
- or containing $u$ but not $v$

(*dominate*) $u$ dominates $v$ iff $v$'s neighbors are $u$ or $u$'s neighbors

(*Lemma 6*) if $u$ dominates $v$, then $u,v$ are exchangeable

lemma 7 is deg'-based, lemma 8 is distance-based

## branching rules

