# stealth.html P2 ai 分类卡表达重构 · 设计文档

> 日期: 2026-07-21
> 状态: 待用户 review
> 范围: `learning/interview-tools/stealth.html` · ai 分类 · 14 张「项目/能力主张」卡(10 全改 + 4 轻过)
> 上游: `docs/superpowers/specs/2026-07-21-stealth-full-refactor-roadmap.md`(整体重构接力蓝图,P2 子项目)
> 参照: `STEALTH-CARDS-GUIDE.md` §1/§6、A 的 spec `2026-07-21-stealth-p0-frontend-mastercards-design.md`(模板)
> 方法论: CLEAR-L + 五步逐字稿 + tentpole + 5Why + 三段推理链 + 诚实边界(三件套主卡 + A 已验证)

## 1. 背景与目标

整体重构主轴(roadmap §1):讲自己项目时填充词、流水账、自我矮化,**讲"做了什么"不讲"为什么决策+代价+反思"**。三件套主卡(9cec423)+ A·P0 老前端 5 张(77d9084, kb-v324)已验证五步范式有效。

本轮把范式复制到 **P2 ai 分类卡**。勘察结论:ai 65 张裂成 3 个 genre,对五步适配度差很大——
- **20 张问答弹药**(纯知识点 10 + 速查表 10):温度/Token/Attention/benchmark罗列/调参速查,**不该套五步**(套了别扭),留作弹药(平行 A 的 10 张保留卡)。
- **8 张系统设计**:大多"假设性设计/方法论"genre(`从0设计企业级Coding Agent平台`/`scale到十万文件`),且已成熟(带源码+tradeoff+诚实边界)。五步的"①真实 ownership+④真数字 eval"对假设性题适配弱。**本轮只拎出其中 2 张真实 Manager 项目叙事**(4020/4085),其余 6 张跳过。
- **37 张五步雏形**:半截 STAR,缺 ownership+②本质矛盾+⑤方法论,**五步主战场**。本轮从中挑 12 张(10 全改 + 2 标杆轻过)。

**目标**:挑 14 张有真实项目/判断力主张的 ai 卡——10 张套五步重写、4 张已成熟卡轻过对齐——补齐 ②本质矛盾 + ⑤方法论 + ownership,经得起"为什么这么做/代价/换你怎么办"追问。纯概念/速查弹药保留。

## 2. 范围

### 2.1 全改 10 张(套五步重写 card-body,补 ownership+②+⑤)

**Agent 设计内核 5 张:**

| 卡 | 行 | data-g | 标题 | 项目锚点 |
|---|---|---|---|---|
| C1 | 3350 | Agent 基础 | 从零设计一个 Agent,你的思路是什么 | code_assistant 18 工具 / prd-tools Reference |
| C2 | 3386 | Agent 基础 | Agent 的记忆怎么设计:短期、长期、工作记忆 | prd-tools Reference/Spec/Plan |
| C3 | 3413 | Agent 基础 | Agent 的工作记忆怎么管,对话越来越长咋办 | Manager 16 字段 Checkpoint |
| C4 | 3483 | Loop 工程 | Harness Engineering:Agent 等于 Model 加 Harness | Manager / code_assistant |
| C5 | 3495 | Loop 工程 | Agent 自进化闭环怎么设计 | Manager Self-Evolution |

**选型与检索决策 5 张:**

| 卡 | 行 | data-g | 标题 | 项目锚点 |
|---|---|---|---|---|
| C6 | 3362 | Agent 基础 | 什么场景才该上 Agent,别什么活都套 Agent | 判断框架三层 |
| C7 | 3566 | Agent 基础 | Agent 框架怎么选(LangGraph vs…) | Manager 选 LangGraph |
| C8 | 3582 | Agent 基础 | ReAct vs Plan-and-Execute vs Reflexion | prd-tools Plan-Execute / code 轻 Reflexion |
| C9 | 3622 | Agent 基础 | 单 Agent 还是多 Agent(决策树) | Manager 9 外+3 内 |
| C10 | 3673 | RAG 检索 | 向量库怎么选(为什么自己写不用 Chroma)⭐ | code 自研 JSON+余弦 |

### 2.2 轻过 4 张(已成熟,补 ②⑤ 显式 + 去堆名词 + 对齐 declarative,不大改)

