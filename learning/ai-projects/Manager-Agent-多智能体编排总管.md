# Manager Agent · 多智能体编排总管 · 面试深度说明书

> **一句话定位**：14 个专业 Agent 之上的"总管/编排层"——统一 WebSocket 入口，把用户一句话变成可执行的多步 DAG 计划，调度 10+ 下游专家 Agent，汇总、审计、自我进化。
>
> **端口** `13106` · **技术栈** Nuxt 4 + Nitro + LangGraph(JS) + WebSocket + Zod + LangSmith + Postgres/Redis checkpoint · **模型** DashScope qwen3.5-flash(OpenAI 兼容)
>
> **配套阅读**：[Code Assist 工程化代码助手](Code-Assist-Agent-工程化代码助手.md)（本项目的下游之一） · [Multi-Agent](../agent-books/Multi-Agent.md) · [ReAct 反思 任务规划](../agent-books/ReAct-反思-任务规划.md) · [异常处理 安全 熔断](../agent-books/异常处理-安全-熔断.md)

---

## 0. 30 秒电梯演讲（开场怎么说）

> "我深度参与了一个 **LangGraph 多智能体编排系统**——它是 14 个专业 Agent（RAG 问答、NL2SQL 问数、代码助手、爬虫、GUI 自动化、办公 Copilot、多模态、作曲、视频…）之上的**总管层**。用户只跟总管对话，总管负责**理解意图 → 路由 → 规划多步 DAG → 并行调度下游 → 汇总 → critic 审计 → 自我进化**。
>
> 它有三个我觉得最值得讲的工程亮点：第一，**路由不是单次 LLM 猜**，而是 Bandit(Thompson 采样) + RL(Q-learning) + Causal(因果归因) 三套自适应引擎并行喂提示；第二，**Agent 会自己变聪明**——失败归因沉淀成 Prompt 补丁和硬规则，经 shadow→金丝雀→A/B 验证后才晋级；第三，**HITL 人工确认**和**证据闸门**保证高风险操作可审计、无引用不强行作答。"

**为什么面试稀缺**：多 Agent 编排 + LangGraph 状态机 + HITL + 自进化是一个仓库全覆盖的高频考点，且这是**真实多服务架构**，不是 PPT。

---

## 1. 项目定位与核心价值

### 1.1 编排层 vs 专家层（最重要的边界）

总管**不做专业事**——不写 SQL、不改代码、不建向量库。它只做七件事：

```
理解意图 → 路由 → 规划 → 调度下游 → 汇总 → critic 审计 → 自进化
```

这是经典的 **Supervisor / Orchestrator 模式**。为什么不让一个"超级 Prompt"包打天下？

| 方案 | 问题 |
|------|------|
| 单 Prompt 端到端 | 上下文爆炸、无法并行、无法 HITL、无法增量进化、出错难定位 |
| 每个能力一个 Agent 但无编排 | 用户要自己知道找谁、跨 Agent 协作无法串联、状态散落 |
| **编排层 + 专家层（本项目）** | **职责清晰、可并行、可 HITL、可观测、可进化** |

### 1.2 和"纯 ReAct Agent"的区别

普通 ReAct 是"一个 Agent + 一堆工具"的循环。Manager 不是——它是**状态机编排多个 Agent**：

- ReAct 的"工具"是无状态的函数调用；Manager 的"工具"是**各自带状态、带自己 LangGraph、带自己 WS 的完整服务**。
- ReAct 靠 LLM 决定下一步；Manager 用 **probe 探针 + 结构化路由 + Planner** 决定，LLM 只是其中一环，且每一步都有确定性兜底。

### 1.3 能力边界（面试要主动说清）

| 适合 | 不适合 |
|------|--------|
| 统一聊天入口、多 Agent 路由 | 在总管进程里做重型爬取/文件处理 |
| 人工确认高风险操作 | 复杂 GUI 自动化（交给 Lobster_Agent） |
| 任务编排与多步 DAG | 替代完整 CI/CD |

---

## 2. 技术架构总览

### 2.1 分层架构

```
┌─────────────────────────────────────────────────────────────┐
│  前端  Nuxt 4 + Vue 3（Cosmic 聊天页 / 进化看板）            │
└───────────────┬─────────────────────────────────────────────┘
                │ WebSocket (8 种入站事件 / 12+ 种出站事件)
┌───────────────▼─────────────────────────────────────────────┐
│  Manager 总管 (13106)                                        │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  LangGraph 状态机 (38 节点)                           │   │
│  │  resource→tool_health→probe→metacog→security_gate     │   │
│  │  →decompose→intent_classify→route→prefetch→plan       │   │
│  │  →execute(DAG 调度)→synth→critic→optimizer→verifier   │   │
│  │  →monitor→finalize                                    │   │
│  │  旁路：clarify / web_search / fix / admin_confirm     │   │
│  └──────────────────────────────────────────────────────┘   │
│  + 自我进化飞轮（Bandit/RL/Causal + shadow→金丝雀→A/B）     │
│  + 四层记忆 + 向量召回（DashScope text-embedding-v2）        │
│  + 自主循环（autonomyPlugin 每 10min tick）                  │
│  + 可观测性（jsonl 原始流 → metrics/Prometheus/OTel 三出口） │
└──┬──────┬──────┬──────┬──────┬──────┬──────┬──────┬─────────┘
   │ WS   │ WS   │ WS   │ WS   │ WS   │HTTP  │HTTP  │HTTP
   ▼      ▼      ▼      ▼      ▼      ▼     ▼     ▼
  DB    RAG   Code   Crawler Lobster Admin Music Video ... (10+ 专家)
 13101  13102 13103  13104   13108  13105 13110 13111
```

### 2.2 技术栈选型理由

| 技术 | 选型理由（面试可答） |
|------|------|
| **LangGraph** | 多 Agent 编排是有分支/回环/HITL/失败恢复的**状态机**，不是单次函数调用；LangGraph 提供 checkpoint、条件边、recursionLimit、LangSmith trace |
| **WebSocket** | 编排是**双向**的：服务端流式推 phase/step_status，还要反过来问前端要确认（plan_confirm/human_confirm）；SSE 单向做不到 |
| **Zod** | 入站消息 discriminatedUnion 强校验，把非法包挡在 graph 之前 |
| **Postgres + Redis checkpoint** | 跨 run 续接（pg thread_id=sess-{sessionId}）+ HITL 快照三级存储 |
| **LangSmith / OTel** | 多 Agent 问题定位复杂，需 trace 到每个节点每次调用 |

---

## 3. 核心流程：一次请求的生命周期

### 3.1 主干状态机（背下来）

```
START
  │
  ▼
resource_node        ← 预算/模型选择(modelTier)
  ▼
tool_health          ← 下游 Agent 健康探测（down 的不进 allowedAgents）
  ▼
probe_node           ← 轻量探活：DB 表匹配 / RAG 文档命中数（规划前快照能力）
  ▼
metacog_node ──(能力边界外? final 非空)──► finalize   ← 早退：越界请求直接返回
  │
  ▼
security_gate        ← 写操作/SQL 注入风险识别
  ▼
decompose            ← 多意图句拆成 1-8 条 TaskClause（25% 灰度）
  ▼
intent_classify      ← 意图识别（四级降级：rag_fast→merged→llm→skip）
  ▼
route                ← 产出 intent + allowedAgents（注入 5 类 advice）
  ▼
prefetch             ← 并行预取 DB plan ∥ RAG retrieve（降首步延迟）
  │
  ├── intent=single ───► 对应执行节点(db/rag/code/...)
  │
  ▼ intent=multi
planner → scheduler → execution_mode → vote_agg → plan_lint
  │                                              │
  │                                     [plan_preview HITL]
  ▼                                              ▼
multi (DAG 优先级并行调度) ──► afterExecution 谓词
  │                              │
  │                   needsHumanConfirm? ──► finalize(不发 final)
  │                   needsClarify?     ──► clarify
  ▼
synth → evaluator → critic ──(要修)──► optimizer → fix ──► synth (回环)
                       │
                       ▼ (通过)
                  verifier → monitor → finalize → END
```

