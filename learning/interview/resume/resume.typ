#set page(paper: "a4", margin: (x: 14mm, y: 13mm))
#set text(font: ("Hiragino Sans GB", "Heiti SC", "Helvetica Neue", "Arial"), size: 10pt, lang: "zh", fill: rgb("#222222"))
#set par(leading: 0.6em, spacing: 0.55em, justify: false)

// 配色:Navy 主色 + 翡翠绿单点强调(仅核心对比型数据)
#let accent = rgb("#1A2B4A")
#let pop = rgb("#059669")
#let muted = rgb("#555555")
#let faint = rgb("#888888")
#let lineColor = rgb("#cccccc")
#let hairline = rgb("#e0e0e0")

// 章节标题:字号微缩 + 横线改细中灰(更克制)
#show heading.where(level: 2): it => block(above: 8pt, below: 4pt)[
  #set text(size: 11.5pt, fill: accent, weight: "bold", tracking: 0.3pt)
  #it.body
  #v(-3pt)
  #line(length: 100%, stroke: 0.6pt + lineColor)
]
// 项目名:左侧 2pt Navy 竖条 + 11pt 加粗黑
#show heading.where(level: 3): it => block(above: 6pt, below: 3pt)[
  #box(
    inset: (left: 6pt),
    stroke: (left: 2.5pt + accent),
  )[
    #set text(size: 11pt, fill: rgb("#1a1a1a"), weight: "bold")
    #it.body
  ]
]

// 双层高亮:hl=技术词强调(Navy 加粗), mh=核心数据强调(翡翠绿加粗)
#let hl(body) = text(fill: accent, weight: "bold")[#body]
#let mh(body) = text(fill: pop, weight: "bold")[#body]

// ===== 头部:左信息 + 右证件照 =====
#grid(
  columns: (1fr, auto),
  column-gutter: 14pt,
  align: (left + top, right + top),
  [
    #text(size: 22pt, weight: "bold", fill: rgb("#1a1a1a"), tracking: 0.5pt)[邓泽霖]
    #v(3pt)
    #text(size: 11pt, weight: "bold", fill: accent)[高级前端工程师]
    #text(size: 10.5pt, fill: muted)[ · ]
    #text(size: 11pt, weight: "bold", fill: accent)[AI 工程师方向]
    #text(size: 10.5pt, fill: muted)[ · 4 年大厂经验 · 连续 ]
    #mh[2 年 A 绩效]
    #v(2pt)
    #text(size: 9pt, fill: muted)[188-4617-4594 · 2597419838\@qq.com · #link("https://zachary-lz.vercel.app")[个人主页] · #link("https://github.com/zachary-lz-glm")[github.com/zachary-lz-glm]]
  ],
  image("photo.jpg", width: 78pt, height: 104pt, fit: "cover"),
)

#v(4pt)
#line(length: 100%, stroke: 0.4pt + hairline)

== 个人优势

#hl[4 年大厂前端 + 1.5 年 LLM 工程化],连续 #mh[2 年 A 绩效]。主导公司级 Spec-Driven 平台落地（#mh[20+ 人]日常使用）,业余独立设计实现 code_assistent（Coding Agent）+ Manager_Agent（Multi-Agent Orchestrator）。核心方向:#hl[Coding Agent / Multi-Agent 编排 / Agent Safety / RAG 工程],求职 AI 工程师（Agent 工程化方向）。

#set list(marker: text(fill: accent)[•], indent: 2pt, body-indent: 5pt, spacing: 4pt)

== 专业技能

#hl[LLM / AI 工程栈（Python · LangGraph · Claude Code Skill）]:Multi-Agent 编排（Supervisor / Plan-Execute / ReAct · Sub-agent）· Agent Safety · HITL · Self-Evolution · MCP 协议

#hl[RAG & Eval]:Hybrid Retrieval（BM25 + Dense + Reranking）· 代码 RAG · Citation Grounding · rubric Eval · Golden Set · LLM-as-Judge

