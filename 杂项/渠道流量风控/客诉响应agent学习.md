
目录结构：

```
MtuCrpv3
```

## casebook

经过人工确认的案件精炼档案。

## dashboard

客诉案件处理流程的可视化Web界面。

## metadata

- agent使用到各个数据表的schema。
- 每个数据表的表ID、功能性解释、用到了哪些step中。

## query\_steps

记录：
- 哪些step会触发取数操作，会取什么表

执行：
- 每个step取数行为的抽象
- Talos CLI用作取数

定位是一个执行引擎，不主动做决策，只接受调用、被动执行

## review

知识审查协调skill

## rules

规则引擎：将经验从prompt中抽取出来，变成可维护/可检索/可演化的结构化知识
- 哪些规则：`rules.yaml`
- 每类风险长什么样：`risk_profiles.yaml`
- 数值阈值是多少：`thresholds.yaml`

## skill

案例数据复核skill

## steps

客诉响应注册的步骤