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
    #text(size: 11pt, weight: "bold")[AI 工程师 · Agentic Workflow 方向] #text(size: 10.5pt)[ · 4 年大厂经验 · 连续 2 年 A 绩效]
    #v(1pt)
    #text(size: 9pt, fill: rgb("#555555"))[188-4617-4594 · 2597419838\@qq.com · #link("https://zachary-lz.vercel.app")[个人主页] · #link("https://github.com/zachary-lz-glm")[github.com/zachary-lz-glm]]
  ],
  image("photo.jpg", width: 84pt, height: 112pt, fit: "cover"),
)

#v(4pt)
#line(length: 100%, stroke: 0.5pt + rgb("#e0e0e0"))

== 个人优势

4 年大厂经验,连续 2 年 A 绩效。基于 Claude Code 独立设计并落地两套生产级 Agentic Workflow 平台:

#set list(marker: text(fill: accent)[•], indent: 2pt, body-indent: 5pt, spacing: 4pt)

- #hl[Spec-Driven Development Platform] — 一次蒸馏产出 plan.md 三段式(开发计划 + QA 矩阵 + 回滚方案) + final-quality-gate 5 维准出报告;需求耗时 #hl[5h → 2h/需求],#hl[20+ 人团队]推广;消融实验:去掉证据链层产物评分 82 → 54。
- #hl[Multi-Agent 自动化流水线] — 自动产出 #hl[18 个生产版本]（v233 → v251）,真实运行 #hl[6 个月+],长跑 100+ 轮负担不变。
- #hl[Schema 驱动营销中台 + 400+ 权益组件库] — 4 年大厂业务硬证据:覆盖 10+ 国家 / 20+ 活动类型 / 8 业务项目。

== 专业技能

#hl[AI / Agentic Workflow]:Claude Code Skill 工作流 · Sub-agent 编排 · Multi-Agent 编排 · RAG(混合检索) · Prompt Engineering · Context Engineering · MCP 协议 · Function Calling / Tool Use · Eval(产物质量门禁) · Embedding 选型 · Vector Database

#hl[前端工程]:React + TypeScript · 状态管理(Redux / Zustand)· Node.js Serverless BFF · 组件库设计(SDK 抽象 + Rollup 双模打包 + Changesets)· Lerna + Nx Monorepo · Schema 驱动架构 · 微前端(qiankun)· 性能优化 / 工程化(Webpack / Rollup)

#hl[工程效能]:CI/CD 流水线 · Sentry 监控 · Service Worker 缓存 · 自动化测试(Vitest / Jest)

== 工作经历

#text(weight: "bold")[滴滴出行 · 国际化事业部] ｜ AI 工程师 · Agentic Workflow 方向 ｜ 2022.06 - 至今

负责国际化营销中台前端架构 + Agentic Workflow 工程化体系搭建。独立设计并落地两套生产级 Agent 工作流平台(Spec-Driven Development Platform + Multi-Agent 自动化流水线),主导 Schema 驱动架构和 400+ 营销权益组件库,覆盖 10+ 国家、20+ 种活动类型。连续 2 年 A 绩效,核心交付质量团队前列。

#block(breakable: false, spacing: 14pt)[
== 项目经历

=== Spec-Driven Development Platform — 企业级 AI 代码理解与 SDLC 自动化平台
#text(size: 8.5pt, fill: rgb("#666666"))[独立设计并主导落地 · Claude Code Skill · RAG · MCP 协议 · Context Engineering · Sub-agent]

#text(weight: "bold")[业务场景]:B 端 PRD 到代码缺少可追溯的中间产物 Spec,AI 直接分析 PRD 缺乏历史代码上下文与隐性业务逻辑,产出计划不可执行,需求理解偏差导致返工频发。本平台基于 Claude Code + MCP 用 RAG + verified_by 证据链解决这一企业级 AI 编码痛点。

