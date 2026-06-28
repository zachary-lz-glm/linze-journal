# 手机速查页 loop v2 — 启动 prompt（独立 subagent + 固定间隔双 cron）

> **用法**：在 `d:\work\linze-journal` 目录开**新** Claude Code 会话，把下面"━━━ 开始 ━━━"到"━━━ 结束 ━━━"整段粘贴。保持会话开着即可走人。
>
> **核心机制**：每轮 cron 触发派一个**独立 subagent** 在自己的上下文里干活，返回 1 行简报就销毁 → 主会话只留简报，长跑**不爆上下文、不风格漂移**。worker 每 3 分钟优化 1 张，reviewer 每 15 分钟质检一批。

━━━ 开始 ━━━

帮我启动 loop v2，持续优化面试手机速查页（`learning/interview-tools/stealth.html`）为"照念就能答好"的可念答案。

## 前置检查
1. 确认 `.claude/settings.local.json` 的 allow 里含：`Edit`、`WebSearch`、`mcp__web_reader__webReader`、`Bash(cd *)`、`Bash(awk *)`、`Bash(git checkout *)`、`Bash(git add *)`、`Bash(git commit *)`、`Bash(git push *)`。缺哪个**告诉我**加，你不能自己改自己的权限。
2. 任务说明文件已就位：`.claude/loop-worker.md`、`.claude/loop-reviewer.md`、`.claude/loop-review-log.md`。

## 启动（两个 cron）
**A. Worker cron**（每 3 分钟优化 1 张）—— CronCreate 参数：`cron="*/3 * * * *"`, `recurring=true`, `durable=true`，prompt 逐字用下面这段：
> 派一个 general-purpose subagent，把 `D:/work/linze-journal/.claude/loop-worker.md` 的内容作为它的任务说明逐字执行。它返回 1 行简报后，你只需原样转述给我，不要自己读文件/改代码/跑 git。若它回传的内容含"DONE"或"预算用尽"，用 CronList 找到本 worker cron 的 job-id 并 CronDelete 它，告诉我 worker loop 已自动停止。

**B. Reviewer cron**（每 15 分钟质检）—— CronCreate 参数：`cron="*/15 * * * *"`, `recurring=true`, `durable=true`，prompt 逐字用下面这段：
> 派一个 general-purpose subagent，把 `D:/work/linze-journal/.claude/loop-reviewer.md` 的内容作为它的任务说明逐字执行。它返回 1 行简报后原样转述，不要自己读文件/改代码。若回传含"DONE"，用 CronList 找到本 reviewer cron 的 job-id 并 CronDelete 它，告诉我 reviewer loop 已自动停止。

**C. 立即手动派一次 worker subagent**（按 A 里同样方式，不等首次 cron 触发），确认 round 1 跑通：
- grep/Read/Edit/git/awk 全程**不弹权限**
- div 自检输出 0
- push 成功
**若 round 1 在任何 git/awk 命令上弹权限**，停下告诉我**具体命令**，我补精确规则后再走。
跑通后告诉我两个 cron 的 job-id，我就可以走了。

## 停止 / 调整
- 停止：跟我说"停 loop"（你 CronList + CronDelete 两个），或各自 DONE 自停，或 7 天后自动过期。
- 调整频率：跟我说，改 CronCreate 参数（如 worker 想更快 `*/2`、更慢 `*/5`）。
- 人工复核入口：`.claude/loop-review-log.md`（reviewer 判"已放弃·需人工"的卡）。

━━━ 结束 ━━━

## 备注（给我自己看的，不用给 Claude）
- **固定间隔双 cron**：worker `*/3`（~20 张/小时）、reviewer `*/15`（每批 4 张，~16 张/小时）。两者共存无冲突——每轮派完 subagent 就 idle，REPL 大部分时间空闲，两个 cron 都能按时触发。
- **3 min 间隔下若某轮 subagent 耗时 >3 min**：该次 cron 触发时 REPL 正 busy，自动跳过，等下个 idle 再触发，**不会堆积**。
- 每轮独立 subagent → 主会话只留 1 行简报，长跑不爆上下文（核心优势与速度无关）。
- marker 状态机：无标记 → `待复核` → `已复核` / 退回无标记(带 `<!-- loop-retry:N 原因 -->`) / `已放弃`(入 review-log)。
- 任务有界：当前 ~143 张待优化，一晚基本跑完 → worker DONE 自删；待复核清空后 reviewer 也 DONE 自删。
- v1（`loop-启动prompt.md`）已删除。
