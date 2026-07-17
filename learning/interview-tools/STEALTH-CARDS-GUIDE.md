# stealth.html 卡片写作与优化指南

> 给未来的自己 / 下一个 Claude session：怎么把 `stealth.html`（面试手机速查页）的卡片写到"经得起追问、不穿帮、像真人说话"。
> 这份是 2026-07-17 大改时沉淀的经验。相关上下文见仓库根 `CLAUDE.md` 和 `learning/interview-kb/`。

## 0. 这个页面是干嘛的

`learning/interview-tools/stealth.html` 是**面试中用手机速查**的单页（核心资产）。结构：顶部 7 个 tab（开场/项目/基础/手撕/AI/综合），每个 tab 下用 `quickbar` 二级子分组按钮定位，点卡片展开看答案。

设计目标：**面试现场 3 秒能找到、5 秒能念出来**。所以卡片要 scannable（金色一句话 core + 口语正文），不能是长篇文档。

---

## 1. 卡片写作铁律（最重要）

### 1.1 语气：像真懂项目的人在聊天，不是速查表

> ⚠️ **Agent / 技术项目卡（Manager、Code 等）例外**：这类卡反过来——要**结构化、对标参考卡「从 PRD 到上线的完整链路」**（declarative、`<strong>领起标签</strong>` 组织、可用 ①② 内联），**别太口语**（禁"说白了 / 得说句实话 / 我自己比较得意 / 被问 X 我答"这类碎词）。详见 §6。

- **第一人称口语**。用"说白了 / 其实 / 得说句实话 / 我自己比较得意的是 / 这里有个坑 / 被追 XX 我一般答"这种自然连接词。
- **禁用速查表腔**：不要"必背""杀手锏""被问 X 必答""金句钩子""①②③"这种框架标签。少滥用 `<strong>`。
- **不用太完美、太工整**。可以有不完整的句子、停顿感。口语比书面更重要。
- **但要有信息密度**：核心机制、关键数字、坑、诚实边界都要在，只是用嘴说出来。

✅ 好的 core："一个多智能体的'总管'——自己不干活，专门拆任务、派给十几个专业 Agent、再查结果对不对"
❌ 差的 core："基于 Nuxt4 + LangGraph 的多 Agent 编排网关——39 节点状态机（40 边含 20 条件边）+ 12 能力 Agent + Probe/Health 双层探活 + Self-Evolution + HITL"（堆术语、不像人话）

### 1.2 标题：提炼核心，绝不带英文项目名
- 标题是一个**人会问的问题**或一个**核心点**。
- **绝对不带英文项目名前缀**（禁 "Manager_Agent xxx" / "code_assistent xxx"）——这是侧边栏索引（drawer）可读性的关键。
- ✅ "39 个节点是怎么长出来的" / "模型要改代码，怎么防止它乱来" / "被问'上线了吗'我怎么答"
- ❌ "Manager_Agent 39 节点拓扑（必背·被问'画一下 graph'）"

### 1.3 校准：数字必须核对源码，绝不编造（防穿帮）
这是**最关键的诚实边界**。简历 / AI 生成的"预测答案"/ 甚至用户自己的档案里的数字，**很多是编的或美化**，被面试官追问"怎么测的 / 给我看代码"会直接翻车。

- 每个数字先判"已实现 / 部分 / 没找到"，用 **✅可说 / ⚠️软化 / ❌别说** 三档。
- **Agent 项目**：核对真实源码 `D:/work/agent-main/Manager_Agent/` 和 `D:/work/agent-main/code_assistent_Agent/`。
- **完整校准清单**见 `learning/interview-kb/明日面试_预测题校准与匹配分析.md`（已公开）和 `learning/ai-projects/` 两份深度说明书。
- 不确定的数字：**软化（"大概 / 约 / 小范围验证过"）或省略**。绝不编百分比 / 提升倍数 / 团队规模。

**已知雷区（说了必穿帮，见校准文档）：**
- Manager 模型是**阿里云 qwen-flash**，不是 Claude/GPT；12 Agent = **9 外 + 3 内**（不是 8+4）；失败归因**纯规则非 LLM**；**自动晋级默认关闭**；Checkpoint 是自建 16 字段快照。
- Code 向量检索是**自研 JSON+内存余弦**（不是 Chroma）；增量靠 **sha256**（不是 git 钩子）；**没有** Diff 预览用户确认才执行 / 独立代码审查 Agent / HITL 写确认。
- Spec-Driven/prd-tools 真身是 **Claude Code 插件**（/reference + /prd-distill），不是 SDD 平台、不直接生成代码；"prd2code-gen 6 步闭环"**不存在**；"20+ 人团队"要软化（ADR-0005 写 1-5 人）。

