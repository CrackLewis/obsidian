
## 字体

- 数学花体：
	- `\mathcal`：$\mathcal{MATHCAL},\mathcal{mathcal}$ 
	- （Fraktur字体）`\mathfrak`：$\mathfrak{MATHFRAK},\mathfrak{fraktur}$ 
	- （Blackboard字体）`\mathbb`：$\mathbb{MATHBLACKBOARD}$
- 粗体：
	- `\textbf`：$\textbf{boldfont0123}$ 
	- `\mathbf`：$\mathbf{boldfont\alpha\beta\gamma+-*/\times0123}$ 
- 斜体：
	- `\textit`：$\textit{italicfont}$
	- `\mathit`：$\mathit{mathitalic}$
- 正体：
	- `\textrm`：$\textrm{textroman}$ 
	- `\mathrm`：$\mathrm{mathroman}$
- slanted：（md不支持）
	- `\textsl`：$\textsl{slanted}$ 
- 其他：
	- `\textup`：$\textup{upright}$
	- （md不支持）`\emph`：$\emph{cos}$
	- （Typewriter）`\texttt`：$\texttt{Typewriter}$
	- （md不支持）`\textsc`：$\textsc{Small Caps}$ 

## 分隔符与连字符

- 间隙微调：
	- `\,`：$a\,b$（3mu=0.167em）
	- `\:`：$a\:b$（4mu=0.222em）
	- `\;`：$a\;b$（5mu=0.278em）
- 连字符：
	- `\!`：$a\!b$
- 大间隙：
	- `\quad`：$a\quad b$ （18mu=1em）
	- `\qquad`：$a\qquad b$（36mu=2em）

## 运算符

|     符号      |      宏      |       符号        |        宏        |          符号          |          宏           |         符号         |         宏          |
| :---------: | :---------: | :-------------: | :-------------: | :------------------: | :------------------: | :----------------: | :----------------: |
|    $\pm$    |    `\pm`    |     $\cap$      |     `\cap`      |        $\cup$        |        `\cup`        |      $\cdot$       |      `\cdot`       |
|    $\mp$    |    `\mp`    |     $\Cap$      |     `\Cap`      |        $\Cup$        |        `\Cup`        |      $\uplus$      |      `\uplus`      |
|  $\times$   |  `\times`   |    $\sqcap$     |    `\sqcap`     |       $\sqcup$       |       `\sqcup`       |    $\bigsqcup$     |    `\bigsqcup`     |
|   $\ast$    |   `\ast`    |    $\wedge$     |    `\wedge`     |        $\vee$        |        `\vee`        |  $\bigtriangleup$  |  `\bigtriangleup`  |
|   $\div$    |   `\div`    |   $\barwedge$   |   `\barwedge`   |      $\veebar$       |      `\veebar`       | $\bigtriangledown$ | `\bigtriangledown` |
| $\setminus$ | `\setminus` | $\triangleleft$ | `\triangleleft` |   $\triangleright$   |   `\triangleright`   |      $\star$       |      `\star`       |
| $\dotplus$  | `\dotplus`  |   $\lozenge$    |   `\lozenge`    |   $\blacklozenge$    |   `\blacklozenge`    |     $\bigstar$     |     `\bigstar`     |
|  $\amalg$   |  `\amalg`   |     $\circ$     |     `\circ`     |      $\bullet$       |      `\bullet`       |     $\bigcirc$     |     `\bigcirc`     |
|  $\dagger$  |  `\dagger`  |    $\square$    |    `\square`    |    $\blacksquare$    |    `\blacksquare`    |    $\bigoplus$     |    `\bigoplus`     |
| $\ddagger$  | `\ddagger`  |   $\triangle$   |   `\triangle`   |   $\blacktriangle$   |   `\blacktriangle`   |    $\bigotimes$    |    `\bigotimes`    |
|    $\wr$    |    `\wr`    | $\triangledown$ | `\triangledown` | $\blacktriangledown$ | `\blacktriangledown` |     $\bigodot$     |     `\bigodot`     |
| $\diamond$  | `\diamond`  |    $\ominus$    |    `\ominus`    |       $\oplus$       |       `\oplus`       |   $\circledcirc$   |   `\circledcirc`   |
|  $\oslash$  |  `\oslash`  |    $\otimes$    |    `\otimes`    |    $\circledast$     |    `\circledast`     |   $\circleddash$   |   `\circleddash`   |
|   $\odot$   |   `\odot`   |                 |                 |                      |                      |                    |                    |

## 逻辑、集合、几何

