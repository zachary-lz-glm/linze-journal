# Agent开发基础
![图片](https://docimg4.docs.qq.com/image/AgAAMBOerw0qP0U3ztlNlaEUeNmp9Cwf.png?w=1254&h=1192)
# 你对 Agent 了解多少呢？
Agent（智能体）是一种能够感知环境、自主决策、执行行动的 AI 系统。与传统的"一问一答"式 LLM 调用不同，Agent 具备以下核心能力：
本质定义：Agent = LLM（大脑） + 感知（Perception） + 记忆（Memory） + 规划（Planning） + 工具使用（Tool Use） + 行动（Action）。Agent 以目标为导向，可以在无人干预的情况下，自主拆解任务、选择工具、执行操作、观察结果并迭代优化，直到任务完成。
学术渊源：Agent 的概念最早可追溯到人工智能的 BDI（Belief-Desire-Intention）架构。2023 年以来，随着 GPT-4 等大模型能力的提升，基于 LLM 的 Agent 成为热门研究方向。标志性工作包括 AutoGPT（2023）、BabyAGI（2023）、ReAct 论文（Yao et al., 2022）以及 Generative Agents（斯坦福小镇，2023）。
产业现状：根据 LangChain 2025 年底的调研，超过 57% 的组织已有 Agent 在生产环境中运行。Gartner 预测，到 2028 年 33% 的企业软件将嵌入 Agentic AI 能力。这个领域正从"能不能做"转向"如何规模化、可靠地部署"。
大厂面试追问角度：面试官可能追问"你在实际项目中如何落地 Agent"，回答要点：选择合适的框架（如 LangGraph）、设计稳健的 Agent Loop、关注 Error Recovery、成本控制和可观测性。
---

# Agent 和 LLM（大型语言模型）有什么区别？
这是一个核心概念辨析题，需要从多个维度清晰区分：
一句话总结：LLM 是 Agent 的"大脑"，但 Agent 还需要"眼睛"（感知）、"手脚"（工具）、"记忆"和"思考方法"（推理策略）才构成完整的智能体。就像人的大脑很重要，但仅有大脑不足以完成任何实际任务。
面试加分点：可以类比操作系统 — LLM 相当于 CPU，Agent 相当于整个操作系统，包含了进程调度（规划）、内存管理（记忆）、I/O 设备（工具）和文件系统（持久化存储）。
---

# 一个完整的 Agent 智能体架构一般包括哪些部分？
学术界和工业界对 Agent 架构有高度一致的共识，核心组件包括：
（1）Profile / 角色定义
- System Prompt 定义 Agent 的身份、能力边界、行为约束
- 例如："你是一个高级数据分析师，擅长 SQL 查询和数据可视化"
（2）Planning / 规划模块
- 任务分解（Task Decomposition）：将复杂目标拆解为可执行的子任务
- 策略选择：决定执行顺序和方法
- 典型范式：CoT（Chain-of-Thought）、ReAct、Plan-and-Solve、Tree-of-Thought
（3）Memory / 记忆系统
- 短期记忆（Short-term Memory）：当前对话的上下文窗口
- 长期记忆（Long-term Memory）：通过向量数据库、KV 存储等持久化历史信息
- 工作记忆（Working Memory）：Agent 当前推理链中的中间状态
（4）Tools / 工具集
- 搜索引擎、代码解释器、API 调用、数据库查询、文件操作等
- 通过 Function Calling / Tool Use 协议与 LLM 集成
- MCP（Model Context Protocol）是 2025 年兴起的工具标准化协议
（5）Action / 行动执行器
- 将 LLM 的决策转化为实际操作
- 包括工具调用的执行、结果的收集和格式化
（6）Observation / 感知与反馈
- 收集行动执行的结果
- 将外部环境的反馈注入到下一轮推理中
（7）Orchestration / 编排层
- Agent Loop 的核心控制逻辑
- 状态管理、错误处理、退出条件判断、超时控制
这七个组件共同构成了一个完整的 Agent 系统。在工程实践中，还需要加上**可观测性（Observability）**层用于监控和调试、**安全护栏（Guardrails）**层用于防止异常行为。
---

# Agent 的工作模式都有什么？
这是对 Agent 推理-执行范式的考察，主流工作模式包括：
（1）ToolsCallingAgent（工具调用型）
- 最基础的模式，LLM 根据用户请求直接选择并调用工具
- 流程：用户输入 → LLM 决定调用哪个工具 → 执行工具 → 返回结果
- 适用场景：简单的单步任务，如天气查询、翻译
- 代表实现：OpenAI Function Calling
（2）ReActAgent（推理-行动型）
- 来自 Yao et al., 2022 论文，核心是 Thought → Action → Observation 的循环
- LLM 先"思考"（生成推理链），再"行动"（调用工具），然后"观察"（分析结果），循环直至得出最终答案
- 优点：可解释性强，可追踪推理过程，自我纠错能力较好
- 缺点：每轮推理需要额外的模型调用，延迟和成本较高；错误可能在循环中传播
- 适用场景：复杂的多步推理任务，需要动态适应的场景
（3）ReflectionAgent（反思型）
- 在 ReAct 基础上增加了自我评估层
- Agent 生成初始响应后，切换到"批评者"模式，检查准确性、逻辑一致性
- 如果发现问题，自动修正并重新生成
- 典型实现：Reflexion 框架
- 适用场景：对准确性要求极高的场景，如代码生成、学术写作
（4）PlanAndSolveAgent（规划-执行型）
- 先制定全局计划，再逐步执行
- 流程：用户输入 → Planner 生成步骤列表 → Executor 依次执行每个步骤 → 汇总结果
- 优点：对复杂任务有更好的全局视野，不容易陷入局部循环
- 缺点：计划一旦确定，灵活性不足；重新规划成本高
- 适用场景：步骤明确的多步任务，如数据分析、报告生成
（5）Multi-Agent（多智能体协作型）
- 多个专业化 Agent 协作完成复杂任务
- 模式包括：层级式（一个 Orchestrator + 多个 Worker）、对话式（Agent 之间互相交流）、竞争式（多个方案择优）
- 代表框架：CrewAI、AutoGen、MetaGPT
- 适用场景：软件开发（PM → 架构师 → 开发 → 测试）、复杂研究
（6）Human-in-the-Loop（人机协作型）
- 在关键节点暂停执行，等待人类审核、批准或提供输入
- 适用场景：高风险决策（金融交易、法律文书）、需要人类判断的创意任务
选择建议：从简单模式开始，按需增加复杂度。单 Agent + ReAct 能解决大部分真实场景，不要过早引入多 Agent。
---

# 了解过 Agent 的设计范式吗？了解其他的 Agent 范式吗？
Agent 设计范式是更高层次的架构方法论，目前业界公认的七大设计范式：
① ReAct 范式（推理+行动）
- 交替进行推理和行动，是最基础也最重要的单 Agent 模式
- 推荐作为复杂任务的默认起点
② Reflection 范式（自我反思）
- Agent 输出后进行自我评估，发现错误后迭代改进
- 实现方式：Critic Agent 审查 Actor Agent 的输出
③ Tool Use 范式（工具使用）
- Agent 作为工具编排器，智能选择和组合外部工具
- 关键挑战：工具描述的清晰度直接影响 Agent 的工具选择准确性
④ Planning 范式（规划先行）
- 先生成执行计划，再按计划执行
- 变体：Plan-and-Solve、LATS（Language Agent Tree Search）、AdaPlanner（自适应规划）
⑤ Multi-Agent Collaboration 范式（多智能体协作）
- 多个专业化 Agent 分工合作
- 子模式：Sequential（串行管道）、Parallel（并行执行）、Hierarchical（层级调度）
⑥ Sequential Workflow 范式（流水线工作流）
- 预定义的步骤序列，每步处理结果传递给下一步
- 确定性强，适合业务流程固定的场景
⑦ Human-in-the-Loop 范式（人机协同）
- 人类作为 Agent 系统的一部分参与决策
- 适合高风险、需要合规审核的场景
其他前沿范式：
- LATS（Language Agent Tree Search）：结合蒙特卡洛树搜索进行探索式规划
- Voyager：在 Minecraft 中实现自主探索和技能积累的终身学习 Agent
- Generative Agents：斯坦福小镇，模拟人类社会行为的 Agent 架构
- Self-Discover：让 LLM 自主发现并组合推理策略
- RAISE：结合了记忆检索和反思的综合框架
---

# Agent 推理模式、推理模式的差异化设计、推理模式的选择机制
主流推理模式对比：
差异化设计要点：
1. 推理深度：Direct < CoT < ReAct < Plan-and-Solve < ToT
2. 工具依赖：Direct/CoT 不需要工具，ReAct 强依赖工具，Plan-and-Solve 适度依赖
3. 计算开销：与推理深度正相关，需要权衡效果与成本
4. 容错机制：ReAct 通过观察修正，Reflexion 通过显式自我批评修正
选择机制（决策树）：
- 任务是否需要外部信息？否 → CoT / Direct；是 → 进入下一判断
- 任务步骤是否明确？是 → Plan-and-Solve；否 → 进入下一判断
- 任务是否需要动态适应？是 → ReAct；否 → 进入下一判断
- 任务是否对准确性有极高要求？是 → Reflexion / ToT
- 实际项目中通常采用混合模式：用 Plan-and-Solve 做全局规划，每个子任务内部用 ReAct 执行
---

# 了解过市面上有哪些智能体 Agent 吗？
可以从框架层和产品层两个维度回答：
开发框架层：
- LangChain / LangGraph：最广泛采用的 Agent 框架，LangGraph 提供图状态编排，支持复杂的有状态工作流
- CrewAI：基于角色的多 Agent 协作框架，超过 10 万开发者通过社区课程获得认证
- AutoGen / Microsoft Agent Framework：微软将 AutoGen 和 Semantic Kernel 合并为统一的 Agent Framework，1.0 GA 版本目标 2026 Q1 发布
- LlamaIndex：专注于 RAG 和知识密集型 Agent 工作流
- SmolAgents（HuggingFace）：轻量级 Agent 框架，核心逻辑约 1000 行代码
- MetaGPT：模拟软件开发团队的多 Agent 系统
- Dify / Coze：低代码 Agent 搭建平台
产品层：
- Claude Code：Anthropic 的命令行 Agent 编码工具
- ChatGPT with Plugins / GPTs：OpenAI 的消费级 Agent
- GitHub Copilot：代码 Agent，超 80% BNY Mellon 开发者日常使用
- Cursor / Windsurf：AI 编码 IDE，集成 Agent 式交互
- Devin：Cognition 的自主软件工程 Agent
- Manus：2025 年爆火的通用 Agent 产品
- Perplexity：搜索型 Agent
- AutoGPT / AgentGPT：早期的自主 Agent 先驱
---

# Agent Loop 听说过吗？
Agent Loop 是 Agent 系统的核心执行循环，也叫 Agent 主循环或控制循环。它是 Agent "自主性"的实现机制。
基本结构：
```plaintext
while not done:
    1. 感知（Perceive）：获取当前状态、用户输入、环境反馈
    2. 思考（Think）：LLM 推理，决定下一步行动
    3. 行动（Act）：执行工具调用、生成内容等
    4. 观察（Observe）：收集行动结果
    5. 判断（Evaluate）：任务是否完成？是否需要继续？
```
关键设计要素：
1. 退出条件：
    1. 模型判断任务完成（生成 Final Answer）
    2. 达到最大迭代次数（防止无限循环）
    3. 超时机制（总执行时间限制）
    4. 重复行动检测（连续相同工具调用说明陷入死循环）
2. 状态管理：每次循环需要维护并更新 Agent 的内部状态，包括已执行的步骤、收集的信息、中间结果
3. 错误恢复：工具调用失败时需要有 fallback 机制，如重试、换工具、降级处理
4. 成本控制：每次循环都消耗 Token，需要监控和限制总消耗
以 Claude Code 为例：每次用户输入后，Agent Loop 会持续运行，读取文件、修改代码、执行命令、观察结果、再做判断，直到认为任务完成或达到限制。
面试追问：如果面试官问"如何防止 Agent Loop 死循环"，要回答：设置 max_iterations、检测工具调用重复模式、设置总 Token 预算、加入 timeout 机制、在循环中注入"如果连续 3 次没有进展则总结当前状态并退出"的指令。
---

# 你认为当前 Agent 技术难以突破的核心瓶颈有哪些？
这是一道考察技术深度和行业洞察的开放题，需要从多个层面回答：
① 可靠性瓶颈（Reliability）
- Agent 的错误会级联传播：ReAct 循环中某一步的错误会影响后续所有步骤
- LLM 的幻觉问题在 Agent 场景中被放大：幻觉可能导致错误的工具调用，产生不可预知的后果
- 行业数据：LangChain 调研中 32% 的受访者将"质量"列为 Agent 投产的最大障碍
② 规划能力不足（Planning）
- 当前 LLM 的规划能力仍然有限，面对复杂任务容易制定次优甚至错误的计划
- 长链任务中容易"迷失"，忘记最初目标
- 自我纠错能力有限，经常在错误方向上"执着"
③ 成本与延迟（Cost & Latency）
- Agent 的多轮交互导致 Token 消耗量远超单次调用，成本非线性增长
- 每增加一个推理步骤就增加一次 LLM 调用，延迟累积
- 编码 Agent 单次会话可能涉及 50-100 次 API 调用
④ 长上下文退化（Context Rot）
- 即使模型支持百万级 Token 窗口，实际性能随上下文增长显著下降
- "Lost in the Middle" 现象：模型对上下文中间位置的信息召回率明显低于首尾
- Chroma 的研究表明，大多数模型在达到标称上下文长度之前就开始不可靠
⑤ 安全与可控性（Safety & Control）
- Agent 具有执行外部操作的能力（删除文件、发送请求等），风险远高于纯文本生成
- Prompt Injection 攻击在 Agent 场景更危险
- 缺乏成熟的权限控制和审计机制
⑥ 评测标准缺失（Evaluation）
- 缺乏统一的 Agent 能力评测基准
- 传统的 NLP 评测指标不适用于 Agent 的动态交互场景
- LangChain 调研显示只有 52% 的组织实施了 Agent 评测
⑦ 可观测性不足（Observability）
- Agent 的多步执行过程难以追踪和调试
- 故障定位困难：不清楚是 LLM 推理错误还是工具返回错误还是上下文污染
- 好消息是 89% 的组织已实施某种形式的 Agent 可观测性
---

# 近半年一年大模型领域有哪些让你印象深刻的技术或产品进展？
模型能力跃进：
- Claude Opus 4.6：Anthropic 最新旗舰，1M 上下文窗口且性能不衰减，在多项基准中排名前列
- GPT-5 系列：400K 上下文窗口，128K 最大输出，幻觉率降低 80%
- Gemini 3.1 Pro：在智能指数排行中与 GPT-5.4 并列第一
- DeepSeek V3/R1：开源模型表现惊艳，MoE 架构 + RL 训练，数学和编码性能优秀
- Llama 4 Scout：10M Token 上下文窗口，开源界最大
Agent 基础设施成熟：
- MCP（Model Context Protocol）：Anthropic 推出的工具标准化协议，成为行业标准
- Microsoft Agent Framework：AutoGen + Semantic Kernel 合并，企业级 Agent 开发统一
- LangGraph 成为主流：图状态编排成为复杂 Agent 工作流的事实标准
产品创新：
- Claude Code：命令行 Agent 编码，新增语音控制功能
- Cursor / Windsurf：AI 编码 IDE 大爆发，Memory Bank 机制提升跨会话连续性
- Manus：通用 Agent 产品引爆市场讨论
- Deep Research：多个平台推出的深度研究 Agent 功能
行业数据：
- NVIDIA 2026 报告显示 64% 的组织在生产环境部署 AI，88% 看到收入增长
- Agentic AI 市场规模从 2024 年的 54 亿美元增长到 2025 年的 78 亿美元
---

# 你常用哪些大模型相关的工具/框架？
从一个大厂 AI 架构师的角度，按类别回答：
模型调用层：
- OpenAI API / Anthropic API / Google Vertex AI — 主力模型接口
- vLLM / TGI — 开源模型推理部署
- Ollama — 本地模型快速试验
Agent 开发框架：
- LangChain + LangGraph — 复杂 Agent 工作流的主力选择
- CrewAI — 多 Agent 协作快速原型
- LlamaIndex — RAG 和知识密集型 Agent
Prompt 工程与评测：
- LangSmith — Agent 可观测性和评测平台
- PromptFoo — Prompt 评测自动化
- Weights & Biases — 实验追踪
向量数据库：
- Qdrant / Milvus / Pinecone — 长期记忆存储
- Chroma — 轻量级嵌入和检索
部署与运维：
- Docker + Kubernetes — 容器化部署
- FastAPI — Agent 服务化
- Redis — 会话状态管理和缓存
编码工具：
- Claude Code / Cursor — 日常 AI 辅助编码
- GitHub Copilot — 代码补全