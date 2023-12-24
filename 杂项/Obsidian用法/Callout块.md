
[Source](https://help.obsidian.md/Editing+and+formatting/Callouts)

格式：
```md
> [!TITLE] head
> content
```

`TITLE`需要替换为如下类型之一：
- note
- abstract
- info、todo、tip
- success、warning、question、failure
- danger
- bug
- example
- quote

例如：

> [!note] 二重积分的换元方法
> $$\iint dxdy=\iint \left|\begin{matrix}x_r' & y_r'\\ x_\theta' & y_\theta'\end{matrix}\right|drd\theta=\iint rdrd\theta$$

## 嵌套

```md
> [!example]- 我是可折叠嵌套框
> > [!note] 我是子框
> > > [!success] 我是二级子框
```

> [!example]- 我是可折叠嵌套框
> > [!note] 我是子框
> > > [!success] 我是二级子框

WIP