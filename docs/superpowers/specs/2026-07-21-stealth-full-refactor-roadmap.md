# stealth.html 整体表达重构 · 行动指南(下个会话接力蓝图)

> 给下个会话:本会话(2026-07-21)上下文已满,这份是接力蓝图。**读完直接开 `superpowers:brainstorming`**,拿本指南当输入。
> 本会话已完成:Agent 三件套(Manager/Code/PRD)三张主陈述卡五步逐字稿(commit `9cec423`)。方法论已沉淀到 memory([[stealth-project-storytelling]] 等)。
> 整合来源:本会话四篇精读 + 另一个 agent 的 GUIDE v2 分析 + opendesign 一面转写诊断 + CLEAR 校正。

---

## 1. 诊断:问题不在单卡,在所有项目卡的叙事方式

opendesign 一面转写暴露的根因(另一个 agent 精读得出):
- **不是沟通能力差**——讲别人产品(opendesign 灵感按钮 11:28:"能把好的网站通过固定化模式抽离复用")清晰、有判断、有热情;讲自己项目(39节点/18工具)就填充词、流水账、自我矮化。
- **是"讲自己项目没做过反思性准备"**——没想过"我为什么这么做、代价、换我会怎么改",所以一被追问就掉回时间线复述。
- 面试官诊断原话(10:46):"要再多准备怎么介绍表达自己做过的项目……更要深入挖掘亮点,有条理有组织地讲出来。"

**opendesign 一面 4 个失分点(逐条):**