| 符号 | 宏 | 符号 | 宏 | 符号 | 宏 | 符号 | 宏 |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| $\therefore$ | `\therefore` | $\partial$ | `\partial` | $\mathbb{P}$ | `\mathbb{P}` | $\measuredangle$ | `\measuredangle` |
| $\because$ | `\because` | $\imath$ | `\imath` | $\mathbb{N}$ | `\mathbb{N}` | $\sphericalangle$ | `\sphericalangle` |
| $\cdots$ | `\cdots` | $\jmath$ | `\jmath` | $\mathbb{Z}$ | `\mathbb{Z}` | $\varnothing$ | `\varnothing` |
| $\ddots$ | `\ddots` | $\Re$ | `\Re` | $\mathbb{I}$ | `\mathbb{I}` | $\infty$ | `\infty` |
| $\vdots$ | `\vdots` | $\Im$ | `\Im` | $\mathbb{Q}$ | `\mathbb{Q}` | $\mho$ | `\mho` |
| $\S$ | `\S` | $\forall$ | `\forall` | $\mathbb{R}$ | `\mathbb{R}` | $\wp$ | `\wp` |
| $\P$ | `\P` | $\exists$ | `\exists` | $\mathbb{C}$ | `\mathbb{C}` | $\copyright$ | `\copyright` |
| $\top$ | `\top` | $\angle$ | `\angle` | | | | |

## 货币、部分非英语符号

（大部分符号不被MathJax/KaTeX支持）

|   符号    |    宏    |   符号    |    宏    |  符号   |   宏   |    符号     |     宏     |
| :-----: | :-----: | :-----: | :-----: | :---: | :---: | :-------: | :-------: |
|  $\ae$  |  `\ae`  |  $\AE$  |  `\AE`  | $\l$  | `\l`  |   $\L$    |   `\L`    |
|  $\o$   |  `\o`   |  $\O$   |  `\O`   | $\oe$ | `\oe` |   $\OE$   |   `\OE`   |
|  $\ss$  |  `\ss`  |  $\SS$  |  `\SS`  | $\$$  | `\$`  | $\pounds$ | `\pounds` |
| $\cent$ | `\cent` | $\euro$ | `\euro` | $\AA$ | `\AA` |           |           |

## 元素归属、集合包含关系

| 符号 | 宏 | 符号 | 宏 | 符号 | 宏 | 符号 | 宏 |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| $\sqsubset$ | `\sqsubset` | $\sqsupset$ | `\sqsupset` | $\sqsubseteq$ | `\sqsubseteq` | $\sqsupseteq$ | `\sqsupseteq` |
| $\subset$ | `\subset` | $\supset$ | `\supset` | $\subseteq$ | `\subseteq` | $\supseteq$ | `\supseteq` |
| $\nsubseteq$ | `\nsubseteq` | $\nsupseteq$ | `\nsupseteq` | $\subseteqq$ | `\subseteqq` | $\supseteqq$ | `\supseteqq` |
| $\nsubseteq$ | `\nsubseteq` | $\nsupseteqq$ | `\nsupseteqq` | $\in$ | `\in` | $\ni$ | `\ni` |
| $\notin$ | `\notin` | | | | | | |

## 上标和角标

