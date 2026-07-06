# ReAct / 反思 / 任务规划
# ReAct / 反思 / 任务规划
# 你设计的 Agent 是怎么实现 ReAct 模式的？
实现架构：
```python
class ReActAgent:
    def __init__(self, llm, tools, max_iterations=10):
        self.llm = llm
        self.tools = {t.name: t for t in tools}
        self.max_iterations = max_iterations
    
    def run(self, query):
        messages = [{"role": "system", "content": self.system_prompt}]
        messages.append({"role": "user", "content": query})
        
        for i in range(self.max_iterations):
            # 1. Think - LLM 推理
            response = self.llm.call(messages, tools=list(self.tools.values()))
            
            # 2. 检查是否为最终回答
            if not response.tool_calls:
                return response.content  # 最终答案
            
            # 3. Act - 执行工具
            messages.append(response.message)  # 记录 assistant 的 tool_call
            
            for tool_call in response.tool_calls:
                try:
                    result = self.tools[tool_call.name].execute(tool_call.args)
                except Exception as e:
                    result = f"工具执行失败: {str(e)}"
                
                # 4. Observe - 注入观察结果
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(result)
                })
        
        return "达到最大迭代次数，以下是目前收集的信息：..." + self._summarize(messages)
```
关键设计决策：
- System Prompt 中的 ReAct 指令：明确要求模型先思考（Thought），再决定行动（Action），观察结果后再思考
- 工具描述质量：每个工具的 description 是 Agent 准确选择的关键
- 错误恢复：工具失败时不终止，而是将错误信息返回给模型，让模型自行决定换工具或换策略
- 循环退出：除最大迭代次数外，还可以检测连续相同工具调用（死循环检测）
---
# 什么是 Agent 的反思机制？
反思机制（Reflection） 是让 Agent 在生成输出后进行自我审视和改进的能力。
实现方式：
```python
# 两阶段反思
def generate_with_reflection(query, context):
    # 阶段一：生成初始回答
    initial_response = llm.call(f"请回答：{query}", context=context)
    
    # 阶段二：反思审查
    reflection = llm.call(f"""
    请审查以下回答的质量：
    
    用户问题：{query}
    初始回答：{initial_response}
    
    检查维度：
    1. 事实准确性：回答中是否有明显错误？
    2. 完整性：是否遗漏了重要信息？
    3. 语气适当性：语气是否专业、温和、得体？
    4. 逻辑一致性：回答是否自相矛盾？
    
    如果发现问题，请输出改进后的版本。
    如果没有问题，输出"APPROVED"。
    """)
    
    if "APPROVED" in reflection:
        return initial_response
    else:
        return reflection  # 改进后的版本
```
心理咨询 Agent 中的语气检查：
```python
TONE_CHECK_PROMPT = """
你是心理咨询质控专家。请审查以下回复是否符合专业标准：

回复内容：{response}

检查要点：
1. 是否使用了共情性语言（如"我理解你的感受"）？
2. 是否避免了评判性词汇（如"你不应该"、"你错了"）？
3. 是否保持了温暖但专业的距离？
4. 是否避免了给出简单化的建议（如"想开点"）？
5. 是否注意到了潜在的危险信号需要进一步追问？

输出：{"passed": true/false, "issues": [...], "revised_response": "..."}
"""
```
---
# 为什么要用 Planning & Solve 架构？还了解什么架构？ReAct 和 Reflection 架构有什么差别？
为什么用 Plan-and-Solve：
当任务复杂度高、涉及多个步骤且步骤间有依赖关系时，Plan-and-Solve 优于 ReAct。原因是：ReAct 是"走一步看一步"，可能在执行过程中偏离最优路径；Plan-and-Solve 先制定全局计划，确保整体方向正确。
三大架构对比：
其他重要架构：
- LATS（Language Agent Tree Search）：树搜索 + ReAct，探索多条推理路径
- Self-Discover：LLM 自动选择和组合推理策略
- AdaPlanner：自适应规划，执行中动态调整计划
- Voyager：终身学习 Agent，积累可复用技能
---
# 关于 ReAct 的知识，那几个模式有什么差别？
ReAct 及其变体模式对比：
① 标准 ReAct：Thought → Action → Observation，线性循环
- 适合：大多数需要工具的任务
- 弱点：可能在错误方向上持续推进
② ReAct + Reflection：在 ReAct 循环中加入反思步骤
- Thought → Action → Observation → Reflection → 继续或修正
- 适合：需要高准确度的场景
③ ReAct + Planning：先生成计划，再在每步中用 ReAct 执行
- Plan → (Thought → Action → Observation) × N → 检查计划进度
- 适合：复杂的多步骤任务
④ ReWOO（Reasoning Without Observation）：先生成所有推理和工具调用计划，一次性批量执行所有工具，最后统一推理
- 减少了 LLM 调用次数（从 N 次减到 2 次）
- 适合：工具调用之间没有依赖关系的场景
⑤ Multi-Agent ReAct：多个 ReAct Agent 并行工作，各自有独立的循环
- 适合：可并行化的子任务
---
# 任务分解后，会根据任务执行结果调整任务列表吗？
是的，好的 Agent 必须支持动态调整计划。 这是 AdaPlanner（自适应规划）的核心思想。
```python
class AdaptivePlanner:
    def execute_plan(self, task):
        plan = self.create_plan(task)  # 初始计划
        
        for i, step in enumerate(plan.steps):
            result = self.execute_step(step)
            
            # 检查执行结果是否符合预期
            evaluation = self.evaluate_step_result(step, result)
            
            if evaluation.status == "success":
                plan.update_context(step, result)  # 更新后续步骤的上下文
                
            elif evaluation.status == "partial_success":
                # 调整后续步骤以适应部分结果
                remaining_steps = plan.steps[i+1:]
                plan.steps[i+1:] = self.revise_plan(remaining_steps, result)
                
            elif evaluation.status == "failure":
                # 重大调整：可能需要重新规划
                if evaluation.is_recoverable:
                    plan.insert_recovery_step(i+1, evaluation.recovery_action)
                else:
                    plan = self.replan(task, completed=plan.steps[:i], failure=result)
```
调整时机：
- 某个步骤执行失败 → 插入恢复步骤或跳过
- 步骤返回意外结果（如搜索无结果）→ 调整后续查询策略
- 发现新信息改变了问题本质 → 全局重新规划
- 中间步骤发现任务已经可以提前完成 → 跳过剩余步骤
---
# 复杂任务怎么去拆解任务，以及如何更好地调用工具？
任务拆解方法论：
```python
DECOMPOSITION_PROMPT = """
将以下复杂任务拆解为可执行的子任务：

任务：{task}

要求：
1. 每个子任务应该是原子操作（单一、明确、可验证）
2. 标注子任务之间的依赖关系（哪些可以并行，哪些必须串行）
3. 为每个子任务推荐最合适的工具
4. 估计每个子任务的难度（low/medium/high）

输出格式：
{
  "subtasks": [
    {"id": 1, "description": "...", "depends_on": [], "tools": ["..."], "difficulty": "low"},
    {"id": 2, "description": "...", "depends_on": [1], "tools": ["..."], "difficulty": "medium"}
  ],
  "execution_order": [[1,3], [2,4], [5]]  // 第一组并行，第二组并行，第三组串行
}
"""
```
更好地调用工具的策略：
1. 工具选择精准化：为每个子任务匹配最合适的工具，而非让模型自由选择
2. 参数预填充：利用上下文信息预填充工具参数
3. 结果验证：每次工具调用后验证结果是否合理
4. Fallback 链：主工具失败时自动切换到备选工具
5. 批量调用：独立的工具调用并行执行
---
# 举例复杂任务下执行流程
任务："帮我分析特斯拉过去一年的股价走势，与竞争对手对比，并生成投资建议报告"
```python
[Planning Phase]
├── 子任务 1：获取特斯拉(TSLA)过去一年的股价数据
├── 子任务 2：获取竞争对手(BYD, Rivian, Lucid)的股价数据
├── 子任务 3：收集特斯拉近期新闻和财报数据
├── 子任务 4：数据分析（收益率、波动率、相关性）
├── 子任务 5：竞对对比分析
├── 子任务 6：生成可视化图表
└── 子任务 7：撰写投资建议报告

[Execution Phase]
Step 1-3（并行）：
  Agent 调用 stock_api.get_historical_prices("TSLA", period="1Y")
  Agent 调用 stock_api.get_historical_prices("BYD", period="1Y")  // 并行
  Agent 调用 news_search("Tesla earnings 2025")                   // 并行

Step 4（串行，依赖 1-2 结果）：
  Agent 调用 code_interpreter("""
    import pandas as pd
    tsla_returns = calculate_returns(tsla_data)
    volatility = calculate_volatility(tsla_data)
    correlation = calculate_correlation(tsla_data, byd_data)
  """)

Step 5（串行，依赖 4）：
  Agent 调用 LLM 分析对比结果，生成文字洞察

Step 6（串行，依赖 4）：
  Agent 调用 code_interpreter 生成 matplotlib 图表

Step 7（串行，依赖 3-6 所有结果）：
  Agent 汇总所有信息，调用 document_generator 生成报告

[Verification Phase]
  验证 Agent 检查报告的数据准确性和逻辑一致性
  如有问题，反馈给相关步骤重新执行
```
---