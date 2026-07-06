# Multi-Agent
# 聊一下 Multi-Agent，你是怎么做意图识别的？
Multi-Agent 系统概述：
Multi-Agent 系统通过多个专业化 Agent 的协作来解决复杂问题。核心挑战之一就是意图识别——准确理解用户意图并路由到正确的 Agent。
意图识别的实现方式：
方案一：LLM Router（主流方案）
```python
ROUTER_PROMPT = """你是一个意图路由器。根据用户输入，判断应该由哪个 Agent 处理。

可用 Agent：
1. code_agent: 处理代码编写、调试、代码审查相关任务
2. data_agent: 处理数据分析、可视化、报表生成相关任务
3. research_agent: 处理信息检索、调研、资料整理相关任务
4. writing_agent: 处理文案撰写、文档编辑、翻译相关任务

输出 JSON: {"agent": "agent_name", "confidence": 0.0-1.0, "reasoning": "..."}
"""

def route(user_input):
    result = llm.call(ROUTER_PROMPT + f"\n\n用户输入：{user_input}")
    routing = json.loads(result)
    if routing["confidence"] < 0.7:
        return fallback_agent  # 低置信度走兜底
    return get_agent(routing["agent"])
```
方案二：嵌入相似度 + 分类器（低延迟方案）
```plaintext
# 预处理：为每个 Agent 的能力描述生成嵌入
agent_embeddings = {
    "code_agent": embed("代码编写 调试 审查 编程 bug修复"),
    "data_agent": embed("数据分析 可视化 图表 报表 统计"),
    # ...
}

# 运行时
user_embedding = embed(user_input)
scores = {name: cosine_similarity(user_embedding, emb) 
          for name, emb in agent_embeddings.items()}
best_agent = max(scores, key=scores.get)
```
方案三：关键词 + 规则引擎（确定性方案）
- 适合领域明确、意图有限的场景
- 正则匹配 + 关键词词典 + 规则优先级
- 优点：零延迟、100% 可预测
实际项目推荐：规则兜底 + LLM Router 组合。先用规则匹配高确定性意图，匹配不上再走 LLM Router。
---
# 怎么提升意图识别的准确率？
系统化提升方案：
（1）Prompt 优化
- 为每个 Agent 编写清晰的能力描述，特别是区分容易混淆的 Agent
- 在 Router Prompt 中加入 Few-shot 示例，覆盖易混淆案例
- 加入"思考过程"要求（CoT），让模型先分析再决策
（2）上下文增强
- 不只看当前消息，还看最近 N 轮对话上下文
- 用户画像信息辅助判断（如用户是开发者 → 代码类意图权重提高）
（3）多级路由
```plaintext
Level 1: 粗分类（5大类）→ 准确率 95%+
Level 2: 细分类（20小类）→ 准确率 90%+
Level 3: Agent 内部再确认 → 不匹配时反馈给 Router
```
（4）反馈闭环
- 路由错误时，用户反馈"不对"→ 记录错误案例
- 用错误案例更新 Router 的 Few-shot 示例
- 定期分析错误模式，优化 Agent 能力描述
（5）置信度阈值 + Fallback
- 设置置信度阈值（如 0.7）
- 低于阈值时：向用户确认意图 / 走通用 Agent / 多 Agent 并行处理后择优
（6）Ensemble 方法
- 用多个模型/方法分别做意图识别
- 投票或加权融合最终结果
- 如：规则引擎 + 轻量分类器 + LLM Router 三票择优
量化指标：意图识别准确率、Top-3 召回率、平均路由延迟、用户纠正率。
---
# 了解目前主流的 MultiAgent 框架吗？如果将你的心理咨询 Agent 拆分，你认为状态同步的难点在哪？
主流 Multi-Agent 框架：
心理咨询 Agent 拆分示例：
```plaintext
├── 接待 Agent：初始评估、情绪识别、风险筛查
├── 倾听 Agent：共情回应、情感支持、非指导性对话
├── CBT Agent：认知行为疗法技术引导
├── 危机干预 Agent：自杀/自伤风险应对
└── 总结 Agent：会话总结、建议生成、后续计划
```
状态同步的核心难点：
（1）情绪状态的连续性
- 用户的情绪状态是一个连续变化的过程
- 从"接待 Agent"切换到"倾听 Agent"时，情绪状态必须无缝传递
- 如果丢失了"用户在前一段提到了离世的亲人导致情绪波动"这个状态，后续 Agent 的回应会显得突兀
（2）信任关系的建立不可分割
- 心理咨询中的信任关系（therapeutic alliance）是渐进建立的
- 切换 Agent 可能让用户感受到风格变化，破坏信任感
- 解决：统一人格/语气配置，所有 Agent 共享同一个"人格层"
（3）敏感信息的安全传递
- 用户可能透露创伤经历、自杀想法等高度敏感信息
- Agent 间传递这些信息需要严格的安全控制
- 不能将原始敏感内容写入日志或外部存储
（4）实时性要求
- 危机信号（如用户提到自杀）必须被立即识别并切换到危机干预 Agent
- 状态同步的延迟必须极低（毫秒级）
解决方案：
- 使用共享的 State Graph（如 LangGraph 的 State），所有 Agent 读写同一个状态
- 状态中包含：emotion_state、risk_level、disclosed_topics、therapeutic_goals
- 状态更新是原子操作，保证一致性
---
# 多 Agent 怎么实现，之间如何完成通信？怎么协作？
实现方式：
（1）共享状态图（Shared State Graph）— 推荐
```python
# LangGraph 实现
from langgraph.graph import StateGraph

class TeamState(TypedDict):
    task: str
    plan: list
    research_results: str
    draft: str
    review: str
    final_output: str

graph = StateGraph(TeamState)
graph.add_node("planner", planner_agent)
graph.add_node("researcher", researcher_agent)
graph.add_node("writer", writer_agent)
graph.add_node("reviewer", reviewer_agent)

graph.add_edge("planner", "researcher")
graph.add_edge("researcher", "writer")
graph.add_edge("writer", "reviewer")
graph.add_conditional_edges("reviewer", 
    lambda state: "writer" if state["review"] == "needs_revision" else END)
```
（2）消息传递（Message Passing）
```python
# Agent 之间通过消息队列通信
class AgentMessage:
    sender: str
    receiver: str
    content: str
    metadata: dict

# 使用事件总线
event_bus.publish(AgentMessage(
    sender="researcher",
    receiver="writer",
    content="调研完成，以下是关键发现...",
    metadata={"task_id": "123"}
))
```
（3）黑板模式（Blackboard Pattern）
- 共享的"黑板"数据结构，所有 Agent 可读可写
- 适合需要多个 Agent 对同一问题贡献信息的场景
协作模式：
- 串行管道：Agent A → Agent B → Agent C，适合流水线式任务
- 并行执行：多个 Agent 同时处理不同子任务，结果汇总
- 层级调度：Orchestrator Agent 负责分配和协调
- 辩论/评审：多个 Agent 对同一问题给出不同方案，由评审 Agent 择优
- 投票共识：多个 Agent 投票决定最终方案
---
# 多 Agent 执行策略的智能选择和切换机制设计
核心思路：根据任务特征动态选择最优的执行策略。
```python
class StrategySelector:
    def select_strategy(self, task):
        complexity = self.assess_complexity(task)
        time_sensitivity = self.assess_urgency(task)
        subtask_dependency = self.analyze_dependencies(task)
        
        if complexity == "low" and len(task.subtasks) <= 2:
            return SingleAgentStrategy()  # 简单任务单 Agent 处理
        
        elif subtask_dependency == "independent":
            return ParallelStrategy()  # 子任务独立→并行执行
        
        elif subtask_dependency == "sequential":
            return PipelineStrategy()  # 子任务有顺序→流水线
        
        elif complexity == "high" and time_sensitivity == "low":
            return DebateStrategy()  # 复杂+不紧急→多Agent辩论
        
        else:
            return HierarchicalStrategy()  # 默认层级调度
```
切换机制：
- 运行中检测到某个策略效果不佳（如单 Agent 处理超时），自动切换到多 Agent 并行
- 错误率超过阈值时，从自动模式切换到 Human-in-the-Loop 模式
- 基于历史任务数据训练策略选择模型，持续优化
---
# 对 Manus 技术特点的理解及其多智能体方案的判断依据
Manus 技术特点：
Manus 是 2025 年 3 月由中国公司 Butterfly Effect（Monica）发布的首个通用自主 Agent 平台，后被 Meta 收购。
核心技术架构：
1. 三层 Agent 架构：Planner（规划）+ Executor（执行）+ Verifier（验证）
2. 多模型混合：集成 Claude、Qwen 微调版本等多个 LLM，根据任务类型选择最优模型
3. CodeAct 范式：Agent 的"行动"是生成并执行 Python 代码，而非固定格式的 tool_call。灵活性极高，可以在一段代码中组合多个工具。
4. 云端沙箱执行：每个任务在独立的云端虚拟机中执行，异步处理，用户可以离线等待
5. Wide Research：多个通用 Agent 实例并行工作，不是角色分工模式，而是"同质化并行"
多智能体方案的判断依据：
- 任务本身涉及多个独立子领域（如旅行规划 = 机票+酒店+行程+预算）→ 需要多 Agent
- 任务需要规划-执行-验证的完整流程 → 需要多 Agent（至少 3 个角色）
- 单 Agent 的上下文窗口不足以承载所有信息 → 拆分 Agent 各持部分上下文
- 需要提高可靠性（验证 Agent 检查执行 Agent 的输出）→ 多 Agent 互检
Manus 的局限（面试中可以提到以示客观）：
- 幻觉问题仍然存在
- 复杂任务可能运行数小时
- 成本较高（密集调用多个大模型 API）
- 实际评测中有些任务（如实时预订）仍然失败率较高
---
# 语义路由怎么实现，怎么评估语义路由的效果？
语义路由实现：
```python
class SemanticRouter:
    def __init__(self, routes):
        """
        routes: [{"name": "billing", "descriptions": ["账单", "费用", "收费", "付款"],
                  "handler": billing_agent}, ...]
        """
        self.routes = routes
        # 为每个路由生成嵌入向量
        for route in self.routes:
            texts = [route["name"]] + route["descriptions"]
            route["embedding"] = embed_model.encode(texts)  # 多文本取均值
    
    def route(self, query):
        query_embedding = embed_model.encode(query)
        scores = []
        for route in self.routes:
            score = cosine_similarity(query_embedding, route["embedding"])
            scores.append((route["name"], score, route["handler"]))
        
        scores.sort(key=lambda x: x[1], reverse=True)
        best_match = scores[0]
        
        if best_match[1] < 0.6:  # 低置信度阈值
            return self.fallback_handler
        return best_match[2]
```
评估方法：
1. 离线评估：
    1. 构建标注数据集：{query, expected_route} × N 条
    2. 指标：准确率、Top-3 召回率、混淆矩阵
    3. 重点关注相似意图的区分度（如"退款"应路由到"billing"而非"support"）
2. 在线评估：
    1. 用户纠正率：用户说"不对"后重新路由的比例
    2. 路由后的任务完成率：正确路由 → 任务完成率高
    3. 平均路由延迟
3. A/B 测试：
    1. 对比不同路由策略（语义路由 vs 规则路由 vs LLM 路由）
    2. 观察端到端任务完成率和用户满意度
---
# Skill 和 Agent 的关系，为什么不用 Skill 而用子 Agent？
关系：Skill 是 Agent 的能力单元，Agent 可以拥有多个 Skill。Skill 是"技能"，Agent 是"角色"。
为什么某些场景需要子 Agent 而非 Skill？
选择子 Agent 的判断标准：
- 子任务需要大量独立上下文（如分析一份长文档）→ 子 Agent
- 子任务需要不同的工具集或不同的模型 → 子 Agent
- 多个子任务可以并行执行 → 子 Agent
- 子任务的失败不应影响主流程 → 子 Agent（错误隔离）
- 子任务简单、不需要独立上下文 → Skill 即可
---