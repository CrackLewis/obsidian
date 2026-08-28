
OpenClaw是一个可有效接收用户指令，执行实际任务（办公、查资料、处理邮件等）的agent应用

## 手动安装

Debian下安装：

```sh
$ curl -fsSL https://openclaw.ai/install.sh | bash
```

Windows下安装：

```sh
# PowerShell
iwr -useb https://openclaw.ai/install.ps1 | iex

# CMD
curl -fsSL https://openclaw.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
```

或者通过npm（`node>=22.0`）：

```sh
$ npm install -g openclaw --registry=https://registry.npmmirror.com
```

初次启动前，openclaw可能不在`PATH`内。如果是npm安装的，可能在`~/.npm-global/bin`下，需要修改`.bashrc`包含到`PATH`中

## onboarding

初次quickstart，填自己的model provider，channel可以填飞书或skip

skill配置：`npm`包管理；skills任选；missing dependencies跳过

如果设备在国内，国外api key建议是不填

ui选webui；设备条件差的选tui

## onboarding之后

如果没有channel，则需要部署一个（飞书/微信/etc）

如果缺技能，在clawhub/skillhub上选技能部署到本地

更多高级玩法待解锁