#hl[LLM 基础]:Transformer / Attention 原理 · Prompt 工程 · LLM API 成本与延迟优化

#hl[前端工程（4 年主业）]:React + TypeScript · Serverless BFF · Server-Driven UI · Schema-as-Code · Plugin Architecture · Monorepo

== 工作经历

#text(weight: "bold")[滴滴出行 · 国际化事业部] #text(fill: muted)[｜ 高级前端工程师 ｜ 2022.06 - 至今 ｜ 连续 ]
#mh[2 年 A 绩效]

2022.06 - 2024 前端 owner,主导国际化营销中台从 0 到 1（Server-Driven UI + 400+ 权益组件库）;2024 起 All-in LLM 工程化,主导公司级 Spec-Driven 平台落地（#mh[20+ 人团队]日常使用）。

#block(spacing: 10pt)[
== 项目经历

=== Spec-Driven Development Platform — Agentic Coding 工作流
#text(size: 9pt, fill: muted)[公司团队项目 · 主导负责 · PRD/Spec 工程层 · Claude Code Skill · Citation Grounding · Sub-agent]

#text(weight: "bold")[项目定位]:把 Spec 作为可追溯工程中间产物的企业级平台,用 Agentic RAG + Citation Grounding 把 LLM 编码约束在可审计边界内,解决 B 端 PRD 缺历史代码上下文导致计划不可执行、返工频发痛点。

#text(weight: "bold")[核心技术]:
- #hl[蒸馏式知识库 + Hybrid Retrieval] — 历史代码 / PRD / 跨层契约蒸馏为 6 类知识（代码结构 / 编码规则 / 契约 / PRD 路由 / 业务领域 / 实体索引）,倒排索引 + 实体图按需检索
- #hl[Plan-and-Execute 闭环 + Quality Gate] — 一次蒸馏产出三份产物（开发计划精确到行号 + QA Matrix + Rollback Plan）+ Final Quality Gate 5 维准出报告,区别于单点 PRD → Plan 工具
- #hl[Citation Grounding + Spec Review Gate] — 每条事实附带 file:line citation,源码 Read 后才写入,禁止推断;Spec 必须用户 approved 才能进入 Plan（HITL gate）,降低 Hallucination 与错误计划被执行风险

#text(weight: "bold")[量化产出]:需求理解耗时 #mh[5h → 2h / 需求]（n=5 PRDs）;蒸馏 determinism #mh[40% → 85%+]（n=10）;#mh[20+ 人团队]日常使用;Grounding 对比实验 rubric #mh[82 → 54]。

]

#block(spacing: 10pt)[
=== Manager_Agent — Multi-Agent Supervisor Orchestrator
#text(size: 9pt, fill: muted)[个人项目 · 独立设计实现 · Multi-Agent 编排层 · LangGraph · Supervisor · Self-Evolution]

#text(weight: "bold")[业务场景]:企业级 AI 助手需统一调度多个专业 Agent（知识库 / NL2SQL / 代码 / 爬虫 / GUI / 办公 / 多模态）,基于 LangGraph Supervisor 编排模式调度 #mh[12 个能力 Agent]（8 外部 + 4 内部）。

#text(weight: "bold")[核心技术]:
- #hl[Multi-Agent Supervisor 编排] — #mh[39 节点] 状态机,编排层与专家层分离（总管只做意图路由 / 任务规划 / 结果汇总）,支持 #mh[14 路意图分发] 与子句拆解（多意图 → 多步 plan）
- #hl[Plan-and-Execute + Critic 闭环 + HITL] — Planner → Executor 并行 → Critic 事实性审查 → Synth 综合;高风险写操作 HITL 确认,file + Redis 双后端 checkpoint 支持跨进程续跑;recursionLimit #mh[48] 内长跑稳定
- #hl[Self-Evolution Layer（无标注自进化）] — ① 失败归因 12 分类 → ② LLM 假设生成（每 30min ≤3 条） → ③ 假设金丝雀 A/B 验证命中后晋级 Prompt 补丁 → ④ 经验回放注入 router few-shot,整套机制无需人工标注

