# code_assistent_Agent — 金牌项目深挖稿

> **用途**：面试当场可念版。被问"讲讲你的 Coding Agent / Agent Safety 怎么做 / 怎么让 LLM 改仓库不闯祸"任意一题，都从这份稿切入。
> **念法节奏**：电梯演讲 30 秒 → 业务背景 30 秒 → 架构 1 分钟 → 深挖锚点按追问展开 → 量化与边界收口。
> **总控制**：完整讲 3-4 分钟，被追问可延展到 8-10 分钟。
> **素材出处**：stealth.html C0-C14 + 简历 resume.typ + 项目源码 `/Users/didi/work/agent-main/code_assistent_Agent/`。

---

## 一、30 秒电梯演讲（必背，张口就来）

> **code_assistent_Agent 是"LLM 改仓库的高风险场景"下的工程化 Coding Agent**——把 LLM 改仓库约束在可审计的工程边界内，覆盖 <strong>Read-before-Write → 语义检索 → AST 分析 → Diff 预览 → 受控写盘 → 自动验证</strong>完整闭环。**18 工具 ReAct 循环 + Custom CheckpointSaver（extends BaseCheckpointSaver）+ 三层 guard 函数 + Sandbox 三态 + Shadow Patch 四件套自进化**。**最有工程含量的不是用 LangGraph，是手写 Myers diff + unified hunk parser 的双向 Diff 工程 + 三函数三件事的 Safety 设计 + DJB2 hash 分桶的 Prompt A/B**。

**钩子三件套**：定位（工程化原型非 chat 贴代码）+ 量化产出（18 工具 / 800 文件仓库默认 / 7 个 .test.ts + smoke）+ 核心创新（双向 Diff 工程 + Shadow Patch 自进化 + 三函数三件事 Safety）。

---

## 二、业务背景（30 秒，先讲为什么做）

**痛点定位**：LLM 改仓库的高风险场景下<strong>"模型 + 写权限 = 事故"</strong>。市面 Cursor / Copilot / Windsurf 都是<strong>解决"从 0 到 1 写新代码"</strong>，假设开发者本人在用、信任开发者。但企业级场景下 LLM 直接改仓库要<strong>可审计、可回滚、防 LLM 闯祸</strong>——这是市面工具不做的赛道。

**核心洞察**：**Coding Agent 的难点不是生成代码，是把"生成"约束在工程边界内**——read-before-write / 严格 diff 校验 / 受控写盘 / 自动验证 / 沙箱执行 / 自进化。每一层都得做，少一层就翻车。

**金句钩子**：**"LLM 改仓库不难，难的是改成什么样都能审计、能回滚、能进化。"**

**诚实档位（必带，防被问"上线了吗"翻车）**：工程化原型 / 内部工具级——<strong>800 文件 demo / 单 JWT secret / 进程内限流 / 800 文件之外没测过</strong>。<strong>不是真生产</strong>，但设计已预留接入生产路径。被问"团队里有人用吗"诚实答"除了我自己 demo 没人用，对比 Spec-Driven 真落地 20+ 人团队，code_assistent 零使用数据"。

---

## 三、架构（1 分钟，先说清楚再展开）

### LangGraph ReAct 循环

```
START → agent(LLM 决策)
          ↓ (有 tool_calls?)
        tools(并行执行所有 tool_calls)
          ↓ (无条件)
        agent ... 循环到无 tool_calls → END
```

- **StateGraph + MessagesAnnotation**，checkpointer 是自研 FileSaver
- **不是 MCP**——全是 LangChain tool() 包装的本地函数
- **不是 Function Calling 字面 OpenAI API**——走 LangGraph 抽象层
- **Graph 单例缓存**：按 model-embeddingModel-chatOnly 做 key，避免重复 compile

### 18 工具按 8 类分