> **⚠️ 注意节点顺序（critic 纠正点）**：是 `security_gate → decompose → intent_classify`，即**先拆子句再做意图识别**。理由：一句里塞两个意图时 LLM 容易"取平均"，拆成子句后 intent_classify 的 merged 理解更准。很多文档写反了，面试要按 `managerGraph.graph.ts` L121-123 为准。

### 3.2 关键设计：probe 在 plan 之前

> "先确认下游**有没有文档 / 库是否通**，再让 LLM 规划，减少幻觉式路由。"

probe 用轻量 HTTP（DB probe 12s、health probe 4s 超时不阻塞主路径），把下游能力快照喂给 Planner，避免在无 RAG 命中时硬加 RAG 步。

### 3.3 端到端时序（一次 multi 意图请求）

```
用户:"查张三销售数据并画柱状图"
  → resource/tool_health/probe (能力快照)
  → decompose 拆成 [db:查张三销售] + [visualize:画柱状图]
  → route: intent=multi, allowedAgents=[db,code,visualize]
  → prefetch 并行: DB plan ∥ RAG retrieve
  → plan: steps=[db→code→visualize] (code 算数, visualize 出图)
  → plan_lint: 校验实体"张三"在 query 里、依赖关系对
  → [plan_preview]: 发 plan_steps 给前端, await 用户确认 (≤600s)
  → multi DAG 调度: db 先跑(高优先级) → code(覆盖权威) → visualize(规则出图)
  → synth 合成 → critic 审计 → verifier 验真 → finalize
  → 进化飞轮: attributeFailure → 写记忆 → 向量索引 → 失败洞察 → 进化实验
```

---

## 4. 关键技术深挖（重头戏）

### 4.1 LangGraph 状态机：条件边谓词 + Annotation reducer

#### （1）条件边谓词驱动所有旁路与回环

整张图 38 个节点，所有分叉（clarify/web_search/fix/admin_confirm_resume/plan_preview）都由 `addConditionalEdges` 的**内联谓词函数**决定，节点本身不感知图结构。

```ts
// managerGraph.graph.ts —— 旁路全靠条件边谓词
function routeAfterPrefetch(s: any) {
  if (Boolean(s?.meta?.needsClarify)) return 'clarify'
  if (shouldRouteToWebSearch(s)) return 'web_search'
  return s.intent === 'multi' ? 'planner' : s.intent   // single 直跳执行节点
}

// 13 个执行节点(db/rag/code/.../multi)共用一个出口谓词
const afterExecution = (s: any) => {
  if (Boolean(s?.meta?.needsHumanConfirm)) return 'finalize'
  if (Boolean(s?.meta?.needsClarify)) return 'clarify'
  return 'synth'
}
```

**为什么这么设计（面试金句）**：把路由逻辑收口到纯函数谓词里，节点只负责写 state——于是节点是**纯函数**，可单测、可复用（`createMetacogNode` 根本不知道自己被谁调用）；整张图拓扑收口在 `graph.ts` 一个文件，重构时只改边不改节点；LangSmith trace 里每条边为何被选一目了然。

#### （2）Annotation reducer 决定字段合并语义（LangGraph 最隐蔽的坑）

```ts
// managerGraph.ts —— 每个 channel 配 reducer，决定多节点并发写时怎么合并
messages: Annotation<BaseMessage[]>({
  reducer: (x, y) => x.concat(y),        // 累积对话历史
  default: () => [],
}),
entities: Annotation<{ names: string[]; ... }>({
  /**
   * 仅用本轮路由返回值覆盖，不做跨轮累积合并。
   * 否则前几轮的人名/记录会一直留在 state，污染 planLint、规划与下游提示。
   */
  reducer: (x, y) => y === undefined ? x : normalizeEntities(y),
}),
```

> **面试金句**："reducer 选错是 LangGraph 最隐蔽的 bug——图能跑，但 state 悄悄错了。"
>
> - `messages` 用 concat（累积）
> - `entities` **故意用覆盖**（不是累积），带注释说明理由——否则上周的"张三"会污染今天的 planLint
> - `results` 用 `{...x,...y}` 浅合并（各 Agent 写各自的 key 互不冲突）
> - `retryCount`/`humanDecision` 用 last-writer-wins

#### （3）双闸 retryBudget 防 fix→synth 死循环

LangGraph 的 `recursionLimit` 是硬墙（撞上直接抛异常）。Manager 调到 **48**（默认 25 装不下 multi 多步 + fix 回环），并用业务层软上限提前软着陆：

```ts
// managerGraph.retryBudget.ts
export function resolveManagerRetryLimits(state, policy?) {
  const isMulti = state?.intent === 'multi' || (state?.plan?.length ?? 0) > 1
  const maxRetries = isMulti
    ? Math.min(5, policy?.critic?.maxRetriesMulti ?? 2)    // multi 给 2 次
    : Math.min(3, policy?.critic?.maxRetriesSingle ?? 1)   // single 给 1 次
  return { retryCount, maxRetry, maxRetries, isMulti }
}
export function canManagerRetryMore(limits) {
  const ceiling = limits.isMulti ? limits.maxRetries : limits.maxRetriesSingle
  return limits.retryCount < limits.maxRetry && limits.retryCount < ceiling
}
```

> **面试金句**："框架硬约束（recursionLimit）+ 业务软约束（retryBudget）分层治理——业务层先软着陆，框架层兜底防穿。"

---

### 4.2 意图路由：四级降级 + 路由不漂移三重防御

#### （1）意图分类四级降级链

`intent_classify` 不押宝单次 LLM，而是按优先级尝试四条路径，任一挂掉自动降级：

```
rag_fast (playbook 命中 score≥0.78，直接复用，省一次 LLM)
   ↓ 未命中
merged   (一次 LLM 同时做多轮合并+槽位+意图，替代 3 次调用)
   ↓ 失败
llm      (单次 LLM 意图识别)
   ↓ 失败
skip     (下游自行处理)
```

#### （2）路由不漂移的三重防御（面试高频："路由会不会错乱"）

| 防线 | 机制 | 代码 |
|------|------|------|
| ① 能力漂移降权 | 召回命中的 suggestedAgents 若含用户没要求的 agent，`score *= 0.35` | `userIntentSupremacy.ts` |
| ② 剔除误带 | 按意图结果剔除误带的 admin（`stripAdminIfNotInCurrentTurn`） | `routeFinalize.ts` |
| ③ PlanLint 越权检查 | multi 任务下 step 的 agent 必须在 allowedAgents 内 | `planLinterNode.ts` |

加上 `dbOnlyRoute`/`ragOnlyRoute` 收敛：纯查库问句直接收敛为单 db，跳过 multi 扩写。

> **核心原则（routeFinalize）**：**路由 LLM 的 intent 是唯一权威，代码只做规范化/约束补全，不做意图翻转**。所有 advice（bandit/causal/...）都只是 `routerHintBlock` 提示文本，不直接改 intent。

---

### 4.3 三套自适应学习引擎（最大差异化亮点）

路由层注入 **5 类 advice**，其中三套是**自适应学习引擎**，职责正交、互不冲突：

#### （1）routeBandit —— Thompson 采样多臂老虎机（探索/利用）

每个意图（db/rag/code/...）维护一个 `Beta(α,β)` 分布的 arm。reward 来自 `compositeScore`，`α+=reward, β+=1-reward`。

```ts
// managerGraph.routeBandit.ts —— 用两个均匀随机数近似 Beta 采样
function sampleBeta(alpha: number, beta: number): number {
  const a = Math.max(0.5, alpha), b = Math.max(0.5, beta)
  const u1 = randomBytes(4).readUInt32BE(0) / 0xffffffff
  const u2 = randomBytes(4).readUInt32BE(0) / 0xffffffff
  const x = Math.pow(u1, 1 / a), y = Math.pow(u2, 1 / b)
  return x + y > 0 ? x / (x + y) : 0.5
}
// 探索按 sessionId 稳定分桶（默认 8%，上限 25%）
export function sessionUsesBanditExplore(sessionId?, percent = 8) {
  const h = createHash('sha256').update(`route-bandit|${sid}`).digest()
  return h.readUInt32BE(0) % 100 < percent
}
```

