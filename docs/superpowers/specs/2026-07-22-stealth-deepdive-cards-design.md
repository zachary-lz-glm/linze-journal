# stealth.html D · 实现细节深挖卡 · 设计文档

> 日期: 2026-07-22
> 状态: 待用户 review
> 范围: `learning/interview-tools/stealth.html` · proj 分类 · **4 张新增深挖卡**(前端项目/Manager 智能体/Code 智能体/PRD 工作流 各 1 张)
> 上游: `docs/superpowers/specs/2026-07-21-stealth-full-refactor-roadmap.md`(整体重构接力蓝图,D 子项目,§3「补每项目一张实现细节深挖卡」)
> 参照: `STEALTH-CARDS-GUIDE.md` §1/§6、A spec `2026-07-21-stealth-p0-frontend-mastercards-design.md`、B spec `2026-07-22-stealth-p1-ammo-dimensions-design.md`、C spec `2026-07-21-stealth-p2-ai-mastercards-design.md`(模板)
> 方法论: CLEAR-L(为什么这块是我做的)+ 三段推理链(自研/拒绝X因为Y代价Z)+ 诚实边界。深挖卡偏实现,**不套完整五步**(那是主陈述卡的事)

## 1. 背景与目标

整体重构主轴(roadmap §1):讲自己项目时填充词、流水账、自我矮化,讲"做了什么"不讲"为什么决策+代价+反思"。A(P0 老前端 5 张,kb-v324)/ C(P2 ai 14 张,kb-v326)/ B(P1 弹药卡 69 张补维度,kb-v327)已分别把**主陈述卡**(五步)、**机制弹药卡**(加段)两类范式验证有效。

D 是整体重构的**最后一个内容子项目**(之后只剩「PRD归位」+「跨场挖模式」)。roadmap §3 定义:给每个项目补**一张「实现细节深挖卡」**——用途是面试官追问"这个具体怎么设计的 / 给我讲讲实现细节 / 数据结构长什么样"时,能立刻翻出来深度展开。

**三类卡的分工(深挖卡占的生态位):**
- **主陈述卡**(A/C/三件套已改,五步):开场讲"为什么决策 + 代价 + 反思"。
- **机制弹药卡**(B 已补维度):被追问单点机制时答"我的取舍"。
- **实现深挖卡**(本轮新增):被追问"具体实现"时,讲**数据结构 / 关键算法 / 代码引用 / 踩坑**——比主卡更技术、比弹药更系统,是"我最得意那块工程怎么造的"。

**目标**:4 张 Form A 结构化实现卡,各聚焦一个项目的旗舰实现细节,经得起"具体怎么设计 / 给我看数据结构"追问,且**与该项目的现有主卡/弹药卡不重复**(主卡只点到决策层,深挖落到实现层)。

## 2. 范围

### 2.1 新增 4 张深挖卡(每项目 1 张,Form A)

| 项目 | data-g | 深挖主题 | 源码核对路径 | 插入锚点(主陈述卡) |
|---|---|---|---|---|
| 前端项目 | `前端项目` | 联动 DSL dAction + 双求值渲染引擎 | **无源码**(记忆+A spec §6.4 卡4素材+现有卡) | 「最有价值的项目:Schema 营销中台」(2860)后 |
| Manager 智能体 | `Manager 智能体` | 39节点状态图 + probe-before-plan 工程实现 | `agent-main/Manager_Agent/server/utils/managerGraph.graph.ts`(+ probe/node 文件) | 「这个项目 30 秒怎么说?」(646)后 |
| Code 智能体 | `Code 智能体` | 自研 JSON+内存余弦向量检索 | `agent-main/code_assistent_Agent/server/services/vectorSearch.ts`+`code_experience_vectors.ts`+`stores/codeStore.ts` | 「这个 Code Agent 到底是什么?」(809)后 |
| PRD 工作流 | `PRD 工作流` | /reference 6文件 SSOT 怎么蒸馏 | `/Users/didi/work/prd-tools/`(plugins/+docs/) | 「AI工作流完整介绍(面试第一答)」(2380)后 |

> 锚点取主陈述卡**唯一 title 子串**;assemble 脚本按 title 定位→depth 数到该卡闭合 `</div>`→在其后插入深挖卡(见 §7)。

### 2.2 排除(不在本轮)

