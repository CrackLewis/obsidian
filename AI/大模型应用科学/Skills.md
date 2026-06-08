
skill是一种：
- 由自然语言和编程语言混合编写的
- 面向特定任务场景设计的
- 可被Agent类AI应用复用的
- 能力模块或任务执行单元

## 与prompt、tool、workflow的区别

prompt是一次性的自然语言指令

tool是更偏底层的、主要由编程语言实现的Agent能力接口

workflow是流程趋向于固定的作业规范

而skill：
- 可复用：prompt不可复用
- 会包含自然语言指令：tool更偏底层
- 流程不会完全固定，会根据实际情况借助LLM能力决定作业流程

## 核心思想和定位

将复杂的任务（写一个完整代码模块、自动化处理任务等）拆分为可复用、可调用、可维护的能力模块

将专家经验、任务规范和最佳实践显性化，使 Agent 可以稳定复现高质量工作方式，如：写项目的模块化思想、软件开发流程、测试和交付流程等

降低推理出工作流程的成本：既然流程是固定的，就没必要推理

提升Agent对同一任务输出的一致性，通过固定处理/输出格式避免不确定性

让Agent更清楚什么时候该用tool，什么时候不该用

## skill的常见组成

适用场景：什么时候该用，什么时候不该用

任务目标：能帮助Agent解决什么问题

*执行步骤*：主要组成部分，规定任务如何完成
- 比如，开发一个模块：1、确定项目定位/结构和模块的预期功能；2、确定模块的文件结构；3、在每个文件建立dummy impl，编写并运行冒烟测试；4、编写部分难度较低的子模块，审查子模块代码，编写并运行子模块测试；5、编写模块的核心逻辑；6、审查模块核心逻辑的代码并酌情修改；7、编写核心模块的功能测试并运行；8、如果成功则继续，否则跳转至第6步；9、编写集成测试，运行并检查结果，如果失败返回第6步；10、编写模块文档描述模块作用。

*工具使用规范*：如果需要使用tool，则说明tool的使用方式

*输出格式*：指示任务如何组织并输出结果

*约束条件*：说明哪些事情不能做或应该避免
- 比如，在编写代码时：1、参考代码风格，避免不合风格或突兀的标识名；2、代码应当避免过度内聚，在保持性能的基础上保持较高的模块化程度，等等

*错误处理与边界情况*：明确指出skill应当考虑的异常情况，及其解决方案

## skill的主要作用

作用：提升回答的专业性和健壮性；流程可复用，可维护；tool调用质量更高，滥用风险更低

## 编写skill的大致流程

skill的大致目录结构：

```
my-skill/
+ scripts/             # skill内部需要明确为编程语言脚本的逻辑
  + foo1.js            
  + foo2.sh
  + foo2.bat
  + foo2.ps1
+ references/          # skill需要使用的自然语言辅助文件
  + metric-table.md
+ assets/              # skill内的静态文件
  + template.tex
  + DemoClass.cpp
+ SKILL.md             # skill描述文件
```

最重要的是`SKILL.md`，它记录该skill的所有要点。

`SKILL.md`的写作要点：
- 导言区`description`写清楚：干什么的+啥时候用+（啥时候不用）
- 在skill主体写清楚工作流和任务清单
- 写清楚如何组织输出格式

### demo: stop-slop