> **为什么 Thompson 不用 UCB/ε-greedy**：Thompson 天然表达不确定性（样本少方差大更易被采到），是贝叶斯最优的 Bernoulli bandit 解，无需手调 ε。sessionId 分桶保证同一用户探索状态稳定不抖。

#### （2）routePolicyRl —— 上下文 Q-learning（critic 补漏点）

独立维护 5 个**上下文桶**的 Q 表：`global / clarify / slow / implicit / first_pass`，按当前会话特征路由到不同 Q 表，用 `advantage + baseline` 更新。

> **为什么 bandit 和 rl 同时跑**：bandit 回答"这个意图整体回报高不高"（无上下文），rl 回答"在当前上下文（比如 slow 桶）下哪个意图 Q 值高"（有上下文）。冲突时两段都写进 prompt，LLM 自己权衡——**用户意图最高**（userIntentSupremacy）。

#### （3）routeCausal —— 近似因果归因（ATT）

从历史 learning-signals 重建轻量结构因果图，对 4 个因子（needs_clarify / high_latency / implicit_stress / low_route_conf）计算**平均处理效应 ATT**（有因子组均值 − 无因子组均值），还能算 intent×factor 交互（如"低路由置信 + db 意图"组合特别容易失败）。

```ts
// managerGraph.routeCausal.ts —— ATT（条件均值差）近似因果
for (const factor of FACTOR_NODES) {
  const withF = signals.filter(s => signalFactors(s).includes(factor)).map(s => s.compositeScore)
  const withoutF = signals.filter(s => !signalFactors(s).includes(factor)).map(s => s.compositeScore)
  if (withF.length >= 3 && withoutF.length >= 3) {
    const effect = mean(withF) - mean(withoutF)   // ATT 近似
    edges.push({ from: factor, to: 'composite_outcome', effect, support: withF.length })
  }
}
```

> **面试金句**："Causal 用 ATT（条件均值差）而非真因果推断（DiD/IPTW）是工程取舍——样本小、计算轻、可解释；代价是混杂因子未控制，所以**只作 routerHintBlock 弱提示 + 10 分钟刷新防抖**，不直接改路由。这是'不是简单统计，是近似因果归因'的差异化亮点。"

#### （4）routeStrategy + worldModel（critic 补漏点）

- **routeStrategy**：动态阈值调节的真正执行者——产出 `preferClarifyBoost`、`clarifyThresholdAdjust`、`forceLowCostMode`、per-agent `healthPenalty`，把"近期质量低"翻译成"这次多澄清一点"。
- **worldModel**：per-session 快照，输出 `posture`（aggressive/balanced/conservative/clarify_first），这个姿态字**直接影响** clarifyThreshold/maxParallel/lowCostMode——它是路由决策的"元层"。

> 三套学习引擎的 reward **统一从 `unifiedLearning` 反喂**：一次 run 的 compositeScore 同时喂给 bandit 的 α/β、rl 的 Q-update、causal 的脏标记（触发 10 分钟重建）。

---

### 4.4 任务规划：四级产出链 + Planner 硬规则进化 + PlanLint

#### （1）planNode 四级产出链

```
① db_chart/db_only/rag_only/admin_only 快捷路径 (规则直出，不调 LLM)
   ↓ 不命中
② 单 intent 直出单步
   ↓
③ multi 走 LLM 规划 + 拓扑补全
   ↓ LLM 失败
④ tryRuleBasedMultiFallback 按 PIPELINE_AGENT_ORDER 枚举兜底
   ↓ 全失败
⑤ default 兜底
```

**PIPELINE_AGENT_ORDER（硬编码拓扑序）**：`rag → db → crawler → multimodal → music → video → clean → code → admin → visualize → report`（取数→清洗→计算→办公→输出）。

#### （2）Planner 硬规则进化（自我进化在规划层的落地）

Planner 维护 active（生效）+ shadow（候选）两套 JSON 规则。规则定义 `when` 条件 + `requireAgents`/`forbidAgents`/`requireAfter` 依赖：

```ts
// managerGraph.plannerRules.ts —— plan_lint 强制执行 active 规则
export function lintPlanWithPlannerRules(state, steps, rules): string[] {
  for (const rule of rules.rules) {
    if (!ruleMatches(state, rule, taskText)) continue
    for (const req of rule.requireAgents || [])
      if (!agentSet.has(req)) issues.push(`规划规则[${rule.id}]：缺少必需步骤 agent=${req}`)
    for (const ban of rule.forbidAgents || [])
      if (agentSet.has(ban)) issues.push(`规划规则[${rule.id}]：禁止 agent=${ban}`)
  }
}
```

shadow 规则 `confidence ≥ 0.68` 才能晋级 active。LLM Planner 会反复犯同类错误（漏 clean、visualize 不依赖 code），硬规则把"失败归因"沉淀成可执行的 lint 规则，让系统**越用越稳**。

#### （3）PlanLint 三档策略（不是一失败就阻断）

| 档位 | 触发 | 处理 |
|------|------|------|
| auto repair | route 含某 agent 但 plan 漏了 | `applyRoutePlanCoverage` 自动补全，不阻断 |
| soft pass | 纯 rag 任务的时间/对象口径丢失 | 降为非阻断，继续执行 |
| hard block | 关键实体丢失（DB 步没姓名）/ 越权 / 依赖不存在 | 生成 clarifyQuestions 走 clarify 旁路 |

---

### 4.5 下游编排：DAG 优先级调度 + 动态超时 + 熔断 + 证据闸门

#### （1）DAG + 优先级有限并行调度（不是 Promise.all）

execute 阶段是带依赖图 + 优先级的有限并行：每轮挑 ready（依赖已满足）步骤按优先级排序，在 `maxParallel` 内启动一批，`Promise.race` 等最快的一个完成再补批。

```ts
// managerGraph.multiNode.ts —— 优先级 = 下游深度×100 + agent基础优先级 - 健康惩罚
const stepPriority = (s: Step) => {
  const depth = computeDownstreamDepth(s.id)        // 被多步依赖的上游优先
  return depth * 100 + baseAgentPriority(s.agent)   // db/rag/crawler=300, code=240, visualize=140
       - healthPenalty(s.agent)                     // degraded=40, down=200
}
ready.sort((a, b) => stepPriority(b) - stepPriority(a))
```

> **设计理由**：深度大的上游优先跑缩短关键路径；数据源 Agent 高优先级保证数据先到；health 差的降权避免拖累批次。死锁兜底 `MAX_SCHEDULE_WAIT_SPINS=48` 防止依赖环卡死。

#### （2）动态超时缩放（不是固定值）

```ts
// managerGraph.agentRunner.ts
const scaledTimeoutForAgent = (agent, baseMs) => {
  const scaled = baseMs * timeoutScale * perAgent
  const p95 = toolHealthP95ByAgent.get(agent) || 0
  const p95Floor = p95 >= 8000 ? p95 * 1.2 + 5000 : 0   // 慢 agent 不被误杀
  const budgetCap = timeLeft > 8000 ? timeLeft - 4000 : maxStepTimeoutMs
  return Math.max(12000, Math.min(maxStepTimeoutMs, budgetCap, Math.max(scaled, p95Floor)))
}
```

四个因子：base×缩放、p95 floor（Docker 冷启动 DB p95 可能 20s，硬顶 10s 必超时）、budgetCap（不超全局 deadline）、下限 12s。

#### （3）运行时熔断 + retryable regex

连续失败 ≥2 次的 agent 加入 `runtimeCircuitOpenAgents`，可选 Agent（clean/visualize/report）被熔断降级跳过保核心链路。`retryable` 用 regex 判定：`timeout/econnrefused/503` 可重试，但 `permission/forbidden/invalid/syntax` 即使含 timeout 也不重试（避免对 403 无脑重试）。

#### （4）证据闸门 evidenceGate（无引用不强行 final）