```
读 (7): list_files / read_file（分页）/ semantic_search（关键词）
        / git_status / git_diff / git_current_branch / git_log
向量+AST (3): vector_search（语义）/ ast_analyze / analyze_dependencies
写 (5): write_file / apply_diff / git_create_branch / git_commit / generate_docs
校验+执行 (2): validate_project / run_tests
记忆 (1): remember_preference
-- chatOnlyMode 减到 11 工具（去掉写盘/git 类）
```

### 三层 Safety（三函数三件事，不是凑数）

源码 `server/utils/files.ts` 实际 3 个独立 guard 函数：
- `isSensitiveRepoPath` (line 18)：阻 .env / .npmrc / id_rsa / *.pem / *.key 等密钥扩展名——<strong>读和写都拦</strong>，防密钥泄露
- `isRestrictedWritePath` (line 57)：阻 .git / .nuxt / .output / .data 目录——<strong>只拦写</strong>，防误改构建产物
- `DEFAULT_IGNORED_DIRS` (line 96)：list_files 跳过 node_modules / dist——<strong>只影响遍历</strong>，性能优化

**三件事不可互相替代**——读路径防密钥、写路径防构建产物、遍历跳过防性能炸。

### Sandbox 三态

```
off:        不沙箱（需显式 CODE_SANDBOX_MODE=0，默认不是这个）
subprocess: 默认模式（CODE_SANDBOX_MODE 缺省 fallback）
            env 白名单 + npm script 白名单
docker:     --network=none --memory=512m -v cwd:/workspace:ro
```

**关键认知**：docker 模式只用于<strong>执行类工具</strong>（run_tests / validate_project），写文件走 files.ts 的原子写（宿主进程权限，不在 docker 内）——这是<strong>"执行隔离 vs 写入校验"</strong>的分工，不是漏洞。

---

## 四、6 个深挖锚点（面试官追问任何一个，深入讲）

### 锚点 1：双向 Diff 工程（前端 Myers + 后端 hunk parser）

**问题**：LLM 生成 unified diff 经常算不准行号、context 容易错、空白字符不一致。

**机制**：
- **前端**（DiffViewer.client.vue 182 行）：手写 Myers diff 算法（完整 trace 回溯 + ops 反转）+ 渲染 unified diff 格式，纯前端无依赖
- **后端**（agent.ts:applyUnifiedDiffOrThrow）：parseUnifiedHunks 解析 `@@ -a,b +c,d @@` header + 严格校验 context line 必须匹配 + 顺序校验 + 删除校验——<strong>任何对不上 throw，模型必须重生成</strong>

**杀手锏**：错误信息 "Diff context mismatch near line X" 精确到行——LLM 知道哪里错了能针对性修。

**行业对比（诚实承认）**：Cursor / Claude Code / Aider 已从 unified diff 转向 <strong>search/replace block</strong>（用唯一锚点定位，行号错也能 apply）。Aider blog 提过 unified diff 失败率高所以他们做了 search-replace。<strong>我选 unified diff 是因为当时没研究 Aider，现在回看 search/replace 更可靠，没做范式迁移是技术债</strong>。

**震荡检测（诚实降级）**：源码<strong>根本没实现震荡检测</strong>——全仓库 grep `recentPatch / oscillat / hash_after / cycle` 都 0 命中。当前只靠 agent.ts 内部 max iterations 计数器兜底。<strong>改进方向</strong>才是记录 K 次 patch hash + 横跳模式识别。

### 锚点 2：sha256 乐观锁 + 原子写（防并发覆盖）

**问题**：LLM read foo.ts 拿 hash_a，准备 patch。同时另一个进程（人 / 另一个 Agent / CI）改了 foo.ts，磁盘 hash 变 hash_b。LLM 提交 patch 时校验不一致直接拒绝（HTTP 409）。

**机制**：
- read 时算 hash_a
- patch 时算 hash_b，hash_a == hash_b 才 apply
- tmp + rename 原子写

**杀手锏（reindex 一致性窗口）**：<strong>sha256 锁防磁盘并发，但防不了"基于旧 RAG 结果的错误推理"</strong>——LLM read 的是 foo.ts 旧 chunk（reindex 没跑完），patch 基于旧内容，hash 锁过了（磁盘没变）但推理已经错了，<strong>写穿</strong>。改进方向：vector_search 返回带 content_hash，LLM read 时校验。

