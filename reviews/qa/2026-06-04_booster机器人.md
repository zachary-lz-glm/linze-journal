# Booster（人形机器人）一面 — 面试优化答案

> 日期：2026-06-04 | 通过概率：30%

---

## Q1: 自我介绍
**核心句**：滴滴国际化高级前端，Schema驱动+AI工程双线
**展开**：面试官好，我叫邓泽林，滴滴国际化高级前端，4年经验。我擅长从复杂业务中抽取共性，做过三件有代表性的事：第一，Schema驱动营销中台，覆盖20+活动类型，新增活动前端开发成本归零；第二，权益组件库，400+权益Schema渲染，8个业务接入，两年零事故；第三，正在独立设计AI工程工作流，把PRD转化为结构化开发计划，效率提升60%。核心优势是工程抽象能力和对全链路质量的把控。

## Q2: AI工程工作流后续有完整engineering吗？
**核心句**：定位是PRD→结构化任务拆解，下游对接任意AI Coding工具
**展开**：我们的产品边界很明确：只做PRD到开发计划的蒸馏和拆解。下游用户可以选择Cursor、Windsurf、Claude Code等任意AI Coding工具来执行。市面上已经有很成熟的code generation工具了，所以我们不做重复的事，而是解决它们上游"需求理解不准确"的痛点。

## Q3: PRD和代码之间缺少可追溯中间产物，怎么设计的？
**核心句**：11步蒸馏流水线，证据链+代码锚定+多层门控贯穿全程
**展开**：整个工作流是一条11步的蒸馏流水线，可追溯性由三个核心机制保障。第一是Evidence Ledger（第2步），定义了8种证据类型——prd、tech_doc、code、git_diff、negative_code_search、human、api_doc、reference，AI产出的每条结论必须引用Evidence ID。第二是代码锚定（第4步），每个Layer Impact必须挂code_anchor，标注来源（graph源码确认/rg搜索/reference路由/inferred推断），MODIFY/DELETE类型没有锚点不允许过。第三是多层门控——摄入门控检查PRD读取质量、Spec Review Gate要求人工确认AI是否读懂PRD才允许生成Plan、Readiness Score做5维度综合评分、Final Quality Gate做5项确定性检查（必传文件/上下文包消费/锚点覆盖率/计划完整性/阻塞项质量）。每个环节通过YAML中间文件传递状态，有明确的输入输出契约。

## Q4: 评分根据什么来评？
**核心句**：5维度加权评分+85/60两个阈值分三档
**展开**：Readiness Score从五个维度加权打分：PRD摄入率（权重20）、证据覆盖率（权重25）、代码搜索命中率（权重15）、契约对齐度（权重25）、计划完整性（权重15）。加权汇总后对照85和60两个阈值分三档：85-100分pass可直接进开发，60-84分warning需owner确认，0-59分blocked。另外还有硬性降级规则：P0契约blocked直接fail、多层需求缺contract-delta直接fail。实际验证环节——拿AI产出的Plan文件列表跟实际开发改动做diff对比，覆盖率约80%。

## Q5: PRD过时/临时改动没同步，怎么处理？
**核心句**：源码为SSOT，历史PRD仅作业务理解参考
**展开**：历史PRD的作用是帮AI理解业务场景模式——比如新增活动通常涉及哪些步骤、联动关系怎么配。它不提供精确指令，所以"错了"不会有后果。最终所有结论都落到源码确认。如果PRD和代码有分叉，以源码为准，工具会把不确定的点标记为"需人工确认"，而不是强行执行。

## Q6: PRD不明确时，从输入到产出的技术环节？
**核心句**：11步蒸馏流水线，每步有YAML中间产物和门控校验
**展开**：技术上是11步蒸馏流水线。第1步PRD Ingestion：支持md/txt/docx和粘贴文本，docx用Python脚本提取文字和图片到_ingest/document.md，图片由子Agent并行分析产出media-analysis.yaml。第2步Evidence Ledger：建立evidence.yaml，后续所有判断只引用Evidence ID。第3步Requirement IR：把PRD转成requirement-ir.yaml，每个需求点含change_type/acceptance_criteria/evidence_ids。第4步Code Search & Layer Impact：先通过Reference路由定位候选文件，再用rg补充扫描，最后精读源码生成graph-context.md和layer-impact.yaml。第5步Contract Delta：多层协作需求生成contract-delta.yaml。第6-7步Spec生成+人工Review Gate。第8步Plan生成。第9步Readiness Score五维评分。第10步Reference回流建议。第11步Final Quality Gate做5项确定性检查。每步通过YAML/MD中间文件传递状态。

