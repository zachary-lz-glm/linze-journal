# Code Assist Agent · 工程化代码助手 · 面试深度说明书

> **一句话定位**：一个 Cursor 类的工程化 Coding Agent——不是聊天框贴代码，而是"读仓库 → 语义检索 → 静态分析 → Bug 扫描 → Diff 预览 → **受控写盘**"的完整工程流。
>
> **端口** `13103` · **技术栈** Nuxt 4 + Pinia + WebSocket + LangGraph(JS) + @langchain/openai + monaco-editor + typescript-estree + jose(JWT) + zod + vitest · **模型** DashScope qwen3.5-flash(OpenAI 兼容)
>
> **配套阅读**：[Manager 多智能体编排总管](Manager-Agent-多智能体编排总管.md)（本项目的上游） · [Tool Calling / Function Call / MCP](../agent-books/Tool-Calling-Function-Call-MCP.md) · [异常处理 安全 熔断](../agent-books/异常处理-安全-熔断.md) · [ReAct 反思 任务规划](../agent-books/ReAct-反思-任务规划.md)

---

## 0. 30 秒电梯演讲（开场怎么说）

> "我做的是一个**工程化 Coding Agent**——和 Copilot/Cursor 一类，但它强调的不是'生成代码'，而是**怎么把一个能直接改仓库的 AI 钉在可控范围内**。
>
> 它的核心流程是：读仓库 → 语义检索定位 → AST 静态分析 → Bug 扫描 → 出 Diff 让用户确认 → 受控写盘。我把**'模型 + 写权限 = 事故'**当作整个项目的安全第一性原理，所以 read-before-write 不是靠 prompt 写一句'先读后写'，而是**四层系统级强制**：工具白名单编译期裁剪 → 工具入口三重门禁 → apply_diff 强制 context 行精确匹配 → 文件系统层路径白名单 + sha256 乐观锁 + 原子写。
>
> 另外两个亮点：一是 **Prompt 自我进化**——负反馈和 validate 失败沉淀成 shadow 补丁，A/B 验证后才晋级；二是它是 Manager 总管的下游，通过 managerTask 协议和文件总线跟总管/DB/RAG 共享上下文。"

**为什么面试稀缺**：Coding Agent + LangGraph ReAct + 沙箱/JWT/限流/路径白名单 + 自进化 + 跨 Agent 协作，是一个项目讲全"AI 工程化"的高密度载体。

---

## 1. 项目定位与核心价值

### 1.1 不是聊天框，是工程化 Coding Agent

| 普通代码聊天 | Code Assist（本项目） |
|------|------|
| 用户贴代码，模型回复代码 | 读真实仓库结构、Git 状态 |
| 无副作用 | 受控写盘（apply_diff/write_file） |
| 无法验证 | 跑 validate_project/run_tests 闭环 |
| 全靠 prompt 约束 | 系统层四层强制安全 |
| 改完即止 | 出 Diff 预览 → 人工确认 → 审计 |

完整流程：**读仓库 → 语义检索 → 静态分析 → Bug 扫描 → 重构建议 → Diff 预览 → 受控写盘 → validate 验证**。

### 1.2 核心安全观：模型 + 写权限 = 事故

> **面试金句**："一个能写文件的 LLM 是事故源。所有安全约束都不能放在 prompt 里——prompt 是软约束，模型会绕过；必须放在代码同步路径上，模型物理上绕不开。"

这是整个项目的第一性原理，决定了所有安全设计的位置（见 4.2）。

### 1.3 它在矩阵中的位置：Manager 的下游

Code Assist（13103）是 Manager 总管的下游专家之一。总管路由到 `code` 意图后，通过 `managerTask` 协议下发结构化任务（task_kind/facts/hint_files/write_allowed），Code Agent 解析后执行，结果作为**权威计算源**回传（详见 [Manager 说明书 §4.10/附录C](Manager-Agent-多智能体编排总管.md)）。

### 1.4 能力边界

| 适合 | 不适合 |
|------|--------|
| 仓库理解、局部重构、测试建议 | 无仓库上下文的任意写盘 |
| 语义找码、受控文件编辑 | 替代完整 CI/CD 和安全审计 |
| Bug 危险模式扫描 | 跨语言深度语义分析（当前聚焦 TS/JS/Vue） |

---

## 2. 技术架构总览

### 2.1 分层架构

```
┌──────────────────────────────────────────────────────────────┐
│  前端  Nuxt4 + Vue3 + Pinia                                   │
│  FileTree(文件树+git徽章) │ MonacoPane(编辑器) │ DiffViewer(Myers diff) │
└───────────────┬──────────────────────────────────────────────┘
                │ WebSocket (单通道: agent-chat / run-script / run-sandbox)
┌───────────────▼──────────────────────────────────────────────┐
│  Code Assist Agent (13103)                                    │
│                                                               │
│  ┌─ task_kind 路由 ─────────────────────────────────────┐    │
│  │ compute(纯LLM) │ inspect(只读) │ edit(可写) │ full  │    │
│  └──────┬─────────────────┬────────────────┬───────────┘    │
│         ▼                 ▼                ▼                 │
│  ┌─ LangGraph ReAct 双节点图 ───────────────────────────┐   │
│  │  agent 节点(ChatOpenAI.bindTools) ⇄ tools 节点(并行)  │   │
│  │  conditional edge: 有 tool_calls→tools, 无→END       │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                               │
│  18 个工具: 只读11 + 写7(write_file/apply_diff/git_commit/…) │
│  + read-before-write 四层强制 + 双层沙箱(vm + npm/docker)     │
│  + 代码 RAG(向量+文件名预筛) + 跨Agent文件总线记忆            │
│  + Prompt shadow→promote A/B 自进化 + NLU 回归门禁           │
│  + FileSaver(JSON checkpoint) 支持多轮                       │
│                                                               │
│  安全: JWT(jose)+scope │ 限流(60/min) │ 路径白名单 │ sha256 乐观锁 │
└──┬─────────────────────────────────────────────────────┬─────┘
   │ managerTask 协议(上行: Manager 下发)                  │ 文件总线
   │                                                      │ ../Manager_Agent/.data
   ▼                                                      ▼
  Manager 总管(13106)                              总管/DB/RAG 记忆共享
```

### 2.2 技术栈选型理由

| 技术 | 选型理由（面试可答） |
|------|------|
| **LangGraph** | ReAct 工具循环需要 checkpoint（多轮）、conditional edge（模型决定何时停）、stream——自写循环要重新解决这些 |
| **WebSocket** | 终端 run-script 需要**双向**（停止/发新命令），SSE 单向做不到；agent-chat 复用同一条 ws 省握手 |
| **monaco-editor** | 浏览器内 IDE，TS 类型推断、多文件切换；用 `?worker` 手动注入（弃用不稳定的 vite 插件） |
| **typescript-estree + typescript** | 双 AST 引擎分工：TS-compiler 抽语义符号最准，estree 抽结构带 loc 喂 LLM |
| **jose** | JWT(HS256) 验签 + scope 细粒度授权，认证与授权分离 |
| **AsyncLocalStorage** | 工具函数签名受 LangChain tool 约束不能加参，ALS 让工具内 `requestActor()` 隐式取上下文 |

---

## 3. 核心流程：一次代码修改请求的生命周期

### 3.1 task_kind 四路分发（前置路由）

不是所有请求都需要昂贵的工具循环。`resolveCodeExecutionPlan` 先把请求分成四类：

```
compute  ──→ runComputeChat 单 LLM 流（不进图，省 token）  ← Manager 下发"汇总这3个数字"
inspect  ──→ 进图但只给 11 个只读工具（不给写工具）        ← "分析下这个文件的复杂度"
edit     ──→ 进图给完整 18 工具，write_allowed=true        ← "把这个函数改成异步"
full     ──→ 进图给完整 18 工具（兜底）                    ← 默认

writeAllowed = manager?.write_allowed ?? (taskKind === 'edit')
```

