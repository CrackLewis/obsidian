
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

