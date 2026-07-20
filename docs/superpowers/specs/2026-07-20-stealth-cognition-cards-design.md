# stealth.html 认知层补卡设计（open design 面试复盘回流）

> 日期：2026-07-20
> 背景：上周面 open design 挂了，4 个核心问题都是"思路和认知"题。现有 27 张 Agent 卡（Manager 11 + Code 16）95% 是"怎么做"实现细节，缺"为什么这么做 / 趋势认知 / 复杂度判断"的元认知层。本次补 5 张「设计权衡」卡 + 1 份复盘文档。

## 1. 诊断（4 问对照缺口）

| 面试官问题 | 考察点 | 现有卡 | 缺口 |
|---|---|---|---|
| ① 代码状态机 vs agent 自主流转 | LLM Supervisor/Swarm vs 硬编码 graph 的权衡；Anthropic「workflow 优先于 autonomous」共识 | 「主干链路」只讲为什么用 LangGraph | 缺 1 张权衡卡 |
| ② 和竞品比，为什么要做 | 多 Agent 竞品认知 + 产品判断力（动机/价值） | Code 有 1 张「vs Cursor/Aider/Devin」；Manager 零竞品 | Manager 缺竞品+动机，1 张 |
| ③ 了解 opencode/ohmyopencode 吗 | 开源 AI coding 生态认知 | 无 | 缺 1 张 |
| ④ 39 节点 / 18 工具是不是太多 | 复杂度合理性、YAGNI、过度设计判断 | 无正面回答 | Manager + Code 各 1 张 |

## 2. 方案决策（已与用户确认）

- **放置**：补进现有 Manager/Code 子组（不新建组）。理由：现场速查面试官问到哪组就翻到哪组，符合手术式修改。
- **颗粒度**：5 张（Manager 3 + Code 2）。
- **复盘文档**：同时写 `reviews/open-design_面试复盘_认知题方向修正.md`。
- **下游 Specialist 数量**：软化为「十几个」（GUIDE §1.3 写 12=9外+3内，校准文档 §5 写 14，两处打架，不报死数）。
- **风格**：结构化参考卡风（GUIDE §6：declarative、`<strong>段首标签。</strong>` 组织、可①②内联）。

## 3. 5 张卡完整设计

> 所有事实以 `learning/interview-kb/明日面试_预测题校准与匹配分析.md` 为准。风格对标现有「主干链路」「和 Cursor/Aider/Devin 比」两张参考卡。

### M-1｜为什么用硬编码状态机，不用 LLM 自主流转？（Manager 组）
- **data-g**：`Manager 智能体`
- **data-kw**：`自动流转 状态机 LLM Supervisor Swarm createSupervisor 动态路由 硬编码 为什么不用 Anthropic workflow agent 混合架构 ReAct 对比 自主 决定下一步`
- **core**：不是不会用自动流转——Code Agent 就是 ReAct 自主流转；Manager 用硬编码 graph 是因为调度的是能写库/写文件的高风险下游，确定性的步骤钉死、需要判断的才交给 LLM，混合架构。
- **正文要点**（3-4 段，每段 `<strong>段首。</strong>`）：
  1. **两种范式先分清。** LLM Supervisor/Swarm（让 LLM 看运行时 state 动态决定下一步去哪个 agent，如 LangGraph 的 createSupervisor、OpenAI Swarm 的 handoff）vs 硬编码状态机（add_conditional_edges 在 build time 写死边）。**LangGraph 两种都支持，不是对立。**
  2. **业界共识。** Anthropic《Building effective agents》核心观点：能 workflow（确定性编排）就别上 autonomous agent，尤其高风险/可审计场景——自主循环是最后手段不是默认选项。
  3. **我的权衡是混合。** Manager 调度的下游能写库（NL2SQL）、能爬数据、未来能改代码——高风险、要 HITL、要可审计。把"必经的确定性步骤"钉死（probe 必在 plan 前、高风险必经 admin_confirm、critic 不过必走 fix），把"需要语义判断的"才交 LLM（route 意图分类、decompose 子句拆解）。
  4. **诚实边界。** 反证我不会只用硬编码：Code Agent 就是 ReAct——LLM 自主选工具循环，因为代码任务探索式、步骤不可预知。硬编码代价是不够灵活（改流程要改图），autonomous 代价是 misroute 不可控/贵/慢。开放式场景（通用聊天）我会更倾向 autonomous。