```ts
// server/utils/code_execution.ts
function inferTaskKind(message, manager): CodeTaskKind | 'full' {
  if (manager?.task_kind) return manager.task_kind            // 总管显式指定优先
  if (looksLikeManagerComputeTask(message)) return 'compute'
  if (wantsCodeEdit(message)) return 'edit'
  if (/分析|analyze|在哪|定位|解释|bug|重构|refactor|测试|test/i.test(message)) return 'inspect'
  return 'full'
}
```

> **面试金句**："分级路由 = 成本 × 安全 × 能力的帕累托。compute 不该走工具循环，inspect 不该看到写工具——最小权限。"

### 3.2 ReAct 工具循环（edit/full 路径）

```
用户:"把 agent.ts 里的 callback 改成 async/await"
  → task_kind=edit, writeAllowed=true
  → buildGraph(chatOnly=false) → bindTools(18个)
  → agent 节点: 模型决定先调 read_file("agent.ts")
  → tools 节点: 并行执行 → ToolMessage 回灌文件内容
  → agent 节点: 看到内容，调 apply_diff(path, diff)
  → tools 节点: read-before-write 校验 → writeText → fs_changed 事件
  → agent 节点: 调 validate_project 验证
  → 无更多 tool_calls → END
  → 前端收到 delta + tool_start/end + fs_changed + meta + done
```

---

## 4. 关键技术深挖（重头戏）

### 4.1 LangGraph ReAct 双节点图

用 `StateGraph(MessagesAnnotation)` 建两个节点，conditional edge 驱动循环：

```ts
// server/services/agent.ts
const graph = new StateGraph(MessagesAnnotation)
graph.addNode('agent', async (state) => {
  // modelWithTools.invoke/stream → { messages: [AIMessage(含 tool_calls)] }
})
graph.addNode('tools', async (state) => {
  const aiMsg = messages[messages.length - 1]
  const toolOutputs = await Promise.all(toolCalls.map(async (call) => {
    const tool = toolsByName.get(call.name)
    const output = await tool.invoke(call.args)
    return new ToolMessage({ tool_call_id: call.id, content: output })
  }))
  return { messages: toolOutputs }   // 回灌
})
graph.addConditionalEdges('agent', (state) => {
  const last = state.messages.at(-1)
  return isAIMessage(last) && last.tool_calls?.length ? 'tools' : END
})
graph.addEdge('tools', 'agent')      // 循环
graph.addEdge(START, 'agent')
```

> **为什么 ReAct 而非 Plan-and-Execute**："代码修改需要边读边决策——读到文件内容才知道下一步，预先规划不现实。ReAct 让模型自己决定何时停（不再发 tool_calls 即终止）。"

> **设计亮点**：agent 节点是**纯函数**（只调模型），副作用全在 tools 节点，便于审计/限流/重试。MessagesAnnotation 自带 reducer 做数组累加，无需自定义。

### 4.2 read-before-write 四层系统级强制（命门）

这是整个项目最核心的设计——**不靠 prompt 祈求，靠四层代码强制**：

```
┌─ 第①层：工具白名单编译期裁剪 ──────────────────────────┐
│ buildGraph(chatOnly) 时决定 bindTools 列表              │
│ chatOnly/inspect/Manager未授权 → 模型根本看不到 write_file │
└─────────────────────────────────────────────────────────┘
┌─ 第②层：工具入口三重门禁 ──────────────────────────────┐
│ ensureDangerousToolAllowed(kind):                       │
│   chat-only → 拒；writeEnabled→拒；JWT+scope→拒         │
└─────────────────────────────────────────────────────────┘
┌─ 第③层：apply_diff 强制 context 行精确匹配 ─────────────┐
│ 先 readText 拿最新原文 → 逐行校验 ' '/'-' 行 → 不匹配抛错 │
└─────────────────────────────────────────────────────────┘
┌─ 第④层：文件系统层 ────────────────────────────────────┐
│ safeResolve 路径越界拦截 + 敏感文件黑名单 + 受限目录拒写  │
│ + sha256 乐观锁 + tmp/rename 原子写                      │
└─────────────────────────────────────────────────────────┘
```

#### （1）工具白名单编译期裁剪（模型物理上看不到）

```ts
// server/services/agent.ts
const tools = opts.chatOnlyMode
  ? [list_files, read_file, semantic_search, vector_search, git_status, git_diff,
     git_current_branch, git_log, ast_analyze, remember_preference, analyze_dependencies]  // 11 只读
  : [list_files, read_file, write_file, apply_diff, semantic_search, vector_search,
     git_status, git_diff, git_current_branch, git_create_branch, git_log, git_commit,
     run_tests, validate_project, ast_analyze, remember_preference, analyze_dependencies, generate_docs]  // 18 全集
const modelWithTools = model.bindTools(tools)
```

> **为什么编译期而非运行期拦截**："模型 bindTools 列表里根本没有 write_file → 模型物理上无法调用，比'运行期拒绝'更安全（避免模型反复尝试）。"

> **⚠️ critic 纠正点**：compiledGraph 按 `modelKey` 缓存，`chatOnlyMode` 被编进了 key（`agent.ts:451`：`${model}-${embeddingModel}-${chatOnly?'chat-only':'full'}`），所以 chatOnly 和 full 各编译一份图互不串。**但 key 没编 apiKey/baseURL**——切换密钥需重启进程或清 compiledGraph，否则用旧密钥。

#### （2）工具入口三重门禁

```ts
// server/services/agent.ts
function ensureDangerousToolAllowed(kind: 'write' | 'runScript') {
  if (runtimeConfig?.chatOnlyMode === true) return { ok: false, error: 'chat-only mode: dangerous tools are disabled' }
  if (kind === 'write' && toolsCfg?.writeEnabled !== true) return { ok: false, error: 'write tool is disabled' }
  if (kind === 'runScript' && toolsCfg?.commandEnabled !== true) return { ok: false, error: 'command tool is disabled' }
  const requireAuth = toolsCfg?.requireAuthForDangerousTools !== false && authCfg?.enabled === true
  const actor = requestActor()                    // 从 AsyncLocalStorage 取 JWT 解析的 {sub,scopes}
  if (requireAuth && !actor) return { ok: false, error: 'unauthorized' }
  if (requireAuth && requireScopes) {
    const needed = kind === 'write' ? 'write:repo' : 'run:script'
    if (!hasAnyScope(actor, scopes)) return { ok: false, error: `missing scope: ${needed}` }
  }
  return { ok: true }
}
```

> **为什么返回 `{ok:false, error}` 而不抛异常**：OpenAI tool_calls 协议要求每个 tool_call 必须有对应 ToolMessage 回灌，抛异常会让对话断裂触发 `tool_calls must be followed by tool messages`。返回错误字符串让模型"看到"拒绝原因并改方案，对话不中断（但也意味着模型会知道权限边界）。

### 4.3 受控写盘：apply_diff 严格校验 + sha256 乐观锁 + 原子写

#### （1）apply_diff：read-verify-write 三段式

```ts
// server/services/agent.ts (apply_diff 工具体)
const oldContent = await readText(input.path, 2_000_000, root)        // ① 先读最新原文
const newContent = applyUnifiedDiffOrThrow(oldContent, input.diff)    // ② 校验+变换
await writeText({ path: input.path, content: newContent, root })      // ③ 后写
```

`applyUnifiedDiffOrThrow` 内部逐行校验：

```ts
// sign===' ' 的 context 行：必须与磁盘精确匹配
if (sign === ' ') {
  const actual = original[cursor] ?? ''
  if (actual !== payload) throw new Error(`Diff context mismatch near line ${cursor + 1}`)
  out.push(actual); cursor += 1
} else if (sign === '-') {            // delete 行同理校验
  if (original[cursor] !== payload) throw new Error(`Diff delete mismatch near line ${cursor + 1}`)
  cursor += 1
} else if (sign === '+') {            // 只有 + 行才写新内容
  out.push(payload)
}
```

> **面试金句**："LLM 对行号/上下文幻觉率高。强制 context 行匹配 = 把'模型以为的文件状态'与'磁盘真实状态'对齐，相当于 git apply --3way 的严格版。不匹配抛错回灌给模型自我修正。"

> **critic 补充**：hunk 之间的"间隙"不会丢——`targetStart > cursor` 时 `out.push(...original.slice(cursor, targetStart))` 原样补进；hunk 乱序（`targetStart < cursor`）抛 `Invalid hunk order`。

