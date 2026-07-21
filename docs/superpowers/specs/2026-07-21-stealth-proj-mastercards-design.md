# stealth.html 项目卡表达重构 · 设计文档

> 日期: 2026-07-21
> 状态: 待用户 review
> 范围: `learning/interview-tools/stealth.html` · proj 分类 · Agent 三件套(Manager / Code / PRD工作流)
> 参照: `STEALTH-CARDS-GUIDE.md` §1/§6、`learning/ai-projects/`、`learning/interview-kb/明日面试_预测题校准与匹配分析.md`

## 1. 背景与目标

用户面试项目表达的根子问题:卡里"做了什么"够了,"为什么这样思考、怎么沉淀方法论"缺。

参照方法论:
- 《算法工程师如何在面试中答出"高级感"》**五步公式**:定义问题 → 拆解问题 → 制定策略 → 呈现结果 → 抽象方法论(第 5 步拉开段位)
- Modern Descartes《ML/AI Engineer Interviewing》**Project Deep Dive** 顺序:motivation → problem → difficulties → impact → ancillary work

目标:给 Agent 三件套各**改造 1 张「项目主陈述卡」**,套五步骨架,补齐现有最弱的「本质矛盾②」和「方法论沉淀⑤」。机制弹药卡完全不动。

## 2. 范围

- ✅ Manager 智能体 / Code 智能体 / PRD 工作流 三件套,各 1 张主陈述卡(共 3 张)
- ❌ 老前端项目(Schema / 组件库 / 联动 / Monorepo)、AI 工具、机制弹药卡:本次不动
- ❌ 不动卡片路由 / 分组 / 标题 / 搜索机制

## 3. 架构决策

### 3.1 双层结构
- **主陈述卡**(本次改造):开场 30 秒~2 分钟用,套五步
- **机制弹药卡**(现有 76 张,不动):被追问单点机制时用,§6 declarative 风格

### 3.2 改造现有雏形,不另立新卡
三件套各已有 1 张主陈述雏形卡:
- Manager「这个项目 30 秒怎么说?」(data-g="Manager 智能体")
- Code「这个 Code Agent 到底是什么?」(data-g="Code 智能体")
- PRD「AI 工作流完整介绍(面试第一答)」(data-g="PRD 工作流")

改造方式:**保留 core 与标题**(好的速查问法、`data-kw`/路由已建),把 `card-body` 改写成五步。标题、`data-g`、`data-kw` 不动 → 零路由风险。

### 3.3 方法论⑤各讲各的
三件套⑤方法论沉淀各自独立命名,不强行统一到同一上位主线。

## 4. 事实校准策略

- 本机资源齐全:`/Users/didi/work/agent-main/Manager_Agent`(源码) + `learning/ai-projects/`(Manager / Code 说明书) + `learning/interview-kb/明日面试_预测题校准与匹配分析.md`(校准清单)。GUIDE 里 `D:/` 是 Windows 残留。
- 默认:数字沿用现有 stealth.html 卡里已校准过的(§1.3 已核对);主卡④结果要引入指标时,以现有卡的数字为准,可疑就软化。
- **§1.3 已知雷区必须回避**:
  - Manager:qwen-flash 非 Claude/GPT;12 Agent = 9 外 + 3 内;失败归因纯规则非 LLM;自动晋级默认关;Checkpoint 自建 16 字段快照
  - Code:向量检索自研 JSON + 内存余弦(非 Chroma);增量靠 sha256(非 git 钩子);无 Diff 预览确认 / 独立审查 Agent / HITL 写确认
  - PRD:prd-tools 真身是 Claude Code 插件(/reference + /prd-distill);"prd2code-gen 6 步闭环"**不存在**;"20+ 人团队"要软化(ADR-0005 写 1-5 人)

## 5. 主卡模板:五步骨架

HTML 结构沿用 GUIDE §2.2 卡片模板,`data-c="proj"` `data-g` 不变。core 保留。`card-body` 改为 5 段,每段 `<strong>段首领起。</strong>` 开头(§6 declarative,不口语碎嘴):

| 段 | 五步(融合 alexeygrigorev 叙事 + 证据链追问) | 填什么 | 现状 |
|----|------|--------|------|
| ① | **业务问题 + 为什么重要** | 解决什么、谁是客户、**不解决会怎样**(lead with problem/impact,不堆技术栈) | 雏形偏技术难点,缺业务后果 |
| ② | **本质矛盾** | 难点本质在哪(非模型更大 / 非堆功能) | ⭐三张均缺,本次重点补 |
| ③ | **关键决策 + 拒绝了什么** | 3 个高杠杆动作,每个讲**为什么选它、考虑并拒绝了什么 alternative** | 雏形有"怎么做"但缺 why + alternatives |
| ④ | **结果 + 怎么验证** | 指标 + **怎么知道它 work(eval/metrics,不是 vibes)** + 可复用价值 | PRD 有,Manager/Code 偏诚实边界 |
| ⑤ | **方法论沉淀 + 局限/下次** | 拔成可迁移框架 + **诚实边界:局限、失败、下次怎么做不同** | ⭐三张均缺,本次重点补 |