```ts
// managerGraph.evidenceGate.ts —— finalize 前的事实性门禁
if (taskNeedsExternalSources(state) && !finalHasExternalSources(state))
  return { pass: false, reason: '联网/抓取任务缺少可核验来源（URL 或 AgentResult.sources）' }
if (agents.has('db') && !hasDbEvidenceInRun(state))
  return { pass: false, reason: '查数任务未获得有效数据依据' }
if (agents.has('rag') && !agents.has('crawler') && !agents.has('db'))
  if (!ragCites) return { pass: false, reason: '知识库检索未获得可引用片段' }
```

> **设计理由**：LLM 倾向于在无数据时编造流畅废话；闸门强制"无依据就不出结论"，把空结果路由到 clarify 或 fix。

---

### 4.6 双重事实性防线：evidenceGate + critic

- **第一道**：`evidenceGate`（上面）—— 结构性、无 LLM、快。
- **第二道**：`critic` LLM 审计 + `agentAnswerJudge` 结构化判定（`structuralAnswerVerdict` 置信度 ≥0.85 直接采信，否则才调 critic LLM）。

两者**交叉判断**避免 critic 幻觉式改道：

```ts
// managerGraph.criticEvidence.ts —— 评估器已确认有数据且高分时，忽略 critic 改道重试
export function criticRetryContradictsRunEvidence({ evaluation, minScore = 0.8 }) {
  const score = Number(evaluation?.score ?? 0)
  const hasData = evaluation?.hasDataEvidence || evaluation?.hasImplicitDataEvidence
  const rec = String(evaluation?.recommendation ?? '')
  if (!hasData || score < minScore) return false
  if (rec === 'clarify' || rec === 'retry') return false
  return true   // 证据已充分，禁止 critic 改道其它取数 Agent，只走 synthOnlyRepair 重汇总
}
```

**critic 快速路径**省调用：`shouldSkipCriticLlm` 对高置信简单任务（routeConfidence>0.9 且单步且非 multi）跳过 critic LLM，但有 `fast_path_blocked` 兜底（code/联网/证据门禁风险时强制不跳）。

---

### 4.7 HITL 人工确认：两套并存的机制（面试深挖点）

这是 Manager 最精巧的设计之一——**两套 HITL 对应两种 SLA**：

| 机制 | 适用 | 实现 | 超时 |
|------|------|------|------|
| **进程内阻塞型** | plan_preview（轻量、用户在场几秒回来） | 节点内 `await waitPlanConfirm()` 拿 Promise，WS 收 plan_confirm 调 `resolvePlanConfirm` 解开 | 600s |
| **跨进程持久化型** | admin 写操作（高风险、可能跨进程重启、需审计） | `saveHumanConfirmCheckpoint` 落 mem/file/Redis(24h TTL)，本 run 拦截不发 final，新 run 带 `resumeAdminConfirm` 从 metacog 直跳 admin_confirm_resume | 24h |

```ts
// planConfirmBridge.ts —— 进程内 Promise 桥
export function waitPlanConfirm(runId, previewId, timeoutMs = 600_000): Promise<PlanConfirmResult> {
  return new Promise((resolve) => {
    const timer = setTimeout(() => { waiters.delete(k); resolve({ action: 'cancel' }) }, timeoutMs)
    waiters.set(k, { resolve: (r) => { clearTimeout(timer); resolve(r) }, timer })
  })
}
```

> **⚠️ critic 纠正点**：admin 写确认的真实行为是——ws.ts 检测到 `meta.needsHumanConfirm` 时 `saveHumanConfirmCheckpoint + emitAdminHumanConfirmRequest` 后**直接 return，根本不发送 final**（图会跑到 finalize 节点，但 ws 层拦截了输出）。用户点确认后**新开一个 run**（新 runId + 新 AbortController），带入 `{...checkpoint, resumeAdminConfirm:true, meta:{allowRiskyWrites:true}}`，metacog 条件边识别 `resumeAdminConfirm` 直跳 `admin_confirm_resume`。是"新 run 复用 checkpoint 快照"，不是 resume 旧 run。

> **为什么 admin 不也用阻塞型**：admin 写可能跨进程重启，进程崩了阻塞型 waiter 就丢了；持久化快照 + 新 run resume 才能保证即使 Node 挂了，checkpoint 在 Redis/文件 24h TTL 内仍可续。

**自治安全边界（critic 补漏点）**：`writeGate.ts` 不仅禁 admin，还禁 **GUI 自动化**（浏览器登录/填表/点击）。自治 run（`meta.autonomousRun=true`）时 `filterAgentsRespectingWriteGate` 同时过滤 admin 和 gui 两个写 agent；crawler（静态抓取）允许。

---

### 4.8 自我进化飞轮（项目最大亮点）

> **面试金句**："Agent 改的不是模型权重，而是自己的**运行时配置和提示词**。"

#### （1）进化什么？三类"制品"

| 制品 | 内容 | 风险 |
|------|------|------|
| **policy 超参** | clarifyThreshold、maxParallel、maxRetries、timeoutMs（连续可调值） | 低 |
| **prompt 补丁** | 往 router/planner 的 SystemMessage append 短规则文本 | 中 |
| **planner 硬规则** | requireAfter/forbidAgents 等结构化约束 | 中 |

> **设计原则（面试金句）**："进化只调阈值和注入 prompt 短规则，**不生成新代码/新 SQL/新工具**——可回滚、可解释、不会引入编译期错误。"

#### （2）shadow → promote 安全晋升四道闸门

```
失败归因(attributeFailure, 纯规则 12 类)
   ↓
失败聚类(analyzeFailureInsights, 扫 800 条历史)
   ↓
生成进化假设(规则归纳 + LLM 假设, temperature=0.2)
   ↓
写 *.shadow.json  ← 闸门①: 物理隔离, 默认 0% 流量
   ↓
sessionId sha256 稳定分桶(默认 5%)  ← 闸门②: 爆炸半径可控 + 同会话一致
   ↓
A/B 实验(compareArms, minSamples=8/臂)  ← 闸门③: 指标证明 lift 显著
   ↓
verifyBeforePromote + confidence 阈值  ← 闸门④: schema/安全校验
   ↓
覆盖 active, 保留 previous 可回滚
```

```ts
// managerGraph.policyCanary.ts —— sessionId 稳定分桶
export function sessionUsesPolicyCanary(sessionId, percent = 5) {
  const h = createHash('sha256').update(`policy-canary|${sid}`).digest()
  return h.readUInt32BE(0) % 100 < percent   // 同一用户每次桶号不变
}
```

#### （3）A/B 实验的非劣性设计（critic 深挖点）

```ts
// managerGraph.evolutionExperiments.ts
const lift = treatmentScore - controlScore
if (lift >= 0.03) return { winner: 'treatment' }   // 晋级门槛低
if (lift <= -0.06) return { winner: 'control' }    // 回滚门槛高
return { winner: 'tie' }                           // 继续跑攒样本
```

> **为什么 0.03 vs 0.06 不对称**：晋级门槛低（0.03）鼓励小幅正向改进通过；回滚门槛高（−0.06）避免小波动把已通过 verifyBeforePromote 的新策略打回去反复抖动。这是把 A/B 实验里的**非劣性设计**搬进 Agent 自进化。`blendedArmScore = 0.55×finalConfidence + 0.45×compositeScore` 用双信号防 prompt 注水（只拉 finalConfidence 不够）。

#### （4）policy 自动回滚兜底

`policyRollout` 记录 baseline finalConfidence，新版本上线后若 `avg 显著劣化 > 0.08` 自动 `restoreManagerPolicyFromPrevious`。

---

### 4.9 记忆系统：四层分层 + 向量 Jaccard 混合 + 冲突消解

#### （1）四层记忆

| 层 | 内容 | 时效 |
|----|------|------|
| **working** | 会话级（最近 8 轮） | TTL 7 天 |
| **semantic** | 跨轮事实（successScore≥0.72 才入，去重到 15 条） | 长期 |
| **experience** | 成败路径（向量索引，1400 条上限） | 长期 + 时间衰减 |
| **reflection** | 失败教训（上限 80 条） | 长期 |

#### （2）向量 + Jaccard 混合召回

