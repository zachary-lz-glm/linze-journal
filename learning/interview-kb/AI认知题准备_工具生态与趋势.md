> **open design 类面试 · AI 认知题弹药库**（多 agent 联网研究 2026-07-20 + 主会话事实核实）
>
> 配套：`learning/interview-kb/明日面试_预测题校准与匹配分析.md`（项目事实 ✅⚠️❌ 清单）、`reviews/open-design_面试复盘_认知题方向修正.md`、`stealth.html`（手机速查）。
>
> ## ⚠️ 事实核实说明（防穿帮）
> - **模型版本号**（已 2026-07 联网核实，但迭代快，面试前刷新）：Claude Opus 4.8 / Sonnet 5 / Haiku 4.5 / Fable 5；OpenAI **GPT-5.6（Sol/Terra/Luna 三档，2026-07-09 发布）**；Google **Gemini 3.1 Pro**（2026-02，旗舰）+ 3.5 Flash；阿里 Qwen3；DeepSeek V3.2-Exp。
> - **coding agent 收购事件**（已核实）：Cursor 2026 收 Continue（acqui-hire，Continue 关停）；OpenAI $3B 收 Windsurf 黄了 → Google ~$2.4B licensing + 挖走 CEO → **Cognition（Devin 母公司）2025-07-14 收购 Windsurf 剩余资产，金额未披露，Cognition 后估值 $10.2B**。
> - **⚠️ 劲爆但用前必须再确认**：2026 传 **SpaceX $60B 收 Cursor 放 xAI**（Q3 交割，来源 Crunchbase）——这种大新闻面试官可能追问，要么核实到能讲细节、要么别提。
> - **候选人对项目相关的事实**（对照校准文档，准确）：Manager 部署 qwen 不是 Claude、自研向量不是 Chroma/Pinecone、没用 Neo4j、18 工具=11只读+7写、HITL 写确认/代码审查 Agent 未完整实现、没接真实流量。
> - **铁律**：任何百分比/倍数/团队规模，不确定就软化（"一个量级"/"小范围验证过"）或省略。模型/收购是易变信息，进场前花 10 分钟刷一遍官方博客。
>
> **用法**：第二节骨架背到"像聊天一样说出来"；第三节速查表背到"脱口而出"（日常用 AI / 工具对比题的弹药）；第五节"日常怎么用 AI"几乎必问，单独背。

---

# open design 类面试 AI 认知题准备

> 定位：上周 open design 被挂，面试官爱问认知/趋势/设计判断题（不关心实现）。这份材料解决两件事——能脱口而出"市面有啥/各家优劣"，以及能讲清"我为什么这么选、知道边界在哪"。
>
> 用法：第二节骨架背到能"像聊天一样说出来"；第三节速查表背到能"脱口而出"（这是日常用 AI / 工具对比题的弹药）；第五节是"日常怎么用 AI"的黄金答法，几乎必问。

---

## 一、预测问题清单（12 个高概率认知题）

按"面试官这次的考察模式"反推，他大概率从下面 12 个里挑 4-6 个问。按出现概率从高到低排：

| # | 问题 | 高频原因 |
|---|------|---------|
| 1 | **你日常怎么用 AI？用什么工具？工作流是啥？** | 几乎必问，开场破冰 + 探深 |
| 2 | **用过哪些 coding agent？Cursor/Claude Code/Devin/Cline 怎么比？** | 候选人简历有 Coding Agent，必被问生态 |
| 3 | **为什么选 LangGraph 不选 AutoGen/CrewAI？** | Manager 项目是核心，必问选型理由 |
| 4 | **Manager 为什么部署在 qwen 不上 Claude？** | 反直觉选择，面试官会追 |
| 5 | **workflow 和 agent 怎么区分？什么场景该上 agent？** | Anthropic 圣经题，认知题母题 |
| 6 | **MCP 是什么、为什么火、安全吗？** | 2026 最热协议，必问 |
| 7 | **怎么评估一个 agent / LLM 系统？** | 显工程化深度 |
| 8 | **怎么看 agent 可靠性 / AGI 时间表？** | 趋势判断题，没有标准答案 |
| 9 | **computer use / browser agent 怎么看？** | 前沿话题，显视野 |
| 10 | **长上下文 vs RAG 怎么选？** | 经典架构判断题 |
| 11 | **怎么跟进 AI 前沿？** | 显学习习惯，几乎必问 |
| 12 | **prompt injection / agent safety 怎么防？** | 候选人项目③强项，主动引过来 |

---

## 二、每题答题骨架

### Q1. 日常怎么用 AI？（见第五节详写）

> 几乎必问，专门单独写。一句话锚点：**分场景用，研发 Claude Code + 自己写的插件，部署 Agent 走 qwen，日常查资料用 ChatGPT/Claude.ai**。

---

### Q2. 用过哪些 coding agent？怎么对比优劣？

**① 考察点**：是否真懂生态、还是只看过营销稿；能否做"维度对比"而不是报菜名。

