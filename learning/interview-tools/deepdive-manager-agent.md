# Manager_Agent — 金牌项目深挖稿

> **用途**：面试当场可念版。被问"讲讲你的 AI 项目 / Multi-Agent 怎么做 / LangGraph 实战 / 怎么保证 Agent 质量"任意一题，都从这份稿切入。
> **念法节奏**：电梯演讲 30 秒 → 业务背景 30 秒 → 架构 1 分钟 → 深挖锚点按追问展开 → 量化与边界收口。
> **总控制**：完整讲 3-4 分钟，被追问可延展到 8-10 分钟。
> **素材出处**：stealth.html M0-M14 + 简历 resume.typ + 项目源码 `/Users/didi/work/agent-main/Manager_Agent/`。

---

## 一、30 秒电梯演讲（必背，张口就来）

> **Manager_Agent 是基于 Nuxt 4 + LangGraph 的多 Agent 编排网关**——本身不写 SQL、不建向量、不改代码，只做意图路由 + 任务规划 + 12 能力 Agent 调度 + 全局 Critic 质检。**39 节点状态机 + 40 条边（含 20 条件边）+ Probe/Health 双层探活 + Shadow→Canary→Promote 自进化 + HITL Checkpoint 三后端**。**最有工程含量的不是用 LangGraph，是把 LangGraph 当骨架自研了统一重试预算 + Critic 仲裁 + 失败归因 11 类 + 经验回放四件套**——这套让多 Agent 系统在中低并发能稳定跑。

**钩子三件套**：编排网关定位（不是单点能力）+ 量化产出（39 节点 / 12 Agent / 4.6 万行 / 145 个 managerGraph.*.ts 文件）+ 核心创新（Probe-before-plan + Self-Evolution 四件套）。

---

## 二、业务背景（30 秒，先讲为什么做）

**痛点定位**：企业级 AI 助手需要统一调度多个专业 Agent（知识库 / NL2SQL / 代码 / 爬虫 / GUI / 办公 / 多模态），但<strong>"一个 Prompt 包打天下"无法支撑</strong>——单 prompt 试图覆盖所有意图，准确率低、context 爆炸、无法针对性优化。多 Agent 各自对外又导致用户找谁、Agent 间不协作。

**核心洞察**：**多 Agent 系统的瓶颈不是单 Agent 能力，是编排层的可靠性**——LLM 路由不可靠、工具调用会失败、失败归因难、经验无法沉淀。Manager_Agent 解决的是<strong>"如何让 12 个专家 Agent 协同工作且整体可审计"</strong>。

**金句钩子**：**"多 Agent 不难，难的是带可观测性、可自进化、可 HITL 的企业级编排。"**

**诚实档位（必带，防被问"上线了吗"翻车）**：偏 demo / 教程级——<strong>54k+ 行 TS 工程量大但没接真实业务流量</strong>，jsonl 文件存储默认、单测几乎 0、207+ 环境变量但无 prod 数据。<strong>机制设计强但实测数据弱</strong>，面试讲设计思路不讲数据指标。

---

## 三、架构（1 分钟，先说清楚再展开）

### 编排层 vs 专家层硬边界

Manager 不做 SQL / 不建向量 / 不改代码——<strong>总管只做意图路由 + 任务规划 + 结果汇总 + Critic 质检</strong>。专家 Agent（12 个）各自负责能力层。这是<strong>"编排层管做什么，专家层管怎么做"</strong>的硬边界。

### LangGraph 状态机 39 节点拓扑（背到能脱口而出）

```
START → resource_node → tool_health → probe_node → metacog_node
  → security_gate → decompose → intent_classify → route
  → prefetch → {clarify | web_search | planner | db | rag | code | admin
                | crawler | gui | clean | visualize | report | multimodal | music | video}
  → planner → scheduler_node → execution_mode_node → vote_aggregator_node
  → plan_lint → {plan_preview | multi | clarify | finalize}
  → multi → synth → evaluator_node → critic → optimizer_node
  → {clarify | multi(replan) | fix | verifier}
  → admin_confirm_resume (HITL 后恢复节点)
  → fix → synth (闭环重试)
  → verifier → monitor_node → finalize → END
```

**30 秒压缩版**（先念这个再展开）：5 节点预处理（resource→health→probe→metacog→security）+ 4 节点路由（decompose→classify→route→prefetch）+ 14 专家节点 + 7 节点质检闭环（planner→lint→multi→synth→evaluator→critic→optimizer→verifier→finalize）+ 1 HITL 恢复节点 + fix→synth 重试闭环。

### Probe + Health 双层探活