```ts
// managerGraph.vectorMemory.ts —— 不是纯向量也不是纯关键词
export function blendRecallScore(vectorSim, jaccard, sceneMatch, successBoost = 0) {
  const vw = 0.55   // 向量权重（MANAGER_VECTOR_SCORE_WEIGHT 可调）
  return vw * vectorSim + (1 - vw) * 0.55 * jaccard + (1 - vw) * 0.45 * sceneMatch + successBoost
}
```

> **为什么混合**：纯向量在小语料（<1400 条）下精度差、对短查询和字面术语（表名/字段名）不敏感；Jaccard 词袋兜底字面命中。embedding 走 DashScope text-embedding-v2，query 带 180s TTL 缓存。

#### （3）冲突消解（记忆系统最容易翻车的点）

防止"失败教训压倒成功经验导致 Agent 越改越保守"：

```ts
// managerGraph.layeredMemory.ts
export function applyMemoryConflictResolution(reflections, experienceSuccessSummaries) {
  const successBag = tokenBag(experienceSuccessSummaries.join(' '))
  return reflections.filter(r => {
    if (r.category === 'success') return true
    const overlap = jaccard(tokenBag(r.lesson), successBag)
    if (overlap > 0.55 && r.score < 0.5) return false   // 成功经验够强且字面相近时，丢掉这条反思
    return true
  })
}
```

#### （4）经验回放防带偏三层防护

1. prompt 显式写"必须以本轮输入为准，勿照搬下列 path"——经验是 few-shot 参考非指令
2. 时间指数衰减 `exp(-days×0.09)`（约 7 天半衰）
3. 负样本隔离——`successScore<0.42` 移到 quarantine，但在 experienceReplay 里**反向注入**作"避雷提示"

#### （5）隐式负反馈（飞轮数据闭环的关键）

显式点赞点踩覆盖率永远 <10%，把四类用户行为映射成固定 feedbackScore：

```ts
const IMPLICIT_FEEDBACK = { user_cancel: 0.22, new_chat_interrupt: 0.28, human_reject: 0.32, retry_penalty: 0.42 }
// retry 惩罚 = retryCount × 0.05（封顶 0.15）从 composite 里扣
```

---

### 4.10 跨 Agent 协议 managerTask（双轨 SSOT）

总管调子 Agent **不是塞一个大 prompt**，而是双轨：

```
自然语言层 message/question (可含总管模板包装)
   +
结构化侧车 manager_rag_task_json / manager_db_task_json
   +
HTTP 编排标记头 x-manager-orchestrated:1 + x-trace-id
```

```ts
// shared/managerSubAgentProtocol.ts —— 结构化侧车
export type ManagerRagTaskPayload = {
  source: 'manager',
  lean_query: string,          // 用于 embedding/检索的核心问句
  sub_queries?: string[],      // 总管已拆好的子问句 → RAG 走 compound 深度检索
  scope_hint?: string,
  retrieval_keywords?: string[],
  force_deep_retrieval?: boolean,
  output_style?: 'manager_bullets' | 'conversational',
}
```

> **为什么双轨**：纯 prompt 被 sanitize/截断后子 Agent 用 regex 二次解析不可靠；结构化 JSON 让子 Agent 直接拿 `sub_queries` 走 compound 检索、拿 `hint_tables` 走精准 schema 搜索。SSOT 在 `shared/managerSubAgentProtocol.ts`，总管和子 Agent 共用，避免各写一套解析逻辑漂移。

---

### 4.11 确定性优先：何时用代码，何时用 LLM

这是编排层"降本降错"的核心思想——**能不用 LLM 就不用**。

| 场景 | 用代码（确定性） | 用 LLM |
|------|------|------|
| 出图表 | `chartOption.ts` 规则生成 ECharts option（只做结构校验，零领域 regex） | 只规划语义（选数/分组/标签） |
| 多源 facts 合并 | `codeFirstAuthority`：code 最后写覆盖同名键（唯一计算源） | — |
| 单源 DB 透传 | `dbPipelineDeterministic`：clean/code/visualize/report 全确定性跳过 LLM | — |
| 失败归因 | `attributeFailure` 纯规则 12 类 | — |
| 路由意图 | （只做规范化/约束） | **LLM 权威** |

> **为什么不让 LLM 直写 ECharts**："LLM 直写 series.data 必出错——数字幻觉、量纲混用（currency 和 percent 同图）、占比冒充金额。Code 是唯一算过的权威源，强制覆盖消除多源冲突。"

---

### 4.12 WS 协议与可观测性

#### （1）入站 8 种事件 + 三层闸门

所有客户端 WS 消息用 `z.discriminatedUnion('type', [...])` 定义 8 种 type（chat/resume/cancel/human_confirm/plan_confirm/feedback/withdraw_turn/clear_experience），先 Zod parse，再过限流（全局 30/10s、chat 8/30s），再鉴权。

#### （2）阶段事件流：send() 单点出口 + jsonl 回放

```ts
const send = (event, data, from, runId) => {
  peer.send(JSON.stringify({ event, data, from, runId }))     // 推前端
  if (runId) void appendRunEvent(runId, { event, data, from, ts })  // 落 .data/runs/<runId>.jsonl
}
```

> 单点出口让所有事件天然带 runId、天然落盘，可回放（断线重连/debug/metrics 反构）。`appendRunEvent` 对 data 做 2000 字符截断防 jsonl 爆掉。

#### （3）可观测性三出口共享一份原始流

```
manager-metrics.jsonl (append-only 事实源: {runId,phase,ms,tokens,usd,model,agent,ts})
   ├── GET /api/metrics          (JSON 实时聚合: token by phase/agent/model + 进化看板 + canary 对比)
   ├── GET /api/metrics/prometheus (文本指标 → Grafana)
   └── GET /api/metrics/traces   (OTel span 反构 → Jaeger, sha256 派生确定性 spanId)
```

LangSmith 是另一条线（LangChain 原生 tracing，看 LLM 内部 prompt/completion）。三者互补：metrics 看趋势/成本，OTel 看单次 trace span 链路，LangSmith 看 LLM 内部。

#### （4）modelTier 分阶段省钱

route/plan/synth/critic 四个 LLM 阶段独立选模型。`shouldAutoLightTier` 启发式判断能否降到 flash：有附件/要 web/multi/步数>2/重文本一律不降；**route 阶段最保守**（文本≤220 且单从句才降）——因为 route 判错会连锁路由到错误 agent，损失远大于省下的 token。

---

### 4.13 自主（autonomous）循环与安全边界

`managerAutonomyPlugin` 是 `setInterval(600s)` 的后台飞轮，一个 tick 串 7 件事：

```
记忆治理 → 学习权重调 → 失败归因 → 进化实验 → proactive nudge 扫描 → autonomous 队列消费 → 日级备份
```

- **重入保护**：`running` 布尔，上一次没跑完就跳过
- **故障隔离**：每个子任务 `.catch(()=>undefined)` 吞异常，一个挂不掉整条链
- **自治队列**：扫逾期的 user_goal/task_stack 生成 job，`cooldown(900s)` + `maxAttempts(2)` + 失败退避 600s
- **headless 执行**：`executeHeadlessManagerRun` 无 WS、无人工确认

> **安全边界三重**（面试必答）：① 所有自治 prompt 硬编码"禁止 admin 写操作"，只允许检索/归纳/建议；② writeGate 同时封锁 admin 和 gui；③ `replanCount<6` 且 `replanMinIntervalMs≥120s` 防止无限 replan。

**自治结果双通道通知**：在线走 `wsSessionHub` 广播，离线落 `.data/autonomous-pending-notify/<sessionId>.json`（按 session 分片），resume 时 `drainPendingAutonomousResults` 补发——"信箱"语义：实时尽量推、离线不丢。

---

## 5. 核心数据结构与协议速查

