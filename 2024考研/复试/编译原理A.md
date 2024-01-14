
## outline

- 基本概念
- 词法分析
- 语法分析

## 基本概念

**形式语言**（formal language）：用精确的数学或机器可处理的公式定义的语言。与自然语言相对。
- 字母表：语言包含的所有基本字母的集合。
- 符号：字母表中的元素。
- 符号串：零或多个字母组成的有序序列，无字母组成的称为空符号串（$\varepsilon$）。
	- 运算：连接积、闭包、正则闭包。

**语法**、**文法**（grammar）：字符串的一套产生式规则。
- 形式定义：文法$G=(N,\Sigma,P,S)$，$N$为非终结符集合，$\Sigma$为终结符集合，$P$为产生式规则集合，$S$为起始符号。
- 举例：$N=\{S,B\}$，$\Sigma=\{a,b,c\}$，$P=\{S\rightarrow aBSc,S\rightarrow abc, Ba\rightarrow aB,Bb\rightarrow bb\}$。此时文法$G$定义语言$L(G)=\{a^nb^nc^n|n\ge 1\}$。
- 与语言的关系：$G$定义唯一的$L(G)$，$L(G)$由至少一种文法定义。

文法的种类：
- 0型：无限制文法，定义递归可枚举语言，自动机形式为图灵机。
- 1型：**上下文有关文法**，定义上下文有关语言，自动机形式为线性有界自动机。
	- 产生式规则形式：两种形式等价。
		- 形式一：$\alpha A\beta\rightarrow \alpha\gamma\beta$，或$S\rightarrow \varepsilon$。
		- 形式二：$\alpha A\beta\rightarrow \alpha B\beta$（其中$|B|\le |A|$），或$S\rightarrow \varepsilon$。
