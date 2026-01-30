
一个虚拟环境管理器

ref's:
- [runoob1](https://www.runoob.com/python3/uv-tutorial.html)

```sh
$ curl -LsSf https://astral.sh/uv/install.sh | sh
```

## 版本管理/安装/切换

查看系统中的Python：

```
uv python list
```

安装某一版本：

```
uv python install 3.13
uv python install pypy3.11
```

设置全局默认版本：

```
uv python default 3.12
```

## 环境管理

创建一个名为env1的虚拟环境：

```
uv venv env1
```

激活虚拟环境：

```
source ./env1/bin/activate
```

## 包管理

`uv`+pip命令

## 项目管理

初始化一个项目myproj1，内含一个`pyproject.toml`：

```
uv init myproj1
```

安装由pyproject.toml或requirements.txt指定的依赖：

```
uv sync
```