定位:core 先念(30 秒钩子,对应 MyEngineeringPath「30-Second Version」);5 段是"被让展开"的 2 分钟版。每段 scannable,不长篇。

**硬约束(读完 4 篇原文后强化):**
- **主卡开场不堆技术栈**。alexeygrigorev 原话:「frame around impact, not technology names('used LangChain and Pinecone')」。现有雏形 body 开场堆 Nuxt4 / LangGraph / Zod / monaco / web-tree-sitter——正是被点名的硬伤。**处理(已定)**:主卡 lead with 业务问题/影响,技术栈只在 body 最后一句带过(如「栈:Nuxt4+LangGraph」,不展开);详细技术栈留给机制弹药卡。
- ③ 每个决策必须讲"考虑过并拒绝了什么",不只"我选 X 因为 Y"。
- ⑤ 诚实边界显式化(局限 / 下次怎么做)。Modern Descartes / alexeygrigorev / 证据链三篇都强调 acknowledge gaps still get hired(GUIDE §1.4 一致)。

## 6. 三件套主卡内容骨架

### 6.1 Manager 主卡(改造「这个项目 30 秒怎么说?」)
- **core(保留)**:多 Agent 系统的"总管层"——统一 WebSocket 入口、语义路由与任务规划,调度 10+ 下游 Specialist,自己只编排不干活
- ①业务问题 + 为什么重要:多个 AI 能力(检索/改代码/爬取/多模态)各起服务、入口分散,用户在多个 Agent 间切换、状态不连续。**不解决=体验割裂、各能力重复造轮子、高风险动作无统一兜底**
- ②本质矛盾:多 Agent 系统的难点不在"单点能力"(单个 Specialist 谁都会做),在"编排可信"——路由判对了吗、中间状态丢了怎么办、高风险动作谁兜底
- ③关键决策 + 拒绝了什么:硬编码状态机(**拒绝 LLM 自主流转**:可解释/可控/可调试,黑盒难定位);Probe+Health 双探活(**拒绝单层探活**:假活/假死);Critic 节点(**拒绝单次 LLM 调用**:无校验回路);HITL checkpoint(**拒绝全自动**:高风险无兜底)
- ④结果 + 怎么验证:诚实边界——研究型/未接真实业务流量;**怎么知道 work**——LangSmith 可观测 + Probe/Health 探活数据(非 vibes)
- ⑤方法论 + 局限:「编排可信三件套——可解释路由 + 状态可恢复 + 高风险可兜底」;**局限/下次**——偏研究型未上生产、失败归因纯规则非 LLM(下次可探索 LLM 归因)

### 6.2 Code 主卡(改造「这个 Code Agent 到底是什么?」)
- **core(保留)**:一个真能改代码仓库的工程化 Agent——读仓库→语义检索→静态分析→出 Diff→受控写盘;安全做在代码路径上,不写在 prompt 里求模型听话
- ①业务问题 + 为什么重要:agent-main 单仓十来个 Agent,缺真能落地改代码的;模型有写权限=可能直接造成事故。**不解决=AI 停在"聊天框贴代码",进不了工程流程**
- ②本质矛盾:难点不是"让它能改"(聊天框贴代码谁都会),是"改得可信"——可控、可验、可回滚。核心投入不在"能改",在"改得可信"
- ③关键决策 + 拒绝了什么:ReAct 双节点(**拒绝 Supervisor**:写代码是探索式非多意图并行);语义检索(**拒绝全量 context**:爆窗口/贵);Diff 受控写盘(**拒绝直接覆盖**:不可回滚);Shadow Patch(**拒绝固定 prompt**:不能自进化)
- ④结果 + 怎么验证:诚实定位——偏研究型,800 文件 demo 跑的,没上生产;**怎么知道 work**——受控写盘 + sha256 增量 + 静态分析自验自修回环(非 vibes)
- ⑤方法论 + 局限:「安全做在代码路径、不写在 prompt」+「探索式 ReAct 与路由式 Supervisor 按场景选」;**局限/下次**——没上生产、无 Diff 预览用户确认/独立审查 Agent(已知改进项)