| 时刻 | 问什么 | 你的原话/崩点 | 反模式 |
|---|---|---|---|
| 05:47 | Claude Code dynamic workflow 对比 | "可能可能可能…他可能自主进化更好" 纯填充词 | 选型讲不出"我vs他们"权衡 |
| 06:45 | 为什么39节点不是更少 | 答 HISTORY(单代理→多路由→流式→堆起来)不是 WHY | 叙事流水账(必读#1头号反模式) |
| 07:34 | 18工具(本有5步主线) | 主动自我矮化"学习目的、看起来冗余复杂" | 缺 CLEAR 的 L |
| 09:51 | Cursor 企业版 | 报菜名只到产品面,被"能看源码吗"追穿 | 浅层 namedrop 无深度 |

一句话:这场输在哪,和必读#1反例几乎一模一样——讲"做了什么/怎么长大",不讲"为什么决策、代价、换我会怎么改"。

---

> **主轴(用户定调):下个会话不要另起方法论炉灶。commit `9cec423` 的三张主卡(stealth.html 里 Manager/Code/PRD 主陈述卡)就是黄金标尺——整体重构是把这套已验证的范式复制扩展到其余项目卡,新卡先读那三张对标仿写。** 以下方法论是对那三张卡"为什么这样写"的拆解,不是要学的新东西。

## 2. 方法论(四篇精读 + CLEAR校正 + opendesign解药,已整合)

### 核心框架
- **CLEAR(校正版)** = Context / **L**eadership(为什么是你) / Execution / Accomplishment-Results。L 是它相对 STAR 的精华。⚠️带 Reflection 的是 CARL/STAR+L,**不是** CLEAR——之前把 CLEAR 的 L 当 Reflection 是错的。
- **主陈述卡五步逐字稿骨架**(本会话验证有效):①业务问题+ownership ②本质矛盾 ③关键决策+拒绝了什么 alternative ④结果+eval非vibes+成本 ⑤方法论+局限/下次。core=30秒钩子。

### 6 个失败→解药(对症下药)

| 你的失败 | 解药 | 来源 |
|---|---|---|
| 叙事流水账(39节点) | 倒着写(**tentpole**):先立 climax 决策再砍背景;自检"是不是 spreadsheet story" | Formation.dev |
| 答不出"为什么X不是Y" | **5层Why**:表层→工程→业务→战略→反思;卡2-3层=面试会散的地方 | zsc第4章 |
| 选型讲不出我vs他们 | **三段推理链**:考虑A/B/C→选B因为→代价是→用D补偿 | 知乎·思考路径 |
| 自我矮化("学习/冗余") | **CLEAR的L**:讲项目前先立"为什么是我/独特价值",戒"只是学习"开场 | CLEAR校正 |
| 被追穿(Cursor源码) | **诚实边界4步**:承认边界→展示相关知识→推理尝试→学习意愿 | zsc·知识盲区 |
| 讲完事实就停 | **+Reflection**:"做前以为X,做完发现Y,下次Z",事实拔成可复用判断 | CARL/STAR+L |

### 改写示范(把"39节点"救回来,tentpole+5Why+trade-off)
> "39 不是设计目标,是结果——每个节点对应一个我想显式解决的决策或踩过的坑。核心决策是 probe 排 plan 前:先并行探一遍下游再让模型规划,否则模型脑补下游状态。为什么不少点?简单任务5节点够,但我做这项目就为验证'复杂多步+人工确认+失败恢复'能否工程化,所以每种情况都做显式节点——好处是可观测/可单测/每条边能讲清,代价是配置复杂。(诚实边界)本质研究型没接真实流量,但正因为研究目的每个机制都做显式,反而每个'为什么'都答得出。"

### 风格铁律(四篇+本会话)
- **impact not technology names**(不堆栈,alexeygrigorev)
- **eval 非 vibes**,有 metrics(alexeygrigorev "actual eval framework or vibes?")
- **acknowledge gaps still get hired**(诚实边界是加分)
- 逐字稿口语连贯能念,但避 §6 碎嘴(说白了/得说句实话/我自己比较得意/被问X我答)
- **strong 标句首自然词**(不孤立、念着不顿)
- 30秒压缩版 = core(myengineeringpath Communication Compression)

### 四篇来源精要
- **moderndescartes**《ML/AI Interviewing》:Project Deep Dive 5维(motivation/problem/difficulties/impact/ancillary)、collaborative 非 skeptical、关注"how you personally experienced"
- **alexeygrigorev**《Project Deep Dive》:5把追问钻头(Business/Decisions/Problems/Evaluation/Learning)、6评估维度、"frame around impact not tech names"、"why not alternatives, what did you reject"
- **掘金·证据链**:入口 vs 证据、简历四列(岗位能力/项目证据/追问入口/复盘材料)、结论-场景-取舍-结果-复盘、5个为什么
- **myengineeringpath**《AI Engineer Guide》:11段模板、30秒版、6 signals(Demo vs Production/Cost/Trade-off/Failure Mode/Architectural Clarity/Communication Compression)

---

## 3. 重构范围与优先级

- **P0** proj 老前端项目卡:Schema驱动 / 权益组件库 / 联动引擎 / Monorepo / BFF。已有故事卡(STAR逐字稿/架构决策故事/推广故事/事故反思)但叙事方式旧,按 CLEAR-L + 五步 + tentpole 重写。
- **P1** proj 机制弹药卡(76张)按**追问链**重组:alexeygrigorev progressive questioning,卡按"追问深度"排序,补 ownership/alternatives/eval 维度。
- **P2** ai 分类项目相关卡(Agent/RAG/系统设计)按 impact-not-tchnames 标尺扫一遍。
- **不动** bagu/code/open 基础题(非项目表达)。
- **补** 每项目一张「实现细节深挖卡」(用户要求,如 PRD 的 reference/prd-distill 具体怎么设计)。

---

## 4. 执行流程(下个会话 superpowers)

1. **`superpowers:brainstorming`**:用本指南作输入,和用户细化 P0/P1 范围、每类卡模板、优先级 → 出 spec(存 `docs/superpowers/specs/`)。
2. **`superpowers:writing-plans`**:分批 plan(每批一个项目或一类卡),每批独立 commit+push。校验先行(check_mastercard.py 模板已在历史 commit 9cec423 前的 plan 里,可复用思路)。
3. **执行(inline 或 subagent-driven)**:多 agent,每 agent 一个子模块。⚠️**每 agent prompt 写死"只动指定文件,禁碰其他文件"**(见 memory [[agent-scope-constraint]]——本会话 Code agent 越权重写 GUIDE 的教训)。校验脚本 + §1.3 雷区抽检 + bump sw.js(看 origin +1) + 个人账号 push。

---

## 5. 铁律约束(本会话 + GUIDE 沉淀)

- **校准 §1.3 雷区**(说了穿帮):
  - Manager:qwen-flash 非 Claude/GPT;12 Agent=9外+3内;失败归因纯规则非 LLM;自动晋级默认关;Checkpoint 自建16字段
  - Code:自研 JSON+内存余弦(非 Chroma);sha256 增量(非 git 钩子);无 Diff 预览确认/独立审查 Agent/HITL 写确认
  - PRD:prd-tools 是 Claude Code 插件(/reference+/prd-distill);"prd2code-gen 6步闭环"**不存在**;"20+人"软化(ADR-0005 写1-5人)
  - 源码核对路径(mac):`/Users/didi/work/agent-main/Manager_Agent/` 和 `/Users/didi/work/agent-main/code_assistent_Agent/`
- **风格标尺**:参考卡「从PRD到上线的完整链路」(A10,declarative);主陈述卡逐字稿口语但避碎嘴;strong 句首自然词。
- **agent 范围约束**:prompt 写死只动目标文件,产出后 `git status` 确认。
- **bump sw.js**:看 origin 已部署版本 +1(GUIDE §4.7),当前线上 kb-v323。
- **个人账号** push(`github-personal:zachary-lz-glm`)。

---

## 6. 待调研(本会话未做,下个会话或另开)

- **跨场挖模式**(另一个 agent 建议方向1,**最值**):`reviews/` 40+ 实录(阿里/字节/快手/小红书/腾讯/拼多多)挑 3-5 场系统读,提炼跨场复现的 **Top3 表达失分模式**——比单场诊断可靠,能告诉你"哪类公司/哪类问题最易崩"。opendesign 单场诊断已验证方法有效。
- **读牛客失败还原**(nowcoder.com/discuss/353159350548111360)识别症状——里面那个三面讲不出亮点的候选人就是同款。
- **扩 bibliography**:AI 工程师系统设计怎么答、反问怎么问显深度、英文 senior behavioral storytelling。

---

## 附:本会话产出索引(下个会话可回看)
- spec:`docs/superpowers/specs/2026-07-21-stealth-proj-mastercards-design.md`(三张主卡设计)
- plan:`docs/superpowers/plans/2026-07-21-stealth-proj-mastercards.md`(7 task 实施计划)
- 上线 commit:`9cec423`(Manager/Code/PRD 三张主卡五步逐字稿 + sw.js kb-v323)
- memory:[[stealth-project-storytelling]] / [[agent-scope-constraint]] / [[stealth-full-refactor-roadmap]]