## Q7: PRD怎么输入给AI？图片怎么处理？
**核心句**：多格式输入→_ingest目录→图片子Agent并行分析
**展开**：PRD支持四种输入格式：.md/.txt直接读取写入_ingest/document.md；.docx用Python脚本（ingest-docx.py）提取文字和图片，文字写入document.md，图片存入media/目录并在文本中插入本地引用占位符；粘贴文本手工建立来源定位。图片分析比较吃上下文，所以设计了并行子Agent策略——主上下文禁止直接读图，每批≤8张图片开1个foreground子Agent，>8张按数量拆成多个子Agent在同一条消息中并行启动。每个子Agent产出media-analysis-part-N.yaml，全部完成后合并为media-analysis.yaml。关键规则：没有人工确认的图片内容不能生成高置信度需求，AI看图提取的信息默认medium置信度。

## Q8: 图片用什么格式提供给AI？
**核心句**：Base64编码通过API的image字段传入
**展开**：图片通常通过Base64编码，放在API请求的content里的image类型消息中传给模型。也可以传图片URL让模型自己下载。对于Claude API，用base64类型传入；对于OpenAI，用image_url类型。我们用的是Base64方式，因为图片已经在本地了，不需要额外的网络请求。

## Q9: 代码仓库很大，AI怎么精准找到需要的代码？
**核心句**：Reference路由定向+三阶段源码扫描+代码锚点校验
**展开**：代码定位分三阶段。第一阶段Reference路由：从requirement-ir提取业务实体和动作词，匹配04-routing-playbooks.yaml的信号→能力面映射，从01-codebase.yaml提取精确文件路径，如存在Evidence Index则用context-pack.py生成预匹配锚点。第二阶段补充扫描：用rg/glob搜索阶段1未覆盖的业务实体，读取命中文件获取callers/callees/imports，对MODIFY/DELETE候选追踪引用链评估blast radius。第三阶段汇总：将命中符号写成函数级技术线索，标注来源（reference_routing或code_scan），每个MODIFY/DELETE类Layer Impact必须有至少一个code_anchor（标注graph/rg/reference/inferred来源），低置信度锚点进入spec风险或plan假设。能力面分前端（9个surface：ui_route/view_component/form_or_schema等）、BFF（10个surface）、后端（10个surface）三个层。

## Q10: Skills在AI里在什么环节调用？AI怎么知道什么时候用？
**核心句**：Skills通过上下文注入+Function Calling机制，模型按意图匹配触发
**展开**：要理解Skills调用原理，需要从三层架构来看。底层是Function Calling——模型经过微调，能在推理时识别意图并生成结构化的函数调用（JSON格式的函数名+参数）。中间层是MCP——在Function Calling之上建立标准化的C/S协议，让工具注册、发现、调用有统一接口。上层是Skills——通过markdown/代码文件定义多步骤工作流（SKILL.md声明触发条件和指令，workflow.md定义执行步骤），内容注入Agent的system prompt。当用户输入到达模型时，模型在推理过程中匹配prompt中定义的Skills trigger条件，然后通过Function Calling机制触发执行。Skills不是某个平台独有的——任何Agent框架都可以实现类似的"上下文注入+工作流定义"模式。

## Q11: Skills和MCP的区别？
**核心句**：MCP解决"工具怎么标准化接入"，Skills解决"复杂工作流怎么编排执行"
**展开**：两者处于AI能力扩展的不同层次。MCP（Model Context Protocol）是工具协议层——本质是C/S架构，工具注册在MCP Server上，AI Agent作为Client通过标准协议调用。核心价值是"一次开发，多平台可用"，解决AI工具碎片化问题。它提供三类能力：可调用的函数（tools）、数据源（resources）、预设模板（prompts）。每次调用偏向单次、无状态。Skills是工作流抽象层——通过markdown/代码文件定义多步骤工作流，直接注入Agent上下文。适合需要大量上下文管理、多步骤执行、状态流转的复杂场景。核心区别：MCP是"工具的插座标准"，Skills是"流程的编排方案"。实际使用中两者互补——Skills编排的复杂工作流中，可以调用MCP提供的标准化工具。

## Q12: Schema复杂表单联动怎么设计？
**核心句**：D2依赖语法，static型前端发布订阅+flash型BFF联动注入
**展开**：我们在Schema里设计了一套D2依赖语法。在组件配置里用dependence数组声明依赖关系——B依赖A，就在B的配置里写A的name path。联动效果通过三元表达式描述：当依赖值等于什么时，visible/value/disable怎么变化。联动分两种：static型是纯前端，通过发布订阅监听依赖项变化，本地解析表达式修改状态；flash型涉及后端数据（比如城市变了联动后面的配置项），走BFF联动接口，后台返回数据重新拼成新Schema注入前端。

