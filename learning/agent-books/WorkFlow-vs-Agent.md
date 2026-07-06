# Workflow vs Agent
# Workflow 和 Agent 有什么区别？
核心区别一句话：Workflow 是"你告诉系统怎么做"，Agent 是"你告诉系统做什么，它自己决定怎么做"。
Anthropic 官方的划分标准：
- Workflow = Orchestration framework + Predefined paths（预定义路径）
- Agent = LLM dynamically directs its own processes and tool usage（LLM 自主控制）
---

# 什么情况下适合用 Workflow，什么情况下适合用 Agent？
适合 Workflow 的场景：
- 业务流程固定且明确，如"客户投诉处理 → 分类 → 分配 → 响应"
- 对可靠性和一致性要求极高（金融、医疗合规场景）
- 需要精确的成本控制和 SLA 保证
- 团队对 AI 能力边界有清晰认知，可以预定义最优路径
- 每个节点的输入输出格式确定
- 需要严格的审计追踪
适合 Agent 的场景：
- 任务需求多样且难以穷举所有路径
- 需要根据中间结果动态调整策略
- 用户的请求本身就是开放式的（如"帮我调研 XX 行业"）
- 需要探索性地使用多种工具
- 对延迟和成本容忍度较高
混合模式（实际项目中最常见）：
- 顶层用 Workflow 做整体编排，保证核心流程可控
- 某些节点内部使用 Agent 处理需要灵活推理的子任务
- 例如：客服系统整体是 Workflow（意图识别→路由→处理→回复），但"处理"节点内部用 Agent 来灵活地查询知识库和生成回答
---

# 如何保证 Workflow 和 Agent 的成功率？
Workflow 成功率保障：
1. 节点级保障：每个节点配备输入校验、输出校验和 fallback 逻辑
2. Prompt 工程：对每个 LLM 调用节点做充分的 Prompt 优化和测试
3. 结构化输出：使用 JSON Schema / Pydantic 等强制输出格式
4. 重试机制：对可恢复的错误进行自动重试（指数退避）
5. 监控告警：每个节点的成功率、延迟、Token 消耗实时监控
6. A/B 测试：通过灰度发布逐步验证新版本
Agent 成功率保障：
1. 约束 Agent 行为空间：限制可用工具集、设置最大迭代次数、限制 Token 预算
2. Guardrails（护栏）：输入过滤 + 输出审核，防止异常行为
3. Few-shot 示例：在 System Prompt 中提供成功执行的范例
4. Self-Check 机制：在关键步骤后加入验证环节
5. Human-in-the-Loop：高风险决策前要求人工确认
6. 可观测性：详细记录每步推理和行动，便于事后分析
7. 评测体系：构建自动化评测集，对 Agent 定期回归测试
8. 模型选择：关键路径使用最强模型（如 Claude Opus / GPT-5），非关键路径使用轻量模型降本
量化指标：任务完成率、端到端延迟 P95、平均推理步数、Token 消耗、异常率。
---

# 智能体模式是模型的自我迭代还是工作流（Workflow）的方式？
这个问题的本质是在问 Agent 的驱动力来源，答案是：两者的有机结合，但以模型的自主推理为核心特征。
模型自我迭代的维度：
- Agent Loop 的核心驱动力是 LLM 的推理能力
- 每次循环中，LLM 根据历史信息和当前状态自主决定下一步
- ReAct、Reflexion 等范式本质上是模型在"自我迭代"中不断改进输出
- 这是 Agent 区别于传统 Workflow 的根本特征
工作流的维度：
- Agent 系统的外部骨架仍然是一个工作流（Agent Loop 本身就是一种特殊的工作流）
- 工具注册、权限控制、错误处理等基础设施是工程化的工作流
- 多 Agent 系统的协作编排也是工作流性质的
正确理解：Agent 不是"纯靠模型自我迭代"也不是"纯 Workflow"，而是在 Workflow 骨架内赋予了模型自主决策的能力。Workflow 提供结构和约束，模型提供智能和灵活性。成熟的 Agent 系统一定是两者的平衡。
---

# 工作流是怎么搭建的？工作流怎么评测的？工作流的项目是怎么部署的？
搭建方式：
1. 代码方式（Code-first）：
    1. LangGraph：将工作流建模为有向图，节点是处理函数，边是状态转移条件
    2. 适合复杂逻辑和需要精细控制的场景
```python
from langgraph.graph import StateGraph
graph = StateGraph(AgentState)
graph.add_node("classifier", classify_intent)
graph.add_node("retriever", retrieve_docs)
graph.add_node("generator", generate_answer)
graph.add_edge("classifier", "retriever")
graph.add_edge("retriever", "generator")
```
1. 低代码方式（Low-code）：
    1. Dify / Coze / n8n / Flowise：拖拽式画布搭建
    2. 适合快速原型和非技术团队
2. 配置驱动方式（Config-driven）：
    1. YAML/JSON 定义工作流结构，代码实现节点逻辑
    2. 适合需要动态修改流程的场景
评测方法：
1. 节点级评测：每个 LLM 节点单独构建 test set，评估准确率、格式一致性
2. 端到端评测：用真实用例跑完整流程，评估最终输出质量
3. 指标体系：
    1. 功能指标：任务完成率、输出质量（人工/自动评分）
    2. 性能指标：延迟 P50/P95/P99、吞吐量
    3. 成本指标：平均 Token 消耗 / 每次调用成本
    4. 稳定性指标：成功率、重试率、异常率
4. 回归测试：每次 Prompt 或流程变更后执行自动化回归
部署架构：
- 中小规模：单体应用 + FastAPI 足够，部署在 Docker 容器中
- 大规模生产：微服务架构
    - 拆分原则：每个 Agent / 核心工作流节点作为独立微服务
    - API Gateway → Agent Orchestrator → 各节点微服务（Classifier Service / Retriever Service / Generator Service）
    - 消息队列（Kafka/RabbitMQ）处理异步任务
    - Redis 做会话状态管理
    - 向量数据库集群做知识检索
    - Kubernetes 做容器编排和自动伸缩
- 推荐实践：从单体开始，当某个节点成为瓶颈时再拆分为微服务（避免过早微服务化带来的运维复杂度）