| 卡 | 行 | data-g | 标题 | 现状 |
|---|---|---|---|---|
| C11 | 4539 | Agent 基础 | Agent Safety 怎么做——规划层加执行层 | 双项目对照+红线暴露,五步高级形态 |
| C12 | 4549 | RAG 检索 | 向量召回 vs 代码实体图——我两个项目各做了一个 | 双项目对照,五步高级形态 |
| C13 | 4020 | 系统设计 | 把 39 节点的多智能体编排瘦身重构 | 真实 Manager 重构叙事,带源码引用 |
| C14 | 4085 | 系统设计 | 设计通用 Multi-Agent 调度系统(Manager 经验升华) | Manager 升华到通用模式,带源码引用 |

### 2.3 跳过 51 张(不动)

- 纯知识点 10:[3337][3400][3437][3447][3459][3511][3524][3781][3791][3836]
- 速查表 10:[3741][3804][3826][3848][3860][3871][3884][3895][3919][3940][3988]
- 系统设计假设性方法论 6:[4003][4038][4058][4109][4131][4154]
- 其余不在本轮的五步雏形(行业视野/工具协议/AI 评测/LLM 工程里偏主张的,留后续或并入 B)

### 2.4 不动路由(比 A 简化)

14 张全部已显式挂 data-g(Agent 基础 / Loop 工程 / RAG 检索 / 系统设计),**不加新 data-g、不动 subOrder、不删卡**。assemble 脚本只做 body swap。

## 3. 架构决策

### 3.1 双层结构(carryover)
- **主陈述/能力主张卡**(本轮 14 张):开场/被让展开时用,套五步
- **问答弹药**(20 张 + 系统设计方法论):被追问单点概念/速查时用,保留

### 3.2 全改 vs 轻过(本轮核心区分)
- **全改 10 张**:card-body 五步重写,补 ownership + ②本质矛盾 + ⑤方法论;check 脚本强校验(≥5 段 `<strong>`)。
- **轻过 4 张**:不重写,只补/对齐——确保 ②⑤ 显式、去堆名词、declarative 风格;check 脚本放宽(≥4 段)。这 4 张同时充当本轮全改卡的**内部风格标尺**。

### 3.3 无 routing 工作(比 A 简化的点)
A 要给 5 张加 `data-g="前端项目"` + subOrder 补值。C 的 14 张已有 data-g,**零 routing 改动**。assemble 只 title-locate + body-swap。

### 3.4 标题修剪(optional,默认保留)
14 张标题基本符合铁律(无英文项目名前缀)。两处可选修剪(执行时定):
- [3566] `Agent 框架怎么选:LangGraph vs LangChain vs AutoGen vs CrewAI vs Dify vs Coze` → 尾巴冗长,可缩为 `Agent 框架怎么选(LangGraph vs…)`
- [4085] `设计通用 Multi-Agent 调度系统(Manager 经验升华)` → 去括注 `(Manager 经验升华)`?

其余 12 张标题保留。修剪与否不影响 assemble(标题当锚点,改标题放最后做,同 A)。

### 3.5 Agent 分工(3 个,5+5+4,各一个连贯主题)
- **Agent-1「Agent 设计内核」(C1-C5,5 全改)**:Agent 怎么造/记/转。跨 Agent 基础+Loop 工程。
- **Agent-2「选型与检索决策」(C6-C10,5 全改)**:判断框架 + 选型 tradeoff + 向量自研。跨 Agent 基础+RAG。
- **Agent-3「标杆对齐」(C11-C14,4 轻过)**:已成熟卡轻过 + 当风格标尺。跨 Agent 基础+RAG+系统设计。

每个 agent 产独立 `.p2-card*-*.html`,prompt 写死"只产指定卡 body 片段到独立文件,禁碰 stealth.html、禁碰其他卡"(memory [[agent-scope-constraint]])。主会话统一 assemble,避免并发改同一文件(GUIDE §4.6)。

## 4. 事实校准策略(简单方案:复用现有清单)

用户定调:数字无所谓,按简单方案——**不派 agent 重读 `agent-main/` 源码**。直接把以下现有 ✅⚠️❌ 清单喂给写卡 agent:

### 4.1 现有清单来源
- `learning/interview-kb/明日面试_预测题校准与匹配分析.md`(已公开校准清单)
- memory + roadmap §5 雷区(见 4.2)
- 14 张卡现有原文(从 `stealth-source-current.html` 抽取,保留已校准的数字)