| 结构 | 形状 | 出处 |
|------|------|------|
| **GraphState** | 30+ channel（messages concat / entities 覆盖 / results 浅合并 / meta 覆盖） | `managerGraph.ts` Annotation.Root |
| **IntentClassifyResult** | primaryIntent + isMulti + suggestedAgents(max8) + planShortcut + confidence(0-1) | `intentClassifyLlm.ts` |
| **BanditArm** | {intent, alpha, beta, pulls, lastReward}（Beta 分布参数） | `routeBandit.ts` |
| **RouteCausalGraph** | {edges: CausalEdge[], intentEffects}（ATT 边） | `routeCausal.ts` |
| **PlannerRule** | {when*, requireAgents?, forbidAgents?, requireAfter?} | `plannerRules.ts` |
| **FailureAttribution** | 12 类枚举 + severity + reasons | `failureAttribution.ts` |
| **EvolutionExperiment** | {artifact, status, baseline, treatment, verdict:{winner,lift}} | `evolutionExperiments.ts` |
| **ManagerRagTaskPayload** | lean_query + sub_queries + retrieval_keywords（侧车 SSOT） | `shared/managerSubAgentProtocol.ts` |
| **AutonomousJob** | {kind, runAfter, attempts, status} | `autonomousQueue.ts` |
| **WS envelope** | {event, data, from, runId} | `manager-ws.ts` |

---

## 6. 设计决策与取舍（why this not that）

| 决策 | 理由 | 代价 |
|------|------|------|
| 单入口单终点扁平 StateGraph（非嵌套 subgraph） | 整张图一张看全、LangSmith trace 线性平、调试肉眼可追 | graph.ts 编译函数长（228 行）但结构清晰 |
| HITL 两套机制（非 LangGraph 原生 interrupt） | 原生 interrupt 依赖 checkpointer + 稳定 thread_id，跨进程不可控；自建快照不依赖 LangGraph 版本 | 自建了快照协议，增加心智负担 |
| Bandit/Causal 用文件 JSON 持久化（非 DB） | 数据量小、读写频率低、便于人工调试 | 多实例部署状态不一致（最终一致） |
| 经验默认不走快路径（`MANAGER_INTENT_RAG_EXPERIENCE_FAST_PATH=0`） | 历史成功路径可能"相似但不同"，会绑架流水线扩写用户没要的步骤 | 牺牲高频相似问句的加速，换路由安全 |
| 进化只调阈值/注入短规则（不生成新代码） | 可回滚、可解释、无编译期错误 | 牺牲表达力，改逻辑必须人工 promote |
| 失败归因用纯规则（不让 LLM 做） | 归因是每条经验都过的信号源头，LLM 慢贵不稳不可复现 | 边缘 case 落 unclear 桶（也有默认建议） |
| metrics 用 jsonl append-only，聚合请求时算 | 不丢、可重放、可纠错、多出口共享一份 | 每次请求重读重算，上量需预聚合 |
| 自治 prompt 硬编码禁止 admin 写 | headless 无人在场，写操作不可逆 | 自治能力限于信息收集，写操作仍需在线确认 |

---

## 7. 工程化亮点

### 7.1 安全

- WS 三层闸门（Zod 校验 + 限流 + 鉴权）把非法包挡在 graph 之前
- 写操作双闸：writeGate 封锁 admin + gui；HITL 强制确认
- `textMarkers.ts`：`looksLikeRiskyAdminWrite` / `looksLikeSqlInjection` 正则做写闸/安全判定基础
- 自治 run 安全边界三重（禁写 + 封 GUI + replan 上限）

### 7.2 成本控制

- modelTier 分阶段动态降级到 flash（route 最保守）
- intent_classify 的 rag_fast 快路径省一次 LLM
- merged 理解节点把 3 次 LLM 合并成 1 次
- critic 快速路径跳过简单任务的 critic LLM
- 确定性优先（图表/归因/透传不用 LLM）

### 7.3 测试（package.json 里的 smoke 矩阵）

```
ci:gate = eval:golden + eval:route + gate:nlu
  + smoke:graph + smoke:chart + smoke:p0/p1
  + smoke:golden + smoke:clause + smoke:skill-draft
  + smoke:batch-a/b/c/d/e
  + smoke:rag-spreadsheet/html/pptx + smoke:db-metrics
  + e2e:golden + smoke:memory-coordination + smoke:evolution-ops
```

黄金路径 smoke + NLU 回归门禁 + 路由 golden——保证进化不把系统改坏。

### 7.4 可观测性

jsonl 原始流 → metrics/Prometheus/OTel 三出口 + LangSmith，详见 4.12。

---

## 8. 面试问答库

### 基础

**Q1：画一下 Manager Agent 的 LangGraph 状态机主干。**
> 单入口单终点：START→resource→tool_health→probe→metacog（可早退）→security_gate→decompose→intent_classify→route→prefetch→（single 直跳执行节点 / multi 走 planner→scheduler→exec_mode→vote→plan_lint→[plan_preview]→multi）→synth→evaluator→critic→optimizer（可回环 fix）→verifier→monitor→finalize→END。旁路 clarify/web_search/fix/admin_confirm_resume 全用条件边谓词挂回主干。

**Q2：为什么总管不直接实现每个子能力？**
> 总管的职责是调度和编排。把能力拆给专业 Agent，系统更易维护、更易扩展、更符合工程分层。这是 Supervisor/Orchestrator 模式的经典拆分，避免"一个 Prompt 包打天下"。

**Q3：为什么要用 LangGraph 而不是手写 async 管线？**
> 多 Agent 编排是有分支/回环/HITL/失败恢复的**状态机**。LangGraph 提供 checkpoint（断点续跑）、条件边（旁路）、recursionLimit（防死循环）、LangSmith trace（可观测）。手写要重新实现这些。

**Q4：DB Agent 调用走 WS 还是 HTTP？**
> WS 优先 HTTP fallback。tryWs 收到 message 事件即返回（不等 end，因为等 end 会超时——这是 DB WS 协议特殊点），支持流式 thinking；catch 后降级 tryHttp 走 /api/ask 带 2 次重试。LRU 只缓存非空结果，避免短超时误判的空答案长期命中造成"永远查不到"。

### 进阶

**Q5：路由会不会错乱？比如用户说查数据库，怎么保证不误判成知识库或乱扩写 report？**
> 三重防御：①意图 RAG 召回时 userIntentSupremacy 做能力漂移检测，召回命中含用户未要求的 agent 则 `score*=0.35` 降权；②routeFinalize 的 stripAdminIfNotInCurrentTurn 剔除误带 admin；③planLinter 越权检查，multi 任务下 step 的 agent 必须在 allowedAgents 内。加上 dbOnlyRoute/ragOnlyRoute 收敛纯查库问句。

**Q6：routeBandit 的多臂老虎机为什么用 Thompson 采样不用 UCB 或 ε-greedy？**
> 每个 intent 维护 Beta(α,β) arm。Thompson 天然表达不确定性（样本少方差大更易被采到），是贝叶斯最优的 Bernoulli bandit 解，无需手调 ε。探索用 sessionId sha256 取模稳定分桶（默认 8%），保证同用户探索状态一致。产出只是 routerHintBlock 提示文本，保留 LLM 最终决策权。

**Q7：Planner 的硬规则怎么进化？怎么避免坏规则搞崩系统？**
> 双文件：active（生效）+ shadow（候选）。自动学习产出的规则先进 shadow，confidence≥0.68 才晋级。lintPlanWithPlannerRules 在 plan_lint 强制执行 active 规则。防崩：规则有 when 条件只在特定场景触发；prompt 明确"与本轮用户意图冲突时以本轮为准"；规则 cap 24 条且 source 标记便于回滚。

**Q8：HITL（人工确认）怎么实现？plan_preview 和 admin 写为什么用两套？**
> plan_preview 是进程内阻塞型——节点 await waitPlanConfirm（600s 超时 Promise），WS 收 plan_confirm 调 resolvePlanConfirm 解开。admin 写是跨进程持久化型——检测 needsHumanConfirm 时落 checkpoint（mem/file/Redis 24h TTL），ws 拦截不发 final，用户确认后**新开 run** 带 resumeAdminConfirm 从 metacog 直跳 admin_confirm_resume。分两套是因为 plan 确认轻量用户在场几秒回来，admin 写高风险可能跨进程重启需审计留痕。

