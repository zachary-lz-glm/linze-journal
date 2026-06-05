# AI Coding / SDD 工程师简历与行业调研报告

> 调研日期：2026-06-02 | 基于 20+ 搜索结果、5 篇深度文章、4 份真实 JD 截图的分析

---

## 一、招聘方在 AI Coding / SDD 简历中寻找什么

### 1.1 核心信号：从"会调 API"到"能造系统"

招聘方（尤其大厂）区分候选人的核心标准不再是"你用了什么 AI 工具"，而是**你是否把 AI 当做一个工程系统来治理**。

来自 [Careery 的 AI Engineer Resume Guide](https://careery.pro/blog/ai-careers/ai-engineer-resume-guide) 的关键区分：

| 信号维度 | AI Engineer（招聘方要的） | ML Engineer（你可能被误读成） |
|----------|--------------------------|-------------------------------|
| 核心动词 | Integrated, orchestrated, deployed, architected, built | Trained, fine-tuned, evaluated, optimized |
| 核心指标 | Retrieval accuracy, latency, API cost, uptime | Model accuracy, F1 score, training time |
| 核心工具 | OpenAI API, LangChain, Pinecone, Bedrock, FastAPI | PyTorch, TensorFlow, MLflow, SageMaker |
| 技术深度 | LLM orchestration, RAG architecture, prompt engineering | Neural network architecture, feature engineering |

**关键结论**：每条简历 bullet 如果读起来像 "trained a model" 或 "improved F1 score"，招聘方会自动把你归类为 ML 方向 -- 而不是他们要招的 AI 产品构建者。

### 1.2 ATS 关键词：2026 年必须出现的术语

根据 [Careery 的 ATS 分析](https://careery.pro/blog/ai-careers/ai-engineer-resume-guide)，以下关键词在 AI Engineer JD 中高频出现：

| 类别 | 关键词 |
|------|--------|
| LLM API | OpenAI API, Anthropic API, Claude, GPT-4o, AWS Bedrock SDK, Vercel AI SDK |
| 框架 | LangChain, LangGraph, LlamaIndex, CrewAI, Semantic Kernel, AutoGen |
| RAG & Embeddings | RAG, vector database, Pinecone, Weaviate, Chroma, pgvector, FAISS, hybrid search |
| Prompt Engineering | structured output, function calling, tool use, prompt chaining, few-shot, guardrails |
| Cloud AI | AWS Bedrock, Azure OpenAI Service, Google Vertex AI |
| Web Frameworks | Next.js, FastAPI, Flask, streaming responses, server-sent events |
| 工具 | Python, TypeScript, Docker, GitHub Actions, CI/CD, **Cursor** |

**注意 Cursor 已经成为 ATS 关键词之一**，说明 AI Coding 工具已经进入主流招聘 JD。

### 1.3 "Vibe Coding" vs "Spec-Driven" 在简历中的风险

来自 [Reddit 社区讨论](https://www.reddit.com/r/vibecoding/comments/1laoeq3/do_you_put_vibe_coding_in_your_cv/) 和 [Facebook Vibe Coding Life 小组](https://www.facebook.com/groups/vibecodinglife/posts/1988509198404274/) 的明确信号：

> **"Vibe coding explicitly means you don't really understand the code, you just instruct AI. That term denotes a lack of skill."**
> **"If you want to get a job, don't call yourself a vibe coder."**

而 SDD / Spec-Driven Development 则是**更安全、更专业的表述方式**。来自 [InterCode 博客](https://intercode.com/blog/vibe-coding-vs-spec-driven-development-in-2026) 和 [Red Hat Developer 文章](https://developers.redhat.com/articles/2026/03/30/vibes-specs-skills-agents-ai-coding) 的分析：

- Vibe Coding = "快速试错的迭代式开发"，缺少规划阶段，产出不可控
- SDD = "先写规范再写代码，规范即文档，文档即代码"，结构化可验证

**对简历的启示**：应该用 SDD/Spec-Driven 而非 Vibe Coding 来描述你的 AI Coding 工作方式。但更重要的是，要能讲清楚 SDD 在你手里具体做了什么 -- 而不只是堆概念。

---

## 二、真实 JD 技能要求提取

### 2.1 你手上的 JD 截图分析（JD1 目录）

#### JD-A：AI 研发效能架构师（SDD 体系）

**来源**：BOSS直聘截图，疑似某中型互联网公司或 AI 公司

**岗位职责**（原文提取）：
1. 主导公司全员 AI-SDD 规格驱动开发体系搭建，统一制定产品/前端/后端标准化 SPEC 文档模板与撰写规范
2. 搭建全技术栈统一项目脚手架、代码规约、接口契约、分层架构，完成研发侧 **Harness 约束体系落地**
3. 梳理 AI 编码工作流，沉淀团队专属提示词库、组件复用规则，管控 AI 生成代码质量与可维护性
4. 统筹各业务线研发流程对齐，推动需求、设计、开发、测试全链路按 SDD 模式协作落地
5. 负责研发流程培训、项目合规巡检，解决多业务线规范不统一、AI 开发混乱等问题
6. 配合组织架构调整，适配设计下沉业务模式，联动设计、招聘侧统一设计与研发底层标准
7. 持续优化研发提效工具链，沉淀通用开发能力，降低团队 AI 编码返工率

**任职要求**（原文提取）：
1. 本科及以上，5 年以上互联网研发架构/研发效能相关经验，有字节/美团等大厂 AI Coding、SDD 实战落地经验优先
2. 精通 Spec-Driven 开发全流程，**清晰区分 Vibe Coding 与标准化 AI 研发边界**，熟练搭建全链路规范体系
3. 具备全栈技术视野，熟悉前后端、客户端主流技术栈，能独立制定通用技术基线与开发约束
4. （第 4 点被截断，推测涉及沟通协作能力）

#### JD-B：Agent Harness Engineer

**来源**：BOSS直聘截图

**岗位职责**（原文提取）：
1. 参与设计并实现 Agent 执行全链路的 tracing & observability 系统
2. 参与构建 Agent 质量评估体系：自动化 eval pipeline、A/B testing、regression detection
3. 开发 Agent debugging 工具
4. 参与核心支撑平台（标注、SBS 评测、数据管道）的架构设计与开发
5. 和 AI 研究团队零距离，能第一时间触碰最新的模型能力，将大模型与 Agent 协同进化的研究成果工程化落地
6. 探索并实践 AI Agent 的日常工作流

**岗位要求**（原文提取）：
1. **使用 Cursor / Claude Code / Codex 等进行重度编程**，对 agentic coding 的能力边界和 failure mode 有切身的体感
2. 极客精神，喜欢折腾新技术，享受新技术带来的生产力突破，拥有一定的全栈工程能力和系统设计功底
3. 熟悉 AI/Agent 技术栈，了解 LLM、Agent framework、prompt engineering
4. 代码质量要求严格，代码是给未来的 AI 和人一起维护的，可读性、架构性等缺一不可
5. 对 Code Agent 的未来有深刻思考，希望加入这股生产力变革的浪潮之中

**加分项**：
1. 有 Agent Observability 系统的开发或深度使用经验
2. 参与过 AI Agent 产品从 0 到 1 的构建

#### JD-C：Agent 工程框架工程师（美团）

**岗位职责**（原文提取）：
1. 主导 Agent 工程框架的设计与改造，覆盖任务调度、状态流转、Tool Calling 动态路由、失败重试等核心机制
2. 模型网关架构设计与迭代，实现多模型统一调用管理、负载均衡与流量调度
3. 设计并落地推理回放与性能治理体系，支持 Prompt、检索结果与工具调用全过程复现
4. 大模型应用容器化部署与工程化交付
5. 与算法团队协作，推动 RAG 检索链路、多 Agent 协作流程的工程化实现

**要求**：本科及以上，8 年以上后端工程经验，有大模型或 AI 系统工程化落地经验者优先

### 2.2 公开渠道的 AI Coding 岗位汇总

| 公司 | 岗位 | 薪资 | 核心要求 |
|------|------|------|----------|
| 字节跳动 | AI应用开发工程师（AI Coding方向） | 未公开 | 全栈工程能力、AI-Native 思维、AI Agent 架构、AI Coding 工程落地经验优先 |
| 字节跳动 | 高级前端工程师（AI方向） | 未公开 | 熟悉 Agent Framework、持续关注行业进展 |
| 字节跳动 | AI应用开发工程师（Cross Platform） | 未公开 | 多模态大模型接入、AI Agent 开发、RAG 优化、MCP |
| 小红书 | 前端架构师（AI Coding / 前端基建） | 30-60K | Webpack/Rspack/Vite 深度优化、Monorepo/CI-CD 体系建设、React Native |
| 京东科技 | AI Coding 架构师 | 50-80K·20薪 | 未详细公开 |
| 智源研究院 | AI Coding Agent 架构师 | 40-70K·15薪 | 未详细公开 |
| 阿里云 | AI Coding — IDE 客户端研发 | 30-60K·16薪 | 未详细公开 |
| 大疆 | 全栈开发工程师（后端） | 未公开 | 独立把控复杂 AI 工程化应用、类 Dify/Coze 工作流平台 |

---

## 三、前端工程师转 AI 方向的简历建议

### 3.1 最平滑的转型路径

来自 [CSDN AI编程社区](https://aicoding.csdn.net/69b8e3ac0a2f6a37c5980e59.html) 和 [知乎专栏](https://zhuanlan.zhihu.com/p/1889007398464745664) 的共识：

**前端 + LangChain / AI Agent 开发 = 最平滑的转型路径**

核心逻辑：
- 前端的交互设计能力 + AI 后端能力 = AI 全栈竞争力
- 大模型应用/智能体工程师是最平滑的转型路径
- 复用高并发、微服务经验，转向 LangChain/AutoGen 等框架

### 3.2 牛客网的高赞建议（极具参考价值）

来自 [牛客网《2026 年，AI 全栈时代到了，前端简历别再只写前端技术了》](https://www.nowcoder.com/discuss/879078076276105216)，这篇是对你最有直接参考价值的文章。核心观点：

**简历中常见的四种同质化问题**：
1. 周期很短，却同时堆上 RAG、流式输出、鉴权与复杂治理 -- 看不出真实投入与掌握深度
2. 段落像功能清单，缺少场景、难点、个人职责与可验证结果
3. 形态集中在教程型对话台或后台管理，差异化不明显
4. Agent 被写成"调模型、接工具"，很少触及运行时、状态机、评测、观测与人在回路

**面试中真正被问的问题**（不是技能清单）：

> "你有没有把 Agent 当成一个系统，而不是一个函数调用？"

具体评审会盯的几件事：
- 有没有独立的 Agent Runtime
- 有没有显式状态机驱动的 Agent Loop
- 有没有把评测做成回归闸门
- 有没有把观测、检测、红队、安全、成本和用户干预整成闭环
- 能不能把这些能力真正接进产品

**前端 + LangChain 开发者的真正优势**（原文）：

> "你更占便宜的地方，是把 Agent 做成用户看得见、停得下来、出了问题能对上账的系统。"

前端日常就是状态、异步、中间态、确认、埋点和展示，这些在 Agent 工程中比纯写脚本的人更顺手。

**推荐的自我定位表述**（原文建议）：

> "我负责把 LLM 编排、工具、状态机、可观测、评测和交互收成一条，给人用的是产品不是脚本。"

### 3.3 Agent 系统的六层架构（简历项目经历的参考框架）

来自牛客网文章，一个有区分度的 Agent 系统应有六层：

1. **交互层**：用户看得见、点得着的界面，步骤展示、审批、中断、重试和结果反馈
2. **编排层**：LangChain/LangGraph 等把 Prompt、模型、工具、记忆和状态流转组织成可维护的流程
3. **运行时 Harness**：管理步数、超时、预算、快照、重试、取消和收尾
4. **安全与检测层**：在输入、工具执行前、输出和轨迹上做规则与模型检测
5. **可观测层**：用 Trace、Metrics、日志把每一步变成可查询、可对比、可回放的事实
6. **评测层**：通过离线集、回归闸门和线上灰度，用数据判断一次改动到底有没有变好

---

## 四、AI 工程师简历常见问题与避坑

### 4.1 最致命的 7 个错误

综合 [Careery](https://careery.pro/blog/ai-careers/ai-engineer-resume-guide)、[Dealmoon](https://www.dealmoon.com/post/2579278)、[Masai School](https://www.masaischool.com/blog/7-resume-mistakes-freshers-are-still-making-in-2026-and-how-to-fix-them/) 等来源：

| 错误 | 正确做法 |
|------|----------|
| **ML 研究式表述伪装成 AI Engineer**（"trained a model", "improved F1"） | 用 AI 工程语言："deployed a RAG pipeline", "architected a multi-model gateway" |
| **技能列表堆砌 40+ 工具** | 列出 15-25 个你真正能在面试中深入讨论的工具 |
| **写 "Worked with AI models"** | 写 "Integrated OpenAI and Anthropic APIs... serving 50K+ requests/day with 99.8% uptime" |
| **没有量化指标** | 每条 bullet 至少包含量化数据：retrieval accuracy, latency, cost savings, user impact |
| **同一份简历投所有岗位** | 按目标 JD 调整关键词和排序 |
| **技能/经验中使用 "Vibe Coding"** | 用 SDD/Spec-Driven 或 "AI-assisted development with structured specs" 替代 |
| **过度依赖 AI 生成简历内容** | AI 生成的简历可能包含"幻觉"、遗漏重要信息，必须人工校对 |

### 4.2 Bullet 写法对比

| 差 | 好 |
|----|-----|
| Worked with AI models and APIs | Integrated OpenAI and Anthropic APIs into a customer-facing product with automatic model fallback, serving 50K+ requests/day with 99.8% uptime and p95 latency under 1.2s |
| Built a chatbot for customer support | Designed a RAG-powered support agent using LangChain, Pinecone, and GPT-4o that resolved 65% of Tier-1 tickets automatically, deflecting 3,000+ conversations/month |
| Used Python for ML projects | Architected a prompt chaining pipeline for automated contract analysis, processing 500+ legal documents/week with 94% extraction accuracy |

### 4.3 简历格式要求（ATS 友好）

- 单栏布局，标准 section headings（Technical Skills, Experience, Projects, Education）
- PDF 格式
- 10-11pt 字体
- 无图标、无图片、无花哨设计
- Technical Skills 放在页面前 1/3 处
- 入门/中级 1 页，高级 2 页以内

---

## 五、"Harness 工程化约束"到底是什么

### 5.1 结论：这是 2025-2026 年正在形成的行业标准术语

"Harness" 在 AI Coding 领域**不是** Harness.io（CI/CD 平台）的产品名，而是一个正在快速标准化的工程概念。

### 5.2 权威定义

**Martin Fowler 的定义**（[martinfowler.com](https://martinfowler.com/articles/harness-engineering.html)）：

> "The term harness has emerged as a shorthand to mean everything in an AI agent except the model itself -- **Agent = Model + Harness**."

**Arxiv 论文 "AI Harness Engineering"**（[arxiv.org](https://arxiv.org/html/2605.13357v1)）：

> 开发 Harness 管理的运行时资源包括：context budget（上下文预算）、tool budget（工具预算）等约束。

**知乎深度解析**（[知乎专栏](https://zhuanlan.zhihu.com/p/2014014859164026634)）：

> Harness Engineering 是围绕 AI Agent（尤其是 Coding Agent）设计的工程范式。

### 5.3 "Harness" 的三层含义

| 层面 | 含义 | 你简历中的对应 |
|------|------|----------------|
| **软件工程传统含义** | Test Harness = 自动化测试基础设施（stubs、drivers、test data） | -- |
| **AI Agent 含义** | Agent Harness = 模型之外的一切：工具调用分发、上下文管理、状态持久化、安全检查 | "Harness 约束体系落地" |
| **研发效能含义** | 研发侧 Harness = 代码规约、脚手架、接口契约、分层架构等工程约束体系 | JD-A 中的 "Harness 约束体系落地" |

### 5.4 从 Scaffold 到 Harness 的范式转变

来自 [Twitter/X 讨论](https://x.com/TaNGSoFT/status/2032190539613999483)：

> 从 "Scaffold（脚手架）" 到 "Harness（约束套件）" 的转变，是 2025-2026 年 AI 工程领域最核心的范式跃迁 -- 从"松散组装结构"到"工程化约束体系"。

### 5.5 Harness Engineering 的六大维度

来自 [Awesome Harness Engineering（GitHub）](https://github.com/walkinglabs/awesome-harness-engineering)：

1. **Context Engineering**（上下文工程）：给 AI 什么信息
2. **Evaluation**（评测）：怎么判断 AI 产出的质量
3. **Observability**（可观测）：怎么追踪 AI 的执行过程
4. **Orchestration**（编排）：怎么组织 AI 的工作流
5. **Safe Autonomy**（安全自治）：怎么约束 AI 的行为边界
6. **Software Architecture**（软件架构）：怎么把 AI 嵌入系统

### 5.6 对你简历的启示

你简历中写的 "Harness 工程化约束体系" 是一个**准确的行业术语**，且在 2026 年正在被更多公司采纳（从你手上的 JD-A 和 JD-B 可以看出）。但需要注意：

1. **不是所有面试官都熟悉这个术语** -- 建议在面试时准备好用通俗语言解释
2. **解释的核心公式**：Agent = Model + Harness，Harness = 模型之外的一切工程约束
3. **你简历中的具体体现**：8 种证据类型、三级门禁、SSOT 规范体系 -- 这些就是你的 Harness 落地实践

---

## 六、综合结论与对你简历的具体建议

### 6.1 你简历的优势（与 JD 的高度匹配）

对比你手上的 JD，你的简历在以下方面高度匹配：

| JD 要求 | 你简历中的对应 | 匹配度 |
|----------|---------------|--------|
| JD-A: SDD 体系搭建 | SDD 体系搭建项目经历 | 极高 |
| JD-A: 区分 Vibe Coding 与标准化研发边界 | 简历中明确写了 "清晰区分 Vibe Coding 与标准化 AI 研发边界" | 极高 |
| JD-A: Harness 约束体系落地 | "Harness 工程化约束体系" | 极高 |
| JD-B: 对 agentic coding failure mode 有体感 | "对 AI Coding 能力边界与 failure mode 有切身体感" | 极高 |
| JD-B: Cursor / Claude Code / Codex 重度使用 | 技能栏有列 | 高 |
| JD-A: 全栈技术视野 | Schema 驱动全栈（BFF + 前端 + 组件库） | 高 |

### 6.2 建议优化的方向

1. **增加量化数据**：SDD 项目的 "PRD 转化效率提升 60%+" 很好，但 Harness 约束体系具体降低了多少返工率、节省了多少时间？建议补充
2. **Bullet 写法更偏向 "built" 而非 "used"**：部分描述偏重 "落地了什么流程"，可以更多强调 "构建了什么系统、解决了什么问题、达到什么指标"
3. **ATS 关键词补充**：考虑在技能栏加入 LLM、RAG、vector database、prompt engineering 等 ATS 高频词
4. **项目描述中突出 Agent 系统六层架构**：牛客网文章提到的六层（交互层、编排层、运行时 Harness、安全与检测层、可观测层、评测层），你的 SDD 体系如果能按这个框架重新组织描述，会更贴近评审的期望

---

## 参考来源

### 深度文章
- [Careery: AI Engineer Resume Guide](https://careery.pro/blog/ai-careers/ai-engineer-resume-guide) -- AI 工程师简历最全面的英文指南
- [牛客网: 2026 年，AI 全栈时代到了，前端简历别再只写前端技术了](https://www.nowcoder.com/discuss/879078076276105216) -- 对前端转 AI 最有参考价值的中文文章
- [InterCode: Vibe Coding vs Spec-Driven Development in 2026](https://intercode.com/blog/vibe-coding-vs-spec-driven-development-in-2026) -- SDD 方法论对比
- [Martin Fowler: Harness Engineering for Coding Agent Users](https://martinfowler.com/articles/harness-engineering.html) -- Harness 权威定义
- [Arxiv: AI Harness Engineering](https://arxiv.org/html/2605.13357v1) -- 学术论文定义

### Harness 术语
- [Martin Fowler: Harness Engineering](https://martinfowler.com/articles/harness-engineering.html)
- [OpenAI: Harness Engineering](https://openai.com/index/harness-engineering/)
- [Awesome Harness Engineering (GitHub)](https://github.com/walkinglabs/awesome-harness-engineering)
- [知乎: Harness Engineering 深度解析](https://zhuanlan.zhihu.com/p/2014014859164026634)
- [TianPan.co: Agent Harness 深度解析](https://tianpan.co/zh/blog/2026-02-27-anatomy-of-an-agent-harness)
- [Analytics Vidhya: Frameworks vs Runtimes vs Harnesses](https://www.analyticsvidhya.com/blog/2025/12/agent-frameworks-vs-runtimes-vs-harnesses/)

### 职位信息
- [字节跳动招聘](https://jobs.bytedance.com/experienced/m/position/detail/7515331585718946066)
- [小红书前端架构师（BOSS直聘）](https://www.zhipin.com/job_detail/44c6968f9fa688d8031_2t-7FldY.html)
- [DJI 大疆 AI实习生](https://we.dji.com/zh-CN/position/detail?positionId=2043544561518043136)

### 转型建议
- [CSDN: 2026年APP开发人员转型建议](https://aicoding.csdn.net/69b8e3ac0a2f6a37c5980e59.html)
- [知乎: 2026建议所有程序员入局AI](https://zhuanlan.zhihu.com/p/1889007398464745664)
- [B站: 前端终极转型指南](https://www.bilibili.com/video/BV1fGwqzdES5/)

### 避坑指南
- [Dealmoon: 用AI写简历的5个致命坑](https://www.dealmoon.com/post/2579278)
- [Masai School: 7 Resume Mistakes in 2026](https://www.masaischool.com/blog/7-resume-mistakes-freshers-are-still-making-in-2026-and-how-to-fix-them/)
- [Reddit: Do You Put Vibe Coding in Your CV?](https://www.reddit.com/r/vibecoding/comments/1laoeq3/do_you_put_vibe_coding_in_your_cv/)

### SDD 参考
- [Jimmy Song: 规范驱动开发（SDD）简介](https://jimmysong.io/zh/book/ai-handbook/sdd/overview/)
- [InfoQ: 规范驱动开发——企业规模化落地实践](https://www.infoq.cn/article/OOwOxKFZQbShKx1timMP)
- [腾讯云: Spec-Driven Development](https://cloud.tencent.com/developer/article/2652352)
- [极客时间: SDD 让 AI 永远在轨道上](https://time.geekbang.org/column/article/963294)

### 行业趋势
- [tonybai: AI工程师生存2026](https://tonybai.com/2026/03/17/ai-engineer-survival-2026-post-hype/)
- [Fortune: Claude Code开发者称软件工程师岗位今年或将消失](https://www.fortunechina.com/shangye/c/2026-02/26/content_472276.htm)
- [超级简历: 2026届大厂AI秋招攻略](https://www.wondercv.com/blog/BsN2umNJ.html)