- **Probe（规划前快筛）**：在 planner 之前用 Promise.allSettled 并行探活 5 下游（RAG/DB/Crawler/GUI/Code），结果进 state.probe，Router/Planner 看到的是<strong>客观事实</strong>而非"猜下游有没有"
- **Health（重量级复核）**：tool_health 节点用 manager-metrics.jsonl 滚动窗口算 p95，分级 healthy/degraded/down
- **Scheduler 联动**：down 移除 allowedAgents；degraded maxParallel-1 + timeoutScale+0.15；db/rag 即使 down 但历史 p95>0 不强制 skip

### HITL Checkpoint 三后端

file（默认）/ redis（生产）/ dual（强一致兜底），TTL 24h。高风险操作触达时 graph 不发 final 发 saveHumanConfirmCheckpoint，确认文本不写入 session.messages（防 RAG 污染）。

---

## 四、5 个深挖锚点（面试官追问任何一个，深入讲）

### 锚点 1：Probe-before-plan（减少幻觉路由）

**问题**：纯 LLM 意图分类不可靠——LLM 不知道下游服务真实状态，可能把"查销售数据"路由到 down 的 RAG。

**机制**：规划前先 Promise.allSettled 探活 5 下游（DB/RAG/Crawler/GUI/Code），结果进 state.probe。Router/Planner 看到"客观快照"而非"猜下游有没有"。

**杀手锏**：DB probe 还检查 `dbConnBad`（连接名带 `_db` 后缀 → 端口冲突误连）。

**边界（诚实承认）**：Probe 不缓存，每次会话跑一遍。timeoutMs 限制（DB 12s / RAG 12s / crawler+gui health 4s）。<strong>没做过误判率统计</strong>——这是观测盲区。

**金句**：**"Probe-before-plan 是 Compound AI Systems 里 retrieve-before-generate 思路延伸：把'下游能力快照'作为规划上下文，比纯 LLM 意图分类更稳。"**

### 锚点 2：统一重试预算（防 recursionLimit 死循环）

**问题**：LangGraph 默认 recursionLimit=25，但 multi + 一次 fix 循环就超。

**机制**（managerGraph.retryBudget.ts）：
- 单步 maxRetriesSingle 默认 1（≤3）
- 多步 maxRetriesMulti 默认 2（≤5）
- 全局 MANAGER_MAX_RETRY 默认 1（≤5）
- recursionLimit 默认 48（25-120 可配）

**关键认知**：canManagerRetryMore 是 <code>retryCount < maxRetry AND retryCount < ceiling</code>——<strong>两条件取交集</strong>。全局 MANAGER_MAX_RETRY=1 时即使 maxRetriesMulti=2，<strong>实际最多重试 1 次</strong>。全局 budget 是更紧的约束。

**诚实边界**：recursionLimit 是<strong>兜底不是策略</strong>——好系统在 48 触顶前就该识别死锁。改进方向是 state hash 重复检测 + 工具调用序列重复检测 + 横跳循环（A→B→A→B）语义级检测——<strong>这些都还没实现</strong>。

### 锚点 3：Plan-and-Execute + Critic 仲裁（Critic 破坏分层悖论）

**问题**：Multi-Agent 系统既要并行调度（Plan-and-Execute 强），又要质量门控（Critic 仲裁）。

**机制**：
- Planner 一次出全局 plan → Executor 并行调度 → Synth 综合
- Critic 事实性审查（输出 {pass, reason}）
- Evaluator 质量评分（输出 {recommendation, score}）
- accept 阈值（evaluatorNode.ts 写死）：>= 0.65 accept / < 0.65 retry_if_possible / < 0.45 retry
- 扣分规则：无答案 -0.28 / 无 evidence -0.22 / 每个 error -0.08（封顶 -0.3）/ needsClarify -0.16 / 每个 unsupported claim -0.03（封顶 -0.2）

**Critic 悖论（最致命杀手锏）**：Critic 做事实审查必须懂专家产出（懂 SQL / 懂截图 / 懂 JSON），懂专家产出就破坏"编排层不碰专家细节"的分层。

**破解话术（诚实分级版）**：让 Critic 审 <strong>"Agent 自己生成的 summary + evidence 列表"</strong>而非 raw output——<strong>间接审查</strong>（criticEvidence.ts 的 formatEvidenceForCriticAudit 函数做这层）。<strong>但"靠 evidence_id 反查源码 / 重跑 SQL 校验"是设计思路，未实现</strong>——当前只是 prompt 里要求 critic 引用 evidence_id，<strong>没做闭环反查校验</strong>。诚实答："Critic 审的是 evidence 列表的格式化版本，反查校验是 roadmap，未落地。"