**Q9：fix→synth 回环怎么防止死循环？**
> 双闸 retryBudget：env MANAGER_MAX_RETRY（默认 1）+ policy maxRetries（single=1/multi=2），取较小值。到顶后 optimizer 即使判 fix 也会被条件边强制路由到 verifier 终结。recursionLimit 默认 48（范围 25-120）是硬墙兜底。框架硬约束 + 业务软约束分层治理。

**Q10：多轮对话和断点续传怎么做？thread_id 怎么定？**
> 两层 checkpoint：LangGraph saver（Postgres/MemorySaver）+ 自建 checkpointStore（mem/file/Redis）。postgres 模式 thread_id=sess-{sessionId} 跨 run 续接，memory 模式 thread_id=run-{runId} 仅 per-run（**不能跨会话**——这点容易讲错）。自建 store 存 buildHumanConfirmCheckpoint 精简快照（16 个业务字段子集），TTL 24h，专门服务 HITL resume。

### 深挖（killer followups，来自 critic）

**Q11：decompose 和 intent_classify 谁在前？倒过来会怎样？**
> 实际是 security_gate→decompose→intent_classify（graph.ts L121-123），**先拆子句再做意图识别**。理由：一句塞两个意图时 LLM 容易取平均，拆成子句后 merged 理解更准。decompose 默认 25% 灰度，灰度外接近透传。倒过来 intent_classify 会漏掉需要拆解才暴露的多意图，且 route 拿不到 clauseCount 做 multi 收敛。

**Q12：Bandit 用 Thompson、RL 用 Q-learning，两套都产出 boost/deprioritize，冲突时谁说了算？**
> 谁都不直接改 intent，都只产 routerHintBlock 文本块 append 到 router prompt，LLM 自己综合（routeFinalize 只信任 LLM 输出）。两者职责正交：bandit 管"这个意图整体回报高不高"（无上下文），rl 管"在当前上下文桶（global/clarify/slow/implicit/first_pass）下哪个 Q 值高"。冲突时两段都写进 prompt，加上 causal 的 ATT 提示和 strategy 的 healthPenalty，最多 5 段 advice 叠加，LLM 权衡。用户意图最高。

**Q13：compareArms 用 lift≥0.03 晋级、lift≤-0.06 回滚，为什么不对称？**
> 故意的保守策略（非劣性设计）：晋级门槛低鼓励小幅正向改进通过；回滚门槛高避免小波动把已通过 verifyBeforePromote 的新策略打回去反复抖动。对称（如都用 0.04）会让 0.03 的正向改进判 tie 浪费时间、0.05 的负向立刻 rollback 误杀真实改进的早期波动。blendedArmScore 用双信号（finalConfidence + compositeScore）防 prompt 注水，minSamplesPerArm=8 保证小样本偶然被挡。

**Q14：sampleBeta 用 `x=u1^(1/α), y=u2^(1/β), x/(x+y)` 近似 Beta 采样，误差在什么范围可接受？**
> 基于 Beta 分布的逆 CDF 性质。α/β 接近 1（均匀分布）时近似最好；α 或 β 很大（>10，大量样本后分布很尖）时浮点精度导致采样退化；α/β<0.5 时 `Math.max(0.5,alpha)` 强制 floor 引入偏差。工程上 reward 是 compositeScore 综合 4 信号，α/β 增长缓慢，大部分意图长期 α+β<20，近似可接受。真要精确应该用 rejection sampling，但那违背"无重依赖"的取舍。样本多了会失真，靠 maxRetries 和定期 curator 归零隐性补偿。

**Q15：memory 模式开 checkpointer，thread_id=run-{runId} 不能跨 run resume，那它意义是什么？**
> 作用很有限。memory 模式（MemorySaver 是进程内 Map）只支持"同一 run 内的 interrupt/恢复"语义。但本项目 HITL 没用 LangGraph 原生 interrupt（用自建 Promise 桥 + checkpointStore），所以 memory 模式几乎没有发挥场景。真正跨 run 续接只有 postgres 模式。memory 模式是"为 API 兼容性存在但实际不被 HITL 使用"，postgres 才是跨 run resume 的正路。

**Q16：自治 run 的安全边界你说了 admin 写禁止，那 GUI 自动化呢？**
> GUI 也禁。writeGate.ts 的 isGuiBlockedForState 判定 `meta.blockGuiWrites` 或 `isAutonomousRunMeta(meta)` 为 true 即禁，filterAgentsRespectingWriteGate 过滤掉 gui。router 把含"登录/填表/点击/浏览器操作"的意图路由到 gui agent，进入 allowedAgents 后 writeGateRouterHint 注入"禁止浏览器自动化，仅允许 crawler 静态抓取"。区分：crawler（静态抓取，自治允许）vs gui（浏览器交互，自治禁止）。

**Q17：把 autonomyPlugin 的 tick 从 10 分钟调到 1 分钟会怎样？**
> 多个子任务有独立节流，不会全坏但有副作用：memoryCurator 节流 600s 无影响；failureInsights 扫 800 条 jsonl 频繁跑增加 IO；evolutionCycle 的 compareArms 攒样本慢，频繁跑多判"insufficient_samples"空转；proactiveLoop 会过早重复 nudge。真正会坏的是：tick 用 running 布尔重入保护，若某个子任务（evolutionCycle 触发 LLM 假设，单次 30s+）超过 1 分钟，下个 tick 直接跳过，导致 proactive/autonomous 被饿死。**10 分钟是给 LLM 子任务留执行余量的工程选择。**

**Q18：recursionLimit=48，multi 有 8 步 + 2 次 fix 回环，步数怎么算？真会撞 48 吗？**
> LangGraph 计的是"超级步"数，每个节点执行算 1 步，条件边不算。前缀到 multi 约 10 步 + multi 内部调度（每批 ready 并行算 1 步，8 步 maxParallel=3 约 3 批=3 步）+ 首次 synth→critic→optimizer 3 步 + 每次回环 fix→synth→critic→optimizer 4 步×2=8 步 + verifier→monitor→finalize 3 步 ≈ 27 步，离 48 有余量。retryCount 在 fix/critic 决定 fix 时 +1，multi 默认最多 fix 2 次就到顶，optimizer 即使判 fix 也被路由到 verifier。

**Q19：reducer 用错了是 LangGraph 最隐蔽的 bug，除了 entities 覆盖，还踩过哪些？**
> results 浅合并 `{...x,...y}` 在 multi 并发场景下确实会覆盖——若两个并行步骤都写 results.code，后写覆盖先写。但 multi 调度器用 byId Map 做步骤级隔离，同一 agent 在一个 plan 里通常只有一个步骤（除非 vote 双候选），并发覆盖概率低。另一个隐性坑：messages 用 concat 越积越长，但 conversationBudget.buildGraphHistoryMessages 在 load 时做 recent K 轮 + 摘要，所以不影响 LLM 输入（输入是 budget 压缩后的），只影响 checkpoint 体积——postgres 模式 checkpoint 会变大。

**Q20：shadow→promote 怎么保证不会把 Agent 改坏？**
> 四道闸门：① shadow 物理隔离默认 0% 流量；② sessionId sha256 稳定分桶默认 5%；③ A/B 实验 compareArms 双臂 minSamples=8，lift 不显著 tie 继续跑、显著负向 rollback；④ verifyBeforePromote（外部共享包 schema/安全校验）+ confidence 阈值（policy 0.72/prompt 0.68/planner 0.65）。promote 前 backupManagerPolicyFile 存 previous，policyRollout 记录 baseline，新版本劣化 >0.08 自动 restore。

---

## 9. 知识点延伸（连接通用概念）

