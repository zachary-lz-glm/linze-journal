# Tool Calling / Function Call / MCP
![图片](https://docimg2.docs.qq.com/image/AgAAMBOerw33roG75mVBhZJqWfHDxNgO.png?w=1254&h=1172)

# 你了解的 Tool 调用机制是怎样的？
Tool Calling 是 Agent 与外部世界交互的核心桥梁，也是 Agent 区别于普通聊天机器人的关键能力。其机制可以分为三个层面理解：
协议层：LLM 厂商定义了标准化的工具描述格式（通常是 JSON Schema），包括工具名称、功能描述、参数定义。这些描述被注入到 System Prompt 或特殊的 tools 参数中，告诉模型"你有哪些工具可以用"。
决策层：模型在推理过程中，根据用户的请求和工具描述，决定是否需要调用工具、调用哪个工具、传入什么参数。模型输出的不是普通文本，而是一个结构化的 Tool Call 对象（包含工具名和参数 JSON）。
执行层：应用层代码（Agent 框架或自定义代码）解析模型输出的 Tool Call，调用对应的真实函数或 API，获取返回结果，再将结果作为新的消息（tool_result）回传给模型，模型基于结果继续推理或生成最终回答。
完整流程：
```python
用户请求 → LLM（带工具描述）→ 输出 tool_call{name, args}
    → 应用层执行真实函数 → 返回 tool_result
    → LLM 根据结果生成最终回答（或继续调用其他工具）
```
主流实现差异：
- OpenAI Function Calling：通过 tools 参数传入，模型返回 tool_calls 数组，支持并行调用
- Anthropic Tool Use：类似机制，通过 tools 参数，返回 tool_use content block
- MCP（Model Context Protocol）：标准化的工具暴露协议，一个 MCP Server 可以被任意 MCP Client 使用
---
# 介绍一下 Function Call 原理，模型生成的 JSON 如何通过逻辑触发表层代码执行并返回给模型？
模型是如何知道该调用哪个工具的？
这是一个非常关键的底层问题，需要从训练和推理两个阶段回答：
训练阶段：
- 模型在 SFT（有监督微调）和 RLHF 阶段被训练了大量的"工具调用"样本
- 训练数据包含：用户请求 + 工具描述 → 正确的 tool_call JSON 输出
- 模型学会了根据用户意图和工具描述之间的语义匹配来选择工具
- 本质上是指令跟随 + 语义匹配能力的结合
推理阶段的决策机制：
1. 工具描述作为 System Prompt 的一部分被注入上下文
2. 模型看到用户请求后，进行语义理解
3. 将用户意图与每个工具的 description 和 parameters 做语义匹配
4. 如果匹配度高，模型决定输出特殊的 tool_call 格式（而非普通文本）
5. 参数提取：模型从用户输入中抽取与工具参数 Schema 对应的值
JSON 触发执行的完整链路：
```python
# 1. 定义工具 Schema
tools = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "获取指定城市的天气信息",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "城市名称"},
                "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]}
            },
            "required": ["city"]
        }
    }
}]

# 2. 调用模型
response = llm.chat(messages=[{"role": "user", "content": "北京今天天气怎么样？"}], tools=tools)

# 3. 模型返回 tool_call（而非普通文本）
# response.choices[0].message.tool_calls = [
#   {"id": "call_abc", "function": {"name": "get_weather", "arguments": '{"city": "北京"}'}}
# ]

# 4. 应用层解析并执行
tool_call = response.choices[0].message.tool_calls[0]
func_name = tool_call.function.name      # "get_weather"
func_args = json.loads(tool_call.function.arguments)  # {"city": "北京"}

# 5. 通过函数注册表找到并执行真实函数
tool_registry = {"get_weather": real_get_weather_api}
result = tool_registry[func_name](**func_args)  # 调用真实 API

# 6. 将结果回传给模型
messages.append({"role": "tool", "tool_call_id": "call_abc", "content": str(result)})
final_response = llm.chat(messages=messages, tools=tools)
# 模型基于天气数据生成自然语言回答
```
关键工程细节：
- 工具描述的质量直接影响调用准确率——描述越清晰、参数定义越准确，模型选择越精准
- 工具数量过多时，模型可能选择错误（因为上下文中的工具描述太多，混淆度增加）
- 并行调用：部分模型支持一次返回多个 tool_call，可并行执行提升效率
---
# MCP 和 Function Calling 的区别
一句话总结：Function Calling 是"模型调用工具的能力"，MCP 是"工具如何被标准化暴露和发现的协议"。Function Calling 解决的是"怎么调用"，MCP 解决的是"调用什么"和"如何连接"。MCP 的底层执行仍然依赖 Function Calling。
类比：Function Calling 好比 USB 接口的电气协议，MCP 好比 USB 的标准规范（包括接口形状、供电标准、设备发现协议等）。
---
# MCP 协议的核心内容、介绍一下 MCP
MCP（Model Context Protocol） 是 Anthropic 于 2024 年 11 月推出的开放标准，旨在标准化 AI 系统与外部工具和数据源的集成方式。2025 年 12 月，Anthropic 将 MCP 捐赠给 Linux Foundation 下的 Agentic AI Foundation（AAIF），OpenAI 和 Block 作为联合创始成员。
核心架构（三角色模型）：
- Host（宿主）：用户交互的应用（如 Claude Desktop、Cursor、ChatGPT）
- Client（客户端）：Host 内部的 MCP 客户端，负责与 MCP Server 通信
- Server（服务器）：暴露工具和数据的服务端（如 GitHub MCP Server、Slack MCP Server）
协议提供的四大能力：
1. Tools（工具）：可执行的函数，如搜索、数据库查询、文件操作
2. Resources（资源）：可读取的数据源，如文件内容、数据库记录
3. Prompts（提示模板）：预定义的 Prompt 片段，可被 Client 调用
4. Sampling（采样）：Server 可以请求 Client 的 LLM 进行推理
技术规范：
- 传输协议：JSON-RPC 2.0 over HTTP（Streamable HTTP）或 stdio（本地进程）
- 授权框架：OAuth 2.1 + OpenID Connect
- 2025.11 规范新增：异步任务（Tasks）、增量权限协商、Server Identity
行业采用情况（截至 2026 年 3 月）：
- 每月 SDK 下载量超 9700 万次（Python + TypeScript）
- 超过 10,000 个活跃 MCP Server
- 主流 Client 支持：Claude、ChatGPT、Cursor、Gemini、VS Code、Microsoft Copilot
- 2026 年路线图聚焦四大方向：Streamable HTTP 演进、Agent 协作、Tasks 成熟、企业就绪
---
# MCP 和 Skill 的区别，二者谁占用上下文窗口比较大？
概念区分：
MCP：是标准化的工具暴露协议，通过 Client-Server 架构连接。工具描述（Schema）注入上下文窗口，实际执行发生在 Server 端。
Skill（技能）：通常指在 System Prompt 或配置文件中预定义的能力描述和行为指南。例如 Cursor 的 Rules、Coze 的 Skills。Skill 更像是 Prompt 层面的"能力定义"，告诉模型如何完成特定类型的任务。
上下文窗口占用对比：
- Skill 通常占用更大。因为 Skill 本质是详细的 Prompt 指令，可能包含角色定义、行为规范、示例（few-shot）、限制条件等，动辄数百到数千 Token。
- MCP 工具描述通常较精简，每个工具的 Schema（name + description + parameters）一般在 100-300 Token。
- 但如果接入了大量 MCP Server（每个暴露多个工具），工具描述的总量也会很大。
最佳实践：只加载当前任务需要的工具和 Skill，避免全量注入。LangGraph 等框架支持动态工具加载。
---
# Skills 是怎么实现的，Skills 和 MCP 区别，怎么使用它们？
Skills 的实现方式：
Skills 本质上是结构化的 Prompt 模板 + 关联的工具集合 + 执行逻辑。
```python
# Skill 的典型实现
class DataAnalysisSkill:
    name = "数据分析"
    description = "能够分析用户上传的数据文件，生成图表和洞察"
    
    system_prompt = """
    你是一位专业的数据分析师。当用户上传数据文件时：
    1. 首先理解数据结构和字段含义
    2. 识别用户的分析需求
    3. 编写 Python 代码进行分析
    4. 生成可视化图表
    5. 总结关键洞察
    
    使用 pandas 进行数据处理，matplotlib/seaborn 进行可视化。
    """
    
    tools = [code_interpreter, file_reader, chart_generator]
    
    def activate(self, context):
        """将 Skill 的 Prompt 和工具注入到 Agent 上下文中"""
        context.add_system_prompt(self.system_prompt)
        context.register_tools(self.tools)
```
在各平台的实现：
- Coze：通过可视化界面定义 Skill，包含 Prompt、工具绑定、触发条件
- Dify：通过 Workflow + Prompt 组合实现 Skill
- Cursor：通过 .cursor/rules/ 下的 .mdc 文件定义 Skill
Skills vs MCP 的核心区别：
Skills 是"教 Agent 如何做事"（知识和方法论层面），MCP 是"给 Agent 提供做事的工具"（能力和资源层面）。一个好的 Agent 需要两者结合：Skill 提供做事的方法论，MCP 提供做事的工具。
使用建议：
- 用 Skill 定义 Agent 的角色、行为准则、领域知识、推理策略
- 用 MCP 接入外部工具和数据源
- Skill 适合固定的、可复用的能力模板
- MCP 适合动态的、需要与外部系统交互的能力
---
# Tool 层怎么定义的？Tool 层具体在 Agent 运行中是怎么被调用的？
Tool 层的定义规范：
每个 Tool 需要定义三个核心要素：
```python
# 标准 Tool 定义
tool_definition = {
    "name": "search_database",          # 工具唯一标识
    "description": "搜索公司产品数据库，支持按名称、类别、价格范围查询。" 
                   "当用户询问产品信息、库存、价格时使用此工具。",  # 关键！描述要清晰
    "parameters": {                      # JSON Schema 格式的参数定义
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "搜索关键词"
            },
            "category": {
                "type": "string",
                "enum": ["electronics", "clothing", "food"],
                "description": "产品类别筛选"
            },
            "max_results": {
                "type": "integer",
                "default": 10,
                "description": "最多返回结果数"
            }
        },
        "required": ["query"]
    }
}
```
Tool 在 Agent 运行中的调用流程：
```python
Agent Loop 迭代 N：
  ├── 1. 上下文构建：system_prompt + tool_definitions + messages
  ├── 2. LLM 推理：输入上下文 → 输出决策
  │     ├── 决策 A：直接回复用户（输出文本）→ 结束循环
  │     └── 决策 B：调用工具（输出 tool_call JSON）→ 继续
  ├── 3. 工具调度器（Tool Dispatcher）：
  │     ├── 解析 tool_call → 提取 name 和 arguments
  │     ├── 通过 Tool Registry 查找对应的执行函数
  │     ├── 参数校验（Schema Validation）
  │     └── 执行函数 → 获取结果
  ├── 4. 结果注入：将 tool_result 追加到 messages
  └── 5. 回到步骤 1，进入迭代 N+1
```
工程关键点：
- Tool Registry（工具注册表）：维护 name → function 的映射
- 参数校验：执行前用 JSON Schema 校验参数合法性
- 超时控制：每个工具调用设置超时限制
- 结果格式化：工具返回的原始数据需要格式化为模型友好的文本
- 错误包装：工具执行失败时，返回结构化的错误信息（而非抛异常），让模型可以理解并尝试其他方案
---
# 如何不用多智能体方案让 1000 个 Tools 正常工作？
这是一个非常实际的工程挑战，1000 个 Tool 的 Schema 全部注入上下文会消耗大量 Token 且导致模型选择混乱。
方案一：两阶段路由（推荐）
```python
第一阶段：意图识别 → 选择 Tool 类别
  用户输入 → 轻量级 LLM/分类器 → 判断属于哪个工具类别
  （如：数据库类、搜索类、文件操作类、API 调用类...共 20 个类别）

第二阶段：类别内精确选择
  将该类别下的 50 个工具 Schema 注入上下文 → LLM 选择具体工具
```
这样每次 LLM 只需要从 50 个工具中选择，而非 1000 个。
方案二：语义检索式工具选择
```python
# 预处理：为每个工具生成嵌入向量
for tool in all_1000_tools:
    tool.embedding = embed_model.encode(tool.name + " " + tool.description)

# 运行时：用用户输入检索最相关的 Top-K 工具
query_embedding = embed_model.encode(user_input)
relevant_tools = vector_search(query_embedding, all_tool_embeddings, top_k=10)
# 只将这 10 个工具注入上下文
```
方案三：工具分层注册
```python
Layer 0：核心工具（始终注入，5-10 个最常用的）
Layer 1：领域工具（根据对话主题动态加载）
Layer 2：长尾工具（仅在 Layer 0/1 无法满足时触发检索加载）
```
方案四：工具描述压缩
- 精简每个工具的 description，只保留核心功能说明
- 将详细参数说明放在调用时再加载（延迟加载）
- 使用工具组（Tool Group）合并功能相近的工具
方案五：动态工具加载 + 上下文热替换
```python
# 只在需要时动态加载工具
def on_tool_needed(category):
    tools = tool_registry.get_tools_by_category(category)
    agent.update_tools(tools)  # 热替换当前可用工具集
```
面试加分：可以补充说"OpenAI 的 GPT Store 和 Coze 的插件系统本质上就是在做工具管理的问题，它们通过分类、搜索和推荐机制来解决大量工具的选择问题。"
---
# 如果 MCP 特别多的话要怎么管理？
当接入了数十甚至上百个 MCP Server 时，面临的核心挑战和管理策略：
挑战：
1. 工具描述总 Token 量爆炸
2. 模型在大量工具中选择准确率下降
3. 多个 Server 的连接管理复杂度增加
4. 权限和安全控制难度增大
管理策略：
（1）MCP Gateway / Registry
- 部署统一的 MCP 网关，所有 Server 注册到网关
- 网关提供：服务发现、负载均衡、健康检查、访问控制
- MCP 2026 路线图中明确提到了 Registry 和 Server Discovery 的标准化
（2）按场景分组
```python
MCP Server Groups:
├── 开发工具组：GitHub, Jira, Sentry, Docker
├── 办公协作组：Slack, Google Drive, Notion, Calendar
├── 数据分析组：PostgreSQL, Snowflake, Tableau
└── 客户服务组：Zendesk, Salesforce, Intercom
```
每个会话只激活相关分组的 MCP Server。
（3）动态激活/去激活
- 根据对话上下文动态判断需要哪些 MCP Server
- 不使用时断开连接，减少资源消耗
- 使用 LLM 做意图识别来决定激活哪组 Server
（4）权限分级管理
- 每个 MCP Server 配置独立的 OAuth scope
- 用户级别的权限控制（如实习生不能访问生产数据库 MCP）
- 操作审计日志
（5）监控与告警
- 每个 MCP Server 的可用性、延迟、错误率监控
- 异常 Server 自动隔离
- 使用量和成本追踪
---
# 特定推理模型不支持 MCP 的技术原因
某些推理模型（如早期的 o1、o3、DeepSeek-R1 等纯推理模型）不支持 MCP/Tool Use，主要原因：
（1）训练目标差异
- 推理模型（Reasoning Model）的训练目标是最大化思维链（CoT）的推理质量
- 训练数据以数学证明、逻辑推导、代码推理为主
- 没有包含 Tool Calling 的训练样本，因此模型不具备输出结构化 tool_call JSON 的能力
（2）输出格式限制
- 推理模型通常使用专门的 <thinking> 标签进行内部推理
- 其输出格式是"思考过程 + 最终答案"的固定模式
- 很难在这种模式中插入 tool_call 的结构化输出
（3）架构设计选择
- 部分推理模型不支持设置 thinking_budget=0 或控制输出格式
- 如 OpenAI 的 o3 不支持 token-based thinking budgets，无法被配置为工具调用模式
（4）Token 预算机制冲突
- 推理模型需要大量 Token 进行内部思考
- Tool Calling 需要在中间暂停推理、执行外部操作、再恢复推理
- 这两种模式在 Token 预算管理上存在冲突
解决方案：
- 用推理模型做规划和分析，用通用模型做工具调用（混合架构）
- 新一代模型（如 Claude Opus 4.6、GPT-5.x）已经同时支持深度推理和工具调用
- 框架层面做适配：检测到推理模型时，先让其推理出需要的信息，再由框架调用工具获取
---
# 如何让大模型格式化输出消息，以及 Pydantic 相比 Prompt Engineering 在工程上的优势？
格式化输出的三种方案：
方案一：Prompt Engineering（提示词工程）
```python
请以 JSON 格式输出，包含以下字段：
- name: 用户姓名
- intent: 用户意图（inquiry/complaint/suggestion之一）
- summary: 简短摘要
```
缺点：模型可能不遵守、格式可能不标准、需要手动解析和校验。
方案二：Structured Output / JSON Mode
- OpenAI 的 response_format: {type: "json_schema", json_schema: {...}}
- Anthropic 的 Tool Use 强制输出
- 模型层面保证输出符合 Schema 缺点：不是所有模型都支持。
方案三：Pydantic + 后处理（推荐工程方案）
```python
from pydantic import BaseModel, Field
from enum import Enum

class Intent(str, Enum):
    INQUIRY = "inquiry"
    COMPLAINT = "complaint"
    SUGGESTION = "suggestion"

class UserMessage(BaseModel):
    name: str = Field(description="用户姓名")
    intent: Intent = Field(description="用户意图分类")
    summary: str = Field(max_length=200, description="简短摘要")

# 将 Pydantic Schema 自动转为 JSON Schema 注入 Prompt
# LLM 输出后自动校验
raw_output = llm.call(prompt)
try:
    result = UserMessage.model_validate_json(raw_output)
except ValidationError as e:
    # 自动重试或 fallback
    result = retry_with_correction(raw_output, e)
```
Pydantic 的工程优势：
---
# A2A 协议、A2A 与 MCP 区别
A2A（Agent-to-Agent Protocol） 是 Google 于 2025 年 4 月发布的开放协议，旨在标准化不同 AI Agent 之间的通信与协作。2025 年 6 月捐赠给 Linux Foundation。
A2A 核心概念：
- Agent Card：JSON 格式的"名片"，描述 Agent 的能力、技能、认证方式
- Task：协作的基本单元，有生命周期状态（submitted → working → input-required → completed/failed）
- Client Agent / Remote Agent：请求方和服务方的角色划分
- Artifact：任务完成后的交付物
A2A vs MCP 关键区别：
互补关系：Google 明确定位 A2A 与 MCP 互补。MCP 让单个 Agent 能使用工具，A2A 让多个 Agent 能协作。一个完整的多 Agent 系统同时需要两者：每个 Agent 内部用 MCP 连接工具，Agent 之间用 A2A 通信。
行业现状：截至 2025 年底，MCP 已成为事实标准，A2A 的采用速度相对较慢。Google Cloud 自身也在为其服务添加 MCP 兼容性。A2A 更多用于大型企业的跨系统 Agent 协作场景。
---
# 谈谈对 A2A 通信的理解。在 A2A 场景下，如何防止两个 Agent 陷入递归对话？
A2A 通信的核心理解：
A2A 通信本质上是一种任务委托与协作协议。Agent A 发现自己无法独立完成某项任务时，通过 A2A 协议将子任务委托给更专业的 Agent B。整个过程是异步的，支持长时间运行的任务。
通信流程：
```python
Agent A（Client）→ 发送任务请求 → Agent B（Remote）
Agent B → 处理任务（可能耗时很长）
Agent B → 发送状态更新（SSE 流式）→ Agent A
Agent B → 需要更多信息时 → 状态变为 input-required → Agent A 补充
Agent B → 完成任务 → 返回 Artifact → Agent A
```
防止递归对话的机制：
（1）最大交互轮次限制
```python
class A2AConversation:
    MAX_TURNS = 10  # 硬性上限
    
    def send_message(self, target_agent, message):
        if self.turn_count >= self.MAX_TURNS:
            return self.force_conclude()  # 强制结束
        self.turn_count += 1
```
（2）任务状态机 + 超时机制
- A2A 定义了明确的 Task 状态：submitted → working → completed/failed
- 设置每个状态的超时时间
- 如果 Task 在 working 状态停留超过阈值，自动转为 failed
（3）递归检测
```python
# 维护调用链（Call Chain）
call_chain = ["AgentA -> AgentB", "AgentB -> AgentC", "AgentC -> AgentA"]  # 检测到环！

def detect_recursion(call_chain):
    agents_in_chain = [call.split(" -> ")[1] for call in call_chain]
    return len(agents_in_chain) != len(set(agents_in_chain))  # 有重复即为递归
```
（4）职责明确化
- 通过 Agent Card 明确每个 Agent 的能力范围
- Client Agent 在委托前检查目标 Agent 的 Agent Card
- 避免两个能力重叠的 Agent 互相委托同类任务
（5）单向委托原则
- 设计 Agent 系统时，遵循层级委托（上级 → 下级），不允许反向委托
- 或者维护一个全局的 Task DAG（有向无环图），确保任务委托不形成环
（6）幂等性设计
- 每个任务有唯一 ID
- Agent 收到已处理过的任务 ID 时直接返回缓存结果，不重复执行

---