### 1.4 诚实边界要主动说（是加分项）
被追问时的真实答案、没实现的部分、已知债务，都要写进卡里——但用口语。主动暴露缺口 = 加分，硬吹被追"代码在哪"= 翻车。
- ✅ "得说句实话：这项目偏研究型，没接真实业务流量……"
- ✅ "这个锁只在 HTTP 直写接口强制，Agent 工具路径目前没传，是已知改进项。"

---

## 2. 结构约定（别改坏路由）

### 2.1 分类与分组
- `data-c`：一级分类 = `open`开场 / `proj`项目 / `bagu`基础 / `code`手撕 / `ai` / `emer`综合。
- **子分组**靠 `getGroup(c)` 函数（文件底部 `<script>` 里）。两种机制：
  1. **`data-g` 显式分组**（推荐，最稳）：卡片直接挂 `<div class="card" data-c="proj" data-g="Manager 智能体">`，getGroup 开头 `if(c.dataset.g)return c.dataset.g` 直接返回。**新增子模块优先用这个。**
  2. **tag + 标题正则**（旧机制，易错）：getGroup 按 `.tag` 的 textContent 和标题正则路由。⚠️ 坑：tag 的 **textContent** 和 **class** 是两回事（`<span class="tag Manager">M0</span>` 的 textContent 是 "M0" 不是 "Manager"），查 textContent 会失配。
- `subOrder` 对象控制各子组在 tab 内的排序顺序。

### 2.2 卡片 HTML 模板
```html
<div class="card" data-c="proj" data-g="Manager 智能体" data-kw="关键词 空格分隔 覆盖各种问法">
  <div class="card-head"><span class="tag proj">短标签</span><div class="card-title">核心标题（不带项目名）</div></div>
  <div class="core">一句口语化核心（金色高亮，最醒目）</div>
  <div class="card-body">
    <p>口语段落……</p>
    <p class="hint">可选：语速/时长/提醒，如"约 45 秒，说完停顿等追问"</p>
  </div>
</div>
```
- 标签 class 跟着分类走：`.tag proj`(蓝) / `.tag ai`(红) / `.tag emer`(橙) / `.tag open`(粉)。
- 开场第一张用 `class="card open"`（默认展开），其余 `class="card"`。
- `data-kw` 是搜索关键词，**把这道题的各种问法都塞进去**（便于现场搜）。
- 正文用 `<p>` 段落；代码用 `<div class="code-blk">`；要点用 `<ul class="points">`。

### 2.3 当前子组布局（2026-07-17）
- **proj**：Schema 项目 → **Manager 智能体**(11卡，2026-07-17 重构) → **Code 智能体**(19卡) → AI 总览/架构/质量/端到端/工具 → 产品思维
- **ai**：Agent 基础 / RAG / LLM 工程 / 工具协议 / AI 评测 / Loop 工程 / AI 前端 / 行业视野 / 追问 / **系统设计**(SD1-6，^SD 路由)
- **emer**：项目数据 / 大麦·TikTok·蚂蚁专属 / HR面 / 软技能 / 反问 / 话术急救

---

## 3. 推荐工作流（多 agent 重写，效果好）

大改动（重写一个子模块 / 重做开场）用这个流程，比单 agent 一次写完质量高、不爆上下文：

1. **备份源**：`cp stealth.html stealth-source-current.html`（重写时拿来当源料）。
2. **并行派 agent**：每个子模块一个 general-purpose agent，各读"源卡 + 校准事实 + 本指南 §1"，产出**可直接粘贴的 HTML 卡**写到独立文件。本次分了 4 路：Manager / Code / 开场 / 捞回。
   - 给每个 agent 的 prompt 必含：本指南 §1 铁律 + 该模块的真实校准数字（✅⚠️❌清单）+ 样例卡 + 卡片模板 + 源料行号。
3. **校验产物**：`grep` 查卡片数 / data-g 或 data-c 取值 / 禁用项（英文项目名标题、loop 标记、html 包裹）/ div 平衡。
4. **组装**：用 Python 脚本按锚点字符串插入（替换旧开场块、在样例卡后插 man+code、在 noRes 前插捞回），比多次 Edit 可靠。脚本最后才写文件（原子）。
5. **bump `sw.js` 的 `CACHE_NAME`**（kb-vN → kb-vN+1），否则 Service Worker 给访客旧缓存。