- **不动 A/B/C/三件套已改已补的卡**(D 是纯新增,零修改现有卡 body)。
- **不重复**主陈述卡(五步决策层)和弹药卡(单点机制)已覆盖的内容——深挖卡只讲"实现细节"这个新维度。
- **不动 PRD 归位**(A4/A10/A5-prd 加 data-g + 物理移动)——那是独立的下一个子项目。
- **不扩到第二个细节/项目**(每项目只 1 张,共 4 张,见 §9 YAGNI)。

### 2.3 routing 改动(比 B 大,比 A 小)

4 张都 `data-c="proj"`,挂各自现有 data-g。**subOrder 不动**(4 个组都已在 subOrder 里;组内按 DOM 顺序展示,插对位置即可,见 §3.3)。assemble 是**插入新卡**(不是 B 的 body-swap),所以动 DOM 物理位置,但不动 data-g/subOrder/getGroup 逻辑。

## 3. 架构决策

### 3.1 形态:Form A 结构化实现卡(已与用户敲定)

4–5 段,每段 `<strong>领起标签。</strong>`,§6 declarative 参考卡风格(对标「从 PRD 到上线的完整链路」)。**必含四要素**(这是它与"纯技术流水账"的分界,也是 check 脚本的判据):

1. **数据结构 / 形态**——讲清楚长什么样(JSON schema / 6 文件结构 / graph 节点边 / dAction 语法)。
2. **核心算法 / 流程**——怎么跑(余弦 top-k / 蒸馏流程 / probe→plan / 双求值)。
3. **为什么自研、拒绝了什么 alternative + 代价**(CLEAR 的 L + 三段推理链)——e.g. Code 拒绝 Chroma、PRD 拒绝全量塞 PRD、Manager 拒绝 LLM 自主流转。
4. **踩坑 + 诚实边界**(eval / 局限)——e.g. "没接真实流量""研究型""框架先行没度量""内存全量算有规模上限"。

可选第 5 段:**代码引用**(如 `managerGraph.graph.ts:67-104`、`vectorSearch.ts`)。深挖卡讲实现,**允许带文件名/行号**,但**只进 body、绝不进 title**(title 是面试官口吻的问题)。

### 3.2 与五步主卡的分界(防重复)

主陈述卡 ③(关键决策)会点到技术选型,但停在"选了什么、拒绝了什么"。深挖卡**从 ③ 往下钻**:数据结构长什么样、算法怎么实现、代码在哪、踩了什么坑。两卡互补——主卡讲"为什么这么决策",深挖讲"这个决策的工程怎么落地"。每张深挖卡的 §6 骨架(见 §5)显式注明"主卡已覆盖的别重复"。

### 3.3 插入位置:主陈述卡正后方(已敲定)

深挖卡插在**该项目主陈述卡正后方**,不是"最相关机制卡"后。理由:
- 深挖卡概念上是"主故事背后的实现",紧跟 opener 最自然。
- 面试时"翻主卡"的本能能顺带翻到实现,不会被埋在组中间。
- 组内按 DOM 顺序展示(getGroup 只按 subOrder 排组、组内稳定排序保 DOM 序),所以 DOM 插对位置 = 显示位置,**无需 subOrder 改动**。

## 4. 事实校准策略

### 4.1 分项目源码核对

- **Manager / Code / PRD(有源码)**:执行阶段每项目派 1 个 agent **先读 agent-main / prd-tools 源码**,产出《该主题真实事实 + ✅⚠️❌ 清单》(数据结构、算法、雷区确认),再据此写卡。辅以 2 份深度说明书(`learning/ai-projects/Code-Assist-Agent-工程化代码助手.md`、`Manager-Agent-多智能体编排总管.md`)+ 校准文档(`learning/interview-kb/明日面试_预测题校准与匹配分析.md`)作 secondary。
- **前端(无源码)**:agent 靠 A spec §6.4 卡4 素材 + 现有卡(2860/2896)+ 记忆。数字一律⚠️软化,诚实边界显式("配置类页面、没接 C 端真实流量")。

### 4.2 §1.3 正向雷区(说了穿帮,写卡 agent 必须回避,check 脚本抽检)

