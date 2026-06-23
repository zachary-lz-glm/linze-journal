# AI 前端面试题 v2 · 前沿概念补强（8 题）

> 补强 v1（[AI题.md](AI题.md) 12 题）的前沿概念短板
> 重点：小红书二面 Harness 答得浅、千问一面被点名的薄弱点、2026 大厂最新考点
>
> 每题格式与 v1 一致：核心句 → 展开 → 追问点 → 项目桥接

---

## 目录

1. [SDD 完整流程（Spec-Driven Development）](#1-sdd-完整流程spec-driven-development)
2. [Harness Engineering 三种引擎](#2-harness-engineering-三种引擎)
3. [React 19 新特性 + RSC](#3-react-19-新特性--rsc)
4. [大模型 KV Cache 原理](#4-大模型-kv-cache-原理)
5. [流式 Markdown 增量解析](#5-流式-markdown-增量解析)
6. [Token 上下文工程深度](#6-token-上下文工程深度)
7. [MCP 协议深度实践](#7-mcp-协议协议深度实践)
8. [Agent Loop vs ReAct vs LangGraph](#8-agent-loop-vs-react-vs-langgraph)

---

## 1. SDD 完整流程（Spec-Driven Development）

**[核心句]** SDD 是编码前先创建 AI 能直接理解和执行的规范文档，完整流程是 proposal → design → specs → tasks → apply → verify → archive。

**[展开]**

SDD（Spec-Driven Development）是 2025-2026 年 AI 工程化的核心范式之一，由 GitHub Spec Kit / OpenAI 等推动。它强调**编码前先写 Spec**，让 AI 基于结构化规范生成代码，而不是直接丢需求让 AI 凭直觉写。

**完整 7 步流程**：

| 步骤 | 产物 | 目的 |
|------|------|------|
| 1. proposal | 提案文档 | 说清"为什么做"，业务价值 |
| 2. design | 架构设计 | 技术选型、模块划分、数据流 |
| 3. specs | 规范文档（SSOT） | 接口契约、字段定义、约束规则 |
| 4. tasks | 任务拆分 | 把 spec 拆成原子任务（AI 可执行） |
| 5. apply | AI 执行 | 按 task 顺序执行，每个 task 产出可验证 |
| 6. verify | 验证 | 跑测试 + 视觉回归 + 人工 Review |
| 7. archive | 归档 | 沉淀经验、更新知识库 |

**和 Vibe Coding / Harness Engineering 的关系**：

```
演进逻辑：Prompt Engineering → Context Engineering → Harness Engineering
对应落地：    Vibe Coding      → SDD              → Harness Engineering

Vibe Coding：自然语言描述需求，AI 生成代码，看感觉（适合探索期）
SDD：编码前先写 Spec，结构化规范驱动（适合标准化生产）
Harness：围绕模型构建完整基础设施，约束 + 反馈 + 记忆 + 技能进化（适合工业级）
```

**三种范式适用场景**：
- **Vibe Coding**：原型探索、个人项目、需求不清晰时
- **SDD**：B 端业务、团队协作、需要可追溯和可审计
- **Harness**：工业级生产、高可靠性要求、需要自进化

**[追问点]**
- **2026 阿里/网易高频题**：SDD 和传统瀑布模型的区别？→ SDD 是 AI 时代的"文档驱动"，但 Spec 是给 AI 看的，不是给人看的
- **EARS 需求规格化**：Executable Acceptance Requirements Syntax，把模糊需求转成可执行语句
- **Spec Kit 工具链**：GitHub Spec Kit / OpenAI Spec-Kit / 网易智企 CodeWave 的实践
- **和企业内 SDD 落地的难点**：团队接受度、Spec 维护成本、Spec 和代码的同步

**[项目桥接]**
"我的 prd-tools 就是 SDD 的工程化落地。完整 7 步映射：proposal（PRD 摄入）→ design（能力面适配器）→ specs（Reference 6 文件 SSOT）→ tasks（Spec/Plan 11 步蒸馏）→ apply（下游 Cursor/Claude Code）→ verify（quality-gate.py 5 项检查）→ archive（反馈回流 Reference）。差异化在于：我加了证据链 + 质量门控，防止 AI 跳步。"

---

## 2. Harness Engineering 三种引擎

**[核心句]** Harness 是围绕模型构建的完整基础设施，三种核心引擎是合并引擎、通信引擎、反思引擎。

**[展开]**

Harness Engineering 是 2025-2026 年最前沿的 AI 工程范式。核心认知：**Agent = Model + Harness**。模型只是发动机，Harness（缰绳）是方向盘、刹车、仪表盘、导航系统的总和。

**和 Agent / Skill / MCP 的关系**：

| 概念 | 层级 | 关注点 |
|------|------|------|
| Agent | 顶层抽象 | 感知→思考→行动的循环 |
| Harness | 围绕模型的控制架构 | 6 层基础设施（信息边界/工具/编排/记忆/评估/约束） |
| Skill | 工作流抽象层 | 多步骤工作流的编排 |
| MCP | 工具协议层 | 工具标准化接入 |

**三种核心引擎**（小红书二面问过，必背）：

### 合并引擎（Merge Engine）
- **作用**：整合多个 Agent 的输出，处理冲突和去重
- **场景**：多 Agent 并行分析不同维度，结果需要合并
- **实现**：基于优先级 + 置信度的合并策略，冲突时人工介入

### 通信引擎（Communication Engine）
- **作用**：Agent 间状态传递，避免上下文重复加载
- **场景**：长任务拆成多个 Agent，每个 Agent 独立上下文
- **实现**：通过中间文件（YAML/JSON）传递状态，类似操作系统的 IPC

### 反思引擎（Reflection Engine）
- **作用**：从失败中提炼规则，形成"错误即规则"的 ratchet 机制
- **场景**：Agent 犯错后，自动分析原因 + 生成候选规则
- **实现**：
  1. 日志收集层：记录每次工作流运行的决策日志、工具调用、产出质量评分
  2. 反思引擎：定期分析日志，识别高频失败模式，自动生成候选规则
  3. 人工审批层：工程师审核候选规则，确认后写入 AGENTS.md 或技能库
  4. 验证层：用 golden sample 重跑，对比优化前后评分

**KSG（Knowledge-Skill-Growth）抽象链路**：
- 短期记忆 → 长期记忆 → 知识库 → 技能手册（逐步抽象提取）
- 这是 Agent 自我迭代的核心

**业界实践**：
- **OpenAI**：AGENTS.md 作为项目目录（~100 行精炼），自定义 Linter 约束 Agent 行为
- **Anthropic**：上下文重置防止记忆漂移，GAN 启发的三 Agent 架构（Planner/Generator/Evaluator）
- **Stripe**：Minions 系统——1300+ PR/周由 AI Agent 驱动
- **Ghostty（Mitchell Hashimoto）**：AGENTS.md 每一行都是一次过去的失败

**[追问点]**
- **2026 小红书/字节高频题**：你的项目哪些是 Harness 的哪些层？
- **自进化机制怎么落地**：日志 + 反思 + 规则 + 验证的四步闭环
- **Harness 和 Context Engineering 的关系**：Context Engineering 是 L1（信息边界），Harness 是 L1-L6 的完整体系

**[项目桥接]**
"我的 prd-tools 是 Harness 的雏形，但缺自动化的技能抽取和进化闭环。映射到六层：
- L1 信息边界：Reference 6 文件 SSOT
- L2 工具系统：MCP 协议 + Skill 接口
- L3 执行编排：11 步蒸馏工作流 + Report Review Gate 硬停止
- L4 记忆状态：Evidence Index 增量构建 + 反馈回流
- L5 评估观测：quality-gate.py 三子命令 + 5 项加权评分
- L6 约束恢复：置信度分级 + questions.md 强制人工确认

**最大缺口在 L4 的反思引擎**——目前是人工回流，没有自动化的'错误即规则'机制，这是后续重点。"

---

## 3. React 19 新特性 + RSC

**[核心句]** React 19 三大新特性：use Hook + Actions + RSC 正式版，让前端写更少代码、跑更快。

**[展开]**

### use Hook（革命性）

- **作用**：在组件内**条件性**读取 Promise / Context，打破 Hooks 必须顶层调用的限制
- **场景**：根据条件加载不同数据
- **示例**：
```jsx
function Component({ shouldFetch }) {
  if (shouldFetch) {
    const data = use(fetchPromise); // 可以在 if 里！
    return <div>{data}</div>;
  }
  return <div>无数据</div>;
}
```

### Actions（表单处理新范式）

- **作用**：统一处理异步操作（提交、状态、错误、乐观更新）
- **核心 API**：`useActionState`、`useFormStatus`、`useOptimistic`
- **场景**：表单提交、数据变更
- **示例**：
```jsx
const [state, formAction, isPending] = useActionState(async (prev, formData) => {
  const result = await submitForm(formData);
  return result;
}, initialState);
```

### React Server Components（RSC）正式版

- **作用**：组件在服务端渲染，**运行时无 JS**，减少 bundle size
- **和 SSR 的本质区别**：
  - SSR：页面级，需要 hydration（客户端重新执行 JS）
  - RSC：组件级，服务端渲染后**不需要 hydration**
- **场景**：静态内容 + 动态数据的混合页面
- **限制**：不能有交互（onClick 等），需要交互的部分用 Client Component（'use client'）

### 其他新特性

- **Document Metadata**：原生支持 `<title>`、`<meta>` 在组件里写
- **Asset Loading**：`preload`、`preinit`、`prefetchDNS` 等 API
- **Ref as Prop**：函数组件不用 forwardRef 了，ref 可以直接作为 prop 传递

**[追问点]**
- **2026 阿里/腾讯高频题**：RSC 的 RCE 漏洞（CVSS 10 分）—— 服务端渲染时如果执行了客户端传来的恶意 key，会有安全风险
- **React 19 优化**：编译器（React Compiler）自动 memoization，不用手写 useMemo/useCallback
- **Next.js 15 和 RSC**：App Router 默认是 RSC，'use client' 切换
- **RSC 和 SSR 的性能对比**：RSC 首屏更快（无 hydration），但 TTFB 慢一点（服务端要算）

**[项目桥接]**
"我的 Schema 渲染引擎如果要迁移到 RSC，可以大幅减少 bundle size——目前前端渲染组件有 35+，全部打成 client bundle 太重。如果用 RSC，静态结构（标题、描述）服务端渲染，交互部分（表单、按钮）用 Client Component，能减少 40%+ 的 client bundle。"

---

## 4. 大模型 KV Cache 原理

**[核心句]** KV Cache 是以空间换时间——缓存自回归生成过程中的 Key/Value 向量，避免重复计算历史部分的注意力。

**[展开]**

### 为什么需要 KV Cache

Transformer 自回归生成时，**每生成一个新 token，都要重新计算 Attention**。如果不缓存，生成 N 个 token 的复杂度是 O(N²)。缓存后变成 O(N)。

### 工作原理

```
Prompt 进入 → Pre-fill 阶段（并行计算所有 token 的 K/V，缓存）→ Decode 阶段（每步只算新 token 的 K/V，追加到 Cache）
```

- **K（Key）**：token 在注意力机制中的"查询键"
- **V（Value）**：token 的"信息值"
- 缓存的就是历史所有 token 的 K/V 向量

### 工程挑战（面试高频）

#### 挑战 1：内存爆炸
- KV Cache 内存占用随序列长度**线性增长**
- 长上下文场景中可能**超过模型权重本身**
- 一个 70B 模型跑 128K 上下文，KV Cache 占用数十 GB

#### 挑战 2：内存带宽瓶颈
- Decode 阶段每步只生成 1 个 token，但需从 HBM 读取全部 KV Cache
- 内存带宽成为瓶颈，不是算力

#### 挑战 3：长上下文精度损失
- Lost in the Middle：开头和结尾信息权重高，中间信息容易丢
- 上下文 >40% 后进入 Dumb Zone，模型推理质量下降

### 优化方案

| 方案 | 原理 | 效果 |
|------|------|------|
| **PagedAttention**（vLLM） | 类似操作系统的虚拟内存分页 | 减少 80% 内存浪费 |
| **GQA / MQA** | 多个 Query 共享一组 K/V | 减少 KV Cache 体积 |
| **Quantization** | KV Cache 量化（FP16 → INT8 / INT4） | 内存减半，精度损失可控 |
| **Context Cache**（阿里云） | 缓存公共前缀的 KV | 多轮对话场景显著降本 |
| **LMCACHE** | 批量数据传输 + 计算和 I/O 流水线 | 企业级大模型推理加速 |

### 前端工程相关

虽然 KV Cache 主要在后端，但**前端工程师需要理解**：
- **为什么上下文越长越贵**：Decode 阶段每步读全部 KV Cache
- **为什么要做上下文压缩**：减少 KV Cache 内存占用 + 减少每步延迟
- **为什么要做 prompt caching**：相同前缀的 KV Cache 可以复用

**[追问点]**
- **2026 阿里/字节大模型岗高频题**：KV Cache 内存怎么估算？→ 模型层数 × 注意力头数 × 序列长度 × 头维度 × 2（K+V）× batch size × 字节数
- **vLLM PagedAttention**：参考操作系统虚拟内存，每个 sequence 的 KV Cache 不连续存储，按页分配
- **GQA（Grouped Query Attention）vs MQA（Multi Query Attention）**：GQA 是 Q 分组共享 K/V，MQA 是所有 Q 共享一组 K/V
- **Speculative Decoding**：小模型先猜，大模型验证，减少大模型调用次数

**[项目桥接]**
"我的 prd-tools 在 Context Engineering 层做了类似 KV Cache 的优化——不是每次都重新读全部 Reference，而是用 context-pack.py 做增量预匹配，只把相关片段加载到上下文。这和后端 KV Cache 的'避免重复计算历史'是同一个思路。"

---

## 5. 流式 Markdown 增量解析

**[核心句]** 流式 Markdown 解析不能等整段再解析，要增量解析 + 智能缓冲，特别是代码块未闭合时不能渲染 Markdown。

**[展开]**

LLM 流式输出是**逐 token 到达**的，但 Markdown 的某些语法（代码块、表格、列表）跨多个 token 才完整，所以需要**增量解析**和**智能缓冲**策略。

### 核心挑战

#### 挑战 1：代码块未闭合
```
LLM 输出：```javascript
function hello() {
  console.log('hi');
}
（还没输出闭合的 ```）

错误做法：直接渲染 Markdown → 代码块渲染成普通文本，混乱
正确做法：检测到代码块开始但未闭合，暂存到 buffer，等闭合后再渲染
```

#### 挑战 2：表格不完整
- 表格的分隔行（|---|---|）必须先出现才能识别为表格
- 流式过程中可能误判为普通文本

#### 挑战 3：列表嵌套
- 缩进列表的层级判断需要看后续行
- 流式过程中可能错误地拆分列表

#### 挑战 4：性能瓶颈
- 每 token 都全量 re-render → 万级 token 卡死
- 需要 rAF 节流 + 增量更新

### 主流方案

#### 方案 1：marked-streaming / markdown-it incremental
- 专门的流式 Markdown 解析器
- 维护解析状态机，只解析新到达的 token
- 代码块未闭合时返回"pending"状态，前端展示为"正在输入..."

#### 方案 2：分块渲染
- 按 chunk（如换行）切分，每块独立渲染
- 优点：实现简单
- 缺点：跨块的 Markdown 语法（如多行代码块）会断

#### 方案 3：缓冲 + 批量解析
- 用 buffer 累积 chunk
- 定时（如 50ms）批量解析
- 代码块/表格检测到不完整时延后解析

### 性能优化（必答）

| 优化 | 原理 | 效果 |
|------|------|------|
| **rAF 节流** | 用 requestAnimationFrame 合并多次渲染 | 减少 60+ 次渲染/秒到 60 次/秒 |
| **Web Worker** | 把 Markdown 解析放到 Worker | 主线程不卡 |
| **虚拟列表** | 万级 token 不全量渲染 | 只渲染可见部分 |
| **useDeferredValue** | React 18+ 的延迟渲染 | 不阻塞用户输入 |
| **增量 DOM 更新** | diff 已渲染部分 vs 新增部分 | 避免全量 re-render |

### Chrome 官方最佳实践

参考 [Chrome - Render LLM Responses](https://developer.chrome.com/docs/ai/render-llm-responses)：
1. 使用流式 Markdown 解析器，避免浏览器做不必要的工作
2. 代码块用专门的 syntax highlighter（如 highlight.js / Shiki），但**异步**渲染
3. 图片懒加载 + 占位符
4. 用 CSS `content-visibility: auto` 让屏幕外内容延迟渲染

**[追问点]**
- **2026 字节/腾讯 AI 前端高频题**：流式 Markdown 代码块未闭合怎么处理？
- **公式渲染（KaTeX/MathJax）**：同样需要等完整公式再渲染
- **代码高亮**：Shiki（VSCode 同款）vs highlight.js vs Prism，性能和效果对比
- **流式 + 虚拟列表 + Web Worker 三件套**：万级 token 也能流畅

**[项目桥接]**
"虽然 prd-tools 不是聊天产品，但流式 Markdown 解析的思路在我的工作流里也用到了——PRD 蒸馏过程中，AI 增量输出 Spec 内容，我用 YAML 中间文件做 buffer + 状态机管理（parsing → complete），避免部分产物被错误消费。"

---

## 6. Token 上下文工程深度

**[核心句]** 上下文窗口是稀缺资源，超过 40% 进入 Dumb Zone，需要预算管理 + 关键信息提取 + 自动摘要。

**[展开]**

### Token 计算基础

- **不同模型的 tokenizer 不同**：GPT 用 tiktoken，Claude 用自己的 tokenizer，千问用 BPE
- **每个 Provider 实现自己的 count_tokens**
- **粗略估算**：英文 1 token ≈ 0.75 词，中文 1 token ≈ 0.5-1 字

### Smart Zone vs Dumb Zone

```
0-40% 上下文：Smart Zone（模型推理质量最高）
40-80%：逐渐下降
>80%：Dumb Zone（明显幻觉、遗忘）
```

研究表明（Anthropic Lost in the Middle）：上下文超过 40% 后，模型推理质量显著下降。

### 上下文预算分配（实战经验）

```
系统提示词（角色、规则）：5-10%
工具定义（MCP / Function Calling）：10-20%
检索文档（RAG / Reference）：20-30%
对话历史：20-30%
用户当前输入：5-10%
模型输出空间预留：20-30%
```

### 上下文压缩技术（必答）

#### 方案 1：滑动窗口
- 保留最近 N 轮对话
- 简单但会丢失早期关键信息

#### 方案 2：关键信息提取
- 把重要实体、决策、约束持久化
- 类似"长期记忆"

#### 方案 3：自动摘要
- 对历史对话做压缩
- 递归摘要：把最老的消息递归压缩成摘要块

#### 方案 4：Progressive Summarization
- 把最老的消息递归压缩成摘要块放在 prompt 开头
- 上下文保持固定大小但会丢失细节

#### 方案 5：MemGPT / Letta 分页机制
- 设置上下文阈值，超过就 flush 出摘要存到外部存储
- 需要时再检索回来
- 类似操作系统的虚拟内存分页

#### 方案 6：Observation Masking（JetBrains 研究）
- 不真删旧消息，用占位符替换保留结构信息
- 大幅减少 Token 但保留上下文结构

#### 方案 7：LLMLingua / TKBF
- 开源的 token 优化库
- 用小模型判断哪些 token 重要，删掉不重要的

### Prompt Caching（降本利器）

- **Anthropic Prompt Caching**：相同前缀的 KV Cache 可以复用，5 分钟内重复请求便宜 90%
- **OpenAI Prompt Caching**：自动启用，无需配置
- **应用**：系统提示词 + 工具定义 + 知识库前缀固定不变，每次只变用户输入

**[追问点]**
- **2026 小红书/星河觉醒高频题**：上下文爆了怎么办？→ 三策略组合
- **Token 估算**：如何在前端实时计算 Token？→ 用 tiktoken.js（OpenAI）/ Claude 的 count_tokens API
- **多轮对话成本控制**：每次都把全部历史发给模型太贵，怎么做？→ 摘要 + 关键信息提取 + Prompt Caching

**[项目桥接]**
"我的 prd-tools 就是 Context Engineering 的工程化落地——不是把整个代码库丢给 AI，而是精选 6 个 SSOT 文件，build-index.py 做倒排索引，context-pack.py 按需求精准匹配代码锚点，按 must/should/optional 分层注入。三层映射：信息选择（索引）+ 预算管理（分层）+ 渐进披露（按需匹配）。"

---

## 7. MCP 协议深度实践

**[核心句]** MCP 是基于 JSON-RPC 的标准化工具协议，三层架构（Server / Client / Host），传输支持 stdio 和 SSE。

**[展开]**

### 协议架构

```
Host（Claude Code / Cursor / VSCode）
  ↓
Client（每个 Host 内置）
  ↓ JSON-RPC
Server（你自己开发的工具服务）
  ↓
Tools / Resources / Prompts
```

### 三种能力

| 能力 | 用途 | 示例 |
|------|------|------|
| **Tools** | 可调用的函数 | read_file / search_code / fetch_url |
| **Resources** | 可读的数据源 | 文件内容 / 数据库记录 / API 响应 |
| **Prompts** | 预置的提示词模板 | 代码 review prompt / 文档生成 prompt |

### 传输层

- **stdio**：本地进程通信，启动一个子进程，通过标准输入输出通信
- **SSE（Server-Sent Events）**：远程通信，HTTP 长连接
- **WebSocket**：双向通信（部分实现）

### 和 Function Calling 的关系

| 维度 | Function Calling | MCP |
|------|------|------|
| 本质 | 模型能力 | 标准化协议 |
| 提出方 | OpenAI | Anthropic |
| 绑定 | 绑定具体模型 | 不绑定模型，跨模型复用 |
| 调用 | 单次 | 长连接，支持工具发现 |
| 层级 | 模型层 | 协议层 |

**关系**：Function Calling 是底层机制，MCP 是在 Function Calling 之上的标准化协议层。实际使用中两者经常配合——MCP 负责工具的标准化暴露，Function Calling 负责模型的工具选择决策。

### 实战要点

#### 1. Server 设计原则
- **单一职责**：一个 Server 做一类事（如 filesystem / git / database）
- **工具描述质量**：函数名用 `{操作}_{实体}_{数据}` 规范（如 `read_file_content`），参数 ≤5 个
- **错误处理**：返回结构化错误（错误码 + 错误信息 + 建议）

#### 2. 工具数量爆炸问题
- 4 个工具时 GPT-4o 准确率 43%
- 51 个工具时降到 2%
- 解决：分层路由（Router 分类意图）+ 动态激活（按需注入）

#### 3. 跨平台复用
- 一个 MCP Server 开发一次，Claude Code / Cursor / VSCode / Codex 都能用
- 这是 MCP 的核心价值——打破工具碎片化

### 业界实践

- **Anthropic 官方 MCP Servers**：filesystem / git / postgres / slack / google-drive 等
- **公司内部 MCP**：飞书文档 / Notion / 内部知识库等
- **开源生态**：mcp-get / mcp-server 等市场

**[追问点]**
- **2026 腾讯/百度高频题**：MCP 和 A2A 协议的区别？→ MCP 是 Agent 和工具之间，A2A（Google 提出）是 Agent 和 Agent 之间
- **MCP 安全**：工具白名单、最小权限、敏感操作二次确认
- **MCP 性能**：stdio 比 HTTP 快，但只能本地；远程场景用 SSE

**[项目桥接]**
"prd-tools 使用了 MCP 协议，前端作为 MCP Client 调用 build-reference 和 prd-distill 两个 Skill。我开发过内部 MCP Server——从飞书文档提取 PRD 转 Markdown，一次开发 Claude Code 和 Cursor 都能用。这就是 Function Calling + MCP 协议的实际落地。"

---

## 8. Agent Loop vs ReAct vs LangGraph

**[核心句]** Agent 的三种主流架构：ReAct（推理+行动循环）、Agent Loop（OpenAI 风格）、LangGraph（图状态机）。

**[展开]**

### ReAct（Reasoning + Acting）

- **核心**：Thought → Action → Observation 循环
- **流程**：
  1. 模型推理下一步该做什么（Thought）
  2. 选择工具并调用（Action）
  3. 接收工具返回结果（Observation）
  4. 重复直到任务完成
- **优点**：简单、灵活
- **缺点**：可能陷入循环、上下文膨胀、不可控

### Agent Loop（OpenAI 风格）

- **核心**：固定的循环结构 + 明确的终止条件
- **流程**：
  ```
  while not done:
      response = model.generate(messages, tools)
      if response.has_tool_call:
          result = execute_tool(response.tool_call)
          messages.append(result)
      else:
          done = True
  ```
- **优点**：可控、可调试
- **缺点**：不够灵活，复杂场景需要状态机

### LangGraph（图状态机）

- **核心**：把 Agent 执行流程建模为**有向图**
- **要素**：
  - 节点（Node）：处理步骤（LLM 调用、工具调用、条件判断）
  - 边（Edge）：流转逻辑（条件路由、循环）
  - 状态（State）：图的全局状态，持久化
- **优点**：
  - 支持状态持久化
  - 支持人工检查点（Human-in-the-loop）
  - 支持循环和分支
  - 适合复杂工作流
- **缺点**：学习曲线陡、过度工程化

### Skill 懒加载机制（腾讯一面纠正过）

- **错误说法**：LangGraph 把所有 Skill 全量灌入上下文，巨耗 token
- **正确说法**：LangGraph 先把 Skill 的 description 拼到一起传一遍，AI 判断需要哪些才**按需懒加载** Skill 内容
- **类似 progressive disclosure**：既节省 token 又不损失能力

### 选型建议

| 场景 | 推荐架构 |
|------|---------|
| 简单问答 + 工具调用 | Function Calling 直接 |
| 多步骤任务 + 灵活推理 | ReAct |
| 固定流程 + 可控 | Agent Loop |
| 复杂工作流 + 状态持久化 | LangGraph |
| 团队工具 + 跨模型复用 | MCP + 任一架构 |

### 主流框架对比

| 框架 | 厂商 | 特点 |
|------|------|------|
| **LangGraph** | LangChain | 图状态机，最灵活 |
| **OpenAI Agents SDK** | OpenAI | 轻量，OpenAI 官方 |
| **AutoGPT** | 开源 | 早期 ReAct 实现 |
| **Claude Agent SDK** | Anthropic | Claude 官方，集成 MCP |
| **BeeMe / Superpowers** | 开源 | 成熟工作流模板 |

**[追问点]**
- **2026 美团/字节高频题**：ReAct 和 Chain of Thought 的区别？→ CoT 只推理不行动，ReAct 推理 + 行动
- **LangGraph 的状态持久化怎么实现**：用 checkpointer（如 SqliteSaver / PostgresSaver）保存中间状态
- **Human-in-the-loop**：在关键节点暂停，等人工确认后继续
- **Agent 失败恢复**：从最近 checkpoint 恢复，不用从头跑

**[项目桥接]**
"我的 prd-tools 用的是 Claude Code Skill 工作流，本质是 Agent Loop + 状态机。11 步蒸馏每步通过 YAML 中间文件传递状态，Spec Review Gate 是 Human-in-the-loop 检查点。如果迁移到 LangGraph，可以用图状态机更清晰地描述 11 步流程，但当前 Claude Code Skill 团队推广成本最低。"

---

## 附录：v1 + v2 合并后的 AI 题库总览（20 题）

### v1 已有（12 题）

1. SSE 流式输出前端怎么实现？
2. AI Agent 前端架构怎么设计？
3. RAG 检索增强生成前端能做什么？
4. MCP 协议是什么？和 Function Calling 的区别？
5. Prompt 注入攻击怎么防御？
6. 你平时怎么用 AI 辅助开发？
7. AI 生成代码你怎么审查？
8. 前端本地能跑 AI 模型吗？
9. 多轮对话的上下文窗口怎么管理？
10. 设计一个 AI 聊天前端应用
11. Context Engineering 是什么？
12. Harness Engineering 是什么？

### v2 新增（8 题）

13. SDD 完整流程（Spec-Driven Development）
14. Harness Engineering 三种引擎
15. React 19 新特性 + RSC
16. 大模型 KV Cache 原理
17. 流式 Markdown 增量解析
18. Token 上下文工程深度
19. MCP 协议深度实践
20. Agent Loop vs ReAct vs LangGraph

---

## 训练建议

### 第一周（紧急补强）

- **必背**：第 1、2、13、14 题（SDD / Harness 三引擎 / Agent 架构）—— 蚂蚁财富 AI Lab 必考
- **必练**：第 5、17 题（流式 Markdown / SSE）—— JD 明确点名
- **必懂**：第 15、18 题（React 19 / Token 工程）—— 二面高频

### 第二周（深度补强）

- 第 4、16、19 题（KV Cache / Token / MCP）—— 大模型岗高频
- 第 8、20 题（Agent Loop / LangGraph）—— 系统设计高频

### 第三周（全面覆盖）

- 把 v1 + v2 共 20 题每题用**核心句 + 项目桥接**口述 1 遍
- 录音回听，标"答得散"的题重练

---

## 参考资源

- [Martin Fowler - Harness Engineering](https://martinfowler.com/articles/harness-engineering.html)
- [Addy Osmani - Agent Harness Engineering](https://addyosmani.com/blog/agent-harness-engineering/)
- [Chrome 官方 - 流式 LLM 渲染最佳实践](https://developer.chrome.com/docs/ai/render-llm-responses)
- [Anthropic Prompt Caching](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching)
- [GitHub Spec Kit](https://github.com/github/spec-kit)
- [LangGraph 文档](https://langchain-ai.github.io/langgraph/)
- [KV Cache 优化全景解析](https://www.cnblogs.com/SCCQ/p/19837994)