### M-2｜和市面多 Agent 竞品比，为什么要做这个总管？（Manager 组）
- **data-g**：`Manager 智能体`
- **data-kw**：`竞品 为什么做 AutoGen CrewAI MetaGPT Manus LangGraph Supervisor 差异化 动机 价值判断 编排 不替代 安全第一 可观测 个人项目`
- **core**：不是做竞品——agent-main 单仓十几个 Agent 缺一个能编排落地的总管；市面框架偏通用角色扮演，我的偏"能上生产的工程范式"：安全、可观测、HITL、可回滚。
- **正文要点**：
  1. **先认竞品强。** 市面多 Agent 编排不少——AutoGen（对话式多 agent）、CrewAI（角色分工）、MetaGPT（软件研发 SOP）、Manus（通用 autonomous）、LangGraph Supervisor（官方 supervisor 模式）。功能广度比不过，它们是成熟框架。
  2. **为什么要做（动机）。** ① agent-main 单仓十几个 Agent（db/rag/code/crawler…）各自为政，缺统一入口和编排层，真实工程缺口；② 想搞清"多 Agent 编排怎么做到能上生产"——光调 API 不难，难的是可观测、HITL、失败恢复、防 misroute，框架给得不完整；③ 个人研究项目，验证一套工程范式。
  3. **差异化（强项）。** ① 安全第一——下游能写库/写文件，HITL+scope 鉴权+审计是地基不是补丁；② 可观测——LangSmith trace 到节点级，路由决策可回看；③ 自进化非劣性设计（金丝雀+A/B+自动回滚），不是裸跑；④ Probe 在 plan 前（规划前先探下游能不能用，减少幻觉式路由）——这个顺序多数竞品没有。
  4. **诚实边界。** 偏研究型、没接真实流量、功能完整度认输。ROI 诚实：做这个最大收获是工程认知，不是用户量。

### M-3｜39 个节点是不是过度设计了？（Manager 组）
- **data-g**：`Manager 智能体`
- **data-kw**：`39节点 过度设计 YAGNI 复杂度 太多 必要性 怎么长出来的 演进 做减法 生产化 每个节点挡什么坑`
- **core**：39 是"长出来"的不是一上来设计的——单下游→多路由→状态机→HITL→自进化逐步叠加；每个节点挡一个坑。但偏研究型，生产化要先做减法。
- **正文要点**：
  1. **怎么长出来的。** 不是设计 39 个节点。演进：单下游代理（3-5 节点）→ 多路由加 route/decompose → 流式加 phase 事件 → HITL 加 admin_confirm/checkpoint → 自进化加 Curator/tool_health，每加一类需求加几个节点，自然到 39。口径说"接近 40"最稳。
  2. **每个节点挡什么坑（讲必要性）。** probe（规划前探活，挡幻觉路由）、decompose（子句拆解在分类前，挡一句两意图取平均）、admin_confirm（HITL 挡误操作）、critic（质检挡漏审）、fix（修复回环）、Curator（治理记忆）。不是堆砌，每个有职责。
  3. **是不是过度设计（诚实答）。** 有部分是。demo/研究阶段堆了一些理想化机制（比如三套自适应路由 Bandit/RL/Causal，职责正交但可能 over-engineered）。生产化第一件事是做减法——看哪些节点在生产流量下根本不走、可以删。
  4. **关键认知。** 复杂度本身不是问题，"无解释的复杂度"才是。能讲清每个节点为什么存在，所以不是过度设计；但主动承认规模偏大、生产要精简——这是加分（显判断力）。**生产化真正要补的不是减节点，是 Postgres 原生 saver 替自研、接 OpenTelemetry 拿真 trace、golden 样本扩到几十个做统计显著。**