- **Manager**:模型是阿里云 **qwen-flash**(非 Claude/GPT/Anthropic);12 Agent = **9 外 + 3 内**(非 8+4);失败归因**纯规则**(非 LLM);**自动晋级默认关**;Checkpoint 自建 16 字段快照。
- **Code**:向量检索**自研 JSON+内存余弦**(非 Chroma);增量靠 **sha256**(非 git 钩子);**没有** Diff 预览用户确认才执行 / 独立代码审查 Agent / HITL 写确认。
- **PRD**:prd-tools 是 **Claude Code 插件**(/reference + /prd-distill),非 SDD 平台、不直接生成代码;**"prd2code-gen 6 步闭环"不存在**;**"20+ 人团队"软化**(ADR-0005 写 1-5 人);"5h→2h"是前后工时对比、非严格 AB。

原则:不确定的数字软化("大概/约/小范围验证过")或省略。**绝不编百分比/提升倍数/团队规模。** agent 项目数字必须核对源码再写;核对不到的,宁可少写也不编。

## 5. 深挖卡模板(Form A 四要素)

HTML 沿用 GUIDE §2.2 卡片模板 + 现有 `<p><strong>段首领起。</strong>` 约定(不加新 class、不加新子组)。core 一句带机制名 + 结构的浓缩(像"自研 JSON+余弦——不引 Chroma,内存里跑语义召回")。

### 骨架(每张按四要素展开,顺序可微调)

```
core: <机制名>——<一句话讲清怎么造的 + 关键取舍>

<p><strong>数据结构 / 形态。</strong>……长什么样(JSON/6文件/graph节点边/dAction语法)……</p>
<p><strong>核心算法 / 流程。</strong>……怎么跑(余弦top-k/蒸馏/probe→plan/双求值)……</p>
<p><strong>为什么自研、拒绝了什么。</strong>自研 X(拒绝 Y 因为 Z,代价 W)……</p>
<p><strong>踩坑和边界。</strong>……(诚实:没接真实流量/研究型/规模上限/框架先行没度量)……</p>
[可选]<p><strong>代码在哪。</strong>`file.ts:行号` ……</p>
```

### 硬约束(carryover from A/B/C)

- **§6 declarative 风格**,禁口语碎嘴(说白了/得说句实话/我自己比较得意/被问X我答/这套东西/你就懂了/听着像)。
- **strong 标句首自然词**,不孤立、念着不顿;每段 strong 领起(≥4 段)。
- **数字按 §4.2 软化**,不编;agent 项目核对源码。
- ①② 只内联枚举(如需要),不堆①②③④⑤ 速查表腔。
- **不重复主卡/弹药卡内容**:§6 每张骨架显式标"主卡已点过 X,深挖别重复,落到实现层"。
- **诚实边界显式**:四要素第 4 项不可省(防纯技术流水账——storytelling memory 点名的头号反模式)。

## 6. 四张卡内容骨架

### 6.1 前端:联动引擎怎么从零造的——dAction 双求值(无源码)

- **core**:联动引擎从零造——dAction 声明式 DSL,渲染期+运行期双求值,400+ 组件按需渲染不卡
- **数据结构/形态**:dAction 联动 DSL——组件依赖从命令式 if-else 变成声明式模板表达式(组件 A 的值 → 组件 B 的 disabled/选项),联动引用、循环依赖、字段类型可静态校验。
- **核心算法/流程**:injectDActions 双求值——渲染期先求值一遍出初始状态(解决 SSR 初始态不对,不用等前端 JS 加载),运行期再求值响应用户操作;联动走精确更新(只重渲染受影响组件,非全量)。
- **为什么自研/拒绝**:从零设计渲染引擎(**拒绝现成 Formily/Ajv**:联动描述力不够、黑盒、双求值做不到);虚拟滚动+按需渲染(**拒绝全量重渲染**:400+ 组件卡死);Rollup+tree-shaking(**拒绝整包**:体积)。
- **踩坑/边界**:这套引擎是为**配置类页面**设计的,不直接迁移 C 端自由布局/数据可视化大屏;400+ 是组合数非组件数;为内部国际化业务设计(诚实:非公开 C 端真实流量产品)。
- **主卡已覆盖不重复**:2860 主卡已讲"配置表达力 vs 可控性"决策层;深挖落到 DSL 语法 + 双求值引擎实现。素材来自 A spec §6.4 卡4 + 现有 2896。
- **数字档**:400+(组合数 ✅)/ 24 基础·30-40 定制组件(✅)/ 35 动态渲染(⚠️软化"三十多个")。