#### （2）sha256 乐观锁（HTTP 路径）

```ts
// server/utils/files.ts (writeText)
const cur = await fileSha256(normalized, params.root)        // 重算当前磁盘哈希
if (cur.sha256 !== expected) throw new Error('File has changed')  // 映射 409
// tmp + rename 原子写
const tmp = `${filePath}.${uuid}.tmp`
await fs.writeFile(tmp, content)
await fs.rename(tmp, filePath)        // rename 失败才退化为直写+清 tmp
```

> **为什么用 sha256 当版本号**：Coding Agent 改文件是多步流程，期间可能人工或别的 agent 改了同一文件。乐观锁防"覆盖别人改动"（lost update）。tmp+rename 防"写到一半崩溃留半个文件"。

### 4.4 安全：JWT + scope + 限流 + 路径白名单 + 双名单

#### （1）双层闸门：认证（你是谁）vs 授权（你能干啥）

```ts
// server/middleware/01-auth.ts —— jose 验 HS256 JWT，解析 scope
const { payload } = await jwtVerify(token, new TextEncoder().encode(secret))
const scopes = typeof payload.scope === 'string'
  ? payload.scope.split(/[\s,]+/) : (Array.isArray(payload.scope) ? payload.scope : [])
event.context.auth = { sub: payload.sub || 'unknown', scopes }
```

> **为什么 HS256 不用 RS256**：内部单体部署，签发（Manager）和校验（Code）在同一可信域，对称密钥省去密钥分发。代价：持有 secret 的方都能伪造 token。

#### （2）路径白名单 + 双名单（防 prompt injection）

```ts
// server/utils/files.ts —— safeResolve 防路径穿越
export function safeResolve(repoRelativePath, rootOverride?) {
  const normalized = repoRelativePath.replaceAll('\\', '/').replace(/^\/+/, '')
  if (isSensitiveRepoPath(normalized)) throw new Error('Access to this path is restricted')  // .env/.pem/id_rsa
  const resolved = path.resolve(root, normalized)
  const rel = path.relative(root, resolved)
  if (rel.startsWith('..') || path.isAbsolute(rel)) throw new Error('Path must be within repository root')
  return resolved
}
```

- `isSensitiveRepoPath`（读黑名单）：`.env*`、`id_rsa`、`.pem/.key/.p12` 等密钥文件——防 LLM 把密钥读进上下文泄露给模型
- `isRestrictedWritePath`（写黑名单）：`.git/.nuxt/.output/.data/dist/node_modules`——防破坏版本库/构建产物

> **为什么用 `path.relative` 而非 `startsWith`**：path.relative 能挡符号链接拼接和 `..` 穿越，比简单 startsWith 可靠。

#### （3）固定窗口限流

`00-rate-limit.ts`：进程内 `Map<IP, {count, resetAt}>`，默认 60 次/min，超限 429。惰性清理（无定时器，桶数 >5000 时触发）。

> **⚠️ 主动暴露的缺口（critic + 面试加分点）**：限流和鉴权中间件**只在 `/api/` 生效**，WebSocket（`_ws.ts`）**完全不走中间件**！run-script/run-sandbox 通过 WS 直达，鉴权只靠 env 开关（`commandToolEnabled:false` 默认关）。如果 WS 端口暴露公网，限流被绕、run-sandbox 可被未授权调用。加固方向：WS open 时验 token，或前置反代理对 `/ws` 走鉴权。**主动点出这个缺口比假装没有强。**

### 4.5 双层沙箱：vm + npm script 白名单 + docker

#### （1）vm 沙箱（5000ms，纯计算试算）

```ts
// server/routes/_ws.ts
const sandbox = {
  console: { log: (...args) => send('stdout', args.map(String).join(' ')), error: (...) },
  setTimeout, clearTimeout,
  process: { env: {} }            // 空 process.env，无 require/fs
}
vm.createContext(sandbox)
const script = new vm.Script(code)
const result = script.runInContext(sandbox, { timeout: 5000 })
```

> **⚠️ critic 深挖点（面试必知的诚实回答）**："Node vm **不是安全沙箱**——攻击者拿到 sandbox 对象后能通过原型链逃逸拿到宿主 global：`({}).constructor.constructor('return this')()` → 拿到 globalThis → process/require/fs。本项目 sandbox 还注入了宿主的 `setTimeout`，逃逸更直接（`setTimeout.constructor` 拿 Function 构造器）。而且 `timeout:5000` 只杀同步执行，逃逸后挂的异步回调不受限。**所以我把真正不可信执行放 npm script 白名单 + docker（`--network=none :ro`），vm 只用于内部受信任的快速试算。**若 WS 的 run-sandbox 暴露公网就是 RCE 面。"

#### （2）npm script 白名单沙箱（真实执行隔离）

`runSandboxNpmScript` 只允许 `package.json.scripts` 里声明的脚本名（`getAllowedScripts` + `includes` 判定），模型不能任意执行 shell。执行走 subprocess（受限 env 白名单）或 docker（`--network=none`、`:ro` 挂载、512MB 内存）。

> **设计理由**："vm 用于纯计算试算（无 IO 风险），timeout 防死循环足够；真实跑测试/lint 必须走 npm script 白名单——只暴露项目已声明的 scripts，模型不该能执行任意 shell。"

### 4.6 静态分析：双 AST 引擎 + 纯规则 Bug 检测

#### （1）双 AST 引擎分工

| 引擎 | 用途 | 优势 |
|------|------|------|
| **typescript 编译器 API**（`createSourceFile` + `ts.isXxx` 谓词） | 语义级符号：import/export/default/require、解构导出 | 对修饰符/binding pattern/re-export 支持最准 |
| **@typescript-eslint/typescript-estree**（`parse({loc,range,jsx})`） | 结构级实体：函数/类/变量 + loc 位置 | ESTree 形状统一，带 loc 喂前端高亮和 LLM |

```ts
// analysis.ts —— TS-compiler 递归收集解构导出名（正则 simpleExplain 会漏）
const collectBindingNames = (binding) => {
  if (ts.isIdentifier(binding)) { addExportName(binding.text); return }
  if (ts.isObjectBindingPattern(binding) || ts.isArrayBindingPattern(binding)) {
    for (const el of binding.elements ?? []) {
      if (el && ts.isBindingElement(el) && el.name) collectBindingNames(el.name)
    }
  }
}
```

> **⚠️ 诚实回答（critic 点出，面试别翻车）**：`web-tree-sitter` 在 package.json 依赖里（0.26.7），但**当前分析链路零 import**——它为浏览器侧 monaco 增量解析预留。如果面试官问"tree-sitter 干嘛用"，正确回答是"分析链路没用，为浏览器侧预留"，**别顺着简历吹成核心**。

#### （2）bugDetector：4 条纯正则规则 + severity

```ts
// analysis.ts
export function detectBugs(text) {
  const issues = []
  if (/==[^=]/.test(src)) issues.push({ rule: 'eqeqeq', severity: 'low' })
  if (/\beval\(/.test(src) || /\bnew Function\(/.test(src)) issues.push({ rule: 'no-eval', severity: 'high' })
  if (/\brequire\(['"]child_process['"]\)/.test(src)) issues.push({ rule: 'no-child-process', severity: 'medium' })
  if (/\bvar\b/.test(src)) issues.push({ rule: 'no-var', severity: 'low' })
  return issues
}
```

> **面试金句**："bugDetector 是纯规则，定位是'危险模式快速扫描'——确定性、零成本、可单测。深度语义 bug（空指针/竞态/数据流）不靠它，靠 agent 工具链（LLM 看代码 + ast_analyze 拿结构 + run_tests 拿执行反馈）形成闭环。这是分层设计，不是短板。"

#### （3）testGenerator：只出脚手架不出成品

解析 `package.json` 探测 vitest/jest（vitest 优先），按模板拼 describe/it 骨架，`.vue` 文件注入 `@vue/test-utils mount` 注释。**不调 LLM**——脚手架确定能跑（语法不会错配），真实断言交给 LLM 在脚手架上补，比一次性 LLM 生成更可控、更少幻觉。

