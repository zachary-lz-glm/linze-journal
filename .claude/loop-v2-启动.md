# 手机速查页 loop v2 — 启动 prompt（单 cron 串行 + 独立 subagent）

> **用法（纯自动，必须）**：在 `d:\work\linze-journal` 目录用 **`claude --dangerously-skip-permissions`** 开新会话（彻底免人工确认）。然后把下面"━━━ 开始 ━━━"到"━━━ 结束 ━━━"整段粘贴，保持会话开着即可走人。
> （已在 `settings.local.json` 设 `bypassPermissions` 兜底；CLI flag 最稳，二选一即可。）
>
> **核心机制**：**单个** cron 每 3 分钟触发一次，每次**只派一个** subagent（worker 或 reviewer），**串行零并发** → 不再有双 cron 同分钟撞车问题。每轮 subagent 在自己上下文里干活、回 1 行简报即销毁 → 主会话只留简报，长跑不爆上下文、不风格漂移。

━━━ 开始 ━━━

帮我启动 loop v2，持续优化面试手机速查页（`learning/interview-tools/stealth.html`）为"照念就能答好"的可念答案。本会话已是 bypassPermissions 模式，所有操作免确认。

## 前置检查
1. 确认已是 bypassPermissions 模式（用 `--dangerously-skip-permissions` 启动，或 settings 里设了）——若不是，停下来告诉我，别继续。
2. 任务说明文件就位：`.claude/loop-worker.md`、`.claude/loop-reviewer.md`、`.claude/loop-review-log.md`。
3. 先 `CronList` 一下，若有残留的旧 loop cron（worker/reviewer 两个），全部 `CronDelete` 掉，避免新旧重复跑。

## 启动（单个 cron，串行）
CronCreate 参数：`cron="*/3 * * * *"`, `recurring=true`, `durable=true`，prompt 逐字用下面这段：
> 你是单 cron 串行调度器。每轮**只派一个** subagent（绝不并行派两个），规则：
> 1. 默认派 worker：派一个 general-purpose subagent，把 `D:/work/linze-journal/.claude/loop-worker.md` 作为任务说明逐字执行，回传 1 行简报后转述给我。
> 2. 每累计派完 **4 个 worker**，下一轮改派 reviewer：派一个 general-purpose subagent 执行 `D:/work/linze-journal/.claude/loop-reviewer.md`，转述其 1 行简报，然后继续派 worker。
> 3. 一旦某轮 worker 回传含"DONE"或"预算用尽"（无卡可改了），后续每轮都改派 reviewer；当 reviewer 也回传"DONE"（待复核清空）→ 用 CronList 找到本 cron 的 job-id 并 CronDelete 它，告诉我全部完成已自动停止。
> 4. 全程不要自己读文件/改代码/跑 git，只派 subagent + 转述 1 行简报。计数或状态忘了没关系，**默认多派 worker**（worker 优先），节奏大致对即可。

**立即手动派第一个 worker subagent**（按上面方式，不等首次 cron 触发），确认 round 1 跑通：全程不弹权限、div 自检输出 0、push 成功。跑通后告诉我 cron 的 job-id，我就可以走了。

## 停止 / 调整
- 停止：跟我说"停 loop"（你 CronList + CronDelete），或全 DONE 自停，或 7 天后自动过期。
- 调整频率：跟我说，改 cron 参数（`*/2` 更快、`*/5` 更慢）。
- 人工复核入口：`.claude/loop-review-log.md`（reviewer 判"已放弃·需人工"的卡）。

━━━ 结束 ━━━

## 备注（给我自己看的，不用给 Claude）
- **单 cron 串行**：每 3 分钟一个 subagent，worker:reviewer ≈ 4:1，**零并发不撞车**。每 5 轮（~15min）一次 review（4 张），跟得上 worker 产出。
- 串行零并发 → 不再有双 cron 同分钟撞车导致的 git `index.lock` / push non-fast-forward 冲突。
- 每轮独立 subagent → 主会话只留 1 行简报，长跑不爆上下文（核心优势与速度无关）。
- **纯自动的关键**：`claude --dangerously-skip-permissions`（或 settings `defaultMode: bypassPermissions`）。这是绕过"cd+重定向""cd+git"两条安全硬规则的唯一可靠方式——allowlist 绕不过。命令去 cd 双保险：git 用 `git -C`、搜索用 Grep 工具、awk 绝对路径。
- marker 状态机：无标记 → `待复核` → `已复核` / 退回无标记(带 `<!-- loop-retry:N 原因 -->`) / `已放弃`(入 review-log)。
- 任务有界：当前 ~143 张待优化；worker DONE 后改派 reviewer 清待复核，reviewer 也 DONE → cron 自删全停。
- v1（`loop-启动prompt.md`）已删除。
