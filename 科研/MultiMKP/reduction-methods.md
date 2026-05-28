
$$
I=(g,k,S,C,P,v^*)
$$

define:
- $N_A(v)=N_g(v)\cap A$: $v$'s neighbor set in $A$
- $\deg_A(v)=|N_A(v)|$: $v$'s neighbor count in $A$
- $\delta_A(v)=k-|A\backslash N_A(v)|$: how many non-neighbors of $v$ can be added to $A$ without violating plex condition
- $\text{loss}_A(v)=|A\backslash N_A(v)|$: how many neighbors $v$ is missing in $A$

## degree-based

consider $v\in C$, we can remove $v$ from $C$ if:
- $\deg_S(v)\le |S|-k$
- any $u\in S$ s.t. $(u,v)\not\in E_g$ and $\deg_S(u)=|S|-k$
- $\deg_{S\cup C}(v)\le |P|-k$

## pair-based

kPlexS, kPlexT, U-MkP UBR1

## other

U-MkP UBR2

AltRB