#### （4）intent 路由双通道：纯分析走快捷流，改代码强制进工具链

```ts
// agent.ts:1620 —— 纯分析零延迟零 token 直接返
if (focusPath && !hasExplicitPath && intent !== 'auto' && !requestedCodeChange) {
  const content = await readText(focusPath, 200_000, rootOverride)
  const metrics = intent === 'analyze' ? computeSimpleMetrics(content) : undefined
  const issues = intent === 'bugs' ? detectBugs(content) : undefined
  // ... formatAnalyzeReply 流式返回，不进图
}
```

> "纯分析请求走本地规则是零延迟零 token；涉及代码改动必须进 LangGraph 工具链，因为 read-before-write/audit/diff 这些安全约束只在工具层强制。**安全约束不能被快捷流绕过。**"

### 4.7 代码 RAG：三段式检索 + 成本控制

#### （1）三段式管线

```
walkFiles(800文件) → ① 文件名 token 预筛(免费)粗排取 top-60 候选
                   → ② sha256 增量缓存(文件没变就跳过 embedding)
                   → ③ 候选切块 embedDocuments → 余弦逐块打分取 top-10
```

```ts
// server/services/vectorSearch.ts —— 文件名 token 预筛
const tokens = Array.from(new Set(tokenize(query))).filter(t => !stop.has(t))
const ranked = files.map(file => {
  let score = 0
  for (const t of tokens) if (file.toLowerCase().includes(t)) score += 1
  return { file, score }
}).sort((a, b) => b.score - a.score)
```

> **为什么不塞全仓**：①成本——800 文件全量 embedding 每次 query 付费不可接受；②context window——12k 塞不下；③精度——lost-in-the-middle 衰减，向量检索先筛信噪比更高。

#### （2）四道成本闸

1. 文件名 token 预筛：候选 800 → 60，砍掉 92% embedding
2. sha256 增量缓存：文件没变跳过 embedDocuments
3. 经验向量库 query embedding 带 300s TTL 缓存（`embedQueryCached`）
4. 经验库 `slice(-300)` 上限控制规模

#### （3）向量索引原子落盘 + 串行写队列

`saveVectorIndex` 用 `state.writing = state.writing.then(...)` 把所有 save 串成 Promise 链（轻量锁），tmp+rename 原子写（crash-safe）。

> **⚠️ critic 点出的维护陷阱**：`vectorSearch.ts` 和 `code_experience_vectors.ts` **各写了一份 cosineSimilarity**，行为不同——前者对不等长向量 `Math.min` 截断（容忍维度变更期），后者不等长直接返回 0（严格防错误召回）。换 embedding 模型（1536→768）时两路后果不同，应统一或文档化。

### 4.8 跨 Agent 文件总线记忆

不走 HTTP/RPC，直接读兄弟目录文件：

```ts
// server/utils/code_cross_agent_memory.ts
const file = join(policyDir, 'manager-memory-semantic.jsonl')   // ../Manager_Agent/.data/
const rows = readJsonlTail(file, 120)                            // 读尾部 120 行
return rows.map(r => {
  const jaccard = computeJaccard(tokenBag(question), tokenBag(r.fact))
  const codeRelated = intent.includes('code') || /代码|函数/.test(r.fact)
  const score = jaccard + (codeRelated ? 0.12 : 0) + r.confidence * 0.1
  return { fact: r.fact, score }
}).filter(r => r.score >= 0.1).slice(0, 4)
```

> **为什么文件总线不用 Redis/HTTP**：①零依赖零运维；②零网络故障面，本地 fs 读不 timeout；③jsonl 天然 append-only 适合记忆流；④Jaccard 纯本地 set 运算不花钱。代价：强耦合部署拓扑（必须 `../Manager_Agent/.data` 存在），跨机器就废——用 `AGENT_SHARED_DATA_DIR` env 留了可挂载共享存储的口子。

读默认开、回写默认关（`enableCrossAgentWriteBack=false`），因为往总管 memory 写是有副作用的。

> **critic 补充**：`readJsonlTail` 对每行 `JSON.parse` 包 try/catch——总管正在 append 写导致末尾半行，解析失败被吞跳过，不崩。fail-graceful：跨 Agent 记忆是"锦上添花"，绝不能挂了拖垮主链路。

### 4.9 Prompt 自我进化（shadow→promote A/B）

> **面试金句**："模型有写权限，prompt 一坏就是事故。所以 prompt 演进必须先影子验证再晋级，绝不直接覆盖线上。"

#### （1）双信号源驱动进化

| 信号 | 触发 | 特点 |
|------|------|------|
| 用户点踩（feedback） | `score===-1` → `evolveFromNegativeFeedback` | 稀疏、主观 |
| **validate 失败**（隐式） | 写盘后校验失败 → `evolveFromValidateFail` | **高频、客观、与"写坏仓库"核心风险直接绑定** |

> "用户反馈覆盖率永远 <10%，validate 失败是代码助手特有的、机器铁证的负信号。把两者合并到同一 shadow 管线。validate 失败生成的 patch 是规则化硬编码（'修改 X 后须先 validate_project'），**刻意不用 LLM 摘要失败原因**——LLM 可能造出错误的'规则'污染 prompt。"

#### （2）shadow→promote 两阶段

```
负反馈/validate失败 → appendCodePromptPatch 写 code-prompt-patches.shadow.json (只计 hits 不上线)
                   → hits 达阈值(默认3) → autoPromote → code-evolved-hints.json (稳定 hint)
                   → 注入时只有 A/B 的 treatment 桶拿到已晋级 hint
                   → control 桶保持干净基线（只拿未晋级 shadow）
```

#### （3）稳定 hash 分桶（不用随机数）

```ts
// code_prompt_ab_router.ts —— DJB2 式确定性 hash
function hashBucket(seed: string): number {
  let h = 0
  for (let i = 0; i < seed.length; i++) h = (h * 31 + seed.charCodeAt(i)) >>> 0
  return h % 100
}
// seed = `${userKey|anon}|${question前120字符}`，bucket < 50 → treatment
```

> **为什么不用 Math.random**："同一用户同一问题两轮落不同桶，策略忽 A 忽 B 会污染 ok/fail 归因，实验结论不可信。确定性 hash 保证同种子同桶，观测才可归因。"

> **⚠️ critic 深挖点（A/B 选择偏差）**：`shouldSkipManagerComputeOverhead` 当 Manager 已注入 facts 时强制 `promptAbVariant='control'` 并跳过经验召回——所有 Manager 下发的 compute 样本系统性落 control 桶。**所以 A/B 实验只覆盖"无上游增强时本地经验是否有用"这个窄假设**，不是全量 compute 质量。面试要讲清楚这个偏差。

> **⚠️ 另一个诚实回答**：control 桶并非"完全无进化提示"——它仍会拿到未晋级的 shadow patch，只是过滤掉已晋级 hint。差别只在已晋级的稳定 hint，这正是实验要测的变量。

#### （4）NLU 跨 Agent 回归门禁

`nlu.cross-agent.test.ts` 不是普通单测，是跨 4 个 Agent（DB/RAG/Extractor/Manager）的 NLU 集成回归：用 `nlu-regression-cases.json` 的真实 case 钉死意图分类、槽位缺失检测、澄清解析、计划映射。

> **为什么代码助手要做 NLU 回归**："意图识别不稳，后续工具调用全跑偏。把'对比方案 A 和 B'误判成 fact_lookup 就不会走比较逻辑给错答案。用例放 JSON（PM/标注也能加 case），断言放测试代码，数据与测试解耦。"

### 4.10 多轮 checkpoint + 兜底（force_write_retry / thread_recover）

#### （1）自研 FileSaver（JSON 文件 checkpoint）

继承 `BaseCheckpointSaver`，按 `[threadId, ns, checkpointId]` 三级键序列化成 base64 存单个 JSON 文件。用户二次发消息传相同 thread_id，`getTuple` 恢复完整 messages 历史（含之前所有工具调用与结果）。