**② 答题要点**（4 句真人话）：
- "我把 coding agent 分三档：**IDE 内嵌**（Cursor、Copilot、Windsurf、Continue）、**终端/IDE 通用 CLI**（Claude Code、Cline、opencode、Aider）、**autonomous cloud**（Devin、OpenHands）——三档解决的问题完全不同。"
- "体验标杆是 Cursor——自研 Composer 模型 + Plan Mode + Background Agents，开发者写得爽的天花板。但我自己平时用 Claude Code 更多，因为它是 Agent SDK 当库暴露，我可以挂自己的 skill 进去。"
- "Devin 是 autonomous 标杆，parallel cloud agents 端到端 ship 代码，但黑盒云端，国内企业基本不敢把代码仓发出去。"
- "一个关键趋势：2026 C 端在剧烈整合——Cursor 收了 Continue、Cognition 收购 Windsurf 剩余资产（金额未披露，Cognition 后估值 $10.2B；OpenAI 30 亿黄了、Google ~24 亿 licensing + 挖走 CEO）、Devin 和 Windsurf 引擎在合并；差异化只能往'企业安全 + 可内网部署'走。"

**③ 关联项目③**："所以我的 Coding Agent 没去抢 Cursor 的 UX——我认输 polish。我卡的是另一条：**企业内网敢不敢让 agent 改生产代码**——JWT/scope/限流/路径白名单/sha256 锁/沙箱/原子写/审计这一层，Cursor/Claude Code 的 hooks 都做不到 first-class。一句话：**Cursor 解决'开发者写得爽'，我解决'企业敢不敢用'**。"

**④ 诚实边界**：不能吹"我比 Cursor 强"——明确说 UX/polish 全认输；Devin/OpenHands 的 benchmark 分数、社区规模也认输。我只在"企业治理深度"这一条上对标。

---

### Q3. 为什么选 LangGraph 不选 AutoGen/CrewAI？

**① 考察点**：框架选型理由 + 设计判断（不是看名气选）。

**② 答题要点**：
- "我有三个硬约束：**39 个节点 + 回环（critic 否决回 plan）+ HITL gate**，这是带全局状态的 DAG，不是几个角色对话。"
- "AutoGen/MAF 的核心抽象是 agent 之间对话轮次（group chat），CrewAI 是 sequential/hierarchical 的角色流水线——它俩根本表达不了'critic 看完 synth 结果决定要不要回炉'这种基于全局状态的回环。"
- "LangGraph 的 add_conditional_edges 是**硬编码路由、零 LLM 成本**——已知流程就该硬编码，只在 probe/route/critic 这种本质要语义判断的节点才调 LLM。CrewAI/AutoGen 那种 LLM 自主流转，每步多一次 LLM call，对已知流程是过度灵活、纯烧 token。"
- "判断点很清晰：**节点 ≤5 且线性 → CrewAI；对话式多角色 → AutoGen；节点 >10 + 回环 + HITL → LangGraph（唯一答案）**。"

**③ 关联项目②**："Manager 的 probe→route→plan→execute→synth→critic→finalize 这套已知流程，30+ 个边硬编码，只有 3-4 个节点真调 LLM——这就是 Anthropic《Building Effective Agents》里'workflow first'原则的落地。"

**④ 诚实边界**：要主动说 "Manager 是研究型、**没接真实流量**"——别让面试官以为这是生产系统；说清"如果节点数 < 10 我会选 CrewAI"，别显得只会 LangGraph。

---

### Q4. Manager 为什么部署在 qwen 不上 Claude？

**① 考察点**：模型选型的 ROI 判断（不是越贵越好）。

**② 答题要点**：
- "这是个**成本 × 并发 × 多副本**的算账问题。Manager 39 节点一次跑下来要调几十次 LLM，自进化 shadow / 金丝雀 / A/B 还要多副本并行实验——Qwen 输出比 Opus 便宜一个量级，Opus 月账单会爆。"
- "而且**国内合规直连**，不用走中转。Manager 是研究型没接真实流量，要的是迭代速度和成本可承受，不是单次推理质量最高。"
- "但同一个选型逻辑下，**我项目④ prd-tools 用的是 Claude 不是 qwen**——PRD 蒸馏的 Spec Review Gate 是防幻觉硬门禁，错了返工更贵，这时 Claude 的指令遵循和拒绝编造值这个钱。"
- "所以我的判断是：**研发工作流/防幻觉硬门禁用 Claude，生产 multi-agent / 成本敏感用开源**——不是越贵越好，是按节点负载分层。"

**③ 关联项目②③④**：三个项目刚好覆盖三种选型——Manager=qwen 跑量、Coding Agent=qwen+Claude Code 宿主、prd-tools=Claude 防幻觉。

**④ 诚实边界**：**不要报编造的"便宜 13 倍"具体倍数**（研究里是 "~13×"，我说"便宜一个量级"更稳）；别吹 qwen 性能"对标 Claude"——只说"agent 工具调用上够用，复杂多步推理/证据链严谨度仍略逊"。

---

### Q5. workflow 和 agent 怎么区分？什么场景该上 agent？

**① 考察点**：Anthropic 圣经题（2024.12《Building Effective Agents》），认知题母题。

