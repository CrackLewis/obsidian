
## 2D transforms

### scale

uniform scale:
$$
\left(\begin{matrix}x' \\ y'\end{matrix}\right)=\left(\begin{matrix}s & 0 \\ 0 & s\end{matrix}\right)\left(\begin{matrix}x \\ y\end{matrix}\right)
$$
(s=0.5)
![[Pasted image 20231225172616.png]]

non-uniform scale:
$$
\left(\begin{matrix}x' \\ y'\end{matrix}\right)=\left(\begin{matrix}s_x & 0 \\ 0 & s_y\end{matrix}\right)\left(\begin{matrix}x \\ y\end{matrix}\right)
$$
(s_x=0.5,s_y=1.0)
![[Pasted image 20231225172644.png]]
### reflection

horizontal reflection:
$$
\left(\begin{matrix}x' \\ y'\end{matrix}\right)=\left(\begin{matrix}-1 & 0 \\ 0 & 1\end{matrix}\right)\left(\begin{matrix}x \\ y\end{matrix}\right)
$$
vertical reflection:
$$
\left(\begin{matrix}x' \\ y'\end{matrix}\right)=\left(\begin{matrix}1 & 0 \\ 0 & -1\end{matrix}\right)\left(\begin{matrix}x \\ y\end{matrix}\right)
$$

### shear

$$
\left(\begin{matrix}x' \\ y'\end{matrix}\right)=\left(\begin{matrix}1 & a \\ 0 & 1\end{matrix}\right)\left(\begin{matrix}x \\ y\end{matrix}\right)
$$
(this will shift the horizontal elements by the ratio of a)
![[Pasted image 20231225173009.png]]

### rotate

rotate the figure about the origin $(0,0)$ by $\theta$:
$$
\left(\begin{matrix}x' \\ y'\end{matrix}\right)=\left(\begin{matrix}\cos\theta & -\sin\theta \\ \sin\theta & \cos\theta\end{matrix}\right)\left(\begin{matrix}x \\ y\end{matrix}\right)
$$

![[Pasted image 20231225173127.png]]

## homogeneous coordinates（齐次坐标）

abbreviated to **HmCo** if not specified.

### translation（平移）

translation:
$$
\left(\begin{matrix}x' \\ y'\end{matrix}\right)=\left(\begin{matrix}1 & 0\\ 0 & 1\end{matrix}\right)\left(\begin{matrix}x \\ y\end{matrix}\right)+\left(\begin{matrix}t_x \\ t_y\end{matrix}\right)
$$

Note that translation is NOT a legal linear transform, since it cannot be represented by finite matrix forms.

The homogeneous coordinates is then introduced to **unify translation and transforms**.

### solution

add a third coordinate (w-coordinate):
- 2D point is $(x,y,1)^T$
- 2D vector is $(x,y,0)^T$

the translation of 2D points will be:
$$
\left(\begin{matrix}x' \\ y' \\ w'\end{matrix}\right)=\left(\begin{matrix}1 & 0 & t_x\\ 0 & 1 & t_y\\ 0 & 0 & 1\end{matrix}\right)\left(\begin{matrix}x \\ y \\ 1\end{matrix}\right)=\left(\begin{matrix}x+t_x \\ y+t_y \\ 1\end{matrix}\right)
$$
the translation of 2D vectors will not cause any effect:
$$
\left(\begin{matrix}x' \\ y' \\ w'\end{matrix}\right)=\left(\begin{matrix}1 & 0 & t_x\\ 0 & 1 & t_y\\ 0 & 0 & 1\end{matrix}\right)\left(\begin{matrix}x \\ y \\ 0\end{matrix}\right)=\left(\begin{matrix}x \\ y \\ 0\end{matrix}\right)
$$

### validity of operations

valid operations if w'=0 or 1:
- vector+vector=vector (w'=0)
- vector+point=point (w'=1)
- point+point=?

In HmCo: $(x,y,w)=(x/w,y/w,1)$.

### affine transformations（仿射变换）

affine map = linear map + translation:
$$
\left(\begin{matrix}x' \\ y'\end{matrix}\right)=\left(\begin{matrix}a & b\\ c & d\end{matrix}\right)\left(\begin{matrix}x \\ y\end{matrix}\right)+\left(\begin{matrix}t_x \\ t_y\end{matrix}\right)
$$

using HmCo:
$$
\left(\begin{matrix}x' \\ y' \\ 1\end{matrix}\right)=\left(\begin{matrix}a & b & t_x\\ c & d & t_y\\ 0 & 0 & 1\end{matrix}\right)\left(\begin{matrix}x \\ y \\ 1\end{matrix}\right)
$$

### 2D transformations in HmCo

scale:
$$
S(s_x,s_y)=\left(\begin{matrix}s_x & 0 & 0 \\ 0 & s_y & 0 \\ 0 & 0 & 1\end{matrix}\right)
$$
rotation:
$$
R(\alpha)=\left(\begin{matrix}\cos\alpha & -\sin\alpha & 0 \\ \sin\alpha & \cos\alpha & 0 \\ 0 & 0 & 1\end{matrix}\right)
$$
translation:
$$
T(t_x,t_y)=\left(\begin{matrix}1 & 0 & t_x\\ 0 & 1 & t_y\\ 0 & 0 & 1\end{matrix}\right)
$$

## inverse transform

$$
x=My\Rightarrow y=M^{-1}x
$$

## composing transforms

### composite transform

rotate by 45 deg and then translate by (1,0):
$$
x'=T_{(1,0)}R_{45}x
$$

![[Pasted image 20231225212503.png]]

transform ordering matters: $R_{45}T_{(1,0)}\neq T_{(1,0)}R_{45}$. 
- matrix multiplications are not commutative
- matrices are applied from right to left

composition of transforms are vital to performance:
$$
x'=A_n A_{n-1} \cdots A_3A_2A_1x\Rightarrow x'=Px
$$
- matrices are pre-multiplied to obtain a single transform matrix
- order of composition matters

## decomposing complex transforms

any transform can be decomposed into finite fundamental transforms.

the general method is to adjust the center by at most two translations and perform linear transforms between the two TrS.

e.g. rotate around a given point $C(x,y)$ by $\alpha$:
- translate center to origin: $T(-x,-y)$
- rotate by $\alpha$: $R(\alpha)$
- translate back: $T(x,y)$

$$
X'=T(x,y)\cdot R(\alpha)\cdot T(-x,-y)\cdot X
$$

![[Pasted image 20231225213454.png]]

## 3D transforms

$$
\left(\begin{matrix}x' \\ y' \\ z' \\ 1\end{matrix}\right)=\left(\begin{matrix}a & b & c & t_x\\ d & e & f & t_y\\ g & h & i & t_z\\ 0 & 0 & 0 & 1\end{matrix}\right)\left(\begin{matrix}x \\ y \\ z \\ 1\end{matrix}\right)
$$