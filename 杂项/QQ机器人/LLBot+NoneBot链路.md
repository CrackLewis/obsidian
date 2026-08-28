
LuckyLilliaBot (llbot)作为QQ客户端，NoneBot作为机器人应用

ref:
- [llbot-nonebot-integration](https://luckylillia.com/guide/install_nonebot)
- [nonebot-docs](https://nonebot.dev/docs)

## llbot配置

首先从[GitHub](https://github.com/LLOneBot/LuckyLilliaBot)获取最新稳定版

运行模式一般选headless

3080是llbot自带的WebUI端口，3010是默认的Milky监听端口（后面会用）

在一个持续会话中执行`./start.sh --qq <qq号>`

为了对接具体的机器人应用，需要修改`bin/llbot/data/config_{qq号}.json`内的对应配置，具体参考文档

## nonebot配置

nonebot通过`uv`安装（失败或者错误的话，考虑换源）：

```sh
uv tool install nb-cli
```