**② 答题要点**：
- "**workflow = 预设路径编排 LLM**，**agent = LLM 自主决定路径和工具调用**——核心原则是'从最简方案开始，需要再加自主性'。"
- "判断口诀：**路径可枚举 → workflow；开放探索或工具组合不可预测 → agent**。Anthropic 给了 5 种 workflow 模式（prompt chaining / routing / parallelization / orchestrator-workers / evaluator-optimizer），从简到繁。"
- "2026 业界其实在回潮——大家发现 autonomous agent 在生产里不可控，企业级普遍退回到 durable deterministic workflow，autonomy 只在关键节点用。"
- "我自己的实践：**先 workflow 验证，再放权**——能用确定性就不上 LLM，能 workflow 就不上 autonomous agent。"

**③ 关联项目**："②Manager 39 节点是 workflow（边硬编码、LLM 只在节点内决策）；③Coding Agent 的 ReAct 双节点（think↔act、LLM 自选 18 工具）才是真 agent；①Schema 中台的字段 DAG + 拓扑排序+循环检测是**非 LLM 时代的 workflow orchestration**，正好说明这套思维我是从前端迁移过来的。"

**④ 诚实边界**：别把 Manager 说成 "autonomous agent"——它本质是 workflow；承认"workflow vs agent 的边界在模糊，multi-agent 系统里两者经常混用"。

---

### Q6. MCP 是什么、为什么火、安全吗？

**① 考察点**：协议认知 + 安全意识。

**② 答题要点**：
- "MCP（Model Context Protocol）是 Anthropic 2024.11 开源的标准协议，被比作'AI 的 USB-C'——把'**M 个模型 × N 个工具的接入问题从 M×N 压成 M+N**'，2026 OpenAI/Google 全采纳，事实标准了。"
- "底层是 JSON-RPC 2.0，灵感来自 LSP（语言服务器协议）；三个原语：**Tools（可执行）/ Resources（可读数据）/ Prompts（模板）**，加一个 sampling（反向调模型）。"
- "为什么火：因为它把'每接一个工具就写一遍胶水'这件事一次性解决，Cursor/Claude Code/Cline/我自己的 agent 通吃；Anthropic 还在推 Remote MCP + OAuth，押的是'**谁定义 agent 接工具的标准比谁家模型最强更长期**'。"
- "**安全是它最大的坑**——spec 自己写明'协议不强制安全'，2026 MCP Security Top 10 头两名是 **Unauthenticated Access + Confused Deputy（混淆代理）**，多数社区 server 没有任何 policy layer。"

**③ 关联项目③④**："我项目④ prd-tools 就是 Claude Code 的两个 skill（/reference + /prd-distill），所以 MCP 对我是日常不是新闻。我项目③ 那套 JWT/scope/限流/路径白名单/sha256 锁/沙箱/原子写/审计，正是在补 MCP 默认不给你的那层 policy——面试官问 MCP 安全我直接拿这套对照讲。"

**④ 诚实边界**：别吹"我解决了 MCP 安全问题"——只说"我在自己的 agent 里做了 first-class 治理"；承认 prompt injection 在学界被认为是"unsolvable"，我只能 defense in depth。

---

### Q7. 怎么评估一个 agent / LLM 系统？

**① 考察点**：工程化深度（demo 跑得通 ≠ 生产稳定）。

**② 答题要点**：
- "三层结构：**golden set（人工标注离线测试集，等同单测）+ LLM-as-judge（强模型按 rubric 评分）+ online eval（真实流量分布漂移检测）**——三层必须都做，单做离线 eval 抓不到生产漂移。"
- "2026 主流是把 eval 进 CI——Braintrust 那句'**evals are the new PRD**'是行业口号，意思是 eval 不只是测试，它就是产品定义。"
- "工具我会分场景选：**Promptfoo**（CLI + 500+ 断言 + 红队/越狱，像写单测）适合工具型 agent 红队；**LangSmith** 跟 LangGraph 深度绑、trace 到节点级；**Langfuse** 开源可自部署、被 ClickHouse 收了；**Braintrust** eval-first 全周期。"
- "可观测性侧，**OpenTelemetry GenAI semantic conventions 是厂商中立逃逸层**，2026 正在收敛成基线——一次埋点换后端，是避免厂商绑定的钥匙。"

**③ 关联项目②④**："Manager 用 LangSmith trace 到 39 节点每一跳（probe→route→...→finalize），不节点级 trace 根本不知道是 critic 还是 synth 在 fail；prd-tools 的 EV-XXX 证据链是把 eval 做成**硬门禁**（无 EV 引用直接 fail），比 LLM-as-judge 软分更可靠。"

**④ 诚实边界**：**这里一定要主动认局限显诚实**——"Manager 部署在 qwen、是研究型没接真流量，所以我只做了 offline eval + golden set，**online eval 是缺的，这是项目边界**"。这一句话比硬装懂更显 senior。

---

### Q8. 怎么看 agent 可靠性 / AGI 时间表？

**① 考察点**：前沿判断 + 不人云亦云。