> **为什么自研不用官方 MemorySaver/PostgresSaver**："①单进程零依赖部署；②可观测性——JSON 能直接 cat 看每轮 messages/工具调用，调试极方便；③零依赖启动。代价是写放大（全量 JSON 重写），用 `enqueueFlush` 串行化 + tmp/rename 原子写规避并发损坏。"

> **⚠️ critic 点出的隐含假设**：`getTuple` 用 `localeCompare` 降序取"最新"，依赖 checkpoint.id 字典序单调（LangGraph 的 id 实际是 ulid/uuidv7 时间前缀格式）。若框架换成纯随机 uuid v4，取到的"最新"可能不是物理最后写入——但每个 checkpoint 都含完整 messages 数组，取到任意较新的都能恢复完整历史。

#### （2）两个系统兜底

LLM 不是确定性函数，会偶发"该写不写"或"调了 tool_call 却没给后续"导致死锁：

- **force_write_retry**：`requestedCodeChange && canWriteTools && !sawWriteLikeTool` → 用新 thread_id（`${orig}-force-write-${Date.now()}`）重跑并注入 ForceWrite 强约束 prompt
- **thread_recover**：`shouldRecoverThreadFromError` 正则匹配 OpenAI 的 `tool_calls must be followed by tool messages` 错误 → 换新 thread_id 重跑

> "两者都用新 thread_id 避开旧 checkpoint 污染。代价是丢失多轮上下文——**有意取舍：确定性 > 上下文连续性**。"

### 4.11 WS 流式协议 + 前端 IDE

#### （1）单通道 + sendJson 闭包注入（生产-消费解耦）

`_ws.ts` 收到 agent-chat 后把 `peer.send` 闭包化为 sendJson 传给 `handleAgentChat`，agent.ts 用 `ctxStorage.run({sendEvent, sendDelta})` 包裹整条 graph 执行，工具内 `requestSendEvent('tool_start')` 从 AsyncLocalStorage 隐式取 sendEvent。

> **为什么用 AsyncLocalStorage**：LangGraph 节点是异步嵌套调用，直接传参会"回调层层穿透"。ALS 让工具代码零侵入拿到 sendEvent，且 handleAgentChat 不耦合传输层（换 SSE 只需换 sendJson 实现）。

#### （2）九类流式事件协议

```
delta(LLM token 流) / phase(节点切换) / tool_start / tool_end /
fs_changed(文件树刷新) / clarify(澄清追问) / meta(task_kind/ab_variant/files_touched) /
done / error
```

> **关键约束**：done 必须与 error 配对（`_ws.ts` catch 里硬编码 error+done 连发），否则前端 `sessionStore.sending` 永远卡 true，UI 死锁。`ws.onclose` 时前端主动 `finishStream + appendDelta('(连接已断开)')` 兜底。

> **⚠️ critic 点出的信息泄露面**：`sanitize()` 只在 run-script 的 stdout/stderr 和 error 文本里跑，**正向 delta 不脱敏**——如果模型在回复里 echo 了 API key，会直送前端。应在 sendDelta 也加 sanitize。

#### （3）前端：DiffViewer(Myers) + Monaco + 流式状态机

- **DiffViewer**：手写 Myers diff（O(ND)，git 同款），纯前端预览（**不是校验**，校验在 sha256 和后端 path 白名单）
- **MonacoPane**：`?worker` 显式注入 5 个 worker（弃用不稳定的 vite 插件），`file:///` URI + getModel 复用 model（多文件切换不丢 TS 类型推断），`applyingFromProps` 标志位防受控组件回环
- **sessionStore**：`streamingAssistantId` 锚点 + `appendDelta` 增量拼接 + 空响应兜底（`(空响应)`）

---

## 5. 核心数据结构与协议速查

| 结构 | 形状 | 出处 |
|------|------|------|
| **MessagesAnnotation.State** | messages: BaseMessage[]（agent append AIMessage，tools append ToolMessage[]） | LangGraph |
| **Actor** | {sub, scopes[]}（JWT 解析，经 AsyncLocalStorage 贯穿） | `agent.ts:196` |
| **CodeExecutionPlan** | {taskKind: compute/inspect/edit/full, writeAllowed, hintFiles, upstreamContext} | `code_execution.ts` |
| **ManagerCodeTaskPayload** | {task_kind, refined_question, facts, hint_files, write_allowed}（总管下发契约） | `manager_task.ts` |
| **ParsedHunk** | {oldStart, oldCount, newStart, newCount, lines}（unified diff） | `agent.ts:230` |
| **VectorIndex** | {files: Record<path, {sha256, chunks:[{startLine,endLine,vec,snippet}]}>} | `vectorSearch.ts` |
| **CodePromptPatch** | {stage, text, source: feedback/validate_fail, hits, promotedAt?} | `code_prompt_evolution.ts` |
| **CodeLearningSignal** | {question, task_kind, ok, score, files_touched, validate_ok} | `code_learning.ts` |
| **工具 schema** | tool(fn, {name, description, schema: z.object})，写类带 reason 字段强制陈述动机 | `agent.ts` |

---

## 6. 设计决策与取舍（why this not that）

| 决策 | 理由 | 代价 |
|------|------|------|
| 危险能力默认全关（writeToolEnabled:false 等） | 安全开关默认值必须最严，避免忘配鉴权就把能改仓库的 agent 暴露 | 可用性下降，需手动 env 解锁 |
| 工具白名单编译期裁剪（非运行期拦截） | 模型 bindTools 里没有 → 物理上无法调用，比运行期拒绝更安全 | 同 model 下 chatOnly/full 各编译一份图 |
| apply_diff 强制 context 匹配（非任意 diff） | LLM 行号幻觉率高，强制匹配 = 模型脑中状态与磁盘对齐 | 偶尔因空格/换行微小差异误报；宁可失败不可错改 |
| 自研 FileSaver（非官方 saver） | 单进程零依赖、可 cat 调试、零依赖启动 | 写放大 O(n)，生产规模换 SQLite |
| task_kind 四路分发 | compute 不进图省 token、inspect 不给写工具最小权限 | 路由正则启发式，边界 case 可能误分类（managerTask.task_kind 优先覆盖） |
| 跨 Agent 走文件总线（非 HTTP/Redis） | 共址部署零网络故障面、Jaccard 本地运算不花钱 | 强耦合部署拓扑，跨机器失效 |
| 影子→晋级两阶段（非直接改 prompt） | 坏提示先小流量验证、可回滚 | 演进慢、实现复杂（两套存储） |
| vm 沙箱与 npm script 沙箱分离 | vm 只跑纯计算试算，真实执行走 npm 白名单 | vm 不是安全沙箱（原型链逃逸），不可信代码必须 docker |
| 鉴权 HS256（非 RS256） | 同可信域省密钥分发 | 持 secret 方都能伪造 token |
| 双 AST 引擎（TS-compiler + estree，非 tree-sitter） | TS 语义最深、estree 形状通用、服务端纯 JS 无 WASM | 放弃 tree-sitter 多语言统一 |

---

## 7. 工程化亮点

### 7.1 安全（四层 read-before-write + 双层沙箱 + 双名单）

详见 §4.2-4.5。核心：模型 + 写权限 = 事故 → 所有约束放代码同步路径。

### 7.2 成本控制

- task_kind 四路分发（compute 不进图）
- 纯分析走快捷流（零 LLM）
- 代码 RAG 四道成本闸（文件名预筛 + sha256 缓存 + query 缓存 + 经验库上限）
- modelTier（继承自总管的分阶段降级）

### 7.3 测试与评估

- **vitest 单测**：analysis/code_clarification/code_cross_agent_memory/code_learning/code_prompt_ab_router
- **NLU 跨 Agent 回归门禁**（`nlu.cross-agent.test.ts`，CI 在 monorepo 顶层跑）
- **code-smoke 评估器**（critic 补充）：`scripts/code-smoke.mjs` 打真实 HTTP 端点，断言 ok/minHits/expectNeedsClarify，带 `--ci` 模式 + `minPassRate` 门禁（默认 0.75），产物 `code-smoke-baseline.json` 的 passRate 被 `/api/learning` 回显到前端——**这是"A/B 进化是否真有效"的唯一量化证据来源**

### 7.4 可观测性