### 4.2 §1.3 正向雷区(说了穿帮,写卡 agent 必须回避)——这是 check 脚本要抽检的
- **Manager 模型是阿里云 qwen-flash**,不是 Claude/GPT/Anthropic
- **12 Agent = 9 外 + 3 内**(不是 8+4)
- **失败归因纯规则**,不是 LLM 归因
- **自动晋级默认关闭**
- **Checkpoint 是自建 16 字段快照**
- **Code 向量检索是自研 JSON+内存余弦**,不是 Chroma
- **增量靠 sha256**,不是 git 钩子
- **Code 没有** Diff 预览用户确认才执行 / 独立代码审查 Agent / HITL 写确认
- **prd-tools 是 Claude Code 插件**(/reference + /prd-distill),不是 SDD 平台、不直接生成代码;"6 步闭环"不存在
- **"20+ 人团队"要软化**(ADR-0005 写 1-5 人)

原则:不确定的数字软化("大概/约/小范围验证过")或省略。**绝不编百分比/提升倍数/团队规模。**

## 5. 主卡模板:五步骨架(carryover 自 A)

HTML 沿用 GUIDE §2.2 卡片模板 + 三件套 `<p><strong>段首领起。</strong>` 约定(不加新 class)。core 保留。card-body 改 5 段(轻过卡可 4 段):

| 段 | 五步 | 填什么 |
|----|------|--------|
| ① | 业务问题 + 为什么重要 + ownership | 解决什么、不解决会怎样、"我在里面 drive 了什么"(不堆技术栈) |
| ② | **本质矛盾** | 难点本质(非堆功能/非更大模型)——⭐本轮重点补 |
| ③ | 关键决策 + 拒绝了什么 alternative | 每个高杠杆决策讲"为什么选 + 拒绝了什么" |
| ④ | 结果 + 怎么验证(eval 非 vibes) | 指标 + 怎么知道 work + 可复用价值 |
| ⑤ | **方法论 + 局限/下次** | 可迁移命名框架 + 诚实边界——⭐本轮重点补 |

硬约束(carryover):
- **主卡开场不堆技术栈**(impact not technology names)。
- ③每个决策讲"拒绝了什么 alternative"。
- ⑤诚实边界显式化(局限/下次怎么做)。acknowledge gaps still get hired。
- §6 declarative 风格,禁口语碎嘴(说白了/得说句实话/我自己比较得意/被问X我答/这套东西/你就懂了)。
- ①②只内联枚举,不堆①②③④⑤速查表腔。

## 6. 14 张卡内容骨架

> 以下五步要点是**骨架锚点**。写卡 agent 必读:本节对应卡要点 + §4 雷区 + stealth-source-current.html 该卡原文(保留 core 和好句、保留已校准数字),产出 verbatim card-body。

### 全改 10 张

#### C1 [3350] 从零设计一个 Agent
- ① 设计 Agent 的通用思路——不是堆工具,是先定"目标可控性"(何时停/谁来批)再配能力。我在 code/prd-tools 两个项目都从零设计过。
- ② 核心矛盾 = **自主性 vs 可控性**:自主权越多能力越强,但越易失控/难 debug。本质是在两者间定边界,不是堆功能。
- ③ 分层(规划定目标+执行调工具+校验把关);HITL 闸门(**拒绝全自主跑完**——生产要人确认);工具小而可组合(**拒绝一个大工具全包**——不可组合)。
- ④ code_assistant 自验证自修复(max_iter+Readiness);prd-tools /reference+/prd-distill 分阶段。eval:每层可观测/可单测/可回放。
- ⑤ 「**先定可控边界再配能力,而非堆工具**」。局限:两项目偏研究型/小范围,没接大规模真实流量;HITL 路径是已知改进。

#### C2 [3386] Agent 记忆怎么设计
- ① 记忆不是"塞越多越好",是分层管理不同生命周期信息。prd-tools 用 Reference(长期)/Spec(本次任务)/Plan(执行轨迹)三层。
- ② 矛盾 = **召回相关性 vs 上下文成本**:全塞相关性高但贵且 lost-in-middle,不塞又丢信息。本质是分层+按需注入。
- ③ 三层划分;按需注入(**拒绝全塞 context**——成本+噪声);结构化优先精确指令(**拒绝纯向量模糊召回**——键值指令用结构化)。
- ④ Reference 作压缩层复用省 token;Plan 可回放断点续。eval:context 长度可控、关键信息不丢。
- ⑤ 「**记忆分层+按需注入,不是全塞 context**」。局限:prd-tools 记忆为 PRD 蒸馏定制;通用 Agent 向量长期记忆我没做。