**② 答题要点**：
- "可靠性我分两层看：**'能不能做对'这一层进步极快**——SWE-bench Verified 头部 ~80% 了（Claude Opus 4.8 80.8%），但已经趋饱和，行业转向 Terminal-Bench v2 / OpenHands Index / SWE-bench Pro 这些更难的基准。"
- "**'敢不敢上生产'这一层是真正的瓶颈**——agent 长任务数百次工具调用、cost 不可控、prompt injection 73%+ 生产部署中招、indirect injection 学界公认 unsolvable。这层不是模型能力问题，是工程治理问题。"
- "AGI 时间表我会分场景答：**单点任务超人**已经到了（写代码、做研究汇总）；**端到端可靠自治**还在远处——Karpathy 2026 自己都宣布 vibe coding 过时、进入 agentic engineering 时代，意思是 AI 真正上生产需要工程护栏，不是靠模型自己。"
- "我的判断：**未来 2-3 年不是 AGI 来不来，是'agent 工程化'能不能跑通**——谁把 reliability + safety + cost 三角解掉，谁就赢。"

**③ 关联项目③**："所以我的 Coding Agent 不是去抢 Devin 的 autonomous 高度，而是去补'企业内网 autonomous'的工程治理层——这是我对这个时代的押注。"

**④ 诚实边界**：别给具体 AGI 年份预测（"2027 AGI"这种话是雷）；说"我相信 scaling law"比说"我相信 AGI 快来了"安全。

---

### Q9. computer use / browser agent 怎么看？

**① 考察点**：前沿视野 + 边界判断。

**② 答题要点**：
- "Claude Computer Use、OpenAI Operator、Perplexity Computer，2026 从研究走向准生产——**表单填写、数据采集已经能用**，跨平台 GUI 控制还在成熟。"
- "它的价值是'**无 API 也能自动化**'的长尾场景，Anthropic 发布时同步出了 ASL-3 安全评估，说明它自己也知道风险。"
- "**短板是成本、延迟、可靠性三重问题 + blast radius 指数级放大**——agent 操作真实环境意味着它能误删、误购、误提交。"
- "我的判断口诀：**API 不存在且任务一次性 → computer use 合适；高频场景就该等 API 出现或自己封装**——computer use 是最后手段不是首选。"

**③ 关联项目③**："我没做过 computer use，但 Coding Agent 的沙箱哲学和它一脉相承——**agent 操作真实文件系统 ≈ agent 操作真实电脑，沙箱 + 白名单 + 审计是同一套范式**。"

**④ 诚实边界**：没做过就直接说"没做过"，然后讲"但范式同构"——比硬装做过强。

---

### Q10. 长上下文 vs RAG 怎么选？

**① 考察点**：经典架构判断。

**② 答题要点**：
- "2026 共识一句话：**'long context + caching when you can, RAG when you must'**——不是对立是互补，RAG 负责检索召回，long context 负责推理。"
- "三个不用长上下文直接塞的理由：**成本**（RAG 单查询便宜约 1250 倍）、**lost-in-the-middle**（中间信息准确率掉 30%+）、**塞得进窗口 ≠ 抽得准、不编造**。"
- "Gemini 1-2M 窗口最大但指令遵循/证据链弱于 Claude——这正是我 prd-tools 选 Claude 不选 Gemini 的关键：要的是结构化抽取的严谨度，不是单纯塞得进。"
- "**长上下文 ≠ 长注意力**，hybrid 架构（RAG 召回 + 长上下文推理）是 2026 默认。"

**③ 关联项目③④**："Coding Agent 自研 text-embedding-v3 + 内存余弦 + sha256 是一个 mini RAG——我刻意没上 Chroma/pgvector，因为代码语料是有限集（一个仓库几千文件），我要的是 sha256 **内容寻址的确定性**（可复现/可缓存/可审计），不是规模；prd-tools 的 PRD 蒸馏本质上是把'长上下文 RAG'转成'短 spec 直接进上下文'，蒸馏本身就是去噪。"

**④ 诚实边界**：**主动说边界**——"我的内存方案在几千文件量级是对的，但要到 Milvus 亿级场景完全是另一套工程，pgvector 是我的第一升级路径"。这种"知道天花板在哪"比假装自建能打一切有说服力。

---

### Q11. 怎么跟进 AI 剂前沿？

**① 考察点**：学习习惯 + 真伪鉴别。

**② 答题要点**（真人话）：
- "一手信息源为主：**Anthropic 工程博客**（《Building Effective Agents》《Effective Context Engineering》）、**OpenAI/Google 官方 release note**、**arXiv** 的 agent/RAG/eval 论文、各家 model card 和 system card。"
- "**benchmark 我盯 SWE-bench Verified / Terminal-Bench v2 / OpenHands Index / MCP-Atlas**——看头部分数 + 看新基准在解决什么旧基准解决不了的问题。"
- "社区侧：Hacker News、Reddit r/LocalLLaMA、Twitter 上跟 Karpathy、Simon Willison、Anthropic 几个 dev rel。"
- "**最关键是把用过的工具当信息源**——我自己写 Claude Code 插件，对 MCP 的能力边界就比看十篇文章深；自己跑过 LangGraph 39 节点，对 agent 框架的痛点就比看对比稿深。**用，是最高效的跟进**。"

**③ 关联项目④**："我做的 prd-tools 本身就是'跟进前沿'的方式——Anthropic 推 Skills，我就用 SKILL.md 模式写一个，写完才真的懂 Skills 的渐进式上下文加载思想。"

**④ 诚实边界**：别说"我每天看 50 篇论文"——不可信；说"一手源 + 用过的工具"更真。

