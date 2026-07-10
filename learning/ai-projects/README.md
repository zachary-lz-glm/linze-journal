# AI 项目实战 · 面试深度说明书

> 两个开源 Agent 项目的源码级深挖，从面试官视角整理成"能讲、能答、能扛追问"的备战资料。
>
> **适合谁**：要在面试里讲"我做过/深度研究过 AI Agent 项目"的候选人。

---

## 两份说明书

| 项目 | 定位 | 一句话亮点 | 链接 |
|------|------|----------|------|
| **Manager 总管**（13106） | 多智能体**编排层** | LangGraph 状态机 + Bandit/RL/Causal 三套自适应路由 + 自我进化飞轮 + HITL | [Manager-Agent-多智能体编排总管](Manager-Agent-多智能体编排总管.md) |
| **Code Assist**（13103） | 工程化 **Coding Agent** | read-before-write 四层系统级强制 + 双层沙箱 + Prompt A/B 自进化 | [Code-Assist-Agent-工程化代码助手](Code-Assist-Agent-工程化代码助手.md) |

两者是**上下游关系**：Manager 是总管，Code Assist 是它调度的下游专家之一。建议两份一起读——Manager 讲"编排"，Code Assist 讲"工程化安全"，互相交叉引用。

---

## 怎么用这份资料备战面试

### 推荐阅读顺序

1. **先读每份的 §0 电梯演讲 + §1 项目定位**——30 秒能讲清"这项目是干嘛的"
2. **背 §3 核心流程**——能画图、能讲请求生命周期是及格线
3. **深挖 §4 关键技术**——这是区分度，每份挑 3-5 个机制讲透
4. **过 §8 面试问答库**——基础题要秒答，深挖题（killer followups）要能扛
5. **用 §10 自测清单验收**——勾得上的才算掌握

### 每份说明书的结构

```
§0  30秒电梯演讲        ← 开场怎么说
§1  项目定位与价值       ← 为什么做、和竞品的区别
§2  技术架构总览         ← 架构图 + 选型理由
§3  核心流程             ← 请求生命周期（背下来）
§4  关键技术深挖         ← 重头戏，带真实代码
§5  数据结构速查
§6  设计决策与取舍       ← why this not that
§7  工程化亮点
§8  面试问答库           ← 基础/进阶/深挖 + killer followups
§9  知识点延伸           ← 连接通用 AI 概念
§10 自测清单
§11 源码精读地图
附录 硬指标 / 常见坑 / 协作
```

### 这套资料的特殊之处

- **面试官视角**：每个机制都配"会被怎么追问"
- **真实代码**：所有代码片段摘自源码（标注 `文件名:行号`），不是伪代码
- **主动暴露取舍**：每个 gotchas 和 critic 深挖点都是"加分回答"——能讲清取舍和已知缺口，比假装完美强得多
- **交叉引用**：连接到知识库里的 [Agent 学习笔记](../agent-books/Agent开发基础.md)理论篇，理论+实战闭环

---

## 两个项目的核心差异（面试对比题）

| 维度 | Manager 总管 | Code Assist |
|------|-------------|-------------|
| **核心矛盾** | 多 Agent 怎么协作不乱 | AI 能写文件怎么不出事 |
| **LangGraph 用法** | 38 节点复杂状态机（条件边谓词） | ReAct 双节点循环（agent⇄tools） |
| **最难的问题** | 路由准不准、自进化安不安全 | read-before-write 怎么强制 |
| **安全重点** | HITL 人工确认 + 写闸（admin/gui） | 四层强制 + 双层沙箱 + 路径白名单 |
| **自进化** | policy/prompt/planner 三类制品 shadow→金丝雀→A/B | prompt shadow→promote A/B（双信号：feedback+validate_fail） |
| **记忆** | 四层分层 + 向量Jaccard混合 + 冲突消解 | 代码RAG + 跨Agent文件总线 |
| **面试一句话** | "让 Agent 自己变聪明还不改坏" | "让 AI 能改仓库还不出事" |

---

## 高频面试场景对照

| 面试官问 | 看这里 |
|---------|--------|
| "讲一个你深度参与的 AI 项目" | 两份 §0 + §1 |
| "Agent 怎么编排多个工具/服务" | Manager §3 + §4.1/4.5 |
| "怎么防止 LLM 乱改代码/出事故" | Code Assist §4.2-4.5（命门） |
| "多轮对话/状态怎么保持" | Manager §4.1(Annotation reducer) + Code Assist §4.10(FileSaver) |
| "Agent 怎么自我优化/进化" | Manager §4.8 + Code Assist §4.9 |
| "怎么做 A/B 实验/灰度" | Manager §4.8(金丝雀) + Code Assist §4.9(分桶) |
| "LangGraph 用过吗，State 怎么定义" | Manager §4.1（reducer 坑） |
| "RAG 怎么做，成本怎么控" | Code Assist §4.7 |
| "怎么保证结果不是 LLM 编的" | Manager §4.6（evidenceGate + critic） |
| "系统怎么防死循环/熔断" | Manager §4.1(retryBudget) + Code Assist §4.10 |

---

## 配套理论笔记

实战前建议先过一遍理论篇，讲的时候能"落地到代码"：

- [ReAct 反思 任务规划](../agent-books/ReAct-反思-任务规划.md) → Code Assist ReAct 双节点
- [Multi-Agent](../agent-books/Multi-Agent.md) → Manager 编排层
- [Tool Calling / Function Call / MCP](../agent-books/Tool-Calling-Function-Call-MCP.md) → 18 工具 + managerTask 协议
- [异常处理 安全 熔断](../agent-books/异常处理-安全-熔断.md) → read-before-write + retryBudget + 沙箱
- [上下文管理与记忆](../agent-books/上下文管理与记忆.md) → 四层记忆 + FileSaver
- [工程化与部署](../agent-books/工程化与部署.md) → A/B 灰度 + 可观测性
- [幻觉与评测](../agent-books/幻觉与评测.md) → evidenceGate + NLU 回归

---

> **最后**：这两份是"会呼吸"的资料——面试前一晚过一遍 §8 的 killer followups，临场能扛住最深挖的追问。祝拿 offer。🎯