#### C3 [3413] 工作记忆怎么管/对话长了咋办
- ① 长对话/多步任务工作记忆爆掉是通病。Manager 用自建 16 字段 Checkpoint 快照。
- ② 矛盾 = **保留执行历史 vs 窗口预算**:全留则窗口爆/模型分心,全砍则丢断点。本质是有损压缩+checkpoint。
- ③ Checkpoint 快照(**拒绝裸塞对话历史**);有损摘要+关键槽位保留(**拒绝无差别截断**——丢决策点);断点续跑(失败从 checkpoint 恢复)。
- ④ 16 字段快照可恢复;长任务不爆窗口。eval:断点续跑能续上、关键状态不丢。
- ⑤ 「**工作记忆=有损压缩+checkpoint,不是无差别截断**」。局限:16 字段为 Manager 任务流定制;hierarchical summary 等通用对话压缩我没深做。

#### C4 [3483] Harness Engineering
- ① Agent ≠ 模型,Agent = 模型 + Harness(工具调度/状态/校验/恢复的工程脚手架)。两项目都搭了 harness。
- ② 矛盾 = **给模型自由度 vs 加约束护栏**:harness 太薄则模型乱跑,太厚则僵化抵消模型能力。本质是工程化"可控的自主"。
- ③ 分层 harness(工具/编排/校验);KSG 关键状态门 + Ratchet 只进不退(**拒绝裸调模型等结果**);失败恢复(**拒绝失败即终止**)。
- ④ Manager 39 节点 + code 自验证自修复都是 harness 落地。eval:失败可恢复、状态可观测。
- ⑤ 「**Agent=模型+harness,价值在 harness 不在模型调参**」。局限:shadow-only/部分机制是已知改进方向,非全量生产。

#### C5 [3495] Agent 自进化闭环怎么设计
- ① 自进化是 Agent 从自身运行学习改进。Manager 设计了 Self-Evolution 机制。
- ② 矛盾 = **学习信号 vs 统计可靠性**:单次反馈噪声大,直接学会把坏经验固化。本质是要统计护栏,不是裸学习。
- ③ 四步闭环(采集/归因/实验/回滚);失败归因纯规则(**拒绝 LLM 归因**——不可靠);shadow-only 默认(**拒绝直接上线学习结果**)。
- ④ Manager Self-Evolution 跑 shadow 模式。eval:有 hold-out/对照,不靠 vibes。
- ⑤ 「**自进化必须配统计护栏+shadow,不能裸学**」。局限:目前 shadow-only,没接真实流量大规模验证——诚实边界;统计严谨性是后续。

#### C6 [3362] 什么场景才该上 Agent
- ① 不是什么活都套 Agent。我有判断框架(三层)。
- ② 矛盾 = **自主性收益 vs 不可控成本**:Agent 适合路径不确定/需动态决策的;确定路径用 workflow 更稳更便宜。本质是按不确定性选范式。
- ③ 判断三层(路径确定→workflow;路径动态/需工具组合→Agent;单轮问答→直接 LLM);**拒绝"什么都要 Agent"**的 over-engineering。
- ④ Manager 走 Agent(多步动态)、prd-tools 部分 workflow 化。eval:按场景匹配,非一刀切。
- ⑤ 「**按不确定性选范式,Agent 不是万能**」。局限:框架是经验归纳,边界 case 靠判断。

#### C7 [3566] Agent 框架怎么选
- ① 框架选型,我为 Manager 选了 LangGraph。我是选型决策者。
- ② 矛盾 = **框架能力 vs 可控性/学习成本**:全功能框架(LangChain)抽象高但黑盒;裸写可控但重复造轮。本质是按可控性需求选抽象层级。
- ③ LangGraph(状态机显式可控,**拒绝 LangChain 全家桶黑盒** / **拒绝裸写重复造轮**);六框架矩阵对比。
- ④ Manager 39 节点状态机用 LangGraph 显式表达。eval:节点/边可观测可调试。
- ⑤ 「**框架选型按可控性需求选抽象层级**」。局限:LangGraph 学习曲线;小项目其实不必上重框架。

