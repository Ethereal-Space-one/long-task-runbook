# Long Task Runbook

给需要跨会话、跨 Agent 协作的工程任务用的 Skill。新会话不必靠一段旧摘要猜进度：先找到实际检出的版本、当前授权和验收证据，再从第一个未完成的步骤继续。

## 安装

### 用 Skills CLI 安装（推荐）

在目标项目根目录运行，按提示选择你实际使用的 Agent，并选择 `Project` 安装范围：

```bash
npx skills add Ethereal-Space-one/long-task-runbook --skill long-task-runbook
```

这条命令从仓库默认分支安装，不固定到某个 Release。要复现指定版本，请下载对应标签下的 ZIP。 [在 skills.sh 查看该 Skill](https://www.skills.sh/ethereal-space-one/long-task-runbook/long-task-runbook)

### 手动安装 ZIP

从 [Releases](https://github.com/Ethereal-Space-one/long-task-runbook/releases/latest) 下载 `long-task-runbook` ZIP。解压后，把含有 `SKILL.md` 和 `references/` 的整个 `long-task-runbook/` 放进对应目录，不要只复制入口文件。

| 工具 | 用户级技能目录 | 在新会话中调用 |
| --- | --- | --- |
| [Codex](https://learn.chatgpt.com/docs/build-skills) | `~/.agents/skills/` | `$long-task-runbook` |
| [Claude Code](https://code.claude.com/docs/en/skills) | `~/.claude/skills/` | `/long-task-runbook` |
| [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/skill/skill-filesystem/README.md) | `${DSH_HOME:-$HOME/.dsh}/skills/` | [`/long-task-runbook` 或技能菜单](https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/client/ui-skill/README.md) |

装完后，在目标项目下打开新会话，先确认客户端发现的是刚安装的那个目录。如果列表里有两个同名项，先核对路径，再调用。这个 ZIP 是 Skill，不是插件或后台服务。

## 第一次使用

交给 Agent 三样东西：**项目接手入口、本轮交付范围、完成后的停止点**。没有项目记录时，可以让 Agent 先建一份简短检查点，不必维护另一套账。

刚装好想试一下？在有 README 的项目里开一个新会话，发送：

> 使用 long-task-runbook，只读本项目的 README 和 Git 工作副本，告诉我当前提交、一个尚未核实的事项，以及下一步怎么验证。没有运行的检查不要写成已通过。到回复为止，不改文件、不提交。

要接手实际任务，把下面的示例路径换成你项目已有的交接文件：

> 使用 long-task-runbook，从 `docs/handoff.md` 接手。本轮只补齐导出功能的回归测试，测试完停在复核，不提交、不推送。若旧记录与实际检出版本不同，先指出差异，再确认哪些测试结果还适用。

审查也可以单独指派：把候选版本、验收条件和可读取的原始证据交给独立审查者。输出应说明**实际检查了什么、哪些条件未满足、下一步是什么**，而不是转述上一位 Agent 的总结。

- [执行入口](skills/long-task-runbook/SKILL.md)：规划、执行、续跑或复核时的入口。
- [任务拆分与指派](skills/long-task-runbook/references/task-packets.md)：任务包、交接和可复制的提示。
- [恢复与复核](skills/long-task-runbook/references/recovery-and-review.md)：恢复实际状态、查验交付证据和确认验收范围。

## 验证 Skill

仓库附带一个[离线接手练习](evals/README.md)，用虚构仓库和本地模拟回执检查 Agent 实际做了什么，不看它有没有说出正确的术语。练习不发真实请求，也不需要账号。先运行 `python3 evals/recovery.py selftest` 验证判分器，再用新会话跑一个场景。