- `code_metrics`：按 `path:ok|fail` 分桶计数 + jsonl 落盘
- `trace_log`：跨 Agent trace（带 from_manager/skip_overhead 标记），是 Manager 跨 Agent 决策的数据源
- A/B counters：`variant:ok|fail`（进程内，多实例需落盘扩展）
- `/api/learning`：一次性返回 learning/experience/evolution/crossAgent/promptAb/metrics 六大画像

### 7.5 Prompt 双通道治理（critic 补充）

- **人工通道**：`playbook_skills.ts` 按 `## ` heading 解析 `skills/*/skill.md`（SSOT），`/api/internal/skills/reload.post.ts`（fail-closed 令牌校验后 clearCache）实现平台热改 prompt 不重启
- **自动通道**：`code_prompt_evolution.ts` 的 shadow→promote
- 两条通道互补：人工改的是 System 段骨架，自动进化的是 append 短规则

### 7.6 平台模型热下发（critic 补充）

`platform_config.ts` 从 ClawHive `/api/internal/agent-config` 拉取本 Agent 的 model_planner/model_executor/model_embedding 覆盖（60s TTL + 失败降级到 stale cache），`compute.post.ts` 每次请求合并。`isPlatformModelOverrideActive` 区分 `platform_configured`/`updated_by` 非 seed/system 才生效——这是 Manager 平台对子 Agent 模型配置的热下发通道。

---

## 8. 面试问答库

### 基础

**Q1：你这个 Coding Agent 用的是 ReAct 还是 Plan-and-Execute？工具循环怎么转？**
> ReAct。LangGraph 两个节点：agent 调 ChatOpenAI.bindTools 产 AIMessage，tools 执行 tool_calls 产 ToolMessage[]。conditional edge 看最后一条 isAIMessage && tool_calls?.length：有则去 tools，无则 END。addEdge('tools','agent') 形成循环，模型自己决定何时停。选 ReAct 是因为代码修改需要边读边决策——读到内容才知道下一步，预先规划不现实。

**Q2：什么是 read-before-write？你怎么实现的，而不是 prompt 里写一句"先读后写"？**
> 四层系统级强制，不靠 prompt：①工具白名单——chatOnly/inspect/Manager 未授权时 buildGraph 不把 write_file 放进 bindTools，模型物理上看不到；②ensureDangerousToolAllowed 在每个写工具入口做 chat-only→开关→JWT→scope 四级校验；③apply_diff 内强制 readText 读老内容再 applyUnifiedDiffOrThrow 校验每行 context/delete 精确匹配；④safeResolve 路径越界拦截 + 敏感文件黑名单 + sha256 乐观锁 + 原子写。

**Q3：为什么用 WebSocket 不用 SSE？**
> 本质是双向性。ws 同时承载：agent-chat（流式推送，SSE 够用）+ run-script 终端（需要客户端发停止/新命令，SSE 做不到）+ run-sandbox（回传代码）。复用一条 ws 省握手、统一协议。选型规则：纯推送选 SSE，双向交互选 WS。

**Q4：你的工具是怎么定义的？模型怎么知道传什么参数？**
> 用 `@langchain/core/tools` 的 `tool(fn, {name, description, schema: z.object})`。schema 用 zod，LangChain 转成 OpenAI function calling 的 JSON Schema 挂到 bindTools。description 是关键——中文写清适用场景引导模型选对工具。写类工具带 reason 字段强制陈述动机（审计用）。

### 进阶

**Q5：模型生成的 diff 行号或上下文是幻觉的，怎么办？**
> applyUnifiedDiffOrThrow 严格校验：遍历每个 hunk，sign===' ' 的 context 行要求 original[cursor]===payload，sign==='-' 的 delete 行同理，不匹配抛 'Diff context mismatch near line X' 回灌给模型，模型看到具体 mismatch 位置会重新 read_file 再生成正确 diff。相当于 git apply --3way 严格版。hunk 乱序（targetStart<cursor）也报错。这就是为什么主推 apply_diff 而非 write_file 全量覆盖——diff 有校验能力，全量覆盖无法防幻觉。

**Q6：Node vm 沙箱隔离了什么？绕不开什么？**
> 隔离的是"全局变量命名空间"——注入剥离的 sandbox（只有 console/setTimeout/空 process.env），代码跑在自己 context 里访问不到宿主 global。**但绕不开**：①共享同进程和事件循环，setTimeout/Promise 回调在 timeout 抛错后仍执行；②无进程级资源隔离，不能防 OOM/死循环耗 CPU；③Node 官方明确 vm 不是安全沙箱——原型链逃逸 `({}).constructor.constructor('return this')()` 能拿 globalThis→process/require/fs。所以真正不可信执行放 npm script 白名单 + docker（--network=none :ro）。

**Q7：多轮对话怎么保持上下文？前面的工具调用还在吗？**
> 自研 FileSaver 继承 BaseCheckpointSaver，graph.compile({checkpointer})。每轮结束 LangGraph 自动 put 写 checkpoint（含完整 messages：System/Human/AI/ToolMessage 全在内），按 thread_id 存 JSON。二次发消息传相同 thread_id，getTuple 恢复完整历史，新 HumanMessage append 再跑图。所以上轮 read_file 的结果下轮仍可见。

**Q8：如果有人用路径穿越攻击，比如写 ../../../etc/passwd，防得住吗？**
> 防得住，三层：①safeResolve 把 path 规范化后 path.resolve(root, normalized)，再 path.relative(root, resolved) 校验结果不以 '..' 开头且非绝对路径；②isSensitiveRepoPath 黑名单 .env/.pem/id_rsa；③isRestrictedWritePath 拒写 .git/node_modules。另外 getRoot 校验 rootOverride 必须在 ALLOWED_ROOTS 白名单内。writeText 还有 800KB 上限和可选 expectedSha256 乐观锁。

**Q9：为什么 bug 检测用纯正则不混 LLM？**
> 4 条规则（==/eval/child_process/var）带 severity，确定性、零成本、可单测。定位是"危险模式快速扫描"，深度语义 bug 靠 agent 工具链（LLM + ast_analyze + run_tests）闭环。这是 lint 层，不是能力短板——快慢两条路分开。

### 深挖（killer followups，来自 critic）

**Q10：你说危险工具编译期裁剪，模型看不到 write_file。但 compiledGraph 是全局单例按 modelKey 缓存——第一个请求 chatOnly=false 编译了图，第二个 chatOnly=true 会拿到同一个图吗？**
> 不会。modelKey = `${model}-${embeddingModel}-${chatOnlyMode?'chat-only':'full'}`，chatOnlyMode 编进了 key。两份 modelKey 不同，比对失败重新 compile，各自独立 bindTools。但代价是同一 model 下 chatOnly/full 各编译一份图（两份内存），且 key 没编 apiKey/baseURL——切密钥不重新 compile 会用旧密钥。

**Q11：apply_diff 强制 context 行匹配。但两个 hunk 之间模型没给 context 行的"间隙"会丢内容吗？**
> 不丢。applyUnifiedDiffOrThrow 对每个 hunk：targetStart=oldStart-1，若 targetStart>cursor 就 `out.push(...original.slice(cursor, targetStart))` 把间隙原文原样补进。只有 hunk 内部 ' ' context 行和 '-' delete 行做严格匹配，'+' 才 push 新行。最后再 `out.push(...original.slice(cursor))` 补齐文件尾部。这是 git apply 标准语义——diff 只描述改动点，其余隐式保留。

**Q12：force_write_retry 用新 thread 重跑。如果第一次已经写了半个文件（apply_diff 改了 A.ts），重跑又写 B.ts，用户看到"改了两个文件"——怎么防止重复落盘？**
> 当前实现不会重复。force_write 的判定是 `!sawWriteLikeTool`——本轮完全没触发任何写工具才重跑。第一次成功 apply_diff 了 A.ts，sendEvent 的 tool_start 分支会把 sawWriteLikeTool 置 true，条件不成立不触发。真正风险场景是：第一次模型口头说要改但没调写工具（requestedCodeChange=true 且 sawWriteLikeTool=false），重跑后改了 B.ts——但此时 A.ts 根本没被改过，不存在"改两个"。force_write 不检查第一次的部分副作用且新 thread 丢多轮上下文——文档化的取舍：确定性 > 上下文连续性。