#text(weight: "bold")[核心技术]:
- #hl[6 文件 SSOT 知识库 + 混合检索] — 历史代码 / PRD / 跨层契约蒸馏成 6 个 yaml(代码结构 / 编码规则 / 契约 / PRD 路由 / 业务领域 / 实体索引),配合倒排索引 + 实体图,按需检索入上下文
- #hl[三 plan 完整闭环] — 一次蒸馏产出 plan.md 三段式(开发计划精确到行号 + QA 矩阵 + 回滚方案) + final-quality-gate 5 维准出报告(完整性 / 一致性 / 可追溯 / 可行性 / 风险),区别于单点 PRD→Plan 工具
- #hl[verified_by 证据链] — 每条事实附带 file:line 溯源,源码 Read 后才写入,禁止推断,降低 AI 编码幻觉
- #hl[Spec Review Gate] — Spec 必须用户 approved 才能进入 Plan,避免错误计划被开发执行

#text(weight: "bold")[量化产出]:需求理解阶段耗时 #hl[5h → 2h / 需求] (5 个需求对照);文件级覆盖率 #hl[80%+];同一 PRD 跑 10 次一致性 #hl[40% → 85%+] (产物稳定性指标);20+ 人团队生产环境推广,后端基于此迭代。

#text(weight: "bold")[消融实验]:去掉证据链层,产物评分 #hl[82 → 54],验证证据链是必需层而非可选层。

]

#block(breakable: false, spacing: 14pt)[
=== Multi-Agent 自动化流水线 — LLM 内容自优化系统
#text(size: 8.5pt, fill: rgb("#666666"))[独立设计并主导落地(生产项目)· Claude Code cron + subagent · 失败自动回滚]

#text(weight: "bold")[业务场景]:LLM 生成内容随时间漂移——风格不一致、质量参差、维护成本线性增长,这是 LLM 工程化的核心瓶颈之一。本系统让 AI 自动持续优化自己的产出。

#text(weight: "bold")[核心技术]:
- Multi-Agent 上下文隔离 — 独立 Context Window,主调度只收一行简报(信息压缩 + 主流程解耦)
- 失败自动回滚 — commit 前结构自检,失败立即回滚
- 风格漂移防护 — 每轮重读样板,对抗 LLM 长跑漂移

#text(weight: "bold")[量化产出]:自动产出 #hl[18 个生产版本]（v233 → v251,跨度 #hl[6 个月+]）;生产环境无破坏性 commit;主调度上下文与运行轮次解耦,#hl[长跑 100+ 轮]负担不变。

]

#block(breakable: false, spacing: 14pt)[
=== Schema 驱动营销中台 + 400+ 权益组件库
#text(size: 8.5pt, fill: rgb("#666666"))[前端 + BFF 架构设计 · React · TypeScript · Node.js Serverless · Lerna + Nx · Rollup]

#text(weight: "bold")[业务场景]:国际化营销中台覆盖 10+ 国家、20+ 活动类型、400+ 种营销权益(优惠券 / 折扣 / 积分 / 立减)全生命周期。传统方式每新增一种需前后端各写一套,周期长易错。

#text(weight: "bold")[核心技术]:
- BFF Template Engine + 双重求值联动(自研 DSL) — safeEval 求初值 + 序列化运行时指令
- Dynamic Rendering — 35+ 组件注册表 + 发布订阅
- Register 注册模式 — 运行时注册权益,新增无需改 SDK
- Monorepo 治理 — Lerna + Nx 管理 15+ 业务模块

#text(weight: "bold")[量化产出]:新增活动前端 #hl[零代码],上线周期 #hl[2 周 → 3 天];权益库覆盖 #hl[8 个业务项目 / 400+ SKU]（底层组件 30-40 个）,新权益接入 2 天 → 2 小时,运行 18 个月+ 仅 2-3 起小 bug。
]

== 教育背景

#text(weight: "bold")[黑龙江大学] ｜ 计算机科学与技术 ｜ 本科 ｜ 2018.09 - 2022.06