## Q13: Schema表达式安全问题
**核心句**：研发写Schema，权限可控+模板约束
**展开**：Schema由研发通过BFF中间层配置，非运营直接编写，从源头控制了注入风险。同时每个活动类型有标准Schema模板，配置基于模板生成，限制了可用的表达式类型和操作范围。

## Q14: 已上线Schema页面怎么保证不会配错崩溃？
**核心句**：Schema模板+分层定位+版本回滚
**展开**：首先是预防——每个活动类型有标准Schema模板，新配置基于模板生成，减少从零开始的出错概率。运行时如果出错，可以快速定位：BFF接口报错能精确到字段级别，前端视图和逻辑分离后可以定位到具体组件。另外还支持Schema版本管理，出问题可以快速回滚到上一个稳定版本。

## Q15: 组件参数类型错误，怎么前置发现？
**核心句**：沙箱预渲染+Schema校验层+TS类型约束
**展开**：前置可以做三层：第一是沙箱预渲染——在发布前把Schema配置和渲染引擎放在沙箱环境里跑一遍，能发现大部分渲染错误。第二是在BFF模板层加Schema校验——对字段类型、必填项、枚举值做声明式约束，配置阶段就拦截非法值。第三是TS类型约束——公共组件的props有类型定义，模板生成时可以做静态检查。事后还有Sentry+LogInsight全链路监控和错误码分类报警兜底。

## Q16: Monorepo构建——有依赖顺序构建，无依赖并行构建？
**核心句**：NX自动分析依赖图，有依赖拓扑排序，无依赖并行构建
**展开**：NX在构建时会自动分析包之间的依赖关系，构建出一个有向无环图（DAG）。被依赖的公共包排在前面先构建，没有依赖关系的包并行构建。具体来说：NX通过读取每个包的package.json里的dependencies，建立依赖图，然后做拓扑排序确定构建顺序。同时NX还支持构建缓存——如果某个包的源码没变且依赖也没变，直接用缓存跳过。Turborepo的原理类似，也是基于依赖图做pipeline编排。

## Q17: useEffect和useLayoutEffect区别？
**核心句**：useLayoutEffect在DOM更新后paint前同步执行；useEffect在paint后异步执行
**展开**：React更新流程是：state变更→虚拟DOM diff→真实DOM更新→浏览器paint。useLayoutEffect的回调在DOM更新之后、浏览器paint之前同步触发，所以读取/修改DOM布局不会引起闪烁。useEffect的回调在浏览器paint之后异步触发，如果在这里修改DOM会导致额外的重绘。使用场景：需要读布局信息或防止视觉闪烁用LayoutEffect；副作用请求、订阅等不涉及DOM布局的用Effect。

## Q18: React从setState到视图变化的内部流程？
**核心句**：setState→调度→协调→提交→绘制，Effect在不同阶段介入
**展开**：完整流程：1）setState触发更新，进入调度器（Scheduler），根据优先级（lane模型）安排更新时机；2）进入协调阶段（Reconciler），从触发更新的组件开始，对Fiber树做深度优先遍历，通过双缓冲（current树和workInProgress树）进行diff，标记需要更新的副作用（effectTag）；3）进入提交阶段（Committer），将workInProgress树上的变更同步应用到真实DOM；4）useLayoutEffect在DOM更新后、paint前同步执行；5）浏览器paint；6）useEffect在paint后异步执行。Batching机制在18版本中通过automatic batching默认开启，多次setState合并为一次更新。

## Q19: 反问环节
**核心句**：展现对公司产品和技术栈的调研兴趣
**展开**：面试中实际问了两个问题：1）"公司是偏向AI应用的公司吗？"——了解到Booster是人形机器人公司，自己设计制造机器人，团队做开发者工具（IDE面向专业开发者用Electron+WebView，App面向非专业开发者做原生开发）。2）"工作技术栈是什么？"——确认了Electron桌面端和原生App开发。建议额外反问：1）团队在机器人应用开发平台上最大的技术挑战是什么？2）面向非专业开发者的低代码方案，怎么平衡灵活性和易用性？

---

## 面试官洞察（Booster人形机器人）

> 面试官对AI工程化的判断非常前瞻，提供了最有价值的行业认知。

### 洞察1：工作流是过渡态，业务知识沉淀才是长期价值