### 6.3 PRD 主卡(改造「AI 工作流完整介绍(面试第一答)」)
- **core(保留)**:把 PRD 自动蒸馏成结构化开发计划,靠 SSOT + 证据链 + 多层门控保质量
- ①业务问题 + 为什么重要:PRD→口传→开发每步损耗致返工 + 经验在老员工脑子换人就丢。**不解决=返工成本高、新人上手慢、AI 编造无约束**
- ②本质矛盾:PRD→代码最难的不是"生成"(LLM 能生成),是"AI 结论可不可信"——核心矛盾是让每条结论可追溯可验证,不是堆更大模型
- ③关键决策 + 拒绝了什么:SSOT(**拒绝多处冗余**:给 AI 编造空间);证据链(**拒绝无引用**:不可追溯);多层门控(**拒绝端到端直出**:质量不可控)
- ④结果 + 怎么验证:5h→2h/需求、文件级准确率 80%、一致性 40%→85%+(**5 需求对照实验,有 metrics 非 vibes**);"20+ 人团队"软化(ADR-0005 写 1-5 人);"prd2code-gen 6 步闭环"诚实说"个人原型探索,非生产闭环"
- ⑤方法论 + 局限:「AI 产出可信三支柱——单一事实源 + 证据链 + 多层门控」;**局限/下次**——团队模式有准确率损耗(约 60%)、6 步闭环是个人原型非生产

## 7. 实施流程(GUIDE §3/§6.6 多 agent)

1. **备份**:`cp stealth.html stealth-source-current.html`
2. **并行派 3 个 agent**(每项目一个),prompt 必含:本指南 §1/§6 铁律 + 五步模板(本文 §5) + 该项目主卡骨架(本文 §6) + 现有雏形卡原文 + `learning/ai-projects/` 说明书 + 校准文档 §1.3 雷区 + 参考卡「从 PRD 到上线」风格标尺。产出可直接粘贴的 `card-body` HTML(到独立文件)。
3. **校验产物**:grep 查五段 `<strong>` 齐 / 卡数不变(仍 3 张) / `data-g` 不变 / div 平衡 / 禁用项(英文项目名标题、口语碎嘴"说白了/得说句实话"、①②③④⑤ 堆叠、html 包裹、loop 残留)
4. **组装**:用 Python 锚点脚本,按 `card-title` 锚点替换 3 张雏形卡的 `card-body`(原子写)。不动 core / title / data-g / data-kw。
5. **数字抽检**:对照 §1.3 雷区,逐项确认 3 张主卡没碰雷区数字。
6. **bump `sw.js`** 的 `CACHE_NAME`(看 origin 已部署版本 +1)。

## 8. 质量门(GUIDE §5)

- [ ] 五步齐全,②本质矛盾 + ⑤方法论是新增重点且非空话
- [ ] **主卡开场不堆技术栈**(lead with 业务问题/影响;技术栈只在 body 最后一句带过、不展开)——alexeygrigorev 点名硬伤
- [ ] **③每个决策讲了"考虑并拒绝了什么 alternative"**,不只"我选 X 因为 Y"
- [ ] **④讲了"怎么知道它 work(eval/metrics)"**,不是 vibes-based
- [ ] **⑤含局限/下次怎么做**(诚实边界显式,原文:acknowledge gaps still get hired)
- [ ] §6 declarative 风格,无口语碎嘴(说白了 / 得说句实话 / 我自己比较得意 / 被问 X 我答)
- [ ] ①② 只内联枚举,不堆 ①②③④⑤ 速查表腔
- [ ] 数字沿用已校准,§1.3 三项目雷区全回避
- [ ] 诚实边界主动说(Manager / Code 没上生产、PRD 6 步闭环不存在)
- [ ] 标题 / core / data-g / data-kw 未改(零路由风险)
- [ ] `card-body` 5 段 `<strong>` 段首领起
- [ ] div 平衡,`<script>` 完整
- [ ] `sw.js` bump(看 origin 已部署 +1)

## 9. 不做什么(YAGNI)

- 不重构机制弹药卡(76 张)
- 不碰老前端项目 / AI 工具 / 其他分类
- 不改卡片路由 / 分组 / 排序 / subOrder / getGroup
- 不重新全面校准所有数字(只沿用 + 回避雷区)
- 不引入新子组 / 新 tab
- 不做主卡的 2-3 张拆分(已否决方案 2)
- 不统一三件套方法论到单一主线(用户选各讲各的)

## 10. 记给未来(本次不进主卡,但原文提示的方向)

- **「有没有 eval 框架,还是 vibes-based」**(alexeygrigorev)——AI 项目第 2-3 层追问。本次主卡④已带"怎么验证",但完整 eval/评测体系更适合做**弹药卡专题**(Manager/Code 各补一张"怎么评测它 work"),本次不做。
- **证据链「5 个为什么连续追问」** / **alexeygrigorev「progressive questioning」**——指向弹药卡层按"追问深度"排序,本次不动弹药卡。
- **MyEngineeringPath 11-section template**——针对**单道题**(如 temperature),不是项目陈述,不照搬。其「30-Second Version / Where Candidates Fail / Senior-Level Upgrade」思想已分别体现在主卡 core / 诚实边界 / ⑤方法论。
- **Modern Descartes「collaborative not skeptical、how you personally experienced」**——主卡用第一人称讲"我怎么经历的",不是教科书"这种项目应该怎么做"。已在 §6 骨架体现。
- **alexeygrigorev「impact not technology names」**——本次用"主卡不堆技术栈"落实;但现有**弹药卡**里也可能有堆技术名词的,未来可按此标尺再扫一遍。
