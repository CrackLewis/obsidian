
- 安装包：`pip install xxx`
- 卸载包：`pip uninstall xxx`
- 换源：`pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple`
- 搜索包：`pip search xxx`

## 指定版本安装

```sh
$ pip install SomePackage # 最新版本
$ pip install SomePackage==1.2.3 # 指定版本：1.2.3
$ pip install "SomePackage>=1.2.3" # 最小版本：不低于1.2.3版本
```

## 更新包

```
$ pip install --upgrade SomePackage
```

## 单包换源安装

```
$ pip install SomePackage -i https://pypi.tuna.tsinghua.edu.cn/simple
```

## 输出已安装的包

```sh
$ pip list
$ pip list -o # 输出可升级的包
```

## 卸载包

```sh
$ pip uninstall some-package
```

## 模拟包的安装过程

不实际执行安装，只下载wheels到本地，然后输出预计会发生的包安装/卸载/更新行为。

```sh
$ pip install SomePackage --dry-run
```

## 安装且不尝试通过卸载修复依赖

如果依赖已存在但版本不兼容，则直接报错退出

```sh
$ pip install SomePackage --no-deps
```

## 导出依赖 + 批量安装依赖

```sh
$ pip freeze >requirements.txt
$ pip install -r requirements.txt
```

## 依赖一致性检查

```sh
$ pip check
```

## 缓存清空

```sh
$ pip cache purge
```