[repo](https://github.com/hardikpandya/stop-slop)

```md
---
name: stop-slop
description: Remove AI writing patterns from prose. Use when drafting, editing, or reviewing text to eliminate predictable AI tells.
metadata:
  trigger: Writing prose, editing drafts, reviewing content for AI patterns
  author: Hardik Pandya (https://hvpandya.com)
---

# Stop Slop

Eliminate predictable AI writing patterns from prose.

## Core Rules

1. **Cut filler phrases.** Remove throat-clearing openers, emphasis crutches, and all adverbs. See [references/phrases.md](references/phrases.md).

2. **Break formulaic structures.** Avoid binary contrasts, negative listings, dramatic fragmentation, rhetorical setups, false agency. See [references/structures.md](references/structures.md).

3. **Use active voice.** Every sentence needs a human subject doing something. No passive constructions. No inanimate objects performing human actions ("the complaint becomes a fix").

4. **Be specific.** No vague declaratives ("The reasons are structural"). Name the specific thing. No lazy extremes ("every," "always," "never") doing vague work.

5. **Put the reader in the room.** No narrator-from-a-distance voice. "You" beats "People." Specifics beat abstractions.

6. **Vary rhythm.** Mix sentence lengths. Two items beat three. End paragraphs differently. No em dashes.

7. **Trust readers.** State facts directly. Skip softening, justification, hand-holding.

8. **Cut quotables.** If it sounds like a pull-quote, rewrite it.

## Quick Checks

Before delivering prose:

- Any adverbs? Kill them.
- Any passive voice? Find the actor, make them the subject.
- Inanimate thing doing a human verb ("the decision emerges")? Name the person.
- Sentence starts with a Wh- word? Restructure it.
- Any "here's what/this/that" throat-clearing? Cut to the point.
- Any "not X, it's Y" contrasts? State Y directly.
- Three consecutive sentences match length? Break one.
- Paragraph ends with punchy one-liner? Vary it.
- Em-dash anywhere? Remove it.
- Vague declarative ("The implications are significant")? Name the specific implication.
- Narrator-from-a-distance ("Nobody designed this")? Put the reader in the scene.
- Meta-joiners ("The rest of this essay...")? Delete. Let the essay move.

## Scoring

Rate 1-10 on each dimension:

| Dimension | Question |
|-----------|----------|
| Directness | Statements or announcements? |
| Rhythm | Varied or metronomic? |
| Trust | Respects reader intelligence? |
| Authenticity | Sounds human? |
| Density | Anything cuttable? |

Below 35/50: revise.

## Examples

See [references/examples.md](references/examples.md) for before/after transformations.
```

### demo: 写作模板

```md
---
name: your-skill-name
description: >
  Use this skill when [specific task types]. Trigger when the user asks for
  [concrete verbs / file types / domains]. Do not use when [exclusions].
---

# Skill Name

## Purpose

Explain what this skill helps Claude do, in one or two paragraphs.

## When to use

Use this skill when:
- ...
- ...
- ...

Do not use this skill when:
- ...
- ...
- ...

## Core workflow

1. Inspect the user's request and identify the task subtype.
2. Check required inputs and constraints.
3. Load additional references only when needed.
4. Apply the relevant procedure.
5. Produce output according to the output contract.
6. State uncertainty or missing information explicitly.

## Task routing

| Situation | Action |
|---|---|
| ... | ... |
| ... | ... |

## Output contract

The response must include:
1. ...
2. ...
3. ...

Only include the following when requested:
- ...
- ...

## Constraints

- Do not ...
- Preserve ...
- Ask for clarification only when ...
- Otherwise make a best-effort attempt and mark assumptions.

## Scripts

Available scripts:
- `scripts/foo.py`: use when ...
- `scripts/bar.sh`: use when ...

Run commands from the skill directory unless otherwise specified.

## References

Read only when relevant:
- `references/a.md`: ...
- `references/b.md`: ...

## Common failure modes

Avoid:
- ...
- ...
- ...

## Examples

### Example 1

User request:
> ...

Expected behavior:
- ...
```

## Claude Code集成skills

大部分知名skills是通过插件市场（plugin marketplace）管理的，属于插件的一部分，可通过安装/卸载插件来变更

假设你需要部署自定义skill，且它是一个这样的目录：

```
my-skill/
+ SKILL.md
+ references/...
+ assets/...
+ scripts/...
```

将其移动到`~/.claude/skills`下。如果没有这个目录，创建一个。然后重启或者重新加载Claude Code即可

如果是第三方skill，至少对其做一个审计，确保它不会进行恶意行为