---

### Q12. prompt injection / agent safety 怎么防？

**① 考察点**：项目③ 最强差异化资产，主动引过来。

**② 答题要点**：
- "**OWASP LLM Top 10 #1 连续多年是 Prompt Injection**，73%+ 生产部署中招；2026 OWASP 专门出了《Agentic Applications Top 10》（goal hijack / rogue agent / tool misuse）。"
- "学界共识是 prompt injection **'unsolvable'**——语义层没法用规则彻底防，**defense in depth 是唯一答案，不是单点**。"
- "工程化防御体系：**zero-trust 输入、最小权限、沙箱、JWT/scope、限流、路径白名单、sha256 锁、原子写、审计**——这一套叠起来才敢说'敢上生产'。"
- "**indirect injection（数据里藏指令）是行业级未解难题**——工具输出当 untrusted data，再过一道 gate，不直接进 system role。"

**③ 关联项目③**（这是候选人最强资产，列细一点）：
- "**只读 11 + 写 7 分开** = 最小权限"
- "**路径白名单** = 防目录穿越"
- "**sha256 锁** = 防工具内容被篡改（每个写工具挂 sha256，变了就 fail）"
- "**沙箱** = blast radius 控制"
- "**原子写** = 防半成品状态污染生产"
- "**审计** = 事后可追溯"
- "这一套是 OWASP LLM01-10 的工程化映射——比空谈'要对齐'强十倍。"

**④ 诚实边界**：别说"我解决了 prompt injection"——说"我做了 defense in depth 的工程化"，承认 unsolvable。

---

## 三、AI 工具速查表（必须脱口而出）

> 原则：**每项一句话定位 + 一句话优劣**，不展开。被问"了解哪些 X"时按这个背。背不到脱口而出就别在面试里提它。

### A. Coding Agent（5 个高频）

| 工具 | 一句话定位 | 一句话优劣 |
|------|-----------|-----------|
| **Cursor** | AI-first IDE 体验标杆，自研 Composer 模型 + Plan/Agent/Background Agents + MCP | 体验天花板；**默认信任开发者本人、无企业 JWT/scope/审计、Composer 锁死不能换 qwen** |
| **Claude Code** | Anthropic 官方 CLI/IDE agent，底层是 Agent SDK（Python/TS），可挂 skill 插件 | 生态最完整（subagents+hooks+MCP）；**强绑 Claude、治理是后加的开关不是 first-class** |
| **Devin（Cognition）** | 第一个 autonomous SWE，parallel cloud agents 端到端 ship 代码 | 功能标杆；**黑盒云端，国内企业不敢把代码仓发出去，价格贵** |
| **Cline** | VS Code/JetBrains 开源（Apache）agent，Plan/Act 双模式 + MCP，5M+ 安装 | 开源社区最大；**IDE 内单机 + 人工审批，无企业治理** |
| **Aider** | git-native 终端 pair programmer，每次改动 atomic commit | git 工作流原生 + 可审计；**面向个人 hacker，无多租户/企业治理** |

> 备用：**opencode(SST)** 开源 CLI 黑马 170K+ stars 75+ 模型 plan/build 双 agent；**OpenHands**（原 OpenDevin）72% SWE-bench、2026 推新 benchmark；**SWE-agent(Princeton)** + SWE-bench 是整个赛道源头，mini-SWE-agent ~100 行 Python 拿 74%。

### B. Agent 框架（5 个高频）

| 框架 | 一句话定位 | 一句话优劣 / 选型判断 |
|------|-----------|-----------|
| **LangGraph** | 把多 Agent 流程建模成有状态的、可循环的有向图，HITL 一等公民，2026 生产首选 | 确定性+可审计+checkpoint 一等公民；**API 啰嗦上手陡、过度自由把架构责任压给作者**。**节点>10+回环+HITL → LangGraph** |
| **Microsoft Agent Framework**（AutoGen+SK 合并） | 对话式多 Agent + 微软栈原生，2026-04 GA，支持 Python/.NET/Go | 对话式心智模型成熟+企业身份合规；**绑 Azure、对话式≠图编排、复杂状态管理弱于 LangGraph** |
| **CrewAI** | role-based crew 隐喻，每个 agent 有 role/goal/backstory，20 行起 demo | 上手最快；**表达不了回环/HITL/带状态复杂流程**。**节点≤5+线性 → CrewAI** |
| **OpenAI Agents SDK（原 Swarm）** | handoff 抽象 + sandbox + Temporal 集成（2026-03 GA） | 心智模型最简+OpenAI 原生+安全亮点；**多 Agent 深度不如 LangGraph、绑 GPT** |
| **Anthropic Skills + Agent SDK** | 不卖全家桶框架、卖 Skills（SKILL.md）+方法论（"workflow 优先于 autonomous agent"） | 思想引领全行业（《Building Effective Agents》是圣经）；**不是传统 multi-agent 框架，留给用户用 SDK 自拼** |

> 备用：**Google ADK** 绑 Gemini + 推 A2A 跨框架互操作；**LlamaIndex Workflows** 事件驱动、RAG/数据底子强、agent 侧弱；**MetaGPT** SOP 编码进 prompt、端到端、研究取向。

