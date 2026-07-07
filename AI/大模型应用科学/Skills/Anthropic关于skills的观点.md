
参考：
- [zhihu](https://www.zhihu.com/question/2027303590776063616/answer/2055743570750002541)
- [原始博客](https://claude.com/blog/lessons-from-building-claude-code-how-we-use-skills)
- [skill docs](https://code.claude.com/docs/en/skills)

## skill是什么

> [!warning]
> skill并不仅仅是一个markdown文件。

skill是一个包含`SKILL.md`作为摘要文件，以及0至若干个参考文档、脚本、资源文件、配置文件等的一个文件夹。只有`SKILL.md`是必需的，剩余部分决定了skill的上限。

## skill的大致种类

目前效果最好的skills可以分为9个大类：
- 库和API参考：引导agent正确使用某个内部库或CLI
- 产品验证：引导agent如何测试自己写的代码
- 数据查询分析：连接数据和监控系统
- 业务流程自动化：将高度重复的workflow压成一条命令
- 代码脚手架：按规范生成样板代码
- 代码质量与审查：通过执行对抗式审查，在workspace内强制执行代码质量
- CI/CD与部署：拉取/推送/部署代码
- Runbook/排障手册：从一个症状作多工具排查
- 基础设施运维：带护栏的例行维护操作

> [!tip]
> 一个优秀的skill应该落在上述9个类中的某一个。如果一个skill试图身兼多职，往往会影响其上限，此种情况下应该拆分skill的职能。

> [!tip]
> Anthropic官方称：**产品验证类skill** 能够对产品的输出效果起到最明显的影响，且值得反复打磨推敲以形成最佳实践。

## 写skills的一些实用技巧

*不要写LLM本来就知道的事情*，比如C/C++语法、热门库的API，或者一些业界/社会通识。重点写能够使LLM跳出常规思维方式的资讯内容。

*写一个Gotchas（陷阱）部分*。这部分包含使用skill会最常遇到的一类问题，以及如何规避它们。例如：项目中的什么数据表是只写的，测试/构建时应该规避什么选项/设置，哪些是项目的潜规则，等等。

*妥善组织skill内的文件，使用逐步披露的方式处理信息*。触发条件、最核心的内容以及skill文件结构写在`SKILL.md`内，其余内容可以组织为`references`、`assets`、`scripts`等目录（不是固定的，可以按需改名）。

*避免催促LLM*。如无必要，避免给出过于具体的指令，而是在提供必要信息的基础上，使用自然语言描述workflow。

![[Pasted image 20260707141051.png]]

*对于需要持续根据用户场景操作的情形，尝试维护一个上下文*。例如用户需要将日志上传到Slack的某个频道，但频道没有指定，则需要skill发起询问并记录。记录的位置可以是skill目录或工作区下的`config.json`，取决于配置应当作用于什么范围。
- Claude内置的`AskUserQuestion` tool可以用于向用户提出一个单选题

*写一个精炼但高效的frontmatter（导言区）*。ClaudeCode等Agent系统会列出所有可用agent，但只有在命中frontmatter所述需求时，才会向上下文加载`SKILL.md`。为了保证skill的调用准确率/召回率足够高，导言区必须精准描述skill的用途、适用场景和排除场景。

*帮助LLM记忆*。用日志/JSON/MD/数据库等方式，在skill目录内或者工作区目录内记录工作内容或结果，以实现跨会话共用内容。

WIPs：使用hooks、分发skills、使用插件及插件市场、写作skills