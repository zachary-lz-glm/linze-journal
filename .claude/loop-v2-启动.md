# 手机速查页 loop v2 — 启动 prompt（独立 subagent + 固定间隔双 cron）

> **用法（纯自动，必须）**：在 `d:\work\linze-journal` 目录用 **`claude --dangerously-skip-permissions`** 开新会话（彻底免人工确认）。然后把下面"━━━ 开始 ━━━"到"━━━ 结束 ━━━"整段粘贴，保持会话开着即可走人。
> （已在 `settings.local.json` 设 `bypassPermissions` 兜底；CLI flag 最稳，二选一即可。）
>
> **核心机制**：每轮 cron 触发派一个**独立 subagent** 在自己的上下文里干活，返回 1 行简报就销毁 → 主会话只留简报，长跑**不爆上下文、不风格漂移**。worker 每 3 分钟优化 1 张，reviewer 每 15 分钟质检一批。

━━━ 开始 ━━━

帮我启动 loop v2，持续优化面试手机速查页（`learning/interview-tools/stealth.html`）为"照念就能答好"的可念答案。本会话已是 bypassPermissions 模式，所有操作免确认。

## 前置检查
1. 确认已是 bypassPermissions 模式（用 `--dangerously-skip-permissions` 启动，或 settings 里设了）——若不是，停下来告诉我，别继续。
2. 任务说明文件就位：`.claude/loop-worker.md`、`.claude/loop-reviewer.md`、`.claude/loop-review-log.md`。

## 启动（两个 cron）
**A. Worker cron**（每 3 分钟优化 1 张）—— CronCreate 参数：`cron="*/3 * * * *"`, `recurring=true`, `durable=true`，prompt 逐字用下面这段：
> 派一个 general-purpose subagent，把 `D:/work/linze-journal/.claude/loop-worker.md` 的内容作为它的任务说明逐字执行。它返回 1 行简报后，你只需原样转述给我，不要自己读文件/改代码/跑 git。若它回传的内容含"DONE"或"预算用尽"，用 CronList 找到本 worker cron 的 job-id 并 CronDelete 它，告诉我 worker loop 已自动停止。

**B. Reviewer cron**（每 15 分钟质检）—— CronCreate 参数：`cron="8,23,38,53 * * * *"`, `recurring=true`, `durable=true`（分钟偏移，避开 worker 的 `*/3` 同分钟触发，降低两者并行写同一文件/git 的冲突），prompt 逐字用下面这段：
> 派一个 general-purpose subagent，把 `D:/work/linze-journal/.claude/loop-reviewer.md` 的内容作为它的任务说明逐字执行。它返回 1 行简报后原样转述，不要自己读文件/改代码。若回传含"DONE"，用 CronList 找到本 reviewer cron 的 job-id 并 CronDelete 它，告诉我 reviewer loop 已自动停止。

**C. 立即手动派一次 worker subagent**（按 A 里同样方式，不等首次 cron 触发），确认 round 1 跑通：全程不弹权限、div 自检输出 0、push 成功。跑通后告诉我两个 cron 的 job-id，我就可以走了。

## 停止 / 调整
- 停止：跟我说"停 loop"（你 CronList + CronDelete 两个），或各自 DONE 自停，或 7 天后自动过期。
- 调整频率：跟我说，改 CronCreate 参数（如 worker `*/2` 更快、`*/5` 更慢）。
- 人工复核入口：`.claude/loop-review-log.md`（reviewer 判"已放弃·需人工"的卡）。

━━━ 结束 ━━━

## 备注（给我自己看的，不用给 Claude）
- **纯自动的关键**：用 `claude --dangerously-skip-permissions` 启动（或 settings `defaultMode: bypassPermissions`）。这是绕过"cd+重定向""cd+git"两条安全硬规则的唯一可靠方式——allowlist 无论怎么加都绕不过这两条。
- 命令形态也已去 cd 作双保险：搜文件用 Grep 工具、awk 绝对路径无 cd、git 用 `git -C d:/work/linze-journal`。即使 subagent 偶尔自由发挥写了带 cd 的命令，bypassPermissions 模式下也不会弹窗。
- 固定间隔双 cron：worker `*/3`（~20 张/小时）、reviewer `8,23,38,53`（每 15 分钟偏移，避并行写冲突）。两者每轮派完 subagent 就 idle，REPL 大部分空闲，两个 cron 都能触发。
- 3 min 间隔下若某轮 subagent 耗时 >3 min：该次触发时 REPL busy，自动跳过，等下个 idle，不堆积。
- 每轮独立 subagent → 主会话只留 1 行简报，长跑不爆上下文（核心优势与速度无关）。
- marker 状态机：无标记 → `待复核` → `已复核` / 退回无标记(带 `<!-- loop-retry:N 原因 -->`) / `已放弃`(入 review-log)。
- 任务有界：当前 ~143 张待优化，一晚基本跑完 → worker DONE 自删；待复核清空后 reviewer 也 DONE 自删。
- v1（`loop-启动prompt.md`）已删除。