### C. MCP + RAG + Eval（6 个高频）

| 工具/概念 | 一句话定位 | 一句话优劣 |
|----------|-----------|-----------|
| **MCP** | Anthropic 2024.11 开源协议，"AI 的 USB-C"，把 M×N 接入压成 M+N | 事实标准、Anthropic+OpenAI+Google 全采纳；**spec 不强制安全、Confused Deputy 进 Top 10、社区 server 多无 policy layer** |
| **pgvector** | Postgres 向量扩展，中小规模 RAG 默认 | 复用 Postgres 事务/权限一手抓；**磁盘高 ~16.5GB、百万级后让位专用库** |
| **Qdrant / Pinecone** | Qdrant=Rust 开源省 RAM；Pinecone=全托管云原生 | Qdrant RAM 最低 ~5.1GB 适合自托管；Pinecone 免运维但**数据出域、成本随规模涨** |
| **GraphRAG（微软）+ LazyGraphRAG** | 从文本抽知识图谱+社区分层摘要，补 vector RAG 答不了的全局/跨文档问题 | LazyGraphRAG 2026 基准反超；**建图成本高（LLM 抽实体烧 token）、增量更新难、很多场景 hybrid 就够** |
| **LangSmith / Langfuse / Braintrust / Promptfoo** | LangSmith=LangGraph 原生 trace；Langfuse=OSS+被 ClickHouse 收；Braintrust=eval-first；Promptfoo=CLI 红队 | **"evals are the new PRD"** 是 Braintrust 口号；LangSmith 绑 LangChain 最深；Promptfoo 500+ 断言像写单测 |
| **OpenTelemetry GenAI** | 厂商中立的 LLM 可观测语义标准，2026 收敛成基线 | 一次埋点换后端（逃逸厂商绑定钥匙）；**纯 OTel 不带产品化 UI、要配后端** |

> 备用：**Agentic RAG（Self-RAG/CRAG）**=把检索当 tool call + 自我反思门禁，2026 生产新默认（但收益与领域强相关）；**Remote MCP + OAuth**=Anthropic 的基础设施牌。

### D. 模型（5 个高频，按 2026-07 版本）

| 模型 | 一句话定位 | 一句话优劣 / 价格 |
|------|-----------|-----------|
| **Claude（Opus 4.8 / Sonnet 5 / Haiku 4.5）** | Anthropic 全档矩阵；Opus 推理旗舰、Sonnet 主力、Haiku 小快 | 指令遵循/证据链最严谨、SWE-bench 80%+；**Opus 最贵 $5/$25 per MTok、国内无直连** |
| **GPT-5.6（Sol/Terra/Luna）** | OpenAI 2026-07 发布三档矩阵，Sol=旗舰 | 推理/编码/研究综合强+生态最成熟；**Sol 贵、国内无直连、上下文 ~400K 不如 Gemini** |
| **Gemini 3.1 Pro** | Google 旗舰，1M context + 原生多模态（含视频） | 上下文最长+视频多模态最强；**agentic 工具调用弱于 Claude、指令遵循/证据链不如 Claude 严谨** |
| **Qwen3（3.7 Max / 3.6 Plus / Coder）** | 阿里开源 frontier，agent 性价比王 | 开源可自部署+国内合规+agent 工具调用强（3.6 Plus MCP-Atlas 73.8%）+成本极低；**复杂多步推理/证据链略逊 Claude** |
| **DeepSeek V3.2-Exp** | 国产 ultra-low-cost 推理模型，被称 GPT-5 级 | **地板价 $0.14/$0.28 per MTok、cache hit $0.0028**；**工具调用/agentic 不如 Qwen/Claude、生态薄** |

> 口诀：**研发/防幻觉用 Claude，生产 multi-agent 用开源（Qwen 主力、DeepSeek 地板价）；不是越贵越好，按节点负载分层。**

### E. 趋势概念（8 个高频，认知题弹药）

| 概念 | 一句话定义 | 怎么用 |
|------|-----------|-------|
| **Workflow vs Agent** | workflow=预设路径、agent=LLM 自主决策；原则"从最简开始" | 5 种 workflow 模式（prompt chaining→routing→parallelization→orchestrator-workers→evaluator-optimizer）→ autonomous agent |
| **Context Engineering** | 取代 prompt engineering 的提法——策划并维护 LLM 上下文窗口的最优 token 集合 | prompt 是术、context 是道；2026 已演化为 **harness engineering**（整个 harness=工具+编排+反馈） |
| **Prompt Caching** | 稳定前缀缓存，命中后输入 token ~10%（90% off） | 口诀"稳定放前面、易变放后面"；Claude TTL 1h vs OpenAI 24h 是关键差异 |
| **Test-Time Compute** | o1/o3/R1/Sonnet Thinking——把算力从训练挪到推理，System-1→System-2 | 数学/代码/复杂推理吊打传统 LLM；**简单任务用推理模型是浪费** |
| **Agentic RAG（CRAG/Self-RAG）** | 把检索当 tool call + 迭代预算 + 自我反思门禁 | 2026 生产新默认；**arXiv 2026 警告收益与领域强相关，延迟/成本翻倍** |
| **Computer Use** | LLM 看屏+控鼠标键盘，2026 从研究走向准生产 | API 不存在且任务一次性才用；**高频场景等 API 或自己封装，是最后手段** |
| **Agent Memory**（Letta/MemGPT） | memory as editable state；三类：recall（事件回放）/archival（长期事实）/procedural（行为模式） | 跨会话一致性、个性化；**memory 污染比无 memory 更糟** |
| **Vibe Coding → Agentic Engineering** | Karpathy 2026 亲口宣布 vibe coding 过时，Software 3.0 时代 | "vibe coding 抬底让人人能写，我做的是给 AI 加 guardrail 抬顶让它上生产" |