### C-1｜了解 opencode / ohmyopencode 吗？（Code 组）
- **data-g**：`Code 智能体`
- **data-kw**：`opencode ohmyopencode SST Anomaly 开源 coding agent terminal Aider OpenHands Cline 竞品 认知 生态 不锁vendor 75模型 自托管`
- **core**：了解。opencode 是 SST/Anomaly 开源 terminal coding agent（75+ 模型、TUI/desktop/IDE、不锁 vendor），ohmyopencode 是社区配置生态——和我 Code Agent 同类，它赢通用生态、我赢企业 Safety/受控。
- **正文要点**：
  1. **opencode 是什么。** SST 团队（已重组为 Anomaly）出的开源 AI coding agent，主打 terminal（TUI），也有 desktop 和 IDE 扩展；75+ 模型 provider；完全开源不锁 vendor。GitHub：sst/opencode → anomalyco/opencode。定位类似 Claude Code / Aider 的开源版。
  2. **ohmyopencode 是什么。** 社区围绕 opencode 做的配置/增强生态（类比 oh-my-zsh 之于 zsh），有 opencode-config-tool（Electron+React 桌面工具管 opencode.json）等。说明 opencode 已成型社区生态，值得跟进。
  3. **和我的 Code Agent 比。** 同一类（terminal coding agent），定位不同：① opencode 是通用开发者工具、生态广、模型多、开源可自托管；② 我偏研究+企业场景，强项是 Safety（JWT/scope/限流/路径白名单/sha256 锁/沙箱/原子写/审计）和受控写盘——安全做在代码路径上不写 prompt 里（详见「和 Cursor/Aider/Devin 比」卡）。
  4. **态度与诚实。** 开源 coding agent 是趋势（opencode/Aider/OpenHands/Cline），跟进学习 provider 抽象和 TUI 交互；但差异化在企业可审计的受控改码，不拼功能广度。诚实：opencode 了解定位、没深度用过；ohmyopencode 知道是社区生态层。

### C-2｜18 个工具是不是太多了？（Code 组）
- **data-g**：`Code 智能体`
- **data-kw**：`18工具 太多 必要性 只读11 写7 收敛 意图路由 task_kind 职责分工 砍 YAGNI 竞品对比 长尾`
- **core**：18 = 11 只读 + 7 写，且只读请求不给写工具——按读/检索/分析/写/记忆职责分，不是堆数量；demo 偏理想化，生产看调用分布砍长尾。
- **正文要点**：
  1. **先拆结构（讲分工不是堆数量）。** 18 = 只读 11（list/read/semantic_search/vector_search/git 只读×4/ast_analyze/analyze_dependencies/remember）+ 写 7（write_file/apply_diff/validate_project/run_tests/git_commit/git_create_branch/generate_docs）。按职责分 5 类：读、检索、分析、写、记忆。
  2. **关键设计：意图路由收敛工具数。** 按 task_kind 四路分发（compute/inspect/edit/full），只读请求（compute/inspect）只给只读工具——模型根本看不到写工具，选不到就不会乱写。所以"18 个"是全量，单次请求模型实际面对的工具远少。这是降复杂度，不是加。
  3. **为什么不能更少（必要性）。** 只读 11 是"理解仓库"最小集（文件树/读文件/语义检索/向量检索/git 状态/AST/依赖图/记忆）；写 7 是"受控改码"最小集（写文件/打补丁/校验/测试/提交/建分支/生成文档）。砍哪个都有场景缺口。
  4. **诚实 + 竞品水位。** demo 阶段偏理想化，有些工具（generate_docs）用得少，生产化看实际调用分布砍长尾；但 read/semantic_search/apply_diff/validate_project 是命门不能砍。和 Cursor/Aider/opencode 比，18 是工程化 coding agent 的合理水位，不算多。

## 4. 复盘文档结构（reviews/open-design_面试复盘_认知题方向修正.md）

