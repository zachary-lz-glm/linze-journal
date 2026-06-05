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
**核心句**：Skills通过Agent的system prompt注入，模型按指令匹配调用
**展开**：Skills本质上是Agent的扩展能力。以Claude Code为例，Skills通过SKILL.md和workflow.md定义指令和流程，这些内容会被注入到system prompt里。当用户输入匹配Skills的trigger条件时，模型会按照prompt中的指令选择调用对应的Skill。底层和function calling类似——模型识别意图，匹配到可用的tool/skill，然后按流程执行。区别是Skills更偏向多步骤工作流，而MCP的tools偏向单次调用。

## Q11: Skills和MCP的区别？
**核心句**：MCP是跨平台工具协议，Skills是Agent原生的多步骤工作流
**展开**：MCP是Model Context Protocol，本质是C/S架构——工具注册在MCP Server上，AI Agent作为Client通过标准协议调用。核心价值是"一次开发，多平台可用"，解决AI工具碎片化问题。它主要提供三类能力：可调用的函数（tools）、数据源（resources）、预设模板（prompts）。Skills则不同，它是Agent原生的能力扩展，通过markdown文件定义指令和流程，直接注入到Agent的上下文里。适合需要多步骤执行、大量上下文管理的复杂工作流。简单说：MCP解决"工具怎么接"，Skills解决"复杂流程怎么做"。

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
**展开**：建议反问：1）团队目前在机器人应用开发平台上最大的技术挑战是什么？2）面向非专业开发者的低代码方案，你们怎么平衡灵活性和易用性？3）Electron桌面端和原生App之间有没有共享的技术架构？

---

## 面试官洞察（Booster人形机器人）

> 面试官对AI工程化的判断非常前瞻，提供了最有价值的行业认知。

### 洞察1：工作流是过渡态，业务知识沉淀才是长期价值

**面试官判断**："工作流现在非常多，一抓一大把"，而且"随着模型能力越来越强，流程化东西应该是越来越弱"。真正需要沉淀的是"业务上的知识库、RAG也好，还是业务上之前踩的坑也好，这种AI本身从外部获取不了的东西"。

**价值**：这是对AI工程化最前瞻的行业判断。面试中讨论"工作流价值"时，应该主动说"工作流会随模型进化而贬值，但领域知识不会"——这比单纯介绍工作流更有深度。

### 洞察2：前端需要自己的Agent

**面试官指出**：需要"前端自己的agent"去做能力补充，而不仅仅是提效。

**价值**：前端Agent方向是明确趋势，说明前端工程师的价值在"设计Agent行为"而非"写UI"。面试中可以用来论证"前端在AI时代的定位"。
