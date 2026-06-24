#set page(paper: "a4", margin: (x: 13mm, y: 12mm))
#set text(font: ("PingFang SC", "Microsoft YaHei", "Helvetica Neue", "Arial"), size: 10pt, lang: "zh", fill: rgb("#222222"))
#set par(leading: 0.55em, spacing: 0.6em, justify: false)

#let accent = rgb("#0b5cad")

// 章节标题
#show heading.where(level: 2): it => block(above: 6pt, below: 4pt)[
  #set text(size: 12pt, fill: accent, weight: "bold")
  #it.body
  #v(-4pt)
  #line(length: 100%, stroke: 1.2pt + accent)
]
// 项目名
#show heading.where(level: 3): it => block(above: 4pt, below: 3pt)[
  #set text(size: 10.6pt, fill: rgb("#1a1a1a"), weight: "bold")
  #it.body
]

#let hl(body) = text(fill: accent, weight: "bold")[#body]

// ===== 头部：左信息 + 右证件照 =====
#grid(
  columns: (1fr, auto),
  column-gutter: 14pt,
  align: (left + top, right + top),
  [
    #text(size: 22pt, weight: "bold", fill: rgb("#1a1a1a"))[邓泽霖]
    #v(2pt)
    #text(size: 11pt, weight: "bold")[AI 工程方向 · 高级前端工程师] #text(size: 10.5pt)[ · 4 年大厂经验 · ] #hl[2 年 A 绩效]
    #v(1pt)
    #text(size: 9pt, fill: rgb("#555555"))[188-4617-4594 · 2597419838\@qq.com · #link("https://zachary-lz.vercel.app")[个人主页] · #link("https://github.com/zachary-lz-glm")[github.com/zachary-lz-glm]]
  ],
  image("photo.jpg", width: 84pt, height: 112pt, fit: "cover"),
)

#v(4pt)
#line(length: 100%, stroke: 0.5pt + rgb("#e0e0e0"))

== 个人优势

#hl[AI 工程化方向独立落地者] —— 独立设计并落地 SDD（Spec-Driven Development）体系，PRD→开发计划耗时从 5h 降到 2h/需求，已在 B 端 20+ 人团队推广，清晰区分 Vibe Coding 与标准化 AI 研发的边界。

#set list(marker: text(fill: accent)[•], indent: 2pt, body-indent: 5pt, spacing: 4pt)

- #hl[Agent / Agentic Workflow 工程实践]：独立搭建 Claude Code 双 Skill 工作流，跑通 PRD→Spec→Plan→人工 Review→反馈回流闭环；深度实践 Prompt / Context Engineering、Tool Use、MCP 协议、RAG（BM25 + 语义混合检索 + RRF）。
- #hl[前端架构 + BFF 全栈能力]：主导 Schema 驱动营销中台（BFF 模板引擎 + 前端动态渲染 + 双重求值联动引擎）与 400+ 营销权益组件库，支撑 20+ 种活动类型、8 个业务项目。

== 专业技能

#hl[AI 工程化]：SDD / Spec-Driven · Claude Code Skill 工作流 · Prompt Engineering · Context Engineering · Harness Engineering · RAG · MCP 协议 · Function Calling · Agent Loop · Claude API

#hl[前端 & 架构]：React + TypeScript · Redux · Node.js Serverless BFF · Lerna + Nx Monorepo · Schema 驱动架构 · Rollup / Webpack · 微前端（qiankun）

#hl[工程效能]：Changesets · zx 自动化 · CI/CD 流水线 · Sentry 监控 · Service Worker 缓存

== 工作经历

#text(weight: "bold")[滴滴出行 · 国际化事业部] ｜ 高级前端工程师 ｜ 2022.06 - 至今

主导国际化营销中台前端架构 + AI 工程化体系搭建。独立落地 SDD 全流程（PRD 蒸馏工作流），主导 Schema 驱动架构和 400+ 营销权益组件库。覆盖 10+ 国家、20+ 种活动类型、8 个业务项目。主导《中台开发规范》《BFF 接口规范》《CI/CD 流水线规范》落地与多场业务技术分享；连续 2 年 A 绩效，核心交付质量团队前列。

#block(breakable: false, spacing: 14pt)[
== 项目经历

=== SDD 工作流落地 — PRD 蒸馏到可执行开发计划
#text(size: 8.5pt, fill: rgb("#666666"))[独立设计 + 落地 · Claude Code Skill · MCP 协议 · Prompt / Context Engineering · Harness 约束体系]