**原子写诚实降级**：files.ts:209-213 的 rename 失败时<strong>无脑 catch {}</strong>（不区分错误类型）fallback 到 writeFile+rm。这个 fallback 破坏原子性——中途崩目标文件留半截。生产级要分错误类型：跨设备 / 权限错直接报错不 fallback。

**vs 悲观锁**：乐观锁本质假设"冲突罕见"。Agent + 人协作场景冲突是常态——但悲观锁会阻塞人类开发，trade-off 后选乐观 + 重试上限。

### 锚点 3：代码 RAG 两阶段过滤

**问题**：全量仓库塞 context 爆炸；纯 grep 靠关键词命中模糊查询不行。

**机制**：
- **阶段 1**：文件名 token 重叠 BM25-like 粗筛 → 选 top-N 候选文件
- **阶段 2**：候选文件按 chunk 切片，embedding 算余弦相似度 → top-15 返回
- **省 token**：不 embed 全仓库，只 embed 候选文件的 chunks
- **sha256 增量缓存**：文件没变就跳过 embedding

**杀手锏（reindex 一致性窗口）**：见锚点 2——<strong>异步 reindex 没跑完时 vector_search 返回旧 chunk</strong>，LLM 基于旧 chunk 推理再 patch，写穿。

**三套默认值不统一（技术债）**：源码 3 条调用路径 3 套默认值——agent 内部 120/2200/12/6，vector-search API 60/2400/18/8，retrieve API 60/2400/18/8。<strong>配置不统一是技术债</strong>。

**召回质量盲区**：recall / precision <strong>没测</strong>——smoke 只测 minHits:0（空也能过）。改进方向是 golden set + 对比 baseline（grep / 全量塞 context / BM25）。

### 锚点 4：Shadow Patch 四件套（被问"自进化效果"必答）

**机制**：
- `code_learning.ts`：每次查询记 ok/hint_files/files_touched/validate_ok/ms → .data/code-learning-signals.jsonl
- `code_experience_vectors.ts`：成功查询 embedding 入库（默认 300 条），下次相似查询语义召回 hint，min score 0.72
- `code_prompt_evolution.ts`：负反馈 / validate 失败 → shadow patch（最多 24 条）；hits≥3 晋级 evolved hint（最多 24 条）
- `code_prompt_ab_router.ts`：DJB2 风格 hash（`h = (h * 31 + charCode) >>> 0`，<strong>31 是乘数不是模数</strong>）后 `% 100`，bucket < treatmentPercent(默认 50) 进 treatment

**致命边界（被问必崩）**：
1. **hits≥3 是拍脑袋**——code_agent_env.ts:66 默认 3，parseEnvInt 限制 2-12。<strong>无 power analysis 推导</strong>。
2. **7 个 golden 全部命中 = 过拟合 golden**——shadow 在它跑的样本上命中 100%，线上分布不同。需要 hold-out set + 线上流量 shadow。
3. **自我强化回音室**——LLM 在错误 prompt 上反复生成同一错 patch，shadow 命中多次晋级错的。没防御机制。
4. **样本量不够**——800 文件 demo 每天撑死几百次 patch 调用，<strong>凑不出统计显著 A/B</strong>。50 样本 10pp 差异置信区间 ±27pp，可能 B 实际更差。

**诚实收口**："这是把'提示工程'做成'可观测、可迭代、可回滚的配置系统'，不是 prompt 写死在代码里——这是工程亮点。但效果数据没度量，是<strong>框架先行</strong>，接生产后要补 hold-out + power analysis + 线上 metric。"

### 锚点 5：Custom CheckpointSaver（被问"自研 Saver 接口"必答）

**为什么自研**：MemorySaver 进程内重启即丢；当时（2024 中）LangGraph 还没出官方 Postgres/Redis backend，被迫自研。