1. **背景**：上周面 open design 挂了，面试官 4 个核心问题（原文列出）。
2. **诊断**：现有速查页重"怎么做"轻"为什么"，与面试官考察方向错位。
3. **4 问逐个拆解**：每问 = 考察点 + 我当时的短板 + 修正后的答题骨架（引用新卡）。
4. **元方法论：怎么准备认知/趋势题**——不是背实现细节，是建"为什么这么做"的判断链：① 知道业界有哪些范式/竞品 ② 知道自己选了什么、为什么 ③ 知道代价和诚实边界。
5. **回流清单**：5 张新卡已加到 stealth.html（列卡名 + 所在组）。
6. **下次认知层自测 checklist**：6 条自测（状态机权衡能讲吗 / 多 Agent 竞品能列 5 个吗 / coding agent 开源生态知道吗 / 复杂度能讲必要性吗 / 诚实边界主动说吗 / 模型栈真相记得吗）。

## 5. 插入锚点与实现方式

- **Manager 3 张**：插在 stealth.html 525 行（"这项目真上生产了吗"卡的 `</div>`）之后、527 行 `<!-- Code 智能体 -->` 注释之前。
- **Code 2 张**：插在 701 行（"和 Cursor/Aider/Devin 比"卡的 `</div>`）之后、703 行 bagu 分类的卡之前。
- **方式**：用 Edit 工具按锚点字符串插入（5 张卡是小改，不用 GUIDE §3 的 Python splice）。每张卡完整 HTML（含 data-g、data-kw、core、card-body）。
- **不动**：现有 27 张卡一字不改；`getGroup` / `subOrder` 不动（补进现有组，路由已支持）。

## 6. 事实校准清单（防穿帮，写卡时逐条核对）

- ✅ 可说：LangGraph 39 节点状态机（说"接近 40"）；7 组条件边；probe 在 plan 前；HITL 两套；自进化 shadow→金丝雀 5%→A/B（lift +0.03 晋级/-0.06 回滚）；Manager 模型 qwen3.5-flash；Code 18 工具=只读 11+写 7；ReAct=ToolNode+function calling；AST 用 typescript-estree；自研向量（text-embedding-v3+内存余弦+sha256）。
- ⚠️ 软化：下游 Specialist 说"十几个"（不报 12/14 死数）；Bandit/RL/Causal 三套自适应路由（说"可能 over-engineered"时不否定其存在）。
- ❌ 别说：Supervisor 模块（叫总管/Router，说"Supervisor 式"可以）；失败归因是 LLM（纯规则）；Claude/GPT 是 Agent 部署模型（实为 qwen）；Chroma/Pinecone/Neo4j（自研）；Diff 预览用户确认才执行/代码审查 Agent/HITL 写确认（未实现）；任何编造百分比。
- opencode/ohmyopencode 是联网核实（2026-07）：opencode=SST/Anomaly 开源 terminal coding agent 75+模型；ohmyopencode=社区配置生态（opencode-config-tool）。

## 7. 风格规范（GUIDE §6）

- declarative 陈述句为主；正文每段 `<strong>段首标签。</strong>` 开头，2-4 段。
- core 是带机制名 + 结构的浓缩句。
- ①② 可内联枚举，不堆成 ①②③④⑤ 速查表。
- 标题不带英文项目名前缀。
- 概念层不堆魔法数字——但 M-3（39 节点）、C-2（18 工具）这两张本身讲数字合理性，数字是主题必带，属 GUIDE §6.4 的"机制/亮点卡带关键数"例外。

## 8. 收尾

- **bump sw.js**：`kb-v314` → `kb-v315`（本地与 origin 一致为 v314，干净，直接 +1）。
- **grep 校验**：Manager 组卡片数 11→14、Code 组 16→18；新卡 data-g 取值正确（`Manager 智能体` / `Code 智能体`）；div 开闭平衡；标题无英文项目名前缀；无 `[loop·待复核]` 残留。
- **git**：个人账号提交推送（不用公司账号）。

## 9. 验收标准

- [ ] stealth.html Manager 组 14 张、Code 组 18 张（各 +3/+2）
- [ ] 5 张新卡 data-g 正确、getGroup 能路由到对应子组
- [ ] div 标签平衡，`<script>` 完整
- [ ] 所有数字对照校准文档立得住（无编造百分比/死数）
- [ ] sw.js `CACHE_NAME` 已 bump 到 kb-v315
- [ ] reviews/open-design_面试复盘_认知题方向修正.md 已写
- [ ] 用个人 GitHub 账号提交推送