### 6.2 Manager:39 节点状态图是怎么搭出来的(源码:managerGraph.graph.ts)

- **core**:硬编码状态图——节点显式,probe 排在 plan 前先探下游真实状态再让模型规划
- **数据结构/形态**:graph 拓扑(节点/边/条件边),每个节点对应一个我想显式解决的决策或踩过的坑;managerTask 协议在节点间流转(待源码核实字段结构)。
- **核心算法/流程**:probe-before-plan——先并行探一遍下游(9 外 3 内 Agent 的能力/真实状态)再让模型 plan,否则模型脑脑补下游状态;硬编码状态机驱动,非 LLM 自主流转。
- **为什么自研/拒绝**:用硬编码状态机(**拒绝 LLM 自主流转**:可控性/可观测/可单测/每条边能讲清);probe 排 plan 前(**拒绝直接 plan**:模型脑补下游状态)。
- **踩坑/边界**:39 是结果非设计目标(每个节点对应一个显式决策/坑);本质研究型、**没接真实流量**;**自动晋级默认关**;失败归因**纯规则**非 LLM。
- **主卡已覆盖不重复**:646 主卡(30 秒)讲定位;658 讲主干链路流程、703 讲 managerTask 协议是什么、795 讲"39 是不是过度设计"。**深挖落到 graph 拓扑怎么设计 + probe-before-plan 的工程实现**,不复述链路/协议/复杂度。
- **待源码核实**(`managerGraph.graph.ts` + probe 节点文件 + `routeAgentOrder.ts`):节点/边/条件边的真实结构;probe 具体探什么、怎么并行;managerTask 的关键字段;"39"是否准确(不准则软化或用"几十个")。
- **雷区**:qwen-flash 非 Claude/GPT · 12Agent=9外3内 · 失败归因纯规则 · 自动晋级默认关。

### 6.3 Code:向量检索为什么不用 Chroma、自研怎么实现(源码:vectorSearch.ts)

- **core**:向量检索自研不引 Chroma——JSON 存向量,内存跑余弦 top-k,sha256 增量只重算变了的
- **数据结构/形态**:JSON 存 {id / 向量 / text / sha256},全量加载进内存(待源码核实 code_experience_vectors 的真实字段)。
- **核心算法/流程**:内存余弦相似度,top-k 召回;sha256 比对文件内容,变了才重算向量(增量),没变的不重算。
- **为什么自研/拒绝**:自研 JSON+余弦(**拒绝 Chroma 等向量库**:依赖重、研究型规模小、零依赖更可控);sha256 增量(**拒绝 git 钩子/全量重算**:全量重算贵、git 钩子耦合仓库)。
- **踩坑/边界**:研究型、**没接真实流量**;内存全量算有**规模上限**(诚实承认,点"若上量会换近似检索/落库");召回质量小范围验证过,非大规模 benchmark。
- **主卡已覆盖不重复**:809 主卡讲 Code Agent 整体定位;858 讲"语义检索 vs 全量 context"的取舍、964 讲 AsyncLocalStorage。**深挖落到自研向量检索的数据结构 + 余弦算法 + sha256 增量的实现**,不复述取舍/上下文。
- **待源码核实**(`server/services/vectorSearch.ts` + `code_experience_vectors.ts` + `stores/codeStore.ts`/`server/utils/files.ts`):JSON 真实结构;余弦实现;sha256 怎么用、增量粒度;top-k;embedding 来源/维度。
- **雷区**:自研非 Chroma · 增量 sha256 非 git 钩子 · 无 Diff 预览确认/独立审查 Agent/HITL 写确认。

### 6.4 PRD:reference 蒸馏的 6 个文件具体怎么来的(源码:prd-tools/plugins/)