---

## 四、高频雷区（说了必穿帮）

> 这部分是**候选人项目的诚实边界清单**。面试里但凡吹过其中一条，被追问就翻车。提前内化，避免自己挖坑。

### 项目② Manager（多 Agent 编排）

1. **"接了真实流量 / 上生产了"** —— ❌ 真相：**研究型、没接真实流量**。被问"日活多少 / 失败率多少 / 真实 case"直接挂。**正确口径**："研究型原型、跑过离线 eval + golden set，online eval 是缺的边界。"
2. **"比 Claude 强 / 跟 Devin 一个水平"** —— ❌ 真相：部署在阿里云 **qwen 不是 Claude**；功能完整度远不如 Devin 的 parallel cloud agents。**正确口径**："我押的是企业内网 + 工程治理那条缝，不是抢 Devin 的 autonomous 高度。"
3. **"39 节点 autonomous agent"** —— ❌ 真相：30+ 边硬编码，只有 probe/route/critic 调 LLM——**本质是 workflow**。**正确口径**："workflow 骨架 + 关键节点 LLM 语义判断 + HITL 仲裁。"
4. **"自进化 shadow/金丝雀/A/B 已上线跑出 X% 提升"** —— ❌ 没有真实数据。**正确口径**：软化成"自进化机制设计了、做了小范围验证、没接真实流量所以没线上收益数据"。
5. **报"qwen 比 Opus 便宜 13 倍"具体倍数** —— ⚠️ 研究里是 "~13×"，**说"便宜一个量级"更稳**，倍数被追"怎么算的"会卡。

### 项目③ Coding Agent

6. **"用了 Chroma / Pinecone / Neo4j"** —— ❌ 真相：**自研向量检索（text-embedding-v3 + 内存余弦 + sha256）**，没用任何向量库/图库。**正确口径**："刻意没上——代码语料是有限集，我要 sha256 内容寻址的确定性，pgvector 是我的升级路径。"
7. **"用 Neo4j 做代码实体图"** —— ❌ 真相：**正则 + typescript-estree AST 抽符号**，没图数据库。**正确口径**："轻量代码实体图，AST + 正则抽确定性符号，受 GraphRAG 启发的退化版。"
8. **"HITL 写确认 + 代码审查 Agent 都实现了"** —— ❌ 真相：**HITL 在 Manager 那边有，但 Coding Agent 的'写确认'和'代码审查 Agent'可能未完整实现**。**正确口径**：先说"实现了 XX、未实现 YY"分清边界，别打包吹。
9. **"18 工具全是我设计的"** —— ⚠️ 别夸大工具数量/能力。**正确口径**：只说"11 只读 + 7 写、写工具全 sha256 锁"这种可核对的细节。

### 项目① Schema 驱动中台

10. **"做的是 AI 项目"** —— ❌ 真相：**非 LLM 时代的前端工程**（字段 DAG + 拓扑排序 + 循环检测）。**正确口径**：定位成"前端时代的 workflow orchestration 经验，迁移到 agent 编排"——这是加分不是减分。

### 项目④ prd-tools

11. **"prd-tools 是公司级生产工具"** —— ⚠️ 真相：**Claude Code 插件、研发工具、团队级**。**正确口径**："团队级研发工作流、防幻觉硬门禁"。

### 通用雷区

12. **报编造百分比/倍数/团队规模** —— ❌ 简历话术和 AI 生成的"预测答案"里这类数字大多编造。**铁律**：不确定就软化（"小范围验证过"/"做过对比"/"一个量级"）或直接省略。
13. **"我解决了 prompt injection"** —— ❌ 学界公认 unsolvable。**正确口径**："我做了 defense in depth 的工程化映射，不是解决，是分层防御。"
14. **"我的方案能打 Cursor/Devin"** —— ❌ UX/polish/benchmark/社区规模全输。**正确口径**：只在"企业治理深度"这一条上对标，其他全认输。
15. **凭旧印象说模型版本号** —— ❌ Claude 不是 3.5、Gemini 不是 2.5、GPT 不是 5、DeepSeek 不是 R1。**记牢**：Opus 4.8 / Sonnet 5 / Haiku 4.5；GPT-5.6（Sol/Terra/Luna）；Gemini 3.1 Pro；Qwen3；DeepSeek V3.2-Exp。

---

## 五、"日常怎么用 AI"黄金答法（60-90 秒）

> **这题几乎必问，必须背到能脱口而出。** 核心：**分场景 + 具体工具名 + 真取舍 + 自己的 agent 反哺自己**。绝不能空话说"我用 ChatGPT 帮我写代码"。

