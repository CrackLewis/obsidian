
```latex
% 推荐
\usepackage{xcolor} % 颜色加工
\usepackage{soul} % 高亮、下划线、删除线等
\usepackage[normalem]{ulem}
% 过旧，不太推荐
\usepackage{color}
```

## TL;DR

| 类别  | 参数式               | 对应的声明式        | 作用      |
| --- | ----------------- | ------------- | ------- |
| 颜色  | `\textcolor{clr}` | `\color{clr}` | 改变颜色    |
| 字体  | `\textrm`         | `\rmfamily`   | 罗马体（默认） |
|     | `\textsf`         | `\sffamily`   |         |
|     | `\texttt`         | `ttfamily`    |         |
| 字形  | `\textup`         | `\upshape`    | 直立体（默认） |
|     | `\textit`         | `\itshape`    | 斜体      |
|     | `\textsl`         | `\slshape`    | 伪斜体     |
|     | `\textsc`         | `\scshape`    | 小型大写字母  |
| 粗细  | `\textmd`         | `\mdseries`   | 中等体（默认） |
|     | `\textbf`         | `\bfseries`   | 粗体      |
| 字号  | 无                 | （详见[[#字号]]）   |         |
| 下划线 | `\ul`、`\uline`    | 无             |         |
| 删除线 | `\st`、`\sout`     | 无             |         |
| 高亮  | `\hl`             | 无             |         |

## 颜色

```latex
% 参数式（参数内有效）
\textcolor{red}{此处是一段红色文本}

% 声明式（作用域内有效）
{\color{blue} 这一个大括号内，所有文本都是蓝色的}
```

自定义颜色：

```latex
\definecolor{mygreen}{RGB}{0,128,0} % 自定义绿色
\textcolor{mygreen}{歪比巴卜}
```

## 字体

参数式：
- `\textrm{xxx}`：罗马式（默认，RoMan）
- `\textsf{xxx}`：无衬线体（Sans-seriF）
- `\texttt{xxx}`：等宽字体（TypewriTer）

对应的声明式：
- `\rmfamily`
- `\sffamily`
- `\ttfamily`

## 字形、粗细

详见TL;DR。



## 字号

所有字号均为声明式指令，在当前作用域生效。

```latex
\Huge        % 248.8%
\huge        % 207.4%
\LARGE       % 172.8%
\Large       % 144%
\large       % 120%
\normalsize  % 默认(100%)
\small        % 90%
\footnotesize % 80%
\scriptsize   % 70%
\tiny         % 50%
```

## 下划线、删除线、高亮

ulem方式：

```latex
\usepackage[normalem]{ulem}

\uline{xxx} % 下划线
\sout{yyy} % 删除线
```

soul方式：

```latex
\usepackage{soul}

\ul{xxx}
% 带颜色的删除线：\setstcolor{red}
\st{yyy}
% soul高亮：\sethlcolor{yellow}
\hl{zzz}
```