#text(weight: "bold")[背景]：B 端 PRD 到代码缺少可追溯的中间产物（Spec），导致 AI Coding 产出不可控、需求理解偏差返工频发。基于 Claude Code + MCP 实现 Spec 自动蒸馏，用 Cursor Agent Mode 按 Spec 驱动编码。

#text(weight: "bold")[行动]：
- #hl[双 Skill 知识底座]：知识库构建 6 模式 + Spec 蒸馏 11 步工作流，反馈回流闭环让 Spec 越用越准；Skill 零依赖设计（不依赖 Node / LLM Key），团队拿到即用。
- #hl[SSOT 规范体系]：6 文件按关注点分离（代码结构 / 编码规则 / 跨层契约 / PRD 路由 / 业务领域 / 实体索引），5 条边界规则避免 AI 编码知识污染。
- #hl[AI Coding 质量管控]：8 种证据类型（含负向搜索 negative_code_search）+ PRD 入口三级门禁，降低返工率。

#text(weight: "bold")[结果]：PRD 到开发计划耗时从 #hl[5h/需求 降到 2h/需求]（5 需求对照）；文件级准确率 #hl[80%]；同一 PRD 跑 10 次一致性从 #hl[40% 提升到 85%+]；已在 B 端 #hl[20+ 人团队推广]，后端基于此迭代。

]

#block(breakable: false, spacing: 14pt)[
=== Schema 驱动营销中台 — BFF 动态生成 + 前端动态渲染
#text(size: 8.5pt, fill: rgb("#666666"))[前端 + BFF 架构设计（与导师联合主导，本人负责前端侧）· React · TypeScript · Node.js Serverless · Lerna + Nx]

#text(weight: "bold")[背景]：营销中台覆盖 10+ 国家、20+ 种活动类型，每种活动字段组合与联动规则不同。传统方式每新增一种活动需前后端各写一套，周期长易错（老代码月均 10+ 线上事故）。

#text(weight: "bold")[行动]：
- #hl[BFF 模板引擎]：模板驱动 Schema 生成，按活动类型分文件管理（25 模板），联动模板复用渲染 handler。
- #hl[双重求值联动引擎（自研 DSL injectDActions）]：一次声明，BFF 端 safeEval 求初始状态（SSR 正确）+ 序列化 d_actions 给前端运行时联动，支持 fetchApi 型与 state 型。
- #hl[前端渲染引擎 + Monorepo 治理]：嵌套路径拍平 + 注册表 35+ 组件动态渲染 + 发布订阅联动；Lerna + Nx 管理 15+ 业务模块。

#text(weight: "bold")[结果]：新增活动类型前端 #hl[零代码]，上线周期从 #hl[2 周缩短到 3 天]，累计支撑 #hl[20+ 种活动类型]，联动配置复用率 #hl[80%+]，上线 2 年仅 2-3 起小 bug（老代码月均 10+）。

]

#block(breakable: false, spacing: 14pt)[
=== 营销权益组件库 — 400+ 权益 React 组件库
#text(size: 8.5pt, fill: rgb("#666666"))[架构设计 + 核心开发（独立完成）· React · TypeScript · Rollup · Changesets]

#text(weight: "bold")[背景]：营销平台管理 400+ 种权益（优惠券、折扣、积分、立减等）全生命周期，类型持续增长，原方案每新增一种都需硬编码，维护成本高。

#text(weight: "bold")[行动]：
- #hl[Register 注册模式]：内置 24 组件 + 运行时注册自定义权益（add / addMultipleCmps），新增权益无需改 SDK。
- #hl[Schema 同构渲染]：组件库与活动表单共享 Schema 渲染架构，两个消费者复用同一套引擎。
- #hl[Rollup 双模打包]（ESM + CJS + 类型声明）+ peerDependencies 隔离 + Changesets 语义化发版。

#text(weight: "bold")[结果]：覆盖 #hl[8 个业务项目]，累计接入 #hl[400+ 种权益 SKU]（底层组件 30-40 个），新权益接入从 #hl[2 天缩短到 2 小时]，零 breaking change 运行 #hl[18 个月+]。
]

== 教育背景

#text(weight: "bold")[黑龙江大学] ｜ 计算机科学与技术 ｜ 本科 ｜ 2018.09 - 2022.06