#text(weight: "bold")[量化产出]:#mh[39 节点 / 40 条边]（含 20 条条件边）· #mh[12 Agent]（8 外部 + 4 内部）· 8 类 WS 消息 · 7 个 eval golden + 34 个 smoke 脚本。

]

#block(spacing: 10pt)[
=== code_assistent_Agent — Agentic Coding / Coding Agent Safety
#text(size: 9pt, fill: muted)[个人项目 · 独立设计实现 · Coding Agent 执行层 · LangGraph · ReAct · Agent Safety · 代码 RAG]

#text(weight: "bold")[业务场景]:LLM 改仓库的高风险场景下"模型 + 写权限 = 事故",本 Agent 完整覆盖 Read-before-Write → 语义检索 → 静态分析 → Diff 预览 → 受控写盘 工程闭环。

#text(weight: "bold")[核心技术]:
- #hl[ReAct Tool Use + 代码 RAG] — #mh[18 个] 仓库工具（读 / 检索 / AST / Patch / 校验 / 执行 / Git）的 agent↔tools 循环 + 仓库语义检索（向量召回 + 增量索引）,区别于端到端 chat 把全量 repo 塞 context;Custom CheckpointSaver 支持跨进程会话恢复
- #hl[Agent Safety — 三层写盘守卫 + Sandbox Isolation] — 路径黑名单 + 受保护目录 + sha256 乐观锁,任一层拦截即拒绝;subprocess 白名单 env + docker 网络隔离双沙箱,优先强隔离不可用时自动降级
- #hl[Auto-Validation + Prompt A/B（Shadow Patch）] — autoValidateAfterWrite 跑 typecheck / lint / test,失败针对性修复;shadow patch 多次命中晋级正式库,hash 分桶 A/B 对照

#text(weight: "bold")[量化产出]:#mh[18 工具] 覆盖 read / search / vector / AST / patch / validate / exec / git 全链路 · 默认服务 800 文件仓库 / 512MB / 90s 超时 · 跨进程会话恢复回归测试 0 丢失。

]

#block(spacing: 10pt)[
=== Server-Driven UI 中台 + 400+ 权益组件库
#text(size: 9pt, fill: muted)[前端 + BFF 架构设计 · Server-Driven UI · Schema-as-Code · Plugin Architecture · React · TypeScript]

#text(weight: "bold")[业务场景]:国际化营销中台覆盖 #mh[10+ 国家 / 20+ 活动类型 / 400+ 营销权益]全生命周期,4 年前端 owner 主导。

#text(weight: "bold")[核心技术]:
- #hl[Server-Driven UI + Plugin Architecture + Schema-as-Code] — Schema 化页面指令驱动运行时渲染,权益作为插件 SDK 注入（新增无需改 SDK / 无需发版）;DSL 引擎两阶段求值（编译期 schema 校验 + 运行期求值）解决跨国家 / 跨活动动态组合
- #hl[Plugin Registry + Hot Swap] — 35+ 渲染组件通过 Registry 注册,发布订阅驱动运行时渲染,组件 hot-swap 不停机

#text(weight: "bold")[量化产出]:标准活动上线 #mh[2 周 → 3 天];权益库 #mh[400+ SKU] 服务 8 个业务项目,新权益接入 #mh[2 天 → 2 小时],运行 18 个月+ 仅 2 起低危 bug。
]

#v(2pt)
#line(length: 100%, stroke: 0.3pt + hairline)
#v(-4pt)

== 教育背景

#text(weight: "bold")[黑龙江大学] #text(fill: muted)[｜ 计算机科学与技术 ｜ 本科 ｜ 2018.09 - 2022.06]