**关键方法**（server/services/checkpointSaver.ts 248 行）：
- `put(config, checkpoint, metadata)`：序列化 thread_id + checkpoint + writes，tmp + rename 原子写
- `getTuple(config)`：按 thread_id + checkpointId 读，处理 pendingSends
- `putWrites(config, writes, taskId)`：按 outer key（thread+ns+parent）+ taskId 累积 writes
- `getPendingSends`：跨进程消息恢复

**杀手锏（side effect reconciliation）**：<strong>崩在 patch 写盘后 validate 前，重启怎么 reconcile</strong>——磁盘是新版但 LLM state 是旧版，LLM 下一步调 validate 跑出 fail，LLM 不知道是自己 patch 错了还是磁盘不一致。<strong>没做 state reconciliation</strong>——这是漏洞，改进方向是 resume-time 先跑 validate 确认磁盘状态。

**杀手锏（0 丢失的水分）**：简历正文写"跨进程会话恢复(回归测试 0 丢失)"——<strong>严格说应该是"关键路径断点续跑 0 丢失"</strong>。测了 kill -9 后重启能续，但<strong>没系统性测"工具调用中"的原子性</strong>（patch 写盘一半被打断）。面试现场用更准的措辞。

**重做还会用自研吗**：诚实答<strong>"会用官方 langgraph-checkpoint-postgres"</strong>——自研的价值在于"file 本地调试 + Redis 生产"的双后端切换设计和对 Agent state 形态的深度理解。

### 锚点 6：三层守卫真实能力（防"Agent Safety"陷阱）

**源码真相**（三函数三件事，不是凑数）：见第三章 Safety 部分。

**真正的盲区**：三层都只到<strong>路径级</strong>，无<strong>内容级</strong>防御——合法路径 + 错误逻辑（prompt 注入让 `if(user.isAdmin)` 改成 `if(true)`）<strong>三层都拦不住</strong>。

**杀手追问"防了什么 LLM 会犯的错"**：诚实补刀——三层守卫防的是<strong>低频但高损</strong>的错误（写 .env 会泄露密钥、改 .git 会破坏版本），<strong>高频错误（改错业务文件、改错函数）三层都拦不住</strong>——后者要靠 read-before-write + diff 预览 + validate 兜底，不是 path guard。

---

## 五、量化指标（最致命的追问，必须答得有数字 + 诚实边界）

### 项目档位（防被查 git ls-files 翻车）

| 简历口径 | 源码实际 | 备注 |
|---------|---------|-----|
| 18 个工具 | 18 个工具（精确） | ✓ |
| 800 文件仓库默认 | 800 文件 / 512MB / 90s | demo 规模非生产 |
| 跨进程会话恢复 0 丢失 | 关键路径断点续跑 0 丢失 | 没测原子性 |
| 默认服务 | 默认配置 | 不是"已上线服务" |

**面试现场用真数 + 主动校准**：被追"800 文件够吗"诚实答"demo 规模，真实业务仓库 5000+ 文件第一天就跪"。

### 默认参数（被问"为什么是这个数"必答）

- `maxCandidates`: agent 内部 120 / API 直调 60 / retrieve 60（<strong>三套默认值不统一</strong>）
- `chunkChars`: 2200 (agent) / 2400 (API)
- `maxChunksPerFile`: 12 (agent) / 18 (API)
- `overlapLines`: 6 (agent) / 8 (API)
- `经验库 min score`: 0.72
- `经验库容量`: 默认 300 条
- `shadow patch hits`: ≥3 晋级（默认 3，限制 2-12）
- `A/B 分桶`: DJB2 hash % 100，treatmentPercent 默认 50
- `sandbox`: 默认 subprocess
- `write 上限`: 800KB
- `command timeout`: 默认 90s（可配 5s-10min）
- `VM 沙箱 timeout`: 5s
- `模型`: qwen-plus（<strong>不是 qwen-coder-plus</strong>，代码语义捕获弱是漏洞）
- `@langchain/langgraph`: ^0.2.0（Manager 已升 1.2.x，code_assistent 卡 0.2 是技术债）