**vs OpenAI Swarm（被问"为什么不用 Swarm"必答）**：Swarm 的 handoff 模式更轻（无中心 Supervisor、Agent 间直接转交），Manager Supervisor 要维护 39 节点 + 8 类 WS 消息。选 Supervisor 的真理由是企业级 AI 助手需要<strong>可审计 + 质量门控</strong>，Swarm handoff 链路难追溯。诚实补一句"Swarm 2024 年底已改成 Agents SDK，但 handoff 范式概念最清晰所以拿来对比"。

### 锚点 4：Self-Evolution Layer（shadow → canary → promote）

**问题**：Prompt 写死不可进化；进化又怕过拟合 / 污染。

**四件套机制**：
- Prompt 补丁：失败洞察 → 写 .data/manager-prompt-patches.shadow.json，晋级后注入 router/planner
- 策略金丝雀：MANAGER_POLICY_CANARY_PERCENT=5，按 sessionId SHA256 稳定分桶
- 进化实验：hypothesis → running → promoted/rolled_back/rejected，minSample 8 / promote lift 3% / rollback drop 6%
- 记忆治理：每 10min maybeCurateManagerMemory，同 key 保留高分样本，< 0.42 进 quarantine

**经验回放**：successScore >= 0.75 记 win；向量召回（OpenAIEmbeddings text-embedding-v2）+ Jaccard 混合排序（jieba 分词），注入 router few-shot。

**三大致命边界（被问必崩，必须准备）**：
1. **7 个 golden 做不了统计显著 A/B**——Wilson 95% CI [59%, 100%]，真实可靠率可能低到 59%。<strong>7 个是冒烟级不是质量证明级</strong>。
2. **经验库只进不出会污染**——没做经验衰减。
3. **LLM 评 LLM 自嗨**——假设生成用 LLM，执行用 LLM，评估也用 LLM。LLM 在错误 prompt 上反复生成同一错 patch，shadow 命中多次晋级错的（自我强化回音室）。

**诚实收口**："框架先行，效果未严格验证；接生产后补三件——① 30+ golden + hold-out 留出集；② 线上流量 shadow 对比；③ power analysis 算显著性。Self-Evolution 是 roadmap，不是已验证机制。"

**阈值 power analysis 漏洞**：minSample 8 / lift 3% / rollback 6% 都是源码默认值（evolutionExperiments.ts:82/87/92 都是 `?? 8`），<strong>无 power analysis 推导</strong>。被追"8 怎么定的"诚实答"默认值未推演，改进方向是按 effect size + 显著性反算样本量"。

### 锚点 5：失败归因 11 类 + 经验回放

**问题**：失败 case 不归因就无法进化；归因错误假设生成器学错。

**11 类失败清单**（按 attributeFailure 优先级排序，先返先胜）：

```
高严重度:
  policy_boundary    能力边界拦截（capabilityOk=false，最优先）
  timeout            时间预算将尽（timeLeft < 1500ms）
  tool_failure       Agent 输出标记失败
  synthesis_error    有结果但无最终合成

中严重度:
  clarify_needed     需澄清
  evidence_gap       有 agent outputs 但无 evidence
  search_gap         无 search 命中
  verification_gap   有 evidence 但无 agent outputs
  route_error        路由错
  plan_error         规划相关弱点

兜底:
  unclear            无明显失败信号
  + success          无失败信号（正常成功）
```

**11 类失败 + success = 12 总分类**，按严重度分 4/6/1 三档。

**多标签处理（漏洞）**：默认单标签按优先级取主因——真实 case 经常同时命中 2 类（如 tool_failure + evidence_gap），当前返 tool_failure。<strong>多标签场景应该每标签一条假设，但当前实现只生成一条</strong>。

**混淆矩阵没测**：11 类的边界没经过严格分类学设计，<strong>evidence_gap vs verification_gap vs search_gap 边界模糊</strong>（都是"缺证据类"）。

---

## 五、量化指标（最致命的追问，必须答得有数字 + 诚实边界）

### 数字口径校准（防被查 git ls-files 翻车）

| 简历口径 | 源码实际 | 差距 |
|---------|---------|-----|
| 213 个 TS 文件 | 307 个 TS 文件 | 虚低 30% |
| 约 4.6 万行 | 53k+ 行 | 虚低 13% |
| 207 个 MANAGER_* 环境变量 | 220 个 | 虚低 6% |
| 143 个 managerGraph.*.ts 文件 | 145 个 | 虚低 1% |
| 42 条边含 14 条件边 | 40 条边含 20 条件边 | 边数接近，条件边差 43% |
| 39 节点 | 39 节点（精确） | ✓ |
| 12 Agent | 12 Agent（精确） | ✓ |

