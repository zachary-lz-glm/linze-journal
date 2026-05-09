# 系统设计白板

> 目标：能在 5-8 分钟内画清楚，不求炫，求结构、边界、取舍。

## 1. 设计 Schema 驱动 BFF

### 一句话

**BFF 负责生成结构和初始状态，前端负责动态渲染和运行时联动。**

### 白板图

```text
后端 API
  |
  v
BFF 数据聚合
  |
  v
模板引擎 Builder
  |-- basic template
  |-- group template
  |-- rules template
  |-- message template
  |-- preview template
  |
  v
injectDActions
  |-- BFF safeEval 初始 visible/disabled
  |-- 序列化 d_actions 给前端
  |
  v
content_schema
  |
  v
前端 Schema Renderer
  |-- formatName dot path
  |-- RegisteredComponents
  |-- Listener 发布订阅
```

### 讲解顺序

1. 先讲背景：23 种活动类型，字段和联动变化快。
2. 再讲职责：BFF 生成 Schema，前端消费 Schema。
3. 重点讲联动：fetchApi 型和 state 型。
4. 最后讲 trade-off：扩展性强，但调试、类型和安全需要治理。

### 追问防御

| 问题 | 回答方向 |
|---|---|
| 为什么不用纯前端表单库？ | 初始状态和选项依赖 BFF，联动跨前后端 |
| 性能怎么保证？ | 按字段依赖局部触发，不整页重算 |
| eval 安全怎么办？ | 承认历史债，受限变量 + DSL/解释器重构 |
| 怎么保证 Schema 正确？ | 模板复用、handler 复用、Schema diff、类型生成 |

---

## 2. 设计前端组件库 / benefit SDK

### 一句话

**核心是 Register 扩展、Schema 同构、打包发版治理。**

### 白板图

```text
业务系统
  |
  | 使用
  v
benefit SDK
  |-- BenefitAdmin 入口
  |-- App 组件模式
  |-- Modal 函数调用模式
  |
  v
Register
  |-- 24 内置组件
  |-- add / addMultipleCmps 运行时扩展
  |
  v
Schema Renderer
  |-- d_component -> Component
  |-- content_schema 迭代渲染
  |
  v
Rollup 输出
  |-- ESM
  |-- CJS
  |-- .d.ts
```

### 讲解顺序

1. 背景：400+ 权益，权益类型持续增长。
2. 扩展：Register 模式避免改 SDK 核心。
3. 复用：和活动表单共享 Schema 渲染思路。
4. 工程：Rollup 双模、peerDependencies、Changesets、alpha/release。

### 追问防御

| 问题 | 回答方向 |
|---|---|
| 怎么避免依赖爆炸？ | peerDependencies + 外部化 React/设计系统 |
| 怎么支持业务自定义？ | 运行时 Register，不侵入 SDK |
| 怎么发版？ | changeset -> alpha 联调 -> release |
| 怎么回滚？ | 锁版本、降级到上一 release、业务侧灰度 |

---

## 3. 设计 Monorepo

### 一句话

**业务包独立发版，共享包统一复用，构建只跑受影响部分。**

### 白板图

```text
repo root
  |-- app/
  |    |-- dive
  |    |-- captain
  |    |-- ride_pass
  |
  |-- packages/
  |    |-- components
  |    |-- utils
  |    |-- rich-text
  |
  |-- package.json workspaces
  |-- yarn.lock
  |-- lerna.json independent
  |-- nx cache / affected
```

### 讲解顺序

1. app 放业务模块，packages 放共享能力。
2. Yarn workspace 做本地链接和依赖安装。
3. Lerna independent 支持业务独立版本。
4. Nx 做缓存和 affected 构建。
5. yarn.lock 和 resolutions 处理依赖一致性。

### 追问防御

| 问题 | 回答方向 |
|---|---|
| 为什么 Lerna + Nx？ | 历史项目 + 独立发版 + Nx 缓存 |
| 怎么避免包互相污染？ | 包边界、依赖声明、lint、CI |
| 构建慢怎么办？ | affected、缓存、拆共享包、并行构建 |
| 依赖冲突怎么办？ | yarn.lock、resolutions、peerDependencies |

---

## 4. 设计 prd-tools / AI 工程工作流

### 一句话

**AI 不直接拍脑袋写代码，而是生成有证据的开发计划。**

### 白板图

```text
build-reference
  |
  v
_reference/ v4.0
  |-- 01-codebase
  |-- 02-coding-rules
  |-- 03-contracts
  |-- 04-routing-playbooks
  |-- 05-domain
  |
  v
prd-distill
  |-- PRD ingestion
  |-- evidence.yaml
  |-- requirement IR
  |-- layer impact
  |-- contract delta
  |-- plan.md / questions.md / report.md
  |
  v
reference update suggestions
  |
  v
人工确认后回流
```

### 讲解顺序

1. 先澄清：不是 AI 直接生成代码。
2. build-reference 构建长期知识库。
3. prd-distill 消费 PRD + reference，输出结构化计划。
4. 可靠性靠证据链、质量门控、反馈回流。
5. 图谱只是发现层，reference 才是精选知识库。

### 追问防御

| 问题 | 回答方向 |
|---|---|
| 为什么不用向量库？ | 向量适合召回，不适合做权威事实源 |
| 知识过期怎么办？ | 健康检查、源码冲突 fatal、反馈回流 |
| AI 错了怎么办？ | evidence、contract delta、人工确认 |
| 怎么量化收益？ | 目前强调工程化原型和方法论，避免硬编数据 |

---

## 5. 设计 AI 流式对话前端

### 一句话

**SSE 负责流，状态机负责过程，渲染层负责不卡。**

### 白板图

```text
User Input
  |
  v
Conversation Store
  |
  v
SSE / ReadableStream
  |-- reconnect
  |-- Last-Event-ID
  |-- heartbeat
  |
  v
Stream Parser
  |-- chunk buffer
  |-- message delta
  |-- tool call delta
  |
  v
Renderer
  |-- markdown incremental
  |-- rAF throttle
  |-- virtual list
  |-- code block guard
```

### 追问防御

| 问题 | 回答方向 |
|---|---|
| SSE vs WebSocket？ | 单向流 SSE，双向协作 WebSocket |
| Markdown 卡怎么办？ | 增量解析、Worker、rAF 节流 |
| 断线怎么办？ | Last-Event-ID、去重、恢复状态 |
| Tool call 怎么展示？ | step 状态机 + 工具卡片 + 二次确认 |
