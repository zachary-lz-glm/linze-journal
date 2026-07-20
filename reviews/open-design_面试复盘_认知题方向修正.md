# open design 面试复盘：认知题方向修正

> 日期：2026-07-20
> 场景：上周面 open design 被挂，面试官 4 个核心问题都是"思路和认知"题。本文复盘失分点 + 回流到 `learning/interview-tools/stealth.html`。

## 1. 背景

面试官明确表示：**不关心细节实现，关注思考、设计过程、对 AI 新趋势新技术的认知。** 4 个核心问题：

1. 你的 agent 现在还在用代码写的状态机，现在已经有 agent 自动流转的状态机，有了解过吗？为什么不用？
2. 你做的这两个 agent 有和市面上类似的竞品对比过吗，为什么要做这个事情？
3. 有了解过 opencode 或者 ohmyopencode 吗？
4. 你的总管 agent 为什么有 39 个节点，代码 agent 为什么有 18 个工具，会不会太多了点，有必要么？

## 2. 诊断：准备方向错位

现有 27 张 Agent 卡（Manager 11 + Code 16）**95% 是"怎么做"实现细节**（主干链路、HITL、Critic、ReAct、18 工具分工、Diff、检索…），而面试官 4 问全是**"为什么这么做 / 趋势认知 / 复杂度判断"**。缺一整个**元认知层**。

这是被挂的主因——不是项目不行，是讲项目的方式没对上考察维度。open design 是设计驱动团队，更看"设计判断力"而非"实现熟练度"。

## 3. 4 问逐个拆解

### Q1 状态机 vs 自动流转
- **考察**：知不知道 LLM Supervisor / Swarm（让模型动态决定下一步）vs 硬编码 graph 的权衡；知不知道 Anthropic《Building effective agents》"workflow 优先于 autonomous"的业界共识；自己项目的权衡。
- **我当时短板**：只会讲"为什么用 LangGraph"（实现层），讲不清"为什么不让 LLM 自己流转"（权衡层）。
- **修正骨架**：两种范式 LangGraph 都支持 → 业界共识 workflow 优先 → 我是混合（确定性步骤钉死、判断交 LLM）→ 反证 Code 就是 ReAct 自主流转 → 诚实边界。
- **回流卡**：Manager 组「为什么用硬编码状态机，不用 LLM 自主流转？」

### Q2 竞品对比 + 为什么要做
- **考察**：多 Agent 竞品认知（AutoGen / CrewAI / MetaGPT / Manus）+ 产品判断力（做这事的动机 / 价值，不是功能对比）。
- **我当时短板**：Code 只有一张功能对比卡（vs Cursor / Aider / Devin），Manager 零竞品；都没答"为什么要做"。
- **修正骨架**：先认竞品强 → 动机三件事（单仓缺编排入口 / 搞清怎么上生产 / 验证范式）→ 差异化（安全 / 可观测 / 自进化非劣性 / Probe 在 plan 前）→ 诚实（研究型、ROI 是认知不是用户量）。
- **回流卡**：Manager 组「和市面多 Agent 竞品比，为什么要做这个总管？」（Code 侧用现有「vs Cursor / Aider / Devin」+ 新「opencode」卡）。

### Q3 opencode / ohmyopencode
- **考察**：对开源 AI coding 生态的认知。
- **我当时短板**：完全没准备，零认知。
- **修正骨架**：opencode = SST / Anomaly 开源 terminal coding agent（75+ 模型、不锁 vendor、可自托管，类 Claude Code / Aider 开源版）；ohmyopencode = 社区配置生态（opencode-config-tool 等，类比 oh-my-zsh）；和我 Code Agent 同类，它赢通用生态、我赢企业 Safety 受控；诚实说了解定位没深度用过。
- **回流卡**：Code 组「了解 opencode / ohmyopencode 吗？」

### Q4 39 节点 / 18 工具是不是太多
- **考察**：复杂度合理性、YAGNI、过度设计判断——open design（设计驱动团队）最在意的**设计判断力**。
- **我当时短板**：没一张卡正面答"会不会过度设计"。
- **修正骨架**：39 是长出来的（演进路径，每节点挡一个坑）→ 诚实认部分 over-engineered（三套自适应路由）→ 关键认知（无解释的复杂度才是问题）→ 生产化先做减法，但真正要补的是 Postgres saver / OTel / golden 扩量。18 工具同理（11 只读 + 7 写，意图路由收敛工具数，单次远少于 18）。
- **回流卡**：Manager 组「39 个节点是不是过度设计了？」+ Code 组「18 个工具是不是太多了？」

## 4. 元方法论：怎么准备认知 / 趋势题

不是背实现细节，是建**"为什么这么做"的判断链**，三层：

1. **知道业界有哪些范式 / 竞品**——能脱口而出 5 个同类：
   - 路由范式：LLM Supervisor / Swarm vs 硬编码状态机
   - 多 Agent 框架：AutoGen / CrewAI / MetaGPT / Manus / LangGraph Supervisor
   - coding agent：Cursor / Aider / Devin / opencode / OpenHands / Cline
2. **知道自己选了什么、为什么**——有自己的判断，不是随大流：
   - 混合架构（确定性钉死、判断交 LLM）、安全第一、Probe 在 plan 前
3. **知道代价和诚实边界**——主动暴露取舍比假装完美强：
   - 硬编码不够灵活、三套路由可能 over-engineered、没接真实流量、模型是 qwen 不是 Claude

**实现细节**（39 节点怎么连、18 工具怎么分）只在被追问"怎么做的"时才展开，**开场和主干要讲"为什么"**。

## 5. 回流清单（已加到 stealth.html，2026-07-20）

**Manager 组（+3）**：
- 为什么用硬编码状态机，不用 LLM 自主流转？
- 和市面多 Agent 竞品比，为什么要做这个总管？
- 39 个节点是不是过度设计了？

**Code 组（+2）**：
- 了解 opencode / ohmyopencode 吗？
- 18 个工具是不是太多了？

## 6. 下次认知层自测 checklist（进场前过一遍）

- [ ] 状态机 vs 自主流转的权衡能讲清吗？（两种范式 + 业界共识 + 我的混合 + Code 反证）
- [ ] 多 Agent 竞品能脱口而出 5 个吗？（AutoGen / CrewAI / MetaGPT / Manus / LangGraph Supervisor）
- [ ] coding agent 开源生态知道吗？（opencode / ohmyopencode / Aider / OpenHands / Cline）
- [ ] 复杂度能讲每个节点 / 工具的必要性吗？能主动认过度设计吗？
- [ ] 诚实边界主动说吗？（研究型 / 没接流量 / 模型是 qwen 不是 Claude）
- [ ] 模型栈真相记得吗？（研发 Claude、部署 qwen）
- [ ] "为什么要做"能讲动机和价值判断吗？（不是功能对比）