| 本项目机制 | 对应通用 AI 概念 | 延伸阅读 |
|------|------|------|
| probe → route → plan → execute → synth → critic | **Plan-and-Execute / ReAct** 状态机 | [ReAct 反思 任务规划](../agent-books/ReAct-反思-任务规划.md) |
| 编排层 + 专家层 | **Supervisor / Orchestrator 模式** | [Multi-Agent](../agent-books/Multi-Agent.md) |
| 子句拆解 decompose | **Query Decomposition**（Compound AI Systems） | [Multi-Agent](../agent-books/Multi-Agent.md) |
| routeBandit Thompson | **多臂老虎机 / 探索-利用权衡** | [幻觉与评测](../agent-books/幻觉与评测.md) |
| routeCausal ATT | **近似因果推断 / ATE** | — |
| routePolicyRl Q-learning | **上下文 Bandit / RL** | — |
| shadow→金丝雀→A/B | **灰度发布 / 非劣性设计** | [工程化与部署](../agent-books/工程化与部署.md) |
| 四层记忆 + 向量召回 | **RAG + 分层记忆** | [上下文管理与记忆](../agent-books/上下文管理与记忆.md) |
| managerTask 双轨协议 | **Function Calling / Tool Use** | [Tool Calling](../agent-books/Tool-Calling-Function-Call-MCP.md) |
| evidenceGate + critic | **LLM-as-Judge / 事实性护栏** | [幻觉与评测](../agent-books/幻觉与评测.md) |
| HITL checkpoint | **Human-in-the-Loop** | [异常处理 安全 熔断](../agent-books/异常处理-安全-熔断.md) |
| retryBudget + recursionLimit | **熔断 / 重试预算** | [异常处理 安全 熔断](../agent-books/异常处理-安全-熔断.md) |

---

## 10. 自测清单（能讲出来才算过）

- [ ] 能画出 probe→route→plan→execute→synth→critic→finalize 的顺序，并解释 **probe 为何在 plan 前**、**decompose 在 intent_classify 前**
- [ ] 能区分编排层与专家层的职责边界，说出"总管不做哪 3 件事"
- [ ] 能解释条件边谓词 vs 节点副作用的区别，说出 afterExecution 被 13 个节点复用的 DRY
- [ ] 能讲清 Annotation reducer 的 4 种合并语义，解释 **entities 为什么故意用覆盖**
- [ ] 能区分 Bandit(Thompson)/RL(Q-learning)/Causal(ATT) 三套引擎的职责，解释**为什么不冲突**
- [ ] 能说出 shadow→promote 的四道闸门 + A/B 非劣性设计 0.03 vs 0.06
- [ ] 能讲清 HITL 两套机制（进程内阻塞 vs 跨进程 checkpoint）对应的两种 SLA
- [ ] 能解释 evidenceGate + critic 双重事实性防线，以及 criticRetryContradictsRunEvidence 的作用
- [ ] 能讲清 managerTask 双轨协议为什么不用纯 prompt
- [ ] 能说出自治 run 的三重安全边界（禁 admin 写 / 封 gui / replan 上限）
- [ ] 能解释 retryBudget + recursionLimit 的分层治理
- [ ] 能区分 memory/postgres 两种 checkpointer 的 thread_id 语义及跨 run 能力

---

## 11. 源码精读地图（按优先级）

| 优先级 | 文件 | 重点 |
|--------|------|------|
| ⭐⭐⭐ | `server/utils/managerGraph.graph.ts` | 全图拓扑、38 节点、所有条件边 |
| ⭐⭐⭐ | `server/utils/managerGraph.ts` | GraphState Annotation.Root（reducer）、invoke Proxy |
| ⭐⭐⭐ | `server/api/manager-ws.ts` | WS 协议总入口、HITL 续跑、事件落盘 |
| ⭐⭐ | `managerGraph.routeBandit.ts` | Thompson 采样、sessionId 分桶 |
| ⭐⭐ | `managerGraph.routeCausal.ts` | ATT 因果图重建 |
| ⭐⭐ | `managerGraph.retryBudget.ts` | 双闸重试预算 |
| ⭐⭐ | `managerGraph.evolutionExperiments.ts` | A/B 实验 compareArms |
| ⭐⭐ | `managerGraph.checkpointStore.ts` | HITL 快照三级存储 |
| ⭐ | `managerGraph.multiNode.ts` | DAG 优先级调度器 |
| ⭐ | `managerGraph.agentRunner.ts` | 动态超时缩放 + 熔断 |
| ⭐ | `managerGraph.evidenceGate.ts` | 证据闸门 |
| ⭐ | `managerGraph.failureAttribution.ts` | 12 类失败归因（纯规则） |
| ⭐ | `shared/managerSubAgentProtocol.ts` | managerTask 双轨 SSOT |

---

## 附录 A：硬指标速查表

| 维度 | 指标 |
|------|------|
| **图** | recursionLimit 默认 48（范围 25-120）；38 节点 |
| **重试** | MANAGER_MAX_RETRY 默认 1（0-5）；single=1/multi=2 |
| **HITL** | plan_confirm 超时 600s；gui_confirm 300s；checkpoint TTL 24h |
| **调度** | maxParallel 默认 3；MAX_SCHEDULE_WAIT_SPINS=48；超时下限 12s |
| **熔断** | 连续失败 ≥2 次；p95Floor = p95×1.2+5000（p95≥8000 时） |
| **进化** | 金丝雀默认 5%；promote confidence（policy 0.72/prompt 0.68/planner 0.65）；A/B minSamples=8/臂；lift 晋级 0.03/回滚 0.06 |
| **记忆** | 向量权重 0.55；经验时间衰减 exp(-days×0.09)（7 天半衰）；working 8 轮/semantic 15 条/reflection 80 条/向量索引 1400 条 |
| **隐式反馈** | user_cancel=0.22/new_chat_interrupt=0.28/human_reject=0.32/retry_penalty=0.42 |
| **WS** | 限流全局 30/10s、chat 8/30s；session TTL 30min、run TTL 12min、maxSessions 220；text 上限 8000 字符 |
| **自治** | tick 600s；队列 cooldown 900s；maxAttempts 2；replanCount 上限 6 |
| **modelTier** | route 降级文本≤220 且单从句 |

---

## 附录 B：常见坑（gotchas）

1. **recursionLimit 默认 25 不够**：multi 多步 + fix 循环会超限，必须手动传 48。
2. **空结果不缓存**：dbClient 的 LRU 只缓存 `!empty`，否则短超时误判的空答案会长期命中造成"永远查不到"。
3. **memory 模式不能跨会话续接**：thread_id=run-{runId} 仅 per-run；postgres 才是跨 run 正路。
4. **entities 覆盖是刻意的**：多轮实体延续靠 session.messages 上下文，不靠 state.entities。
5. **bogusFinal 检测**：ws 会把等于节点名（finalize/synth/critic...）的 final 文本当脏数据丢弃。
6. **shadow 不会自动生效**：必须开 `MANAGER_POLICY_CANARY_PERCENT>0` 才有流量命中。
7. **policyCanary 用 sha256、featureRollout 用 imul(31)**：两套 hash 不能混用，同 sessionId 在两套桶里命中的百分比不相关（设计但易误读为 bug）。
8. **A/B 实验样本不够会一直 pending**：5% 灰度攒样本慢，双臂都要 ≥8 才评估。
9. **appendRunEvent 截断**：jsonl 里的 final 文本可能被截到 2000 字符，token 复盘要看原始 result。
10. **自治 cooldown 是全局的**：lastRunAt 单文件，多 session 共享，高并发自治会被严重限速（单实例设计假设）。

---

## 附录 C：与 Code Assist 的协作

Code Assist（13103）是 Manager 的下游之一。协作链路：

- Manager 路由到 `code` 意图 → 经 `managerCodeDownstream.ts` 调用 Code Agent
- 传参走 **managerTask 双轨协议**（自然语言 + `manager_code_task_json` 侧车）
- Code 计算结果作为**权威源**回传，`codeFirstAuthority` 让 code 覆盖同名键
- visualize/report 步骤优先用 Code 的 `chart_plan` 确定性出图，LLM 只规划语义

详见 [Code Assist 工程化代码助手](Code-Assist-Agent-工程化代码助手.md)。

---

> **最后一句面试话术**："这个项目让我最自豪的不是某一个点，而是它把**多 Agent 编排**做成了一个**会自我修正、会自我进化、还能保证安全**的系统——probe 防幻觉路由、evidenceGate 防编造、retryBudget 防死循环、shadow 金丝雀防改坏、HITL 防不可逆。每一个'防'背后都有一次真实的工程踩坑。"
