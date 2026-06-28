# 手机速查页 loop v2 — 启动 prompt（自驱动循环 + 独立 subagent）

> **用法**：在 `d:\work\linze-journal` 目录开**新** Claude Code 会话，把下面"━━━ 开始 ━━━"到"━━━ 结束 ━━━"整段粘贴。保持会话开着即可走人。
>
> **核心机制**：单 cron 启动一个**自驱动循环**——worker subagent 优化完一张**立即**派下一张（不等固定间隔），每 4 张插入 1 个 reviewer subagent 质检。每轮 subagent 在**独立上下文**里跑 → 主会话只留 1 行简报 → 长跑不爆上下文、不风格漂移、坏轮不传染。

━━━ 开始 ━━━

帮我启动 loop v2，持续优化面试手机速查页（`learning/interview-tools/stealth.html`）为"照念就能答好"的可念答案。

## 前置检查
1. 确认 `.claude/settings.local.json` 的 allow 里含：`Edit`、`WebSearch`、`mcp__web_reader__webReader`、`Bash(cd *)`、`Bash(awk *)`、`Bash(git checkout *)`、`Bash(git add *)`、`Bash(git commit *)`、`Bash(git push *)`。缺哪个**告诉我**加，你不能自己改自己的权限。
2. 任务说明文件已就位：`.claude/loop-worker.md`、`.claude/loop-reviewer.md`、`.claude/loop-review-log.md`。

## 启动（1 个 cron + 自驱动循环）
CronCreate 参数：`cron="*/15 * * * *"`, `recurring=true`, `durable=true`，prompt 逐字用下面这段：
> 进入自驱动优化循环。规则：**不要等待、不要自己读文件/改代码/跑 git，只派 subagent + 把每个 subagent 返回的 1 行简报原样转述给我**。
> 1. 派一个 general-purpose subagent，把 `D:/work/linze-journal/.claude/loop-worker.md` 的内容作为它的任务说明逐字执行，等它返回 1 行简报后转述。
> 2. 若该简报含"DONE"或"预算用尽"→ 停止循环，用 CronList 找到本 cron 的 job-id 并 CronDelete 它，告诉我 loop 已自动停止。
> 3. 否则**立即**派下一个 worker subagent（不要等时间、不要等下次 cron 触发，上一张完成就开下一张）。
> 4. 每累计派完 **4 个 worker** subagent → 接着派一个 general-purpose subagent 执行 `D:/work/linze-journal/.claude/loop-reviewer.md`（质检一批），转述其 1 行简报，然后继续 worker 循环。
> 5. 如此连续直到 DONE。（"每 4 张插 1 次 review"是大致节奏，若上下文 compaction 后计数丢了没关系，节奏大致对即可。）

立即手动派第一个 worker subagent（按上面方式，不等首次 cron 触发），确认 round 1 跑通：
- grep/Read/Edit/git/awk 全程**不弹权限**
- div 自检输出 0
- push 成功
**若 round 1 在任何 git/awk 命令上弹权限**，停下告诉我**具体命令**，我补精确规则后再走。
跑通后告诉我 cron 的 job-id，我就可以走了。

## 停止 / 调整
- 停止：跟我说"停 loop"（你 CronList + CronDelete），或 DONE 自停，或 7 天后自动过期。
- 调整：跟我说，改 CronCreate 参数或 `loop-worker.md`。
- 人工复核入口：`.claude/loop-review-log.md`（reviewer 判"已放弃·需人工"的卡）。

━━━ 结束 ━━━

## 备注（给我自己看的，不用给 Claude）
- **自驱动 = 上一张完成立即开下一张，无固定间隔**，全速跑。当前 ~143 张待优化，可能一晚跑完 → DONE 自删 cron 停机。
- 单 cron `*/15` 仅作**启动 + 中断兜底**：循环一直跑时 REPL busy，cron 不触发（也不需要）；万一循环被中断（网络/限额/重启），REPL 变 idle，下次 cron 触发重启循环，状态靠文件 marker 不丢。
- **review 嵌在 worker 循环里**（每 4 worker 插 1 reviewer），不另起 reviewer cron——因为 cron 只在 REPL idle 时触发，worker 自驱占着 REPL 会饿死任何独立的定时 cron。
- marker 状态机：无标记 → `待复核` → `已复核` / 退回无标记(带 `<!-- loop-retry:N 原因 -->`) / `已放弃`(入 review-log)。
- 成本提醒：全速模式一晚 token 消耗较高；任务有界（~143 张），跑完自停。想限速就改回固定间隔 cron（如 `*/10`，每轮 1 张后等下次触发）。
- v1（`loop-启动prompt.md`）已删除。