**Q13：compute 路径 shouldSkipManagerComputeOverhead 在 Manager 注入 facts 时强制 control 并跳过经验召回。A/B 实验结论会不会被选择偏差污染？**
> 会，且是有意设计带来的偏差。Manager 已注入 facts 的 compute 任务，经验召回是冗余的（facts 已经是上游整理好的），跑经验增强反而引入噪声，所以 skipOverhead 合理。但这导致 treatment/control 分布不随机："有总管上下文"的任务系统性落 control，"裸问"的才参与分桶，且这些样本不计入 A/B 指标。**实验只覆盖"无上游增强时本地经验是否有用"这个窄假设**，不是全量 compute 质量。要测全量得改成分桶但都不注入，或单独建 Manager 样本实验。

**Q14：你说 vm 不是安全沙箱，攻击者怎么逃逸？具体 payload？**
> 经典逃逸：sandbox 对象的 constructor 是 Object，Object.constructor 是 Function，于是 `sandbox.constructor.constructor('return this')()` 拿到宿主全局 this（真正的 globalThis），进而拿到 process/require/fs。具体 payload 如 `({}).constructor.constructor('return process')().env`，或通过任意函数的 .constructor 链爬。本项目 sandbox 注入了宿主 setTimeout，逃逸更直接：`setTimeout.constructor` 拿 Function 构造器再 return this。vm.runInContext 的 timeout 只杀同步，逃逸后挂的异步回调不受限。所以不可信代码必须 docker——vm 只用于内部受信任试算。

**Q15：vectorSearch 的 cosineSimilarity 对不等长向量 Math.min 截断，code_experience_vectors 却不等长直接返 0。换 embedding 模型（1536→768）后果？**
> 两路后果不同。vectorSearch 路径（截断）：算前 768 维点积得数学上无意义但非零的"相似度"会错误召回——但因 vectorIndexKey 用 embeddingModel::root 做键，换模型生成新索引文件，旧 1536 维索引根本不会被新 query 命中，截断实际很少触发。code_experience_vectors 路径（不等长返 0）：旧 1536 维经验向量和新 768 维 query 直接返 0，全部召回失败——经验库"静默失效"，用户感知不到但个性化变差。正确做法是换模型时清空经验库重建。截断是容忍过渡期妥协，严格是防错误召回保守，两套策略针对不同风险偏好，应统一或文档化。

**Q16：shadow patch hits 达 3 自动晋级。如果偶然命中 3 次就晋级，treatment 表现更差——有 hint 级回滚和归因吗？**
> 当前是变体级而非 hint 级观测。recordPromptAbObservation 的 key 是 `${variant}:${ok?'ok':'fail'}`，只能判 treatment 整体优劣，定位不到单条 hint。回滚：手动删 code-evolved-hints.json 的该条，或调 promptAbTreatmentPercent=0 全切 control 止血。CodeEvolvedHint 有 sourcePatchId 可追溯，但 A/B counters 没按 hint 维度分桶。**加分答法**：承认是 P4 局限，生产化应给每条 hint 独立实验 ID + 按 hint 维度 ok/fail 分桶 + 自动 demote（某 hint 在 treatment 下 fail 率超阈值自动回退 shadow），这是 prompt-as-code 的 CI/CD 该有的能力。

**Q17：A/B 用 userKey|question 前 120 字 hash 分桶。同一用户问"怎么改 agent.ts"和"如何修改 agent.ts"——同桶吗？**
> 不同桶。seed 里的 question 是原文前 120 字，字符不同 hash 不同，bucket 可能不同。后果：同意图两轮请求，第一轮 treatment 看到进化 hint，第二轮 control 看不到——单用户体验不一致，指标上"同意图不同表述"分散到两桶稀释变体差异，A/B 更难检出真实效果。这是已知 tradeoff：用 question 原文进 seed 保证"同问题永远同桶"，代价是同意图不同表述漂移。要按意图分桶得先 normalize/intent 再 hash，但那又引入"意图识别"这个不稳定环节。当前优先保证"同种子确定性"这个 A/B 可信的最低要求。

**Q18：retrieve 重排 getFileScoreAdjust 给命中 boost 的文件 +0.15。如果该文件向量 baseScore 只有 0.1，加完 0.25 还是排不进 top10——boost 真有用吗？**
> 幅度是故意克制。向量 cosine 集中在 0.6-0.9，baseScore=0.1 说明语义几乎无关——这种情况 +0.15 也救不回来，是正确的：boost 是"微调"不是"翻盘"，避免把语义无关文件硬塞进结果污染 LLM 上下文。boost 真正生效在 top10 边界附近（0.65 vs 第10名 0.66）。penalty 上限 0.2 比 boost 大正是这个逻辑：语义相关但改错过（0.8-0.2=0.6）要压下去。设计哲学：**个性化只做边界调整，向量语义是主排序键**。

**Q19：run-script 走 WS，WS 不经过中间件。如果有人连上 WS 无限发 run-script，限流和鉴权都失效了——怎么防？**
> 这是当前实现的真实薄弱点。三层兜底：①ensureRunScriptAllowed 检查 chatOnlyMode 和 commandEnabled 全局开关，默认全关；②getAllowedScripts 只允许 package.json.scripts 声明的脚本名；③runSandboxNpmScript 走 subprocess/docker 隔离。但 token 鉴权确实缺：WS 的 run-script 不校验 JWT，只靠 env 开关。加固方向：WS open 时验 token（把 01-auth 逻辑搬到 defineWebSocketHandler 的 open），或前置反代理对 /ws 走鉴权，或对 run-script/run-sandbox 在 message 里二次验 token。**主动点出缺口比假装没有强。**

**Q20：FileSaver 用 localeCompare 降序取最新 checkpoint，依赖 checkpoint.id 字典序单调。LangGraph 的 checkpoint.id 是 uuid v4（随机），字典序不等于时间序——会取错吗？**
> uuid v4 字典序确实不保证等于时间序。但这里不致命：LangGraph 的 checkpoint.id 是按 super-step 顺序生成的，实际是 ulid/uuidv7 时间前缀格式，框架保证单调。即便纯随机 uuid v4，取到的"最新"可能不是物理最后写入的，但每个 checkpoint 都含完整 messages 数组（MessagesAnnotation 全量累加），取到任意较新的都能恢复完整历史——只是可能比"绝对最新"早一步。真正会出错的是并发同 thread 写入，但 enqueueFlush 串行化 + 单请求串行 graph.stream 规避了。可坦承"依赖 id 单调是隐含假设，换 id 策略需校验"。

---

## 9. 知识点延伸（连接通用概念）

| 本项目机制 | 对应通用 AI 概念 | 延伸阅读 |
|------|------|------|
| ReAct agent⇄tools 双节点循环 | **ReAct（Reasoning+Acting）** | [ReAct 反思 任务规划](../agent-books/ReAct-反思-任务规划.md) |
| 18 个工具 + bindTools + zod schema | **Function Calling / Tool Use** | [Tool Calling](../agent-books/Tool-Calling-Function-Call-MCP.md) |
| task_kind 四路分发 | **意图路由 / 最小权限** | — |
| read-before-write + sha256 乐观锁 | **乐观并发控制 / 幂等** | [异常处理 安全 熔断](../agent-books/异常处理-安全-熔断.md) |
| 工具白名单 + scope + 双名单 | **RBAC / 最小权限 / 纵深防御** | [异常处理 安全 熔断](../agent-books/异常处理-安全-熔断.md) |
| vm + npm 白名单 + docker | **沙箱隔离 / 纵深防御** | [工程化与部署](../agent-books/工程化与部署.md) |
| 代码 RAG 三段式检索 | **混合检索 / 增量索引** | [上下文管理与记忆](../agent-books/上下文管理与记忆.md) |
| shadow→promote A/B | **灰度发布 / A/B 实验 / prompt-as-code** | [工程化与部署](../agent-books/工程化与部署.md) |
| FileSaver checkpoint | **状态持久化 / 断点续传** | [上下文管理与记忆](../agent-books/上下文管理与记忆.md) |
| 跨 Agent 文件总线 | **Agent 通信 / 共享记忆** | [Multi-Agent](../agent-books/Multi-Agent.md) |
| Myers diff | **最长公共子序列 / diff 算法** | — |
| NLU 回归门禁 | **意图评测 / 回归测试** | [幻觉与评测](../agent-books/幻觉与评测.md) |