- 2型：上下文无关文法（详见[[编译原理#^9582fd]]），定义上下文无关语言，自动机形式为下推自动机。
	- 产生式规则形式：$A\rightarrow  w$，其中$w\in (N\cup \Sigma)^*$。
- 3型：**正则文法**，定义正则语言，自动机形式为有穷自动机。
	- 产生式规则形式：$A\rightarrow a$，或$A\rightarrow aB$，或$C\rightarrow\varepsilon$。

高级语言的一般特性：
- 分类：强制式（imperative，C/Fortran/Pascal）、应用式（applicative，Lisp）、基于规则（rule-based，Prolog）、面向对象（object-oriented，C++/Java）
- 程序结构：程序>子程序>语句>表达式>数据引用、算符、函数调用
- 数据类型：
	- 初等数据类型：整型、实型、字符型等
	- 复合数据类型：数组、记录、字符串等
	- 抽象数据类型：类
	- 三要素：属性（类型+作用域）、值域（精度+范围）、操作
- 名字和标识符：标识符只是名字的表示符号，而名字有明确意义和属性、代表特定格式存储单元，是数据、函数、过程、类型的助记符。
- 语句和控制结构：
	- 表达式
	- 语句：简单语句（说明、赋值、控制、过程调用）、复合语句
- 动态和静态：允许编译器决定某个问题的策略称为静态策略，只允许运行时决定的策略称为动态策略。

**上下文无关文法**： ^9582fd
- 描述高级语言的**语法规则**
- 产生式（产生式规则）：定义语法单位的一种书写规则
- **推导**：从起始符号出发，反复连续使用产生式对非终结符进行替换展开。
	- 直接推出：$A\rightarrow \gamma\Rightarrow \alpha A\beta\rightarrow \alpha\gamma\beta$。
	- **最左推导**（最右推导）：推导中每一步都替换最左（最右）非终结符。
- 句型：从起始符号推导零或任意步得到的终结符与非终结符的组合
- 句式：不含非终结符的句型
- 语言：由文法推导出的所有合法句式的集合：$L(G)=\{\alpha|S\overset{+}{\Rightarrow} \alpha,\alpha\in V_T^*\}$。
- **语法分析树**：文法句型推导的树形表示，简称分析树。
- 文法的二义性：存在某个句子对应两棵不同的语法树。
	- 特点：文法二义不代表对应语言二义，只有产生该语言的所有文法二义时，该语言才二义；非二义语言的二义文法可改写为非二义文法；语法分析器可以设计消除二义性的规则

## 词法分析

### 词法分析任务

源程序的字符序列=>单词序列

单词属性：
- **单词种别**：语法分析阶段使用的抽象符号
	- 符号特征：关键字、标识符、常数、运算符、界符
	- 编码方案：标识符一种，常数一类一种，其他一字一种
- 属性值：单词的附加信息

接口设计的两类方案：
- 独立一遍：被总控程序调用，一次生成整个单词序列
- 子程序：供语法分析程序调用，调用一次识别一词

### 词法分析器的设计

组件：
- 输入缓冲区：送源程序
- 预处理子程序：剔除无关字符和语句，处理预处理命令
- 扫描缓冲区（历史遗留）：双指示器（起点指示器、搜索指示器），双区缓冲（分为两个等长半区，半区长度>=最长标识符长度-1）
- 扫描器

**状态转换图**：
- **正规文法**：用于描述高级语言的**词法规则**
- 含义：一张有限的方向图，表示利用正规文法识别单词符号的全过程
- 组成：
	- 结点：代表一个状态，分初态、中间态和终态
	- 转移：代表一个状态到另一个状态的转移，用一个字符表示

状态转移图的实现（参考）：
- 变量：ch（当前读入字符）、strToken（当前单词）
- 过程：GetChar（取字符）、GetBC（滤除空字符）、Concat（子程序过程）、IsLetter、IsDigit、Reserve（查保留字表，如是返回保留字号，否则返回0）、Retract（回退搜索指针）、InsertID（将标识符插入符号表，返回符号表指针）、InsertConst（将常数插入常数表，返回常数表指针）

### 正规表达式、有限自动机

目的：自动生成词法分析程序

**正规式**和**正规集**：
- 正规式和正规集定义：若$U,V$是正规式，则$\varepsilon,\varnothing,(U|V),(U\cdot V),(U)^*$都是正规式，它们的正规集分别是$\{\varepsilon\},\varnothing,L(U)\cup L(V),L(U)L(V),(L(U))^*$。
- 优先级：括号>星号>连接>并
- 正规式等价条件：正规集相同
- 运算规律：
	- 交换律、结合律、分配律
	- $\varepsilon U=U\varepsilon=U$，$U^*=(U|\varepsilon)^*$
	- 幂等律：$(a^*)^*=a^*$。

> [!example] 正规式和正规集举例
> 令$\Sigma=\{a,b,0,1\}$，则$\Sigma$上正规式$(a|b)(a|b)$对应的正规集有$L(a|b)(a|b)=\{aa,ab,ba,bb\}$，正规式$ba^*$对应的正规集有$L(ba^*)=\{b,ba,baa,baaa,\cdots\}$。

**确定有限自动机**（definite finite automaton，DFA）：
- 定义：五元组$M=(S,\Sigma,\delta,S_0,F)$，$S$是状态集，$\Sigma$是有穷字符表，$\delta$是$S\times \Sigma\rightarrow S$的转移表，$S_0\in S$是唯一初态，$F\subseteq S$是终态集。
- 表示方式：
	- 状态转移矩阵：$|S|$行$|\Sigma|$列
	- 状态转移图
- 接受（识别、读出）：对$\alpha\in \Sigma^*$，若存在一条从初态$S_0$到某一终态结点的通路，且通路上所有弧标记连接成的字为$\alpha$，则称$\alpha$可被DFA接受。DFA M接受的所有单词称为$L(M)$。

非确定有限自动机（non-definite finite automaton，NFA）：
- 定义：五元组$M=(S,\Sigma,\delta,S_0,F)$，$S$是状态集，$\Sigma$是有穷字符表，$\delta$是$S\times \Sigma^*\rightarrow 2^S$的*状态子集转移表*，$S_0\subseteq S$是*初态集*，$F\subseteq S$是终态集。
- 状态转换图：每条弧的标记可为一个串，每个结点的出弧数量也没有限制。
- 接受（识别、读出）：与DFA类似
- 有限自动机等价：$L(M)=L(M')\Rightarrow$ M,M'等价

正规式与有限自动机的等价性：
- 正规式与NFA等价：对$\Sigma$上任意NFA M，都存在一个正规式$V$，使得$L(V)=L(M)$。
	- 证明：先将初态、终态唯一化，再根据正规式规则不断合并NFA内结构，直至仅剩初态和终态。
- DFA与正规式等价：对$\Sigma$上任意正规式$V$，都有DFA M使得$L(M)=L(V)$。
	- 证明：根据正则式规则构造NFA M‘，使得$L(M')=L(V)$，再将NFA确定化为DFA（细节见下）。

非确定有限自动机的确定化：
- 定义：设$I$是$M'$状态集的子集，则：（详见下方定义举例）
	- $\varepsilon-\text{CLOSURE}(I)$：若$S\in I$，则$S\in \varepsilon-\text{CLOSURE}(I)$，且从$S$出发经过任意条$\varepsilon$弧可达的状态$S'$也满足$S'\in \varepsilon-\text{CLOSURE}(I)$，称作$I$的$\varepsilon-$闭包。
	- $I_a$：$I_a=\varepsilon-\text{CLOSURE}(J)$，其中$J$是从$I$中某一个状态结点出发，经过一条$a$弧到达的状态结点全体。（为下文方便叙述，称作$I$关于$a$的转移集）
- 步骤：（详见下方定义举例）
	- 预处理：把标记非空串、非单字符串的弧拆分，确保所有弧的标记要么为空串，要么为单字符串。另起结点$X,Y$，X用$\varepsilon$弧连接到所有初态，所有终态用$\varepsilon$弧连接到Y。
	- 构造状态转换矩阵：每行记录一个不同状态集，以及该状态集关于字母表各个字母的转移集。如果转移集没出现在已记录的状态集中，则将其抄写到新一行中（空集除外）。
	- 重定义状态：对状态转移矩阵中每个不同状态集标号，作为目标DFA的状态号。
	- 画出新的DFA：根据各个DFA状态号及其转移关系，画出DFA。含NFA结点X的为初态，含NFA结点Y的为终态。

> [!example] NFA确定化的有关定义举例
> ![[Pasted image 20240105131142.png]]
> 对于上图所示的状态转换图，设$I=\{1\}$，则$\varepsilon-\text{CLOSURE}(I)=\{1,2\}$，$I_a=\varepsilon-\text{CLOSURE}\{5,4,3\}=\{5,6,2,4,7,3,8\}$。

> [!example] NFA确定化过程举例
> 设$V=(a|b)^*(aa|bb)(a|b)^*$，构造DFA M使得$L(M)=L(V)$。
> 第一步，构造NFA并作相应的预处理。
> ![[Pasted image 20240105131511.png]]
> 第二步，通过子集法构造状态转移矩阵。
> ![[Pasted image 20240105131736.png]]
> 第三步，对状态子集重命名，得到新的状态转移矩阵。
> ![[Pasted image 20240105131818.png]]
> 第四步，画出状态转移图。
> ![[Pasted image 20240105131840.png]]

确定有限自动机的化简：
- 目的：对DFA M进行化简，指寻找一个状态数更少的DFA M'，使得$L(M')=L(M)$。
- 术语：
	- 状态s、t等价：若从状态s读出$\alpha$后处于终态，则从状态t读出$\alpha$后也处于终态，反之亦然
	- 状态s、t可区分：s、t不等价，例如终态和非终态是可区分的
- 思路：将DFA M的状态集划分为不相交的子集，使M内状态在子集内等价，在子集间可区分。
- 步骤：（例子见下方）
	- 初始划分：$\Pi=\{I^1,I^2\}$，其中$I^1$为终态集，$I^2$为非终态集。
	- 子集划分：对$\Pi$的每个成员集合$I^k$检查，检查是否任意的$a\in \Sigma$都满足$I_a^k$包含于$\Pi$的某个成员集合中。如果不满足，则应对$I^k$划分，使得每个$I^{k_i},i=1,2,\dots,m$满足：对任意的$b\in\Sigma$，都有$I_b^{k_i}$包含于$\Pi$的某个成员集合。
	- 重复进行子集划分，直到子集数量不再增长。

> [!example] DFA化简示例
> ![[Pasted image 20240105131840.png]]
> 初始划分：$\Pi_0=\{I^1,I^2\}$，其中$I^1=\{3,4,5,6\}$，$I^2=\{0,1,2\}$。
> 第一轮子集划分：考察$I^1$，发现$I_a^1=\{3,4\}\subseteq I^1$，$I_b^1=\{4,5\}\subseteq I^1$，满足要求；考察$I^2$，发现$I_a^2=\{1,3\}$不符合要求，根据转移结果划分为$I^3=\{1\}$，$I^4=\{0,2\}$，得$\Pi_1=\{I^1,I^3,I^4\}$。
> 第二轮子集划分：考察$I^4$，发现$I_b^4=\{2,5\}$不符合要求，根据转移结果划分为$I^5=\{0\}$，$I^6=\{2\}$，得$\Pi_2=\{I^1,I^3,I^5,I^6\}$。
> 结果：子集不可再分，合并各个成员集合为一个新状态，并构造新DFA。其中状态3表示$I^1$，状态0、1、2分别表示$I^5,I^3,I^6$。
> ![[Pasted image 20240105135405.png]]

### flex

用途：生成词法分析源码。

源码格式：
```
定义部分
%%%
识别规则部分
%%%
辅助函数部分
```

定义部分：大括弧内定义宏，随后每行定义一个词法单元和其识别的正则表达式。
```
%{
#define ID 68        //identifier
#define NUMBER 69    //number
#define DEFAULT 70   //default
%}
white [\t\n ]
digit [0-9]
letter [A-Za-z]
id ({letter}|_)({letter}|{digit}|_)*
number [1-9]{digit}*|0
```

识别规则部分：对词法单元可以自定义一些操作。
```
{id} {fprintf(yyout,"ID %d %s\n",ID,yytext);}
{number} {fprintf(yyout,"NUMBER %d %s\n",NUMBER,yytext);}
```

辅助函数部分：如果不使用`yy*`函数和库函数，则需要自定义C语言函数。

内置变量：
- `yyin`：源程序输入流，默认为stdin
- `yyout`：信息输出流，默认为stdout
- `yytext`：`char*`类型，指向词法单元识别正则表达式的第一个字符。
- `yyleng`：`int`类型，记录与词法单元匹配单词的长度。

内置函数：
 - `yylex()`：从该函数开始分析，可由flex自动生成
 - `yywrap()`：文件结束处理，如果为1则结束分析一个文件
 - `echo`：将yytext打印到yyout

一个演示程序：详见[[编译原理-flex示例]]。

## 自上而下语法分析

**语法分析器功能**：根据词法分析器提供的单词符号串，分析、判断其是否符合语法规则，即按文法产生式判断输入的单词符号串是否为文法的一个句子。如单词符号串合法，则生成语法树，用于后续部分。

### 自上而下分析方法概述

自上而下方法**基本思想**：
- 对任何输入串，用一切可能方法从开始符号出发，为输入串寻找一个**最左推导**，也就是自上而下建立一棵语法树
- 整个过程是一种带回溯的试探过程

自上而下方法面临的问题：
- **左递归问题**：如果文法存在形似$P\overset{+}{\Rightarrow} P\alpha$的产生式，则称其含有左递归，其会使分析过程陷入无限循环
- 回溯使分析走大段错路
- 虚假匹配现象
- 报告分析不成功时，难于定位
- 效率低，代价高，有理论意义，实践价值不大

### LL(1)分析方法

说文解字：
- L：从左（Left）到右扫描输入串
- L：构造最左（Leftmost）推导
- 1：分析时每步向前看一个字符

目的：构造不带回溯的自上向下分析算法
- 消除左递归
- 消除回溯
- FIRST和FOLLOW集合
- LL(1)分析条件
- LL(1)分析方法

**消除左递归**：
- 消除直接左递归：若$P\rightarrow P\alpha_1|P\alpha_2|\dots|P\alpha_m|\beta_1|\beta_2|\dots|\beta_n$（$\alpha_i\neq \varepsilon$，$\beta_i$不以$P$开头），则可改写为$P\rightarrow \beta_1 P'|\beta_2 P'|\dots|\beta_n P'$、$P'\rightarrow \alpha_1 P'|\alpha_2 P'|\dots|\alpha_m P'|\varepsilon$两条规则。
- 消除间接左递归：非终结符之间可能嵌套推导。例如：$S\rightarrow Qc|c$，$Q\rightarrow Rb|b$，$R\rightarrow Sa|a$。
	- 排序：被推导的比推导的优先处理。如R>Q>S。
	- 代入：按序代入。如$Q\rightarrow Sab|ab|b$，$S\rightarrow Sabc|abc|bc|c$。
	- 消除直接左递归：如$S\rightarrow abcS'|bcS'|cS'$，$S'\rightarrow abcS'|\varepsilon$，$Q\rightarrow Sab|ab|b$，$R\rightarrow Sa|a$。
	- 化简：删除永不使用的产生式。如$S\rightarrow abcS'|bcS'|cS'$，$S'\rightarrow abcS'|\varepsilon$。

**消除回溯，提左因子**：
- 目的：保证在分析过程中，对任意非终结符$A$，用它匹配输入串时能根据当前输入，指派*至多一个产生式*进行分析。即$A\rightarrow \alpha_1|\alpha_2|\dots|\alpha_n$，对输入符号$a$，要么不匹配，要么匹配的$\alpha_i$的分析结果完全决定分析成败。这样就不必进行回溯。
- 操作：提取公共左因子，将文法改造成任何非终结符的所有候选首符集两两不相交的形式。

**LL(1)分析条件**：
- 定义：
	- $\text{FIRST}(\alpha)$：符号串$\alpha$的**终结首符集**，包含由$\alpha$推导出所有合法句子的所有合法首符，即$\text{FIRST}(\alpha)=\{a|\alpha\overset{*}{\Rightarrow} a\dots,a\in V_T\}$。特别地，$\alpha\overset{*}{\Rightarrow}\varepsilon$，则$\varepsilon\in\text{FIRST}(\alpha)$。
	- $\text{FOLLOW}(A)$：非终结符$A$的**后继终结符号集**，即$\text{FOLLOW}(A)=\{a|S\overset{*}{\Rightarrow} \dots Aa\dots, a\in V_T\}$。特别地，若$S\overset{*}{\Rightarrow} \dots A$，则$\#\in \text{FOLLOW}(A)$。
- 唯一、确定、无虚假匹配：消除了左递归，且对任意的$A\rightarrow \alpha_1|\alpha_2|\dots|\alpha_n$和任意的$i,j=1,2,\cdots,n$且$i\neq j$，有$\text{FIRST}(\alpha_i)\cap\text{FIRST}(\alpha_j)=\varnothing$。
- 终结首符和后继终结符无冲突：对文法内的任意非终结符$A$，若有$\varepsilon\in\text{FIRST}(A)$，则有$\text{FIRST}(A)\cap \text{FOLLOW}(A)=\varnothing$。

FIRST和FOLLOW集合的构造：
- 对文法符号$X\in V_T\cup V_N$，构造$\text{FIRST}(X)$：
	- 终结符情形：若$X\in V_T$，则$\text{FIRST}(X)=\{X\}$。
	- 非终结符情形：若$X\in V_N$，则分如下情形：
		- 终结首符产生式：若存在产生式$X\rightarrow a\dots$，则$a\in \text{FIRST}(X)$。
		- 非终结首符产生式一般情形：若存在产生式$X\rightarrow Y\cdots$，则$\text{FIRST}(Y)-\{\varepsilon\}\in\text{FIRST}(X)$。
		- 非终结首符产生式击穿情形：若存在产生式$X\rightarrow Y_1Y_2\dots Y_k$，且$\varepsilon\in \text{FIRST}(Y_j),1\le j\le i-1$，则$\text{FIRST}(Y_i)-\{\varepsilon\}\subseteq \text{FIRST}(X)$。特别地，若$i=k+1$，则$\varepsilon\in \text{FIRST}(X)$。
- 对于符号串$\alpha=X_1X_2\cdots X_n$，构造$\text{FIRST}(\alpha)$：
	- 置$\text{FIRST}(\alpha)=\text{FIRST}(X_1)-\{\varepsilon\}$。
	- 若对$1\le j\le i-1$，$\varepsilon\in \text{FIRST}(X_j)$，则把$\text{FIRST}(X_i)-\{\varepsilon\}$加入$\text{FIRST}(\alpha)$。
	- 若对$1\le j\le n$，$\varepsilon\in \text{FIRST}(X_j)$，则把$\varepsilon$加入$\text{FIRST}(\alpha)$。
- 对于文法的每个非终结符$A$，构造$\text{FOLLOW}(A)$：
	- 若$A$为文法的起始符号，则置$\#$于$\text{FOLLOW}(A)$中。
	- 若有产生式$B\rightarrow \alpha A\beta$，则将$\text{FIRST}(\beta)-\{\varepsilon\}$加到$\text{FOLLOW}(A)$中。
	- 若有$B\rightarrow \alpha A$或$B\rightarrow \alpha A\beta$，则将$\text{FOLLOW}(B)$加到$\text{FOLLOW}(A)$中。
	- 反复使用以上规则，直至$\text{FOLLOW}(A)$不再增大。

> [!example] 构造FIRST(X)的示例
> ![[Pasted image 20240106095507.png]]

> [!example] 构造FIRST($\alpha$)的示例
> ![[Pasted image 20240106095540.png]]

> [!example] 构造FOLLOW(A)的示例
> ![[Pasted image 20240106095614.png]]

**LL(1)分析方法**：设当前输入符号为$a$，要用非终结符$A$匹配，且$A\rightarrow \alpha_1|\alpha_2|\dots|\alpha_n$。
- 若$a\in \text{FIRST}(\alpha_i)$，则指派$\alpha_i$执行匹配任务。
- 否则，若$\varepsilon\in \text{FIRST}(A)$，且$a\in \text{FOLLOW}(A)$，则让$A$与$\varepsilon$匹配。
- 否则，$a$的出现是一种语法错误。

### 递归下降分析程序

含义：为文法每一个非终结符根据其产生式写一个分析子程序（过程），由于文法定义是递归的，因此这些程序也是*递归*的。处理输入串时首先执行开始符号的过程，然后根据产生式右部出现的非终结符，依次调用响应过程，这种*逐步下降*的调用过程对应了分析树的分析过程。

程序构造：（略，见PPT P31-P34）

**扩展巴科斯-诺尔范式**（EBNF）构造：
- 符号：
	- $\rightarrow$（定义为）、$|$（或）
	- $\{\alpha\}$（闭包$\alpha^*$）、$\{\alpha\}_n^0$（$\alpha$可出现$0\sim n$次）、$[\alpha]$（$\alpha$可出现$0\sim 1$次）
- 方法：对于左递归形式的产生式，可以转为EBNF形式处理。例如$E\rightarrow T|E+T$，可以转为$E\rightarrow T\{+T\}$。
- 程序构造：do-while循环。

**预测分析程序**：
- 预测分析表（**LL(1)分析表**）：$|V_N|$行$|V_T+1|$列的表格，一行代表一个非终结符，一列代表一个终结符或结束标记（$\#$），单元格$M[X,a]$代表栈顶为$X$、当前读到单词$a$时使用的产生式。
- 符号栈：放文法符号，初始放$\#$，再放起始符号$S$。
- 总控程序：设栈顶为$X$，当前输入$a$，则对于任何$(X,a)$执行以下三种动作之一：
	- 若$X=a=\#$，则分析成功。
	- 若$X=a\neq \#$，则把$X$弹出，$a$指向下一输入符号。
	- 若$X\in V_N$，则按$M[X,a]$中的产生式进行推导（弹出$X$，将右部符号串反序入栈），或进行出错处理。

预测分析表构造：对文法的每个产生式$A\rightarrow \alpha$：
- 对$\text{FIRST}(\alpha)$的每个终结符$a$，把$A\rightarrow\alpha$加入$M[A,a]$。
- 如果$\varepsilon$在$\text{FIRST}(\alpha)$中，对$\text{FOLLOW}(A)$的每个终结符$b$（包括$\#$），把$A\rightarrow \alpha$加入$M[A,b]$。
- 对于任何未涉及的终结符$c$，都有$M[A,c]=error$。

（LL(1)分析表示例）
![[Pasted image 20240106114147.png]]

> [!example] LL(1)分析过程示例
> ![[Pasted image 20240106122610.png]]

### LL(1)分析中的错误处理

出错场合：
- 栈顶终结符与当前的输入符号不匹配。
- 栈顶的非终结符$A$与当前输入符号$a$，分析表中$M[A,a]$为空。

错误恢复思路：
- 检测到错误时，暂时放弃分析并给出错误信息。
- 如果分析器能到达一个状态，从该状态可以对剩余输入继续分析，则从该状态恢复。

处理方法：
- 发现错误时跳过输入串的一些符号，直到输入符号属于某个同步符号为止，即利用**同步符号机制**迅速从错误中恢复。（否则语法分析只能解析一处错误）
- 非终结符$A$的同步符号集（synch）选择：
	- $\text{FOLLOW}(A)$的所有终结符。
	- $A$的高层构造的候选首符。

> [!example] 同步符号集在文法的应用示例
> 改进的预测分析表：
> ![[Pasted image 20240106153501.png]]
> 预测过程：
> ![[Pasted image 20240106154135.png]]
> ![[Pasted image 20240106154118.png]]

## 自下而上语法分析

### 自下而上分析方法概述

归约与分析树：
- 移进-归约法：使用符号栈，把输入符号逐一移进栈，栈顶出现某个产生式右部时归约为左部。
- 分析树：用树表示“移进-归约”过程，整个过程*自下而上地*构造分析树。
- 关键问题：何时进行归约（最左归约、规范归约），找到构成产生式右部的符号串。

规范归约简述：
- 有关定义：
	- 短语：对于文法$G(S)$，设$\alpha\beta\delta$是一个句型，若有$S\overset{*}{\Rightarrow} \alpha A\delta$且$A\overset{+}{\Rightarrow} \beta$，则称$\beta$是句型$\alpha\beta\delta$关于非终结符$A$的短语。
	- 直接短语：特别地，若$A\rightarrow \beta$，则称$\beta$是句型$\alpha\beta\delta$关于产生式$A\rightarrow \beta$的直接短语。
	- 句柄：句型的最左直接短语。
- 与句型语法树关系：
	- 短语：句型语法树中每棵子树的所有叶子结点从左到右排列起来形成一个相对于子树根的短语。
	- 直接短语：只有父子两代的子树形成的短语。
	- 句柄：语法树中最左那棵只有父子两代的子树形成的短语。
- 定义：设$\alpha$是文法$G$的一个句子，若序列$\alpha_n,\alpha_{n-1},\dots,\alpha_0$满足：$\alpha_n=\alpha$，$\alpha_0=S$，且对任意$0<i\le n$，$\alpha_{i-1}$是从$\alpha_i$将*句柄*替换成相应产生式左部符号得到的，则称该序列是一个**规范归约**。
- 与推导的关系：规范归约是最右推导的逆过程，最右推导又称规范推导。

### 算符优先分析方法

基本思想：
- 简单优先分析法：按一定原则找出所有符号（终结符、非终结符）的优先关系，确定句柄进行规范分析。是规范归约，但效率低，使用价值不大。
- 算符优先分析法：规定终结符（算符）的优先关系，按终结符（算符）的优先关系控制自下而上的语法分析过程（寻找可归约串和进行归约）。它不是规范归约，但分析速度快，适于表达式的语法分析。

#### 算符优先关系表

算符优先关系：
任何两个可能相继出现的终结符$a,b$（中间可能有一个非终结符）的优先关系有低于、等于、高于三种。注意算符优先级*没有传递性和自反性*，即$a\dot{<}b$未必有$b\dot{>}a$，$a\dot{<}b$和$b\dot{<}c$未必有$a\dot{<}c$。

算符优先文法和优先关系表的构造：
- 算符文法：一个文法满足任一产生式右部都不含*两个相继的非终结符*（即不含形如$A\rightarrow \dots QR\dots,Q,R\in V_N$的产生式），则称该文法为算符文法。
- 算符优先关系：设算符文法$G$不含$\varepsilon$-产生式，$a,b\in V_T$，算符间的优先关系定义为：（举例见后文）
	- $a\dot{=} b$：当且仅当$G$含产生式$P\rightarrow \dots ab\dots$，或$P\rightarrow \dots aQb \dots$。
	- $a\dot{<}b$：当且仅当$G$含产生式$P\rightarrow \dots aR\dots$且$R\overset{+}{\Rightarrow}b\dots$或$R\overset{+}{\Rightarrow} Qb\dots$。
	- $a\dot{>}b$：当且仅当$G$含产生式$P\rightarrow \dots Rb\dots$且$R\overset{+}{\Rightarrow}\dots a$或$R\overset{+}{\Rightarrow}\dots aQ$。
- **算符优先文法**：如果一个算符文法$G$中任何终结符对$(a,b)$至多满足以上关系之一，则称$G$为算符优先文法。
- 优先关系表的构造：另开一节叙述，见[[编译原理A#^84f9cd]]。

> [!example] 算符文法的优先关系举例
> ![[Pasted image 20240107140549.png]]

算符优先关系表的构造： ^84f9cd
- 定义：设$P\in V_N$：
	- FIRSTVT：$\text{FIRSTVT}(P)=\{a|P\overset{+}{\Rightarrow} a\dots 或P\overset{+}{\Rightarrow} Qa\dots\}$，其中$a\in V_T$，$Q\in V_N$。
	- LASTVT：$\text{LASTVT}(P)=\{a|P\overset{+}{\Rightarrow}\dots a或 P\overset{+}{\Rightarrow} \dots aQ\}$，其中$a\in V_T$，$Q\in V_N$。
- FIRSTVT、LASTVT构造：对每个产生式检查其首末终结符，加入到对应集合中。
- 若已构造FIRSTVT和LASTVT，则可通过以下检查确定终结符对的优先关系：
	- 若产生式有候选形如$\dots aP\dots$，则任何$b\in \text{FIRSTVT}(P)$都满足$a\dot{<}b$。
	- 若产生式有候选形如$\dots Pb\dots$，则任何$a\in \text{LASTVT}(P)$都满足$a\dot{>}b$。

> [!example] 算符优先关系表的构造算法和构造示例
> ![[Pasted image 20240107160144.png]]

#### 算符优先分析算法

最左素短语：算符优先分析中的可归约串。
- 素短语：至少含一个终结符的短语，除其自身之外不含任何更小的素短语。
- 最左素短语：处于句型最左边的那个素短语。

> [!example] 短语、素短语、最左素短语的关系举例
> ![[Pasted image 20240108103527.png]]
> 有点乱？哎，乱就对了。

定理：
- 算符优先文法句型（括在两个$\#$之间）的一般形式为：$\# N_1a_1 N_2a_2\dots N_n a_n N_{n+1}\#$，其中，$a_i\in V_T$，$N_i\in V_N$。
- 一个算符优先文法$G$的任何句型的最左素短语是满足下列条件的最左子串（例如句型$\#P*P+i\#$中，由于$\#\dot{<}*$和$*\dot{>}+$，所以$P*P$是最左素短语）：
	- $a_{j-1}\dot{<}a_j$。
	- $a_{j}\dot{=}a_{j+1}\dot{=}\cdots \dot{=}a_{i-1}\dot{=}a_i$。
	- $a_i\dot{>}a_{i+1}$。

**算符优先分析算法**：
- 用符号栈$S$实现最左素短语的查找，栈底放$\#$。
- 用任意名字如$N$代替归约的非终结符。
- 算法大意：
	- 将输入串依次逐个存入符号栈$S$中，直到符号栈顶元素$S_k$与下一个待输入的符号$a$有优先关系$S_k\dot{>}a$为止。
	- 至此，最左素短语尾符号$S_k$已在符号栈$S$的栈顶，由此往前在栈中找最左素短语的头符号$S_{j+1}$，直到找到第一个$S_{j}\dot{<}S_{j+1}$为止。
	- 已找到最左素短语$S_{j+1}\dots S_k$，将其归约为某个非终结符$N$，并做相应的语义处理。
- 算法说明：算符优先分析*不是规范归约*，不会对右侧仅一个非终结符的产生式归约，所以归约速度快；$S[j+1\dots k]$归约为非终结符是指，运用产生式$N\rightarrow S[j+1\dots k]$将这一串替换为$N$。

> [!example] 算符优先分析过程举例
> 假设算符文法$G$包含产生式：$N\rightarrow N*N|N+N|(N)|i$，下面的过程对$i*(i+i)$进行了分析。
> ![[Pasted image 20240108113751.png]]

**优先函数**：
- 定义：对于文法$G$的每个终结符$\theta$，函数$f,g$满足：若$\theta_1\dot{<}\theta_2$，则$f(\theta_1)<g(\theta_2)$；若$\theta_1\dot{>}\theta_2$，则$f(\theta_1)>g(\theta_2)$；若$\theta_1\dot{=}\theta_2$，则$f(\theta_1)=g(\theta_2)$，则称$f,g$是优先函数，其中$f(\theta)$为*栈内优先数*，$g(\theta)$为*栈外优先数*。
- 特点：节省存储空间，方便运算，可推导出一些原本不存在优先关系运算符的优先级，函数不唯一。
- 构造方法（建图）：
	- 对算符建偶图$(V,E)$，$V=\{(f,a),(g,a)|a\in V_T\}$；
	- 对非终结符$a,b$，若$a$优先级高于或等于$b$，则从$(f,a)$到$(g,b)$连一条有向边；若$a$优先级低于或等于$b$，则从$(g,b)$到$(f,a)$连一条有向边；
	- 每个结点赋予一个数，该数等于从该结点出发可达结点个数，分别作为$f(a),f(b),g(a),g(b)$等。
	- 检查是否矛盾。
- 构造方法（Floyd迭代）：
	- 初始，对文法$G$的每个$\theta\in V_T$，令$f(\theta)=g(\theta)=1$。
	- 若$\theta_1\dot{>}\theta_2$，但$f(\theta_1)\le g(\theta_2)$，则令$f(\theta_1)=g(\theta_2)+1$。
	- 若$\theta_1\dot{<}\theta_2$，但$f(\theta_1)>g(\theta_2)$，则令$g(\theta_2)=f(\theta_1)+1$。
	- 若$\theta_1\dot{=}\theta_2$，但$f(\theta_1)\neq f(\theta_2)$，则令$f(\theta_1)=g(\theta_2)=\max\{f(\theta_1),g(\theta_2)\}$。
	- 重复上述三步直至过程收敛，否则函数不存在。

文法在内存中的表示：时代的眼泪。

### LR分析方法

基本思想：
- 记住“历史”：记忆已移进和归约的整个符号串
- 展望“未来”：根据所用的产生式推测未来可能碰到的输入符号
- 认识“现实”：根据记录的符号串和预测的输入符号，基于当前的输入符号，确定栈顶符号串是否构成相对某一产生式的句柄

#### LR分析器

组成：总控程序、LR分析表、分析栈

LR分析表分类：
- LR(0)表：基础，有局限性
- SLR表：简单LR表，实用
- 规范LR表：能力强，代价大
- LALR表：向前LR表，介于SLR和规范LR之间

分析栈的元素构成：
- 状态：从分析开始到某一归约阶段的全部“历史”和“展望”资料。
- 符号：文法符号。

LR分析表构成：
- 动作（ACTION）表：`ACTION[S,a]`=动作。
	- 移进（`Sj`）：把当前`a`和状态`j`进栈，随后根据GOTO表进行转移。
	- 归约（`rj`）：按第`j`个产生式归约。
	- 接受（`acc`）：成功结束
	- 出错：空白或出错处理
- 状态转换（GOTO）表：`GOTO[S,X]`表示状态S面对文法符号X时，下一个状态是什么。

LR分析过程：
![[Pasted image 20240108164840.png]]

> [!example] LR分析过程距离
> ![[Pasted image 20240108164915.png]]

**LR文法**：对于一个文法，如果能构造一张LR分析表，使得它的每个入口都是唯一确定，则称该文法为LR文法。
- LR(k)文法：如果一个文法每步至多向前检查k个输入符号，则能使用LR分析器进行分析，称LR(k)文法。
- **LR(0)文法**：如果k=0，则文法无需向前检查，只需要基于当前符号和历史信息进行分析，称LR(0)文法。

#### LR(0)分析表的构造

有关概念、术语：
- 前缀：符号串的任意首部。注意对任意符号串，$\varepsilon$和其自身也是合法前缀。
- 活前缀：最右推导的句型（规范句型）的前缀，且该前缀不超过句柄右端，则称其为一个*活前缀*。（如$S\Rightarrow_{rm} \gamma A w\Rightarrow_{rm} \gamma\beta w$，则$\gamma\beta$任何前缀都是活前缀）
	- 意义：分析栈内始终构成句型活前缀；LR分析器的分析器的工作过程是逐步产生文法的规范句型活前缀的过程。
- LR(0)项目：在文法产生式中加点，用于表示分析过程中的状态（如：$E\rightarrow E+.T$）
	- 对产生式$A\rightarrow \varepsilon$有项目$A\rightarrow .$，对产生式$A\rightarrow\beta$有$|\beta|+1$个项目。

步骤及其意义：
- 第一步：从文法构造识别活前缀的DFA。意义在于构造LR分析表的转移函数。
- 第二步：从上述DFA构造完整的分析表，包括ACTION和GOTO表。

##### 步骤一：从文法构造识别活前缀的DFA

两种方法：
- 方法一：求出文法的所有项目，按一定规则构造NFA再确定化为DFA。
- 方法二：直接构造DFA。

**方法一：先求项目，构造NFA，再简化**
- 拓广文法：引入新的开始符号$S'$使它只在第一个产生式左部出现。
- 构造NFA：
	- 状态结点：项目
	- 有向边：
		- 若状态$i,j$出自同一个产生式，且$j$的圆点跳过$a$落后$i$一个位置，则$i$到$j$有向边标记$a$。
		- 若$i:X\rightarrow \alpha .A\beta$，$j$为所有的$A\rightarrow .\gamma$状态，则$i$到$j$有向边标记$\varepsilon$。
- 确定化上述方法构造的NFA。

> [!example] 从文法构造识别活前缀DFA的方法一举例
> ![[Pasted image 20240109000741.png]]
> ![[Pasted image 20240109000753.png]]

**方法二：直接构造DFA**
- 定义：
	- `closure(I)`：项目集闭包函数，如下计算：
		- 每个`I`的项目都加进`closure(I)`
		- 若$A\rightarrow \alpha .B\beta\in$`closure(I)`且$B\rightarrow\gamma$产生式，若$B\rightarrow .\gamma$不在`closure(I)`，则将$B\rightarrow .\gamma$加进`closure(I)`
		- 重复执行上一步直到`closure(I)`不再扩大
	- `GO(I,X)`：设`X`是文法符号，`GO(I,X)=closure(J)`，其中$J$包含所有形如$A\rightarrow \alpha X.\beta$的项目，其中$A\rightarrow \alpha .X\beta\in I$。
- 构造思想：
	- 从$S'\rightarrow .S$开始，得到DFA的初态项目集
	- 从初态项目集出发，通过状态转换函数GO求其所有的后继项目集，直到项目集数量不再增加

> [!example] 从文法构造识别活前缀DFA的方法二举例
> ![[Pasted image 20240109005116.png]]

识别活前缀的DFA：如果文法G的识别活前缀的DFA的每个状态不存在任何冲突项目：
- 移进项目和归约项目并存。
- 多个归约项目并存。
则称G是一个LR(0)文法。

##### 步骤二：从识别活前缀的DFA构造分析表

项目对活前缀有效：
- 含义：如果存在规范推导$S'\overset{*}\Rightarrow_{rm} \alpha Aw\Rightarrow \alpha\beta_1\beta_2 w$，则称项目$A\rightarrow \beta_1. \beta_2$对活前缀$\alpha\beta_1$有效。
- 意义：归约项目$A\rightarrow \beta_1.$对活前缀$\alpha\beta_1$有效，说明需要归约；移进项目$A\rightarrow \beta_1.\beta_2$对活前缀$\alpha\beta_1$有效，说明句柄还未形成，需要移进。
- LR分析中，符号栈中的活前缀$X_1X_2\dots X_m$的有效项目集就是栈顶状态$S_m$代表的集合。集合中的不同项目表明了分析需要进行的不同操作，依此来填写LR分析表。

**LR(0)分析表的构造**：令DFA的状态$I_k$对应LR(0)的状态$I_k$。
- 移进项目：若$A\rightarrow \alpha .a\beta\in I_k$，且$\text{GO}(I_k,a)=I_j$（$a\in V_T$），则置$\text{ACTION}[k,a]=s_j$。
- 归约项目：若$A\rightarrow \alpha. \in I_k$，则对任意终结符$a$（包括$\#$）置$\text{ACTION}[k,a]=r_j$（$j$为产生式$A\rightarrow \alpha$的编号）
- 接受项目：若项目$S'\rightarrow S. \in I_k$，则置$\text{ACTION}[k,\#]=acc$。
- 转移函数：若$\text{GO}(I_k,A)=I_j$（$A\in V_N$），则置$\text{GOTO}[k,A]=j$。
- 不能用上述方法填入的内容均置为出错标志。

> [!example] LR(0)分析表的构造举例
> ![[Pasted image 20240109112311.png]]

#### LR(0)总结

**LR(0)方法的全过程**：
- 构造LR(0)分析表：
	- 写出文法$G$的拓广文法$G'$。
	- 写出文法$G'$的基本LR(0)项目。
	- 利用函数`closure`和`GO`，求出相应的项目集规范族$C$。
	- 构造识别文法$G'$所有活前缀的DFA。（两种方法）
	- 根据DFA构造LR(0)分析表。
- 运用构造的LR(0)分析表进行语法分析。

![[Pasted image 20240109121054.png]]

**LR(0)分析法存在的问题**：


### yacc

yacc是一种语法分析器的生成器，使用LALR(1)分析方法。

流程：
- 用户编写yacc源程序（如`ansi_c.y`）。
- yacc编译器将yacc源程序翻译为c语言的语法分析源程序（默认为`y.tab.c`）。
- c编译器将语法分析源程序编译为语法分析程序。`ansi_c.y`一般需要配合`ansi_c.lex`，才能正确编译。
- 语法分析程序从输入流捕获源程序，调用词法分析子程序获取单词串，并根据构造的LALR分析表进行分析。

参考格式：
```
// 前置预处理块，用%{和%}包围
%{
#include <stdio.h>
%}

// 第一段：定义段
// 用%token声明单词种别，%start声明起始符号

%token 单词种别1 单词种别2
%token 单词种别3
%token 单词种别4

%start 程序

%%

// 第二部分：规则段
// 每个非终结符都可指定一组推导/归约规则
// 注意每个规则最后的语句块不是必需的，可以省略

程序
    : 全局声明
    | 程序 全局声明
    { fflush(stdout); printf("定义了程序\n"); };

全局声明
    : 变量声明
    | 函数声明
    { fflush(stdout); printf("定义了全局声明\n"); };

变量声明
    : 类型 IDENTIFIER
    { fflush(stdout); printf("定义了变量声明\n"); };

类型
    : INT FLOAT
    { fflush(stdout); printf("声明了类型\n"); };

函数声明
    : 类型 IDENTIFIER ( 形参列表 ) 复合语句
    { fflush(stdout); printf("定义了函数声明\n"); };

// 其余语法单元略

%%

// 第三部分：用户子例程段
// 允许用户自行定义和实现C语言例程，会被拷贝到y.tab.c中

#include <stdio.h>

extern char yytext[];
extern int column;

yyerror(s)
char *s;
{
    fflush(stdout);
    printf("\n%*s\n%*s\n", column, "^", column, s);
}
```

允许的声明符号：
- `%token`：声明一种单词种别
- `%start`：声明起始符号
- `%left`、`%right`：声明运算符为左结合或右结合
- etc.

更多细节详见[[编译原理-bison示例与应用]]。

-----

太臭了，后续内容另开文章了。