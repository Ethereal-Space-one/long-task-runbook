# Long Task Runbook

一个面向多阶段任务的 Agent Skill。把工作拆成可验收的任务包，使用项目检查点恢复进度，并按原始证据复核结果。

## 下载与使用

在 [Releases](https://github.com/Ethereal-Space-one/long-task-runbook/releases/latest) 下载 `long-task-runbook` ZIP。解压后，将整个 `long-task-runbook` 目录放入对应位置。

| 工具 | 用户级技能目录 | 调用示例 |
| --- | --- | --- |
| Codex | `~/.codex/skills/` | `$long-task-runbook` |
| Claude Code | `~/.claude/skills/` | `/long-task-runbook` |
| DeepSeek Harness | `~/.dsh/skills/` | `/long-task-runbook` |

在实际任务中提供项目接手入口和本轮范围。例如「使用 long-task-runbook，从项目接手入口恢复当前任务。完成本包后停在复核。」

## 内容

- [SKILL.md](skills/long-task-runbook/SKILL.md) 包含任务执行入口。
- [任务拆分与指派](skills/long-task-runbook/references/task-packets.md) 包含交接记录和可复制的任务提示。
- [状态恢复与复核](skills/long-task-runbook/references/recovery-and-review.md) 包含按需读取、检查点、证据验收和变更后的复核。
