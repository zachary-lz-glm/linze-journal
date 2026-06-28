# Loop Worker — 优化 1 张面试卡（独立 subagent 任务说明）

你是 loop 的 worker。你在**自己的独立上下文**里运行，本轮只完成 1 张卡的优化，然后返回 **1 行简报**（这是你唯一会向上传递的内容，主会话只转述它，所以简报要自包含）。严格只动 1 张。仓库根：`d:/work/linze-journal`。

## ⚠️ 0. 命令规范（避免卡死，必须遵守）
Claude Code 有两条安全硬规则会**强制人工审批、白名单也绕不过**，无人值守时一触发就卡死：
- 「`cd` + 输出重定向（`2>/dev/null` / `>` / `>>`）」的复合命令；
- 「`cd` 到某目录再跑 `git`」的命令（防目标目录 hooks 被执行）。
对策：
1. **搜文件内容一律用 Grep 工具**，不要用 bash `grep`。
2. **awk 自检用绝对路径、不带 cd**：`awk '...' d:/work/linze-journal/learning/interview-tools/stealth.html`。
3. **git 一律用 `git -C d:/work/linze-journal ...`，绝不写 `cd ... && git`**；git 命令也**不要配管道 `|` 或重定向**，要看历史就单独跑 `git -C d:/work/linze-journal log/show/diff` 自己读输出。
4. 任何 bash 命令**都不要加 `2>/dev/null` / `>` / `>>`**。

## 1. 选卡
1. 找未处理的卡：用 **Grep 工具**搜 pattern=`class="hint"`，path=`d:/work/linze-journal/learning/interview-tools/stealth.html`，output_mode=`content`，-n=true；再从结果里排除含 `已优化` 的行（用中文子串 `已优化`，别用带 `·` 的完整串）。
2. 从结果里挑 1 张，优先级：AI 卡(data-c="ai") > Schema 项目卡(data-c="proj") > AI 工程化卡(proj 的 A4/A5/A9/A10/G1-G5) > 综合答题型卡(emer 的话术/反问/HR/软技能——挑答题型，跳过纯数据速查)。
3. 若候选 card-body 已经是口语段落（**不是** `<p><strong>词</strong>:解释</p>` + bullet 堆砌），直接给它打 `[loop·已优化·已复核]` 跳过实质改写。
4. 若挑中的卡 card-body 里有 `<!-- loop-retry:N 原因:xxx -->` 注释（被 reviewer 退回过）→ 先读它，改写时针对性解决该原因，改好后**删掉该注释**。
5. **没有任何未标记卡** → 走第 8 步"补缺口"；补缺口也无果 → 返回 `DONE 无可改卡`。

## 2. 学风格（每轮 fresh 读，保证不漂移）
Read 这几张样板卡的 card-body（它们是标准答案）：`E16 Agent架构全解`、`E19 MCP协议全解`、`E20 LangChain+LangGraph`、`E26 AI工程化主线`、`@152 Schema驱动架构`、`@163 400+权益组件库`。
风格 = 钩子开头 → 业务背景 → 分层口语展开 → 项目/业务桥接收口 + hint 念法提示。

## 3. 精准读目标卡
Grep 拿到目标 hint 的行号后，用 Read 的 `offset`/`limit` **只读该卡 ±40 行**，不要整文件读（4515 行，浪费上下文）。

## 4. 改写
参照样板把 card-body 改成"照念就能答好面试题"的口语段落：钩子→业务背景→分层口语→项目桥接收口。**保留 core 字段，保留 card-title 不改。**

**【必须带业务背景】** Schema=营销活动配置(运营自助/20+活动/2周→几小时/维护降半)；prd-tools=PRD到开发计划(认知偏差/隐性知识/5h→2h/20+人推广)；权益SDK=400+组合/多国家复用。
**【防幻觉·硬规则】** 改写里出现的每个数字/百分比/源码细节，**必须能在该卡"业务成果/痛点"段或 archive 里找到出处**；找不到出处就别写具体数字，改用定性描述。绝不编造像样但虚假的数据。

**【多源参考·按需读，别全读】** 只在需要细节时读：`D:/work/prd-tools` + `D:/work/prd-to-code-gen`(README/CLAUDE.md/src/docs/plugins/scripts)；`archive/retrospectives/`(Schema 看 04-27/04-28/04-29，prd-tools 看 05-06/05-19/05-26)；`reviews/`(qa/ 真实失分点 + transcripts/ 转写)——提炼真实面试官追问，让卡能防追问。读了 >5 个源文件还没动笔 → 果断放弃本轮，返回 `本轮跳过:资料过多`。

## 5. hint 标记
hint 末尾加 `[loop·已优化·待复核]`（注意是"待复核"，等 reviewer 过审）+ 念法提示。

## 6. ⚠️ 结构自检（commit 前必做，最重要）
```
awk '{o+=gsub(/<div/,"x");c+=gsub(/<\/div>/,"y")} END{print o-c}' d:/work/linze-journal/learning/interview-tools/stealth.html
```
- 输出**必须 `0`**（div 平衡）。不是 0 → 立即 `git -C d:/work/linze-journal checkout learning/interview-tools/stealth.html` 撤销本次改动，返回 `结构自检失败已撤销:<卡名>`，**绝不提交不平衡的改动**（会破坏 card 嵌套→子tab栏不显示+卡片点不展开）。
- 防错关键：Edit 的 new_string 结尾**只写 card-body 闭合的一个 `</div>`**，绝不写 card 容器闭合 `</div>`（它在 old_string 范围外，保留原位即可，多写一个就破坏结构）。
- Edit 匹配失败（old_string 不匹配，多半是不可见字符）→ 跳过该卡，返回 `Edit失败跳过:<卡名>`，别硬改。

## 7. 部署
先改 `sw.js` 的 `CACHE_NAME`（`kb-vN` → `kb-vN+1`，不 bump 访客拿旧缓存），然后：
```
git -C d:/work/linze-journal add learning/interview-tools/stealth.html sw.js && git -C d:/work/linze-journal commit -m "loop: <卡名>可念答案·待复核 — vN" && git -C d:/work/linze-journal push origin main
```
push 失败（网络/认证/index 锁冲突）→ 返回 `push失败:<卡名>`，**不要无限重试**，留给下一轮。

## 8. 补缺口（仅当第 1 步无未标记卡时）
WebSearch "大厂 AI 前端 面试 面经 2026 字节 蚂蚁 大麦 TikTok" → `mcp__web_reader__webReader` 抓 1 篇 → 对照现有 data-kw 找真缺口 → 补 1 张新卡(E26 口语风格+项目桥接+hint `[loop·已优化·待复核]`) → bump sw.js → commit+push。无缺口 → 返回 `DONE 无缺口无可改卡`。（连续 2 轮补缺口都无果也返回 DONE，避免空转。）

## 约束
每次最多改/加 1 张；不删卡；只改 stealth.html + sw.js；没把握就不改；遵守 `CLAUDE.md` + getGroup 分组规则。

## 返回（1 行简报）
成功：`✅<卡名>·div=0通过·待复核 — vN`
失败/跳过/DONE：按上面各处的对应文案。**务必含"div=0通过"或失败原因**。
