
参考资料：
- [blog](https://blog.csdn.net/qq_43486745/article/details/124344365)

```tex
\usepackage[linesnumbered,ruled,vlined]{algorithm2e}
```

基本指令：
- `\KwIn`、`\KwOut`：指定算法的输入输出
- `\caption`：指定算法标题
- `\;`：换行
- `\For{cond}{body}`：for循环
- `\While{cond}{body}`：while循环
- `\If{cond}{body}`：if语句
- `\eIf{cond}{body}{altbody}`：if-else语句
- `\tcc{comment}`：块状注释
- `\tcp{comment}`：行级注释

示例：

```tex
\begin{algorithm}[H]
    \SetAlgoLined %显示end
	\caption{algorithm caption}%算法名字
	\KwIn{input parameters A, B, C}%输入参数
	\KwOut{output result}%输出
	some description\; %\;用于换行
	\For{condition}{
		only if\;
		\If{condition}{
			1\;
		}
	}
	\While{not at end of this document}{
		if and else\;
		\eIf{condition}{
			1\;
		}{
			2\;
		}
	}
	\ForEach{condition}{
		\If{condition}{
			1\;
		}
	}
	return 
\end{algorithm}
```