#### C8 [3582] ReAct vs Plan-and-Execute vs Reflexion
- ① 三种 Agent 范式选型。两项目分别用不同范式。
- ② 矛盾 = **思考-行动耦合度 vs 计划稳定性**:ReAct 灵活但易发散;Plan-Execute 稳但僵;Reflexion 靠反思纠偏但慢。本质是按任务可计划性选耦合度。
- ③ prd-tools 用 Plan-Execute(PRD 流程可预拆);code_assistant 用轻 Reflexion(自验证自修复循环);**拒绝一种范式打天下**。
- ④ 按任务特性匹配范式。eval:各场景行为符合预期。
- ⑤ 「**范式按任务可计划性选,不迷信某一种**」。局限:我的 Reflexion 是轻量版,非完整论文实现。

#### C9 [3622] 单 Agent 还是多 Agent
- ① 单/多 Agent 决策。Manager 用了多 Agent(9 外+3 内 Supervisor+Worker)。
- ② 矛盾 = **专业化收益 vs 协调成本**:多 Agent 专业化强但协调/通信开销大;单 Agent 简单但 context 易混。本质是按专业化+context 隔离需求选。
- ③ 五问决策树(任务可拆?专业差异大?context 会混?…);Manager 多 Agent(9 外能力+3 内管理);**拒绝为了多而多**。
- ④ Manager 多 Agent 架构跑通。eval:专业化分工清晰、context 不混。
- ⑤ 「**单/多 Agent 按专业化+context 隔离需求选**」。局限:多 Agent 协调成本高,简单任务别上。

#### C10 [3673] 向量库怎么选(为什么自己写不用 Chroma)⭐
- ① 向量库选型,我选自研 JSON+内存余弦,不是 Chroma。我是 code_assistant 检索设计者。
- ② 矛盾 = **通用能力 vs 工程成本/可控性**:Chroma 功能全但引入依赖+运维,自研轻但能力有限。本质是按规模/场景权衡,不是"哪个更先进"。
- ③ 自研 JSON+内存余弦(**拒绝 Chroma**:量小不需要、重依赖);sha256 增量(**拒绝 git 钩子**:更轻);text-embedding-v3(现成 embedding)。
- ④ code 仓库规模小,自研够用零依赖。eval:召回准、增量快。
- ⑤ 「**选型按场景规模权衡,不追"更先进"**」。局限:自研只在量小才成立——规模上去必须上专业向量库;主动说的边界,不是藏。

### 轻过 4 张(补 ②⑤ 显式 + 去堆名词 + 对齐 declarative,保留双项目对照/源码引用)

#### C11 [4539] Agent Safety 怎么做
- 现已是五步高级形态(规划层+执行层双项目对照+红线暴露诚实边界)。轻过:补 ②(Safety 本质矛盾 = **防护 vs 不阻碍正常任务**——护栏太严抵消能力,太松则失控)显式化;去堆名词;对齐 declarative。保留 prd-tools+code_assistant 双项目对照。

#### C12 [4549] 向量召回 vs 代码实体图
- 双项目对照(code_assistant 向量 + prd-tools 正则实体图)已成熟。轻过:补 ②(两种检索本质差异 = **模糊语义匹配 vs 精确结构定位**)显式化;对齐风格。保留双项目红线。

#### C13 [4020] 把 39 节点的多智能体编排瘦身重构
- 真实 Manager 重构叙事(genre A,非假设性)。轻过+补五步:补 ①ownership(我是重构主导者)、②(瘦身矛盾 = **可观测性 vs 复杂度**——节点多则可观测但配置爆炸,合并则简但丢单测粒度)显式化。保留 `managerGraph.graph.ts:67-104` 源码引用 + 拆 subgraph/删合并/Critic 降级决策。

#### C14 [4085] 设计通用 Multi-Agent 调度系统(Manager 经验升华)
- Manager 升华到通用模式。轻过+补五步:补 ②(通用化矛盾 = **特化优化 vs 通用抽象**——太特化不通用,太通用失去 Manager 具体优势)显式化。保留 `retryBudget.ts`/`failureAttribution.ts` 源码引用 + 五大支柱。

## 7. 实施流程(GUIDE §3/§6.6 多 agent,复用 A 模板)

