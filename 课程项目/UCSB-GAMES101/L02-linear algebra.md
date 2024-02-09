
## vectors

magnitude（模）

unit vector ($\hat{a}$) : vectors whose magnitude is 1

vector normalization: finding the unit vector of a vector

vector addition:
- geometrically: parallelogram law & triangle law
- algebraically: simply and coordinates

cartesian coordinates（笛卡尔坐标系）:
- a representation method of vectors by a series of orthogonal vectors（正交向量）
- e.g. $A=\displaystyle\left(\begin{matrix}x\\ y\end{matrix}\right)$, $A^T=(x,y)$, $||A||=\sqrt{x^2+y^2}$. 

**vector multiplication**:
- dot (scalar) product: $\overset{\rightarrow}{a}\cdot \overset{\rightarrow}{b}=||\overset{\rightarrow}{a}||\ ||\overset{\rightarrow}{b}||\cos\theta$ .
	- in CarCo 2D: $(x_a,y_a)\cdot (x_b,y_b)=x_a x_b+y_a y_b$
	- for Prj: $\overset{\rightarrow}{b}_{\perp}=\dfrac{\overset{\rightarrow}{a}\cdot \overset{\rightarrow}{b}}{||\overset{\rightarrow}{a}||} \hat{a}$
	- usage: 
		- find angle between two vectors
		- finding projection of one vector on another
		- decompose vectors
		- determine forward & backward
		- measure how close two directions are
- cross (vector) product
	- properties: fig below
	- in CarCo 3D: fig below
	- usage:
		- determine left & right, inside & outside

![[Pasted image 20231225170104.png]]

![[Pasted image 20231225170112.png]]

orthonormal bases（标准正交基） & coordinate frames（坐标系）:
- IMPORTANT
- the critical issue is transforming between those systems & bases
- orthonormal coordinate frames（正交坐标系）: any set of 3 orthogonal vectors in 3D which satisfy:
	- all vectors have a magnitude of 1
	- right-handed property: $w=u\times v$.
	- projection property: $p=(p\cdot u)u+(p\cdot v)v+(p\cdot w)w$. 

## matrices

- 2D arrays
- **in graphics**, pervasively used to represent **transformations**（变换）

what is a matrix:
- an array with $m$ rows, $n$ columns of numbers

**matrix-matrix multiplication**:
- `(MxN)(NxP)=(MxP)`
- properties:
	- non-commutative（非交换的）: $AB\neq BA$
	- associative & distributive: $(AB)C=A(BC), A(B+C)=AB+AC$

matrix-vector multiplication:
- treat vector as a column matrix ($m\times 1$)
- key for transforming points

transpose（转置） of a matrix:
- switch rows and columns
- property: $(AB)^T=B^T A^T$. 

identity matrix and inverses:
- identity matrix: $I_{3\times 3}$ or $E_3$. 
- inverse: $A A^{-1}=I$, $(AB)^{-1}=B^{-1} A^{-1}$.