- **core**:reference 把项目知识蒸馏成 6 个领域文件——每个事实只存一处,根除 AI 编造空间
- **数据结构/形态**:6 个领域文件每个存什么(待源码核实具体哪 6 个 + schema),单一事实源原则——同一事实只存一处。
- **核心算法/流程**:/reference 命令怎么扫项目→蒸馏→6 文件;/prd-distill 怎么消费 6 文件出计划;每个事实只存一处(同一事实散多处 = AI 挑顺口的用 = 编造空间)。
- **为什么自研/拒绝**:单一事实源(**拒绝多处冗余存储**:AI 挑顺口的编造);6 文件按领域切(**拒绝一个大文件/全量塞 PRD**:打爆 context、无法按需引用);Claude Code 插件形态(**拒绝独立 SDD 平台**:轻量、复用 CC 能力)。
- **踩坑/边界**:团队模式 **Pull-based 禁止主动搜源码** → 准确率 60% 损耗(对单仓 80%);"5h→2h"是前后工时对比、**非严格 AB**;团队规模按 ADR-0005 是 1-5 人小范围试用(非生产级铺开)。
- **主卡已覆盖不重复**:2380 主卡(面试第一答)已点名"6 文件/8 证据类型/Readiness 85-60-60/negative_code_search"。**深挖只落到 /reference 这 6 个文件具体怎么蒸馏出来的**(命令流程 + 文件 schema + 单一事实源怎么保证),**不复述证据链/门控/Readiness**(那些是别的机制,留主卡)。
- **待源码核实**(`/Users/didi/work/prd-tools/plugins/` + docs/):/reference 命令的真实实现;6 个领域文件具体是哪 6 个、schema;/prd-distill 流程;"6"是否准确。
- **雷区**:插件非 SDD 平台 · "6 步闭环"不存在 · 不直接生成代码 · "20+ 人"软化 · 5h→2h 非严格 AB。

## 7. 实施流程(GUIDE §3/§6.6 多 agent,复用 A/B/C 模板)

1. **备份**:`cp stealth.html stealth-source-current.html`
2. **重建 check 脚本**(`check_d.py`,从 `check_p1.py` 复制改造):
   - carryover:禁口语碎嘴 / ①②③④⑤ 堆叠 / div 平衡 / 雷区词。
   - **删** B 的"只增不删长度校验"(D 是新卡,无原文可比)。
   - **删** B 的分档(tier),改为**四要素命中**:数据结构词(JSON/schema/结构/字段/文件/节点/边/拓扑/数据结构/存的是)+ 算法词(算法/流程/余弦/top-k/召回/求值/蒸馏/扫描/匹配/计算)+ 拒绝词(拒绝/本可以/没选/而不是/instead/自研)+ 诚实边界词(没接/研究型/诚实/局限/上限/框架先行/规模)。四类各至少命中一个 → warn 不命中(语义靠人工抽检,不阻塞)。
   - **加** §6 strong 段结构:`<strong>领起标签。</strong>` 段数 ≥ 4。
   - **加** `--project front|mgr|code|prd` 入参:雷区**按项目应用**(check_d.py 单次校验一张卡,必须知道它是哪个项目,否则误报——如 Code 卡合法写"不用 Chroma",但 PRD 卡出现"Chroma"就是错)。**全项目 err**:含"6 步闭环"。**Code 专属 warn**:出现"Chroma"须在"不用/拒绝/instead"语境内、出现"git 钩子"须是"不用"语境。**Manager 专属 warn**:出现"Claude/GPT/Anthropic"须是对比非自述模型。雷区皆 warn(靠人工抽检,非 err 阻塞,同 check_p1.py 思路:naive 子串在"拒绝"语境会误报)。
3. **并行派 4 个 agent 产深挖卡 HTML 片段**:
   - **Agent-前端 dAction**(无源码:靠 A spec §6.4 卡4 + 现有卡 2860/2896 + 记忆 + §4.2 软化)
   - **Agent-Manager graph**(**先读 `managerGraph.graph.ts` + probe 节点 + `routeAgentOrder.ts`** 产事实清单,再写卡)
   - **Agent-Code 向量**(**先读 `vectorSearch.ts` + `code_experience_vectors.ts` + `codeStore.ts`/`files.ts`** 产事实清单,再写卡)
   - **Agent-PRD reference**(**先读 `prd-tools/plugins/` + docs** 产事实清单,再写卡)
   - 每个 agent 必读:GUIDE §1/§6 + 本 spec §5 四要素模板+硬约束 + §6 该卡骨架 + §4.2 雷区 + stealth-source-current.html 该项目主卡原文(避免重复)。
   - **prompt 写死"只产出该 1 张深挖卡的 HTML 片段到独立文件,禁碰 stealth.html、禁碰其他卡、禁碰 GUIDE/README/配置"**(memory [[agent-scope-constraint]])。agent 项目 agent 还要写死"先读指定源码产事实清单,数字核对不到就软化或省略,绝不编"。