**面试现场用真数**：主动说"简历 213/4.6 万是早期口径，现在已经 307/53k"，比被识破要稳。

### Eval / Golden 三层体系（被问"测试怎么做"必答）

- **JSON 结构校验**（CI 门禁，零 LLM 调用）：scripts/check-eval-golden-all.mjs 只验证字段完整性
- **smoke 测试**（38 个脚本）：图编译、子句拆解、计划覆盖、调度、路由 JSON 解析等单点验证
- **E2E 黄金路径**（11 条端到端用例）：rag-hit / db-read / db-metrics-direct / db-chart-shortcut / crawler-web-summary / rag-miss-graceful / admin-confirm-flow / admin-confirm-cancel / clause-decompose-structure / multi-db-then-report

**7 个 golden JSON 文件**：e2e-paths(11) / route-media(4) / clause-decompose(3) / gui-route / multi-latency / smoke / web-search

**E2E 期望延迟**：DB 120s / RAG 180s / Crawler 300s / 知识库 miss 120s / Admin 180s

### 关键打分规则（evaluatorNode.ts 写死）

- accept >= 0.65 / retry_if_possible < 0.65 / retry < 0.45
- 无答案 -0.28 / 无 evidence -0.22 / 每个 error -0.08（封顶 -0.3）/ needsClarify -0.16 / 每个 unsupported claim -0.03（封顶 -0.2）/ 每个 timeout -0.06（封顶 -0.16）/ 图表完整性失败 -0.24

---

## 六、可观测性盲区（被问"哪一步慢怎么定位"必答）

### 当前三层（必背）

- **Metrics 层**：每个 phase/agent 调用 append 到 .data/manager-metrics.jsonl
- **p95 算法**：tool_health 节点用滚动窗口（默认最近 50 条）+ 排序取 95 分位
- **Trace 层**：@langchain/langgraph 0.3 自带 LangSmith trace，<strong>到 node 级不到 span 级</strong>

### 致命缺失

- <strong>没接 OpenTelemetry</strong>——LangSmith trace 不是 OTel 标准
- <strong>没做 dashboard</strong>——只有 /api/metrics 返回 JSON
- <strong>没做告警</strong>——Probe 误判 / Critic 否决率突增 / token 预算超限都没告警

**改进方向**：接 OTel + Grafana dashboard + 关键指标告警（路由准确率 / Critic 否决率 / recursionLimit 命中率 / p99 延迟）。

---

## 七、3 个最容易被追问卡的点（提前准备）

### 1. 「自进化的真实效果数据？」
老实说项目偏教程 / 框架先行，没接真实流量；强调机制设计（样本量 8、lift 3%、rollback 6%、稳定分桶）。补一句"阈值都是源码默认值无 power analysis 推导"。

### 2. 「多实例 WS 怎么扩展？」
承认单进程内存 Map 限制（sessions / runs / sessionMeta 都在内存），聊 Redis pubsub + sticky session 方案。

### 3. 「测试覆盖率？」
诚实说以 smoke + E2E golden 为主（38 脚本 + 11 端到端），单测薄弱（只有 1 个）；强调"Agent 测试本身难，golden path 比单测更接近真实质量"。

---

## 八、反问面试官 3 件套（每次必问）

1. **路由不可靠**："你们多 Agent 系统怎么处理 LLM 路由不可靠？我们用 probe-before-plan + 规则粗分 LLM 细分，但都还是工程层兜底，真正解决可能要等模型层能力提升。你们怎么看？"

2. **工具失败重试**："工具调用失败重试策略是什么？我们用统一预算 + Critic 仲裁，但根因可能要等模型层提升——recursionLimit 是兜底不是策略。你们有没有遇到 fix→synth 死循环？怎么破？"

3. **长尾延迟**："Multi-Agent 的 p99 延迟你们怎么压？我们没做延迟预算——recursionLimit 48 是步数上限不是时间上限。长尾是 Multi-Agent 生产化的硬骨头，你们做了预算制 / 并行化 / 早返回 / 超时降级哪些？"

**反问价值**：从"被问"变"主动对话"，证明有 Staff Engineer 视角；暴露面试官深度（如果答不出，说明这公司 Multi-Agent 也没真生产化）；给 offer 决策提供情报。

---

## 九、收口金句

> "Manager_Agent 不是 LangGraph demo，是带 HITL / 自进化 / 可观测性的企业级编排。**机制设计强但实测数据弱**——这是诚实定位。真正解决 Multi-Agent 的根问题要靠模型层提升，我用 probe-before-plan + 统一预算 + shadow A/B 把工程层兜底做扎实——这是我转 LLM 工程化的判断。"