| 符号 | 宏 | 符号 | 宏 | 符号 | 宏 | 符号 | 宏 |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| $a'$ | `a'` | $a''$ | `a''` | $\dot{a}$ | `\dot{a}` | $\ddot{a}$ | `\ddot{a}` |
| $\hat{a}$ | `\hat{a}` | $\check{a}$ | `\check{a}` | $\grave{a}$ | `\grave{a}` | $\acute{a}$ | `\acute{a}` |
| $\tilde{a}$ | `\tilde{a}` | $\breve{a}$ | `\breve{a}` | $\bar{a}$ | `\bar{a}` | $\vec{a}$ | `\vec{a}` |
| $\not{a}$ | `\not{a}` | $a^{\circ}$ | `a^{\circ}` | | | | |

## 上划线、下划线、上下标注

|           符号           |           宏            |         符号          |          宏          |
| :--------------------: | :--------------------: | :-----------------: | :-----------------: |
|   $\widetilde{abc}$    |   `\widetilde{abc}`    |  $\underline{abc}$  |  `\underline{abc}`  |
|    $\widehat{abc}$     |    `\widehat{abc}`     |  $\overbrace{abc}$  |  `\overbrace{abc}`  |
| $\overleftarrow{abc}$  | `\overleftarrow{abc}`  | $\underbrace{abc}$  | `\underbrace{abc}`  |
| $\overrightarrow{abc}$ | `\overrightarrow{abc}` | $\overset{a}{abc}$  | `\overset{a}{abc}`  |
|    $\overline{abc}$    |    `\overline{abc}`    | $\underset{a}{abc}$ | `\underset{a}{abc}` |

## 箭头

| 符号 | 宏 | 符号 | 宏 |
|:---:|:---:|:---:|:---:|
| $\mapsto$ | `\mapsto` | $\to$ | `\to` |
| $\leftarrow$ | `\leftarrow` | $\rightarrow$ | `\rightarrow` |
| $\Leftarrow$ | `\Leftarrow` | $\Rightarrow$ | `\Rightarrow` |
| $\leftrightarrow$ | `\leftrightarrow` | $\Leftrightarrow$ | `\Leftrightarrow` |
| $\leftharpoonup$ | `\leftharpoonup` | $\rightharpoonup$ | `\rightharpoonup` |
| $\leftharpoondown$ | `\leftharpoondown` | $\rightharpoondown$ | `\rightharpoondown` |
| $\leftrightharpoons$ | `\leftrightharpoons` | $\rightleftharpoons$ | `\rightleftharpoons` |
| $\xleftarrow[text]{long}$ | `\xleftarrow[text]{long}` | $\xrightarrow[text]{long}$ | `\xrightarrow[text]{long}` |
| $\overset{a}{\leftarrow}$ | `\overset{a}{\leftarrow}` | $\overset{a}{\rightarrow}$ | `\overset{a}{\rightarrow}` |
| $\underset{a}{\leftarrow}$ | `\underset{a}{\leftarrow}` | $\underset{a}{\rightarrow}$ | `\underset{a}{\rightarrow}` |
| $\uparrow$ | `\uparrow` | $\downarrow$ | `\downarrow` |

## 关系运算符

| 符号 | 宏 | 符号 | 宏 | 符号 | 宏 |
|:---:|:---:|:---:|:---:|:---:|:---:|
| $<$ | `&lt;` | $>$ | `&gt;` | $=$ | `=` |
| $\leq$ | `\leq` | $\geq$ | `\geq` | $\doteq$ | `\doteq` |
| $\leqslant$ | `\leqslant` | $\geqslant$ | `\geqslant` | $\equiv$ | `\equiv` |
| $\nless$ | `\nless` | $\ngtr$ | `\ngtr` | $\neq$ | `\neq` |
| $\nleqslant$ | `\nleqslant` | $\ngeqslant$ | `\ngeqslant` | $\not\equiv$ | `\not\equiv` |
| $\prec$ | `\prec` | $\succ$ | `\succ` | $\overset{\underset{\mathrm{def}}{}}{=}$ | `\overset{\underset{\mathrm{def}}{}}{=}` |
| $\preceq$ | `\preceq` | $\succeq$ | `\succeq` | $\sim$ | `\sim` |
| $\ll$ | `\ll` | $\gg$ | `\gg` | $\approx$ | `\approx` |
| $\vdash$ | `\vdash` | $\dashv$ | `\dashv` | $\simeq$ | `\simeq` |
| $\smile$ | `\smile` | $\frown$ | `\frown` | $\cong$ | `\cong` |
| $\models$ | `\models` | $\perp$ | `\perp` | $\asymp$ | `\asymp` |
| $\mid$ | `\mid` | $\parallel$ | `\parallel` | $\propto$ | `\propto` |
| $\bowtie$ | `\bowtie` | $\Join$ | `\Join` | $\questeq$ | `\questeq` |

## 希腊字母

小写希腊字母：

|     符号     |     宏      |      符号       |       宏       |    符号    |    宏     |     符号     |     宏      |
| :--------: | :--------: | :-----------: | :-----------: | :------: | :------: | :--------: | :--------: |
|  $\alpha$  |  `\alpha`  |    $\beta$    |    `\beta`    | $\zeta$  | `\zeta`  |  $\kappa$  |  `\kappa`  |
| $\epsilon$ | `\epsilon` | $\varepsilon$ | `\varepsilon` | $\iota$  | `\iota`  |   $\xi$    |   `\xi`    |
|  $\theta$  |  `\theta`  |  $\vartheta$  |  `\vartheta`  |  $\nu$   |  `\nu`   | $\varrho$  | `\varrho`  |
| $\lambda$  | `\lambda`  |     $\mu$     |     `\mu`     |  $\rho$  |  `\rho`  | $\upsilon$ | `\upsilon` |
|   $\pi$    |   `\pi`    |   $\varpi$    |   `\varpi`    |  $\tau$  |  `\tau`  |   $\psi$   |   `\psi`   |
|  $\sigma$  |  `\sigma`  |  $\varsigma$  |  `\varsigma`  |  $\chi$  |  `\chi`  |   $\phi$   |   `\phi`   |
| $\varphi$  | `\varphi`  |   $\delta$    |   `\delta`    | $\omega$ | `\omega` |  $\gamma$  |  `\gamma`  |
|   $\eta$   |   `\eta`   |               |               |          |          |            |            |

大写希腊字母的情况略微复杂。有对应拉丁文字母的大写希腊字母没有对应的宏，需要用拉丁文字母表示。

|        符号        |     宏      |      符号       |       宏       |      符号       |    宏     |       符号       |     宏      |
| :--------------: | :--------: | :-----------: | :-----------: | :-----------: | :------: | :------------: | :--------: |
|  $\Alpha$ ($A$)  |  `\Alpha`  | $\Beta$($B$)  |    `\Beta`    | $\Zeta$ ($Z$) | `\Zeta`  | $\Kappa$ ($K$) |  `\Kappa`  |
| $\Epsilon$ ($E$) | `\Epsilon` | $\mathcal{E}$ | `\varEpsilon` | $\Iota$ ($I$) | `\Iota`  |     $\Xi$      |   `\Xi`    |
|     $\Theta$     |  `\Theta`  |  $\varTheta$  |  `\varTheta`  |  $\Nu$ ($N$)  |  `\Nu`   | $\mathcal{P}$  | `\varRho`  |
|    $\Lambda$     | `\Lambda`  |  $\Mu$($M$)   |     `\Mu`     | $\Rho$ ($R$)  |  `\Rho`  |   $\Upsilon$   | `\Upsilon` |
|      $\Pi$       |   `\Pi`    |   $\varPi$    |   `\varPi`    | $\Tau$ ($T$)  |  `\Tau`  |     $\Psi$     |   `\Psi`   |
|     $\Sigma$     |  `\Sigma`  |  $\varsigma$  |  `\varsigma`  | $\Chi$ ($X$)  |  `\Chi`  |     $\Phi$     |   `\Phi`   |
|    $\varPhi$     | `\varPhi`  |   $\Delta$    |   `\Delta`    |   $\Omega$    | `\Omega` |    $\Gamma$    |  `\Gamma`  |
|   $\Eta$ ($H$)   |   `\Eta`   |               |               |               |          |                |            |

## 大运算符

|                          符号                          |                         宏                          |
| :--------------------------------------------------: | :------------------------------------------------: |
|                       $$x^a$$                        |                       `x^a`                        |
|                       $$x_a$$                        |                       `x_a`                        |
|                      $$x_a^b$$                       |                      `x_a^b`                       |
|                     $${x_a}^b$$                      |                     `{x_a}^b`                      |
|                $$_{a}^{b}\textrm{C}$$                |                `_{a}^{b}\textrm{C}`                |
|                   $$\frac{a}{b}$$                    |                   `\frac{a}{b}`                    |
|                  $$x\tfrac{a}{b}$$                   |                  `x\tfrac{a}{b}`                   |
|           $$\frac{\partial }{\partial x}$$           |           `\frac{\partial }{\partial x}`           |
|         $$\frac{\partial^2 }{\partial x^2}$$         |         `\frac{\partial^2 }{\partial x^2}`         |
|         $$\frac{\mathrm{d} }{\mathrm{d} x}$$         |         `\frac{\mathrm{d} }{\mathrm{d} x}`         |
|                       $$\int$$                       |                       `\int`                       |
|                     $$\int_a^b$$                     |                     `\int_a^b`                     |
|                      $$\oint$$                       |                      `\oint`                       |
|                    $$\oint_a^b$$                     |                    `\oint_a^b`                     |
|                    $$\iint_a^b$$                     |                    `\iint_a^b`                     |
|                     $$\bigcap$$                      |                     `\bigcap`                      |
|                   $$\bigcap_a^b$$                    |                   `\bigcap_a^b`                    |
|                     $$\bigcup$$                      |                     `\bigcup`                      |
|                   $$\bigcup_a^b$$                    |                   `\bigcup_a^b`                    |
|           $$\displaystyle \lim_{x \to 0}$$           |           `\displaystyle \lim_{x \to 0}`           |
|                       $$\sum$$                       |                       `\sum`                       |
|                     $$\sum_a^b$$                     |                     `\sum_a^b`                     |
|                     $$\sqrt{x}$$                     |                     `\sqrt{x}`                     |
|                   $$\sqrt[n]{x}$$                    |                   `\sqrt[n]{x}`                    |
| $$\stackrel{n}{b\overline{\smash{)}\vphantom{b}a}}$$ | `\stackrel{n}{b\overline{\smash{)}\vphantom{b}a}}` |
|                      $$\prod$$                       |                      `\prod`                       |
|                    $$\prod_a^b$$                     |                    `\prod_a^b`                     |
|                     $$\coprod$$                      |                     `\coprod`                      |
|                   $$\coprod_a^b$$                    |                   `\coprod_a^b`                    |
|                                                      |                                                    |
## 大括号

所有的`\:`可以替换为实际的被包含内容

|                 符号                  |                    宏                    |
| :---------------------------------: | :-------------------------------------: |
|       $$\left (\: \right )$$        |          `\left (\: \right )`           |
|       $$\left\|\: \right\|$$        |          `\left\|\: \right\|`           |
|       $$\left [\: \right ]$$        |          `\left [\: \right ]`           |
|       $$\left < \: \right >$$       |          `\left < \: \right >`          |
|       $$\left\{\: \right\}$$        |          `\left\{\: \right\}`           |
| $$\left \lfloor \: \right \rfloor$$ |    `\left \lfloor \: \right \rfloor`    |
|         $$\lVert\:\rVert$$          | `\lVert \: \rVert `（竖线不用转义，这里是为了不让表格串列） |
|  $$\left \lceil \: \right \rceil$$  |     `\left \lceil \: \right \rceil`     |
|     $$\left \{ \cdots \right.$$     |        `\left \{ \cdots \right.`        |
|     $$\left. \cdots \right \}$$     |        `\left. \cdots \right }`         |

## 矩阵、多行公式、方程组

|                                  符号                                   |                                  宏                                  |
| :-------------------------------------------------------------------: | :-----------------------------------------------------------------: |
|            $$\begin{matrix}\cdots\\ \cdots \end{matrix}$$             |            `\begin{matrix}\cdots\\ \cdots \end{matrix}`             |
|            $$\begin{bmatrix}\cdots\\ \cdots\end{bmatrix}$$            |            `\begin{bmatrix}\cdots\\ \cdots\end{bmatrix}`            |
|                           $$\binom{n}{r}$$                            |                           `\binom{n}{r}`                            |
|            $$\begin{pmatrix}\cdots\\ \cdots\end{pmatrix}$$            |            `\begin{pmatrix}\cdots\\ \cdots\end{pmatrix}`            |
| $$\bigl(\begin{smallmatrix}\cdots\\ \cdots \end{smallmatrix}\bigr)$$  | `\bigl(\begin{smallmatrix}\cdots\\ \cdots \end{smallmatrix}\bigr)`  |
|         $$\begin{cases} \cdots, x=\\ \cdots, x= \end{cases}$$         |         `\begin{cases} \cdots, x=\\ \cdots, x= \end{cases}`         |
|            $$\begin{vmatrix}\cdots\\ \cdots\end{vmatrix}$$            |            `\begin{vmatrix}\cdots\\ \cdots\end{vmatrix}`            |
|            $$\begin{Bmatrix}\cdots\\ \cdots\end{Bmatrix}$$            |            `\begin{Bmatrix}\cdots\\ \cdots\end{Bmatrix}`            |
|          $$\begin{align*}y&=\cdots\\ &+\cdots \end{align*}$$          |          `\begin{align*}y&=\cdots\\ &+\cdots \end{align*}`          |
|            $$\begin{Vmatrix}\cdots\\ \cdots\end{Vmatrix}$$            |            `\begin{Vmatrix}\cdots\\ \cdots\end{Vmatrix}`            |
|      $$\left\{\begin{matrix}\cdots\\ \cdots\end{matrix}\right.$$      |      `\left\{\begin{matrix}\cdots\\ \cdots\end{matrix}\right.`      |
| $$\begin{align*}\cdots\\[-1ex] \cdots \\ \hline \cdots \end{align*}$$ | `\begin{align*}\cdots\\[-1ex] \cdots \\ \hline \cdots \end{align*}` |
|      $$\left.\begin{matrix}\cdots\\ \cdots\end{matrix}\right\|$$      |      `\left.\begin{matrix}\cdots\\ \cdots\end{matrix}\right\|`      |
|      $$\left.\begin{matrix}\cdots\\ \cdots\end{matrix}\right\}$$      |      `\left.\begin{matrix}\cdots\\ \cdots\end{matrix}\right\}`      |
|                                                                       |                                                                     |



## 其他公式