### 7 个 .test.ts + 1 个 smoke

- **覆盖的核心模块**：analysis / code_learning / code_clarification / code_cross_agent_memory / code_prompt_ab_router / incoming_question / manager_task / code_execution / code_plan
- **没覆盖的（漏洞）**：agent.ts 主流程（靠 smoke）/ vectorSearch（要真 key）/ sandbox_runner（只 smoke）/ DiffViewer（Myers 算法没单测）/ applyUnifiedDiffOrThrow（diff parser 没单测）
- **CI gate**：scripts/code-smoke.mjs，min pass rate 75%

---

## 六、Token 成本 + Context 管理盲区（被问"烧多少钱"必答）

### token 估算

- **单步 token 构成**：system prompt（含 18 工具 schema + mode workflow + experience + agent patches + inspect hint）≈ 3-5k + tool result ≈ 1-3k + history 累积
- **典型 bug 修复**：5-10 步 ReAct 循环 → 烧 30-50k token
- **长 task（30+ 步）**：context 累积到 100k+，qwen-plus 128k 接近上限

### 致命漏洞：没做 compaction

<strong>第 28 轮 LLM 要改第 1 轮 read 的文件，但 obs 早就被挤掉了</strong>——LLM 凭记忆改（幻觉风险）或重新 read（多一次工具调用）。<strong>没做 Read 工具的"虚拟持久化"</strong>（system prompt 维护"已读文件清单 + hash"，LLM 只引用 file_id，改写时才从 store 拉最新）。

### 改进方向

- token budget 每步入口算
- message sliding window + LLM summary
- 工具结果按 id retrieval（Claude Code file tool 范式）
- 自动切小模型（简单步骤用 flash 级）+ Prompt Caching（@anthropic 5min TTL）

---

## 七、3 个最容易被追问卡的点（提前准备）

### 1. 「prompt 注入防御」
路径级守卫拦不住内容级——合法路径错误逻辑一层都拦不住。诚实承认现有 Safety 防的是 LLM 犯错，不是防 prompt injection。改进方向：对抗性 eval + patch 静态分析 + HITL 风险分级。

### 2. 「事故案例」
真落地的 Coding Agent 必然有事故。准备至少 1 个具体故事：根因分类（RAG 召回错 / Diff apply 错 / Prompt injection / Validation 漏判），事后加的防御机制。诚实答"如果是 demo 没出过；如果是生产，没出过事故 = 没真跑或没发现"。

### 3. 「和 Cursor 的差异化」
功能完整度 Cursor 远超我，<strong>但企业 Safety + 审计赛道 Cursor 不做</strong>——我赌的是企业内部代码代理的市场，不是开发者工具的市场。差异化：Shadow Patch 自进化（Claude Code 没有跨进程 A/B）+ 企业审计（开源产品普遍弱）+ 三层 guard + 沙箱（Cursor 假设开发者信任）。

---

## 八、反问面试官 3 件套（每次必问）

1. **Coding Agent Safety 边界**："你们的 Coding Agent 怎么防 prompt injection？路径级守卫拦不住内容级——你们做了对抗性 eval / patch 静态分析 / HITL 风险分级哪些？"

2. **代码 RAG 召回质量**："你们代码 RAG 的 recall@K 多少？chunking 粒度怎么定？embedding 用通用还是代码专用（voyage-code / qwen-coder）？做过 baseline 对比吗？"

3. **Token 成本 + context 管理**："你们的 Coding Agent 平均一个 task 烧多少 token？长 task context 爆了怎么办——sliding window / summary / 按 id retrieval 哪种？做 Prompt Caching 了吗？"

---

## 九、收口金句

> "code_assistent 不是 Cursor 翻版，是<strong>企业内部代码代理的 Safety 范式</strong>——功能完整度我认输 Cursor，但企业 Safety + 审计赛道 Cursor 不做。**机制设计强但实测数据弱**（800 文件 demo / 没真实使用 / 没事故复盘）——这是诚实定位。我赌的是企业内部代码代理的市场，不是开发者工具的市场。"