**面试官判断**："工作流现在非常多，一抓一大把"，而且"随着模型能力越来越强，流程化东西应该是越来越弱"。真正需要沉淀的是"业务上的知识库、RAG也好，还是业务上之前踩的坑也好，这种AI本身从外部获取不了的东西"。

**价值**：这是对AI工程化最前瞻的行业判断。面试中讨论"工作流价值"时，应该主动说"工作流会随模型进化而贬值，但领域知识不会"——这比单纯介绍工作流更有深度。

### 洞察2：前端需要自己的Agent

**面试官指出**：需要"前端自己的agent"去做能力补充，而不仅仅是提效。

**价值**：前端Agent方向是明确趋势，说明前端工程师的价值在"设计Agent行为"而非"写UI"。面试中可以用来论证"前端在AI时代的定位"。

---

> 以下洞察来自Booster一面录音原文。

### 洞察3：PRD与代码分叉是真实痛点，以源码为SSOT是正确解法

**面试官原话/描述**：面试官主动提出"有些PRD已经过时了，或者有些PRD写完之后，有一些临时改动没有录到文档里面"，"实际的PRD和代码结构、代码的逻辑不一样"，"大部分的PRD可能都会有这个问题"。连续追问"怎么处理这个问题"和"会不会导致最后产出的开发计划把代码库完全弄乱了"。

**价值**：PRD-代码分叉是AI工程工作流必须面对的核心挑战。面试中主动提到这个问题并给出"以源码为SSOT（Single Source of Truth），历史PRD仅作业务场景理解参考"的解法，展示对真实工程难点的认知深度。

### 洞察4：沙箱预渲染是Schema发布前校验的标配方案

**面试官原话/描述**：当候选人承认"上线前的脱离开发环境的那种可能没太关注"时，面试官直接给出了方案："整个渲染环节运行一下，把渲染的组件库、渲染层放在沙箱里面跑一下就可以了，能够前期发现很多问题。"

**价值**：这是低代码/Schema驱动平台的前置质量保障标配。面试中回答"Schema安全性"时，应该主动提到CI/CD中加沙箱预渲染步骤——用完整渲染引擎在隔离环境中跑一遍Schema配置，捕获类型错误、渲染异常等问题，确保配置正确后才允许上线。

### 洞察5：Skills调用原理——从Function Calling到上下文注入

**面试官原话/描述**：面试官连续追问"Skills在AI里是在什么环节调用的"和"AI是怎么知道什么时候在用skills的"，并指出"skills它不是code的独有的，你正常用原始的AI自己去开发一个进程，也会用到skills"。候选人说"原理我可能关注的不太多"后，面试官转向问Skills和MCP的区别。

**价值**：Skills调用原理是AI工程的核心知识。完整理解：Function Calling是底层机制——模型经过微调，能在推理时生成结构化函数调用；MCP是在Function Calling之上的标准化协议层，解决工具接入碎片化问题；Skills是更高层抽象，通过markdown/代码定义多步骤工作流注入Agent上下文。三层关系：Function Calling（调用机制）→ MCP（工具协议）→ Skills（工作流抽象）。面试中回答这类问题要能讲清这个演进链路。

### 洞察6：Monorepo构建的核心问题是依赖图的拓扑排序

**面试官原话/描述**：面试官连续追问了Monorepo构建顺序——"你在构建一个业务包的时候，他会依赖基础组件包，那么这个时候就涉及到包和包之间构建流程的顺序的组织"，"怎么保证这个顺序"。从单个包构建（NX缓存）追问到整个项目级别的依赖排序，候选人未能给出完整回答。

**价值**：Monorepo构建的核心原理：1）NX通过读取每个包的package.json中的dependencies，建立有向无环图（DAG）；2）对DAG做拓扑排序确定构建顺序——被依赖的公共包排在前面先构建；3）没有依赖关系的包并行构建减少时间；4）NX还通过计算输入哈希做构建缓存——源码+依赖不变则直接用缓存。这是Monorepo面试必考题。

### 洞察7：公司定位——人形机器人+开发者工具

**面试官原话/描述**："我们是一个人形机器人公司，就是自己设计和造机器人，然后卖机器人"。团队定位："为开发机器人应用的用户提供开发环境"，包括面向专业开发者的IDE（Electron+WebView）和面向非专业开发者的App（原生开发）。

**价值**：Booster不是AI公司，是硬件+开发者工具公司。技术栈涉及Electron桌面端和原生App开发。面试中展现对公司业务的理解，能区别于纯互联网公司。