---

## 10. 自测清单（能讲出来才算过）

- [ ] 能讲清 ReAct 双节点图 + conditional edge 驱动循环
- [ ] 能说出 read-before-write 的**四层系统级强制**，并解释"为什么不靠 prompt"
- [ ] 能解释 apply_diff 的 read-verify-write 三段式 + context 行精确匹配
- [ ] 能区分工具白名单编译期裁剪 vs 运行期门禁，说出 modelKey 的坑
- [ ] 能讲清 vm 沙箱**隔离了什么、绕不开什么**（原型链逃逸），并解释为什么不可信代码走 docker
- [ ] 能说出 JWT HS256 + scope 的双层闸门（认证 vs 授权）
- [ ] 能解释 sha256 乐观锁防 lost update + tmp/rename 原子写
- [ ] 能讲清代码 RAG 三段式管线 + 四道成本闸
- [ ] 能解释跨 Agent 文件总线为什么不用 HTTP/Redis
- [ ] 能讲清 shadow→promote A/B + 双信号源（feedback + validate_fail）
- [ ] 能主动暴露 WS 不走中间件的安全缺口（面试加分）
- [ ] 能解释 shouldSkipManagerComputeOverhead 导致的 A/B 选择偏差
- [ ] 能区分 bugDetector（纯规则 lint 层）vs agent 工具链（深度语义 bug）
- [ ] 能诚实说明 web-tree-sitter 在依赖里但分析链路零引用
- [ ] 能讲清 force_write_retry / thread_recover 的"新线程隔离"取舍

---

## 11. 源码精读地图（按优先级）

| 优先级 | 文件 | 重点 |
|--------|------|------|
| ⭐⭐⭐ | `server/services/agent.ts` | buildGraph、18 工具、handleAgentChat、ensureDangerousToolAllowed、applyUnifiedDiffOrThrow |
| ⭐⭐⭐ | `server/utils/files.ts` | safeResolve、isSensitiveRepoPath、writeText（sha256+原子写） |
| ⭐⭐ | `server/services/vectorSearch.ts` | 三段式检索、sha256 增量、串行写队列 |
| ⭐⭐ | `server/services/analysis.ts` | 双 AST 引擎、detectBugs、generateTestScaffold（唯一内核） |
| ⭐⭐ | `server/services/checkpointSaver.ts` | 自研 FileSaver、三级键、串行 flush |
| ⭐⭐ | `server/utils/code_prompt_evolution.ts` | shadow→promote、双信号源 |
| ⭐ | `server/routes/_ws.ts` | WS 单通道、vm 沙箱、npm 白名单 |
| ⭐ | `server/middleware/01-auth.ts` + `00-rate-limit.ts` | JWT+scope、固定窗口限流 |
| ⭐ | `server/utils/sandbox_runner.ts` | npm script + docker 沙箱 |
| ⭐ | `server/utils/code_cross_agent_memory.ts` | 文件总线、Jaccard 召回 |
| ⭐ | `server/utils/code_prompt_ab_router.ts` | DJB2 确定性分桶 |
| ⭐ | `server/services/nlu.cross-agent.test.ts` | NLU 跨 Agent 回归门禁 |
| ⭐ | `components/MonacoPane.client.vue` | ?worker 注入、URI model 复用 |

---

## 附录 A：硬指标速查表

| 维度 | 指标 |
|------|------|
| **工具** | chatOnly 11 个 / full 18 个；modelKey 含 chatOnly 不含 apiKey |
| **沙箱** | vm timeout 5000ms；npm script 默认 90000ms（范围 5s-10min）；docker 512MB / `--network=none :ro` |
| **写盘** | writeText 默认 800KB（HTTP 可传 2MB）；read_file 1M 字符、apply_diff 2M、vector_search 200K/文件 |
| **限流** | 默认 60 次/min/IP，窗口 60s，桶清理阈值 5000 |
| **RAG** | maxFiles 800、maxCandidates 60-120、maxResults 10-15、chunkChars 2200-2400、overlap 6-8 行、maxChunksPerFile 12-18 |
| **经验** | 向量 minScore 0.72、maxEntries 300、query embedding 缓存 300s、tokenOverlap 阈值 0.32 |
| **进化** | A/B treatment 50%、shadow 晋级 hits≥3、patch text 截 180、shadow 存上限 24 |
| **checkpoint** | FileSaver JSON、localeCompare 降序取最新 |
| **跨 Agent** | 读尾部 120 行、max 4、score≥0.1 |
| **安全开关** | writeToolEnabled:false / commandToolEnabled:false / authEnabled:false（默认全关） |

---

## 附录 B：常见坑（gotchas）

1. **WS 不走中间件**：rate-limit 和 01-auth 只拦 `/api/`，WS 是限流+鉴权盲区（最大安全缺口，主动暴露）。
2. **vm 不是安全沙箱**：原型链逃逸可拿 globalThis，timeout 只杀同步；不可信代码必须 docker。
3. **delta 不脱敏**：模型在回复里 echo API key 会直送前端（信息泄露面）。
4. **两份 cosineSimilarity 行为不同**：vectorSearch 截断、experienceVectors 不等长返 0，换模型后果不同。
5. **modelKey 不含 apiKey/baseURL**：切密钥需重启或清 compiledGraph。
6. **web-tree-sitter 依赖里但零引用**：为浏览器侧预留，别吹成分析核心。
7. **A/B 选择偏差**：Manager 注入 facts 的样本系统性落 control，实验只覆盖"无上游增强"的窄假设。
8. **force_write_retry / thread_recover 用新 thread**：丢多轮上下文换确定性。
9. **nodeCount 是 rough estimate**：`Object.keys(ast).length` 不等于节点总数，作者自己注释了，别当真实指标。
10. **internal_auth fail-open vs reload.post fail-closed**：两个内部令牌校验策略不一致（安全气味），生产应统一 fail-closed。
11. **tokenize 中文不分词**：文件名预筛对中文 query 几乎失效，中文语义召回靠 embedding 阶段。
12. **A/B question 进 seed**：同意图不同表述分桶漂移，是已知 tradeoff。
13. **FileSaver 依赖 checkpoint.id 字典序单调**：换框架 id 策略需校验。
14. **write-file zod 允许 maxBytes 2MB**：客户端可主动放宽上限，无服务端硬顶。

---

## 附录 C：与 Manager 总管的协作

Code Assist 是 Manager 的下游专家。协作链路：

```
Manager 路由到 code 意图
  → managerCodeDownstream.ts 调用 Code Agent
  → 下发 managerTask 双轨协议:
      自然语言层 question + 结构化侧车 manager_code_task_json
      { task_kind, refined_question, facts, hint_files, hint_symbols, write_allowed }
  → Code Agent 解析 (parseManagerCodeTask):
      task_kind 决定走 compute/inspect/edit/full
      write_allowed 决定工具白名单
      upstream_context/facts 注入 system prompt
  → 执行后结果作为"权威计算源"回传
  → Manager 的 codeFirstAuthority 让 code 覆盖同名键
  → visualize/report 优先用 Code 的 chart_plan 确定性出图
```

**跨 Agent 记忆**：Code 通过文件总线读 `../Manager_Agent/.data/manager-memory-semantic.jsonl`（Jaccard 召回），实现总管-DB-RAG-Code 四 Agent 画像共享。详见 [Manager 说明书 §4.10](Manager-Agent-多智能体编排总管.md)。

---

> **最后一句面试话术**："这个项目让我学到的最重要的一课是——**当一个 AI 有了副作用能力（写文件、执行命令），所有约束都不能放在它自己能改的 prompt 里**。工具白名单、门禁、diff 校验、沙箱、乐观锁，每一层都是'假设模型会犯错'的防线。这种'纵深防御 + 最小权限 + 主动暴露缺口'的工程思维，比任何单一技术点都更重要。"
