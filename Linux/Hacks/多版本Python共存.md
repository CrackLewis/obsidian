
一种解决方案是`update-alternatives`。但它需要对Python3的4个软链接分别注册，非常麻烦。

另一种是pyenv，通过虚拟环境配置来覆盖系统Python。

其他方案待探索。

## pyenv

下载安装脚本并执行。它的效果是为当前用户安装pyenv：

```sh
$ curl https://pyenv.run | bash
```

pyenv在`~/.pyenv`目录下。需要通过修改`~/.bashrc`使它在每次终端启动时都能运作：

```sh
echo -e '\n#pyenv' >>~/.bashrc &&
echo 'export PATH="$HOME/.pyenv/bin:$PATH"' >> ~/.bashrc &&
echo 'eval "$(pyenv init -)"' >> ~/.bashrc &&
echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc &&
source ~/.bashrc
```

常见命令：
- `pyenv version`：当前生效的Python版本
- `pyenv versions`：已安装的Python版本
- `pyenv install 3.x.x`：安装Python 3.x.x到用户目录
- `pyenv uninstall 3.x.x`：移除Python 3.x.x
- `pyenv local 3.x.x`：对当前目录和子目录，使用Python 3.x.x版本
- `pyenv global 3.x.x`：对所有打开了pyenv的终端，使用Python 3.x.x版本
- `pyenv rehash`：重建环境变量。博客说每次增删Python时都应重新执行一次。