4. **校验产物**:`check_d.py <片段> --project front|mgr|code|prd` 逐张跑 4 个片段,四要素命中 + strong≥4 + 雷区 warn 为 0 人工确认通过 + div 平衡。
5. **组装**(`assemble_d.py`,**新写**——D 是新增卡,assemble 是**插入**非 body-swap):
   - 按 4 个主陈述卡 title 子串定位(§2.1 锚点)→ depth 数到该卡闭合 `</div>` → 在其后插入深挖卡 HTML(原子写 + 全文 div 平衡断言)。
   - **不动**任何现有卡 body/data-g/subOrder/title。
6. **数字抽检**:对照 §4.2 雷区 + 各卡"待源码核实"项,grep 确认 4 张没把 Manager 说成 Claude/GPT、向量说成 Chroma、增量说成 git 钩子、PRD 说成 SDD/6 步闭环。
7. **quickbar 分组抽检**:4 张深挖卡在各自 data-g 组里、显示在主卡正后方、tab 计数正确。
8. **bump `sw.js`** 的 `CACHE_NAME`(origin 已部署 kb-v327 → **kb-v328**,bump 前必看 origin,kb-v325 撞号教训: `git show origin/main:sw.js | grep CACHE_NAME`)+ 个人账号 `git push origin main`(remote origin 已指向 github-personal:zachary-lz-glm)。

## 8. 质量门(GUIDE §5)

- [ ] 4 张深挖卡都 Form A 四要素齐全(数据结构 + 算法 + 自研/拒绝 + 踩坑/边界),strong 段 ≥ 4
- [ ] 每张落到"实现层",不重复主卡(决策层)/弹药卡(单点机制)已覆盖内容
- [ ] 每张诚实边界显式(四要素第 4 项非空,防纯技术流水账)
- [ ] agent 项目(Manager/Code/PRD)关键数字核对过源码;前端数字已软化
- [ ] §4.2 雷区 0 命中(6 步闭环 err;Chroma/git钩子/Claude/GPT 仅在"拒绝/对比"语境)
- [ ] 4 张挂对 data-g、`data-c="proj"`、插在主卡正后方、subOrder 未动、quickbar 分组正常、tab 计数正确
- [ ] §6 declarative 风格,无口语碎嘴;①② 只内联不堆①②③④⑤
- [ ] title 是面试官口吻问题、无英文项目名前缀、无文件路径(代码引用只进 body)
- [ ] A/B/C/三件套现有卡 body 未动
- [ ] div 平衡,`<script>` 完整
- [ ] sw.js bump kb-v327→kb-v328(看 origin 已部署 +1)

## 9. 不做什么(YAGNI)

- 每项目**只 1 张**深挖卡(共 4 张),不贪多、不加第二个细节
- 不动 A/B/C/三件套已改/已补的现有卡(D 纯新增,零修改现有 body)
- 不重复主陈述卡/弹药卡已覆盖的内容(深挖只讲实现细节新维度)
- 不为深挖卡套完整五步(Form A 是实现深挖,不是项目主陈述)
- 不引入新子组/tab、不动 data-g/subOrder/getGroup 逻辑(挂现有 data-g,组内 DOM 序)
- 不做 PRD 归位(A4/A10/A5-prd 加 data-g+物理移动)——独立下个子项目
- 不全面校准所有数字(agent 项目只核对"待源码核实"项 + §4.2 雷区,前端一律软化)

## 10. 记给未来(本轮不进,留给后续)

- **PRD 归位子项目**:A 厘清出的 A4/A10/A5-prd 加 data-g="PRD 工作流" + 物理移动到 PRD 区 + 软化 A10"20+ 人"(roadmap + A/B spec 均记)。
- **跨场挖模式**(roadmap §6 最值):reviews/ 40+ 实录挑 3-5 场系统读,提炼跨场复现的 Top3 表达失分模式——D 完成后整体重构的内容部分就收尾了,剩这一个调研项。
- **无 data-g 的老项目追问卡**(A1-A10/Monorepo/联动引擎/版本管理等 ~15-20 张):若后续要补,先立"P1.5 老追问卡补 data-g + 维度"子项目。