### 完整答法（约 80 秒口播）

> "我日常用 AI 是**分场景**的，三套完全不一样的工作流。
>
> **第一套是研发工作流**——我自己写代码用 **Claude Code**，挂我自己写的两个 skill 插件（/reference 查领域知识、/prd-distill 把 PRD 蒸馏成 spec + plan，配套一个 EV-XXX 证据链防幻觉、再加一个代码级 Spec Review Gate 硬门禁）。研发工作流我**不计较 token 成本**，要的是'宁可慢也要对'——所以研发侧用 Claude 不用开源。
>
> **第二套是部署 Agent**——我做的 Manager 是 39 节点的 LangGraph 状态机，**部署在阿里云 Qwen 不上 Claude**。这是工程取舍：multi-agent 一次跑几十次 LLM call、自进化还要多副本并行实验，Qwen 输出比 Opus 便宜一个量级才跑得起，而且国内合规直连。研发用 Claude、部署用 Qwen，**不是越贵越好，是按场景分层**。
>
> **第三套是日常查资料**——快速问题用 **ChatGPT/Claude.ai**，跟前沿我盯 Anthropic 工程博客、arXiv 的 agent/eval 论文、SWE-bench/Terminal-Bench 这几个 benchmark。
>
> **最有趣的一点是，我做的 agent 项目反过来在帮我提效**——我写 prd-tools 的时候，蒸馏 PRD 的能力我自己天天用；Manager 那套 critic 节点（自我反思门禁）的思想，我后来搬到 prd-tools 的 Spec Review Gate 里。**做 agent 的人，自己的工作流也会慢慢 agent 化**。
>
> 对工具优劣我的真实判断是——Cursor 的 Plan/Composer/Background Agents 是开发者体验天花板，我全认输 UX；Claude Code 是生态最完整、能挂自己的 skill，所以是我的日常主力；Devin 是 autonomous 标杆但黑盒云端、国内基本不可用。**2026 C 端在剧烈整合——Cursor 收了 Continue、Cognition 收了 Windsurf 剩余资产、Devin 和 Windsurf 在合并——差异化只能往'企业安全 + 可内网部署'走，这正是我押的那条缝。**"

### 这套答法的"得分点"拆解（面试官要听什么）

| 得分点 | 对应内容 |
|--------|---------|
| **分场景意识**（不是一刀切） | 研发 Claude / 部署 qwen / 查资料通用 |
| **具体工具名 + 自己写的插件** | Claude Code + /reference + /prd-distill（立刻显得"真在用"不是"看过"） |
| **真实的成本/合规取舍** | "便宜一个量级 + 国内合规直连"（不空话） |
| **分场景选型的判断力** | "不是越贵越好，是按场景分层"（这是面试官要的设计判断） |
| **学习习惯** | 一手源（Anthropic 博客/arXiv/benchmark） |
| **闭环：做 agent 反哺自己** | critic → Spec Review Gate（显系统观，不报菜名） |
| **生态判断 + 趋势** | Cursor/Claude Code/Devin 优劣 + 2026 整合趋势 |
| **明确护城河** | "企业安全 + 可内网部署这条缝"（不假装全能） |

### 加分收尾（如果时间够，加这一句）

> "其实做 agent 这一年我最大的认知变化是——**Anthropic 那篇《Building Effective Agents》说的'workflow 优先于 autonomous agent'是真的**。我最早做 Manager 时恨不得全 agent 化，做完才发现 39 节点里 30+ 该硬编码、只有 3-4 个节点真需要 LLM。**'least autonomy' 是我今年学到的最重要的工程判断**。"

这一句能让面试官记住你——因为它显示你**做过、痛过、想明白了**，而不是只会转述别人的方法论。

---

## 附：一句话总记忆锚

如果只记一句话：**"分场景用 AI——研发 Claude、部署 qwen、查资料通用；我做的是企业内网 agent 治理这条缝，全认输 UX，只在'safety + 可内网部署'这一条上对标。"** 其他所有答案都是这句话的展开。
---

## 附：关键信息源（2026-07 核实）

**模型**：
- [OpenAI GPT-5.6（Sol/Terra/Luna）](https://openai.com/index/gpt-5-6/)
- [Google Gemini 3.1 Pro](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-1-pro/)
- Claude Opus 4.8 / Sonnet 5 / Haiku 4.5 / Fable 5（Anthropic 当前矩阵）

**coding agent 收购**：
- [Cognition 收购 Windsurf（TechCrunch）](https://techcrunch.com/2025/07/14/cognition-maker-of-the-ai-coding-agent-devin-acquires-windsurf/)
- [OpenAI $3B 收 Windsurf 黄了（Fortune）](https://fortune.com/2025/07/11/the-exclusivity-on-openais-3-billion-acquisition-for-coding-startup-windsfurf-has-expired/)
- [Cursor 收购 Continue（The New Stack）](https://thenewstack.io/cursor-acquires-continue-coding/)

**协议 / 方法论**：
- [Anthropic《Building Effective Agents》](https://www.anthropic.com/research/building-effective-agents)（workflow 优先于 autonomous agent 圣经）
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [OpenCode（SST/Anomaly）](https://opencode.ai/)