> 校准事实的获取也可以单独派 agent：让它读 `agent-main/` 真实源码 + 深度说明书 + 校准文档，产出《真实事实 + ✅⚠️❌ 可说清单》，再喂给写卡 agent。

---

## 4. 踩过的坑（别再踩）

1. **tag textContent vs class 不一致**：`<span class="tag Manager">M0</span>` 让 getGroup 的 `tag==='Manager'` 失配，39 张 agent 卡全掉进 Schema 组（"侧边栏看不到内容"的根因）。→ 新卡用 `data-g` 显式分组。
2. **Service Worker 缓存**：改完文件不 bump `CACHE_NAME`，线上访客（和自己）看到的还是旧版。bump 后也要**硬刷新一次**让新 SW 接管。
3. **AI 生成的答案数字大多立不住**：简历话术 / "预测答案" / 用户档案里的百分比、倍数、团队规模，先怀疑、再核对源码。见 §1.3。
4. **回退要用 git**：要回到某个历史版本，`git show <commit>:learning/interview-tools/stealth.html`，别手动删。
5. **loop 自动化留下的标记**：旧卡里可能有 `[loop·待复核]` 之类残留，清理掉。

---

## 5. 质量自检清单（交活前过一遍）

- [ ] 标题没有英文项目名前缀？
- [ ] 语气是口语、没有速查表腔（必背/杀手锏/①②③）？
- [ ] 每个数字都核对过源码 / 能答出"怎么测的"？
- [ ] 诚实边界（没实现的、已知债）有没有主动说？
- [ ] `data-kw` 覆盖了这道题的各种问法？
- [ ] div 开/闭标签平衡？`<script>` 完整？
- [ ] 新子组在 `subOrder` 里有排序值？`getGroup` 能正确路由？
- [ ] `sw.js` 的 `CACHE_NAME` bump 了？

---

## 6. Agent 项目卡重构经验（2026-07-17 · Manager 模块实战）

> Manager 智能体从 23 张重写成 11 张、三轮迭代后定稿的经验。**Code 智能体和后续 Agent 项目卡直接复用。**

### 6.1 风格标尺：参考卡「从 PRD 到上线的完整链路」

用户最满意的一张是 `stealth.html` 里 proj 的「从 PRD 到上线的完整链路？」(A10)。Agent / 技术项目卡**逐句对标它**：

- declarative 陈述句为主（"X 是 Y / 走 Z / 靠 W"），不是松散口语。
- 正文每段 `<strong>领起标签。</strong>` 开头，2-4 段，每段一个机制/要点，信息密、有条理。
- core 是一句带机制名 + 结构的浓缩（像"双轨：…三阶段…6 步…已跑通"）。
- ①② 可内联枚举（参考卡就这么用），但别堆成 ①②③④⑤ 速查表。

### 6.2 去口语（重要，对 §1.1 的修正）

Agent 项目卡**别用** §1.1 那套口语连接词：说白了、得说句实话、我自己比较得意、被问 X 我答、这套东西、你就懂了、听着像。这些是上一版 Manager 卡被批"太随意 / 太口语化"的根因。declarative，不碎嘴。

### 6.3 全覆盖源文档

Agent 项目卡要**全覆盖 README + 学习指南**，不只是学习指南"知识自测"5 条（那是优先核心，但其它机制也要有卡）。先做**覆盖审计**（每个文档的节标 ✓ 已覆盖 / ❌ 缺 / △ 不够全），再决定补哪些卡。Manager 那次补了：流式交互、可观测性、4 个工程模式（Retrieve-first / Evidence Gate / Retry Budget / Platform Sync），自进化扩到 9 个子机制。

### 6.4 概念层，不堆配置数

机制名点到（Probe / Critic / HITL / 金丝雀 / managerTask / phase），**不写源码配置数**（39 节点、recursionLimit、slice(-1200)、16 字段、CANARY_PERCENT 这种）。面试不问这么细，细节稍微提一下就行。

### 6.5 诚实边界用陈述式

"自动晋级默认关"这种直接陈述，不要"得说句实话……"。

### 6.6 流程（guide §3 验证有效）

多 agent 重构：每个 agent 拿「两份源文档 + 参考卡 + 本指南 §1/§6 铁律 + 分配的卡题」产出 HTML；主会话用 Python 锚点脚本 splice（替换子模块注释之间的整块）+ grep 校验（卡数 / div 平衡 / 禁用项 / 标题）+ bump `sw.js`。比单 agent 一次写完质量高、不爆上下文。
