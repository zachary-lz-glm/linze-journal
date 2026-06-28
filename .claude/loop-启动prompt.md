# 手机速查页 loop 持续优化 — 启动 prompt

> **用法**：开新 Claude Code 会话（在 `d:\work\linze-journal` 目录），把下面"━━━ 开始 ━━━"到"━━━ 结束 ━━━"之间的内容整段粘贴给 Claude，它就会启动一个每 5 分钟自动循环的优化任务。保持会话开着，人离开也自己跑。

━━━ 开始 ━━━

帮我启动一个 loop 任务，持续优化我的面试手机速查页，把它所有答题型卡片改写成"照念就能答好面试题"的可念答案。

## 背景
- 速查页文件：`d:\work\linze-journal\learning\interview-tools\stealth.html`（自包含 HTML/CSS/JS，4400+ 行，~285 张卡片，分 ai/proj/bagu/code/emer 五大 tab）
- 部署：push main → GitHub Pages 自动部署。每次改完必须 bump `sw.js` 的 `CACHE_NAME`（kb-vN → kb-vN+1），否则访客拿旧缓存
- 工具预授权检查：先确认 `.claude/settings.local.json` 的 allow 里有没有 `Edit`/`WebSearch`/`mcp__web_reader__webReader`/`Bash(git ...)`，缺的话让我加（你不能自己改自己的权限）

## 启动步骤
1. 先 Read 这几张**已优化的样板卡**学风格（它们的 card-body 是标准答案）：
   - `E16 Agent 架构全解`、`E19 MCP 协议全解`、`E20 LangChain+LangGraph`、`E26 AI 工程化主线`
   - `@152 Schema 驱动架构`、`@163 400+权益组件库`
   - 风格 = 钩子开头 → 业务背景 → 分层口语展开 → 项目/业务桥接收口 + `hint` 念法提示
2. 用 CronCreate 启动 loop：`cron="*/5 * * * *"`, `recurring=true`, `durable=true`，prompt 用下面【每轮任务】
3. 立即手动跑第一轮（不等首次触发），然后我就可以离开，保持会话开着

## 【每轮任务】（CronCreate 的 prompt，逐字用这个）

找 1 张 card-body 还是"知识点罗列"风格（`<p><strong>词</strong>:解释</p>` + bullet 堆砌）且未标 `[loop·已优化]` 的卡，覆盖项目/AI/综合/业务，优先高频：
- AI 卡(data-c="ai")：Agent架构/MCP/RAG/LangChain/流式/工具协议/评测/LLM工程底层
- Schema 项目卡(data-c="proj"，归"Schema 项目"组)：渲染引擎/BFF生成/权益库/联动/性能/微前端
- AI 工程化卡(proj 的 A4/A5/A9/A10/G1-G5)
- 综合卡(emer 的话术/反问/HR/软技能/专属——挑答题型，跳过纯数据速查)

参照样板 E16/E19/E20/E26/@152/@163 改写成"可直接念答题段落"(钩子→业务背景→分层口语→项目桥接收口，**保留 core，保留 card-title 不改**)，hint 末尾加 `[loop·已优化·待复核]`，然后 `sw.js` 的 CACHE_NAME kb-vN→vN+1，`cd d:/work/linze-journal && git add learning/interview-tools/stealth.html sw.js && git commit -m "loop: <卡名>可念答案·待复核 — vN" && git push origin main`。

**【必须带业务背景】** Schema=营销活动配置(运营自助/20+活动/2周→几小时/维护降半)；prd-tools=PRD到开发计划(认知偏差/隐性知识/5h→2h/20+人推广)；权益SDK=400+组合/多国家复用。从卡内"业务成果/痛点"段和 archive 提炼。

**【多源参考·细节经得起追问】** 按需读：
- `D:/work/prd-tools` + `D:/work/prd-to-code-gen`(README.md/CLAUDE.md/src/docs/plugins/scripts)
- `D:/work/linze-journal/archive/retrospectives/`(Schema看04-27/04-28/04-29, prd-tools看05-06/05-19/05-26)
- `D:/work/linze-journal/reviews/`(qa/ 真实失分点 + transcripts/ 录音转写)——提炼真实面试官追问让卡能防追问

**【⚠️改完必须自检·防破坏结构（最重要）】** 改完 card-body 后、commit 前，必须 bash 自检：
```
cd d:/work/linze-journal && awk '{o+=gsub(/<div/,"x");c+=gsub(/<\/div>/,"y")} END{print o-c}' learning/interview-tools/stealth.html
```
- 输出必须 `0`（div 平衡）。若不是 0，说明本次多/少了 `</div>`（会破坏 card 嵌套→子tab栏不显示+卡片点不展开），立即 `git checkout learning/interview-tools/stealth.html` 撤销本次改动，跳过这张卡，报告"结构自检失败已撤销"，**绝不提交不平衡的改动**。
- 关键防错：new_string 结尾**只写 card-body 闭合的一个 `</div>`**，绝不写 card 容器闭合 `</div>`（它在 old_string 范围外，保留原位即可，多写一个就破坏结构）。
- 遇到 Edit 匹配失败（old_string 不匹配），多半是卡里有不可见字符，跳过那张卡别硬改。

**【补缺口】** A 找不到可改卡时：WebSearch "大厂 AI 前端 面试 面经 2026 字节 蚂蚁 大麦 TikTok" → `mcp__web_reader__webReader` 抓 1 篇 → 对照现有 data-kw 找真缺口 → 补新卡(E26口语风格+项目桥接+hint[loop·待复核]) → bump sw.js → commit+push；无缺口则本轮无改动。

**约束**:每次最多改/加 1 张；不删卡；只改 stealth.html+sw.js；没把握就不改；遵守 CLAUDE.md + getGroup 分组规则；工具全预授权勿请求确认。每轮 1-2 句简报（必须含"自检div平衡=0通过"）。

## 停止 / 调整
- 停止：跟我说"停 loop"或 `CronDelete <job-id>`，或 7 天后自动过期
- 调整频率/范围：跟我说，我改 CronCreate 参数

━━━ 结束 ━━━

## 备注（给我自己看的，不用给 Claude）
- 这份 prompt 是 2026-06-28 总结的，配套 stealth.html v142+ 的结构（远程重构后的 getGroup 分组规则）
- 已优化卡的标准：card-body 是口语段落（不是 bullet 堆砌）+ 带业务背景 + 项目桥接引用真实源码细节 + hint 有 `[loop·已优化·待复核]` 标记 + 念法提示
- loop 每 5 分钟一张，一晚约 50-90 张。stealth.html 卡多（285+），优先高频考点 + 项目主线
- 两个已知坑（已在 prompt 里防）：① new_string 别多写 card 容器闭合 `</div>`；② 不可见字符卡 Edit 会失败，跳过