1. **备份**:`cp stealth.html stealth-source-current.html`
2. **重建 check 脚本**(`check_p2.py`,从 `check_mastercard.py` 复制改造):carryover 5 段 strong/禁口语/①②③④⑤堆叠/loop残留/div平衡;**删** A 的老前端雷区(#6)和硬数字(#7);**加** §4.2 正向雷区抽检(Manager≠Claude/GPT、向量≠Chroma、增量≠git钩子、prd-tools≠SDD、"20+人"硬数)。**全改/轻过阈值切换**:脚本接 `--light` 标志,默认全改卡 ≥5 段 `<strong>`,带 `--light` 时轻过卡放宽到 ≥4 段(校验时全改卡不带标志、轻过卡带 `--light` 分别跑)。
3. **并行派 3 agent 产 card-body 片段**(Agent-1 C1-C5 / Agent-2 C6-C10 / Agent-3 C11-C14):
   - 每个 agent 必读:GUIDE §1/§6 + 本 spec §5 五步模板+硬约束 + §6 该卡骨架 + §4 雷区 + stealth-source-current.html 该卡原文。
   - prompt 写死"只产指定卡 body 片段到独立文件,禁碰 stealth.html、禁碰其他卡"。
   - 轻过卡(Agent-3)prompt 注明"保留绝大部分原文,只补 ②⑤ 显式+去堆名词+对齐 declarative,不大改"。
4. **校验产物**:`check_p2.py` 跑 14 个 body 片段,全改卡 ≥5 段 strong、轻过卡 ≥4 段,雷区词 0。
5. **组装**(`assemble_p2.py`):title-locate + body-swap 14 张(原子写)。**不动** data-g/subOrder/标题(除非选做 §3.4 标题修剪,则最后做)。
6. **数字抽检**:对照 §4.2 雷区,grep 确认 14 张卡没把 Manager 说成 Claude/GPT、向量说成 Chroma 等。
7. **bump `sw.js`** 的 `CACHE_NAME`(origin 已部署 kb-v324 → **kb-v325**)+ 个人账号 push。

## 8. 质量门(GUIDE §5)

- [ ] 全改 10 张五步齐全,②本质矛盾 + ⑤方法论非空话
- [ ] 轻过 4 张 ②⑤ 已显式化、风格对齐 declarative、未过度改写
- [ ] 主卡开场不堆技术栈(impact not technology names)
- [ ] ③每个决策讲了"拒绝了什么 alternative"
- [ ] ④讲了"怎么验证(eval/metrics)",非 vibes;数字按 §4.2 软化(不确定的软化/省略)
- [ ] ⑤含局限/下次(诚实边界显式)
- [ ] §6 declarative 风格,无口语碎嘴
- [ ] ①②只内联枚举,不堆①②③④⑤
- [ ] §4.2 雷区 0 命中(Manager≠Claude/GPT、向量≠Chroma、增量≠git钩子、prd-tools≠SDD、无"20+人"硬数)
- [ ] 14 张 data-g/subOrder/标题未误动(除可选修剪);51 张跳过卡未动
- [ ] div 平衡,`<script>` 完整
- [ ] sw.js bump kb-v324→kb-v325(看 origin 已部署 +1)

## 9. 不做什么(YAGNI)

- 不动 51 张跳过卡(问答弹药 + 系统设计假设性方法论 + 其余五步雏形)
- 不加新 data-g / 不动 subOrder(14 张已有 data-g)
- 不派 agent 重读 `agent-main/` 源码(复用现有校准清单)
- 不全面校准所有 ai 数字(只按 §4.2 雷区软化可疑项)
- 不引入新子组/tab
- 不重写轻过 4 张(只补②⑤+对齐)
- 不删任何卡

## 10. 记给未来(本轮不进,留给后续子项目)

- **B(P1 弹药卡补维度)**:roadmap §3,proj 76 张机制卡按追问链重组 + 补 ownership/alternatives/eval。
- **D(深挖卡)**:每项目一张「实现细节深挖卡」。
- **「PRD 工作流卡归位」**(A 厘清出):A4/A10/A5-prd 部分加 data-g="PRD 工作流" + 物理移动 + 和 PRD 主卡对齐。
- **ai 其余主张卡**(本轮跳过的行业视野/工具协议/AI 评测/LLM 工程里偏主张的):若面试反馈需要,可开 C2 子项目套五步。
- **系统设计假设性方法论 6 张**(4003/4038/4058/4109/4131/4154):它们是"假设性系统设计答题"genre,适配五步弱,若要提升走"答题方法论标尺"而非五步重写,另立。
