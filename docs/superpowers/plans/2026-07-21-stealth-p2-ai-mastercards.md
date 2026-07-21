# stealth P2 ai 分类卡五步重构 · 实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: 用 superpowers:subagent-driven-development(推荐)或 superpowers:executing-plans 逐 task 执行。步骤用 `- [ ]` 跟踪。

**Goal:** 把 stealth.html ai 分类的 14 张「项目/能力主张」卡(10 全改 C1-C10 + 4 轻过 C11-C14)card-body 改写/对齐成五步骨架(业务+ownership/本质矛盾/决策+alternatives/结果+eval/方法论+局限),20 张问答弹药 + 51 张其余卡不动,零 routing 改动(14 张已有 data-g)。

**Architecture:** 双层(主张卡+弹药)。3 个 agent 各产 card-body 片段到独立文件(Agent-1 C1-C5 全改 / Agent-2 C6-C10 全改 / Agent-3 C11-C14 轻过)→ Python 锚点脚本只 splice 14 张 body(不动 data-g/subOrder/title)→ 结构校验(check_p2.py)+ §4.2 雷区人工 grep 抽检 → bump sw.js kb-v325 + 个人账号 push。

**Tech Stack:** HTML(stealth.html 单页,无构建工具)、Python 3(组装/校验脚本)、grep/bash(验收)。

## Global Constraints

- **范围严格 14 张**:全改 C1-C10 + 轻过 C11-C14。51 张跳过卡(20 问答弹药 + 系统设计假设性方法论 6 + 其余五步雏形)body **一律不动**。
- **零 routing 改动**:14 张已有 data-g(Agent 基础/Loop 工程/RAG 检索/系统设计),**不加新 data-g、不动 subOrder、不删卡**。assemble 只 body swap。
- **数字校准复用现有清单**(简单方案,不派 agent 重读 `agent-main/` 源码):memory + roadmap §5 + `learning/interview-kb/明日面试_预测题校准与匹配分析.md` + 14 张卡现有已校准数字。不确定的软化("大概/约/小范围验证过")或省略。**绝不编百分比/提升倍数/团队规模。**
- **§4.2 正向雷区**(说了穿帮,写卡 agent 必回避):Manager=qwen-flash 非 Claude/GPT/Anthropic · 12 Agent=9外+3内 · 失败归因纯规则非 LLM · 自动晋级默认关 · Checkpoint 自建16字段 · Code 向量自研 JSON+余弦非 Chroma · 增量 sha256 非 git钩子 · Code 无 Diff预览/独立审查Agent/HITL写确认 · prd-tools 是 Claude Code 插件非 SDD 平台/"6步闭环"不存在 · "20+人"软化(1-5人)。
  - ⚠️ **check 脚本不做 naive 雷区子串检查**——ai 卡会合法"提到被拒绝的选项"(如 C10 标题就说"不用 Chroma"、C-cards 提"Claude Code 插件"),naive grep 会误报。雷区改由 **Task 7 人工 grep + 读上下文**判断"误用 vs 合法提及"。脚本只自动查"6 步闭环"(此短语不存在,任何出现都是错)。
- **§6 declarative 风格**;禁口语碎嘴:说白了 / 得说句实话 / 我自己比较得意 / 被问X我答 / 这套东西 / 你就懂了 / 听着像。
- **主卡开场不堆技术栈**(impact not technology names):技术名词只在必要处带过,不展开罗列。
- **标题/core/data-kw**:14 张标题**默认全部保留**(已验证精确串,见 Task 1);§3.4 两处可选修剪([3566] 冗长尾巴、[4085]"(Manager 经验升华)")**默认不做**,若做放 Task 6 最后。
- **改完 bump `sw.js` 的 `CACHE_NAME`**:**kb-v324 → kb-v325**(已确认 origin 已部署 kb-v324)。
- 用**个人 GitHub 账号**推送(origin = `github-personal:zachary-lz-glm`,已确认);本项目 main 工作流,直接 commit main + push 触发 Pages。
- stealth.html 单页大文件,组装用 **Python 锚点替换 + 原子写**,不用多次 Edit。
- agent 产**独立文件**,主会话统一组装,避免并发改同一文件(GUIDE §4.6)。
- **每 agent prompt 写死「只产指定卡的 card-body 片段到独立文件,禁碰 stealth.html、禁碰其他卡」**(memory [[agent-scope-constraint]])。

## File Structure

| 文件 | 责任 | 动作 |
|------|------|------|
| `learning/interview-tools/stealth.html` | 速查页主体 | 改:14 张 card-body |
| `learning/interview-tools/stealth-source-current.html` | 重写前源料备份 | 建 |
| `learning/interview-tools/check_p2.py` | 校验 agent 产物(五段/禁用项/div 平衡,--light 阈值) | 建(从 check_mastercard.py 复制改造) |
| `learning/interview-tools/assemble_p2.py` | 锚点 splice 14 张 body(不动 data-g/subOrder/title) | 建 |
| `learning/interview-tools/.p2-prompt-template.md` | 三 agent 共用 prompt 公共部分 | 建 |
| `learning/interview-tools/.p2-c{1-14}-*.html` | 14 张 body 产物(临时) | 建,组装后删 |
| `learning/interview-tools/.p2-anchors.txt` | 14 张精确标题 + 唯一性记录 | 建,组装后删 |
| `sw.js` | Service Worker 缓存版本 | 改:CACHE_NAME kb-v324→kb-v325 |

---

### Task 1: 备份源 + 验证 14 张卡锚点

**Files:**
- Create: `learning/interview-tools/stealth-source-current.html`
- Create: `learning/interview-tools/.p2-anchors.txt`

**Interfaces:**
- Produces: `.p2-anchors.txt` 含 14 张卡精确 card-title 原文(已验证,见下),供 Task 6 assemble 校对

- [ ] **Step 1: 备份 stealth.html**

```bash
cp learning/interview-tools/stealth.html learning/interview-tools/stealth-source-current.html
```

- [ ] **Step 2: 验证 14 张卡 card-title 唯一 + 精确串(全角标点)**

```bash
cd learning/interview-tools
python3 - <<'PY'
import re
html = open("stealth.html", encoding="utf-8").read()
titles = [
 "从零设计一个 Agent，你的思路是什么",
 "Agent 的记忆怎么设计：短期、长期、工作记忆",
 "Agent 的工作记忆怎么管，对话越来越长咋办",
 "Harness Engineering：Agent 等于 Model 加 Harness",
 "Agent 自进化闭环怎么设计",
 "什么场景才该上 Agent，别什么活都套 Agent",
 "Agent 框架怎么选：LangGraph vs LangChain vs AutoGen vs CrewAI vs Dify vs Coze",
 "ReAct vs Plan-and-Execute vs Reflexion，什么时候用哪个",
 "单 Agent 还是多 Agent，一个决策树",
 "向量库怎么选——还有我为什么自己写不用 Chroma",
 "Agent Safety 怎么做——规划层加执行层",
 "向量召回 vs 代码实体图——我两个项目各做了一个",
 "把 39 节点的多智能体编排瘦身重构",
 "设计通用 Multi-Agent 调度系统（Manager 经验升华）",
]
ok = True
for i, t in enumerate(titles, 1):
    n = len(re.findall(r'card-title">' + re.escape(t) + r'</div>', html))
    # 验证每张有 card-body
    idx = html.find(f'card-title">{t}')
    has_body = idx > 0 and html.find('<div class="card-body">', idx) > 0
    flag = "✅" if (n == 1 and has_body) else "❌"
    if flag == "❌": ok = False
    print(f"{flag} C{i} [标题{n}次, body={'有' if has_body else '无'}] {t}")
print("ALL OK" if ok else "有异常,停下排查")
PY
```
Expected: 14 行全 `✅`,`ALL OK`。若某张 ❌(标题 ≠1 次或无 card-body),停下排查:标题被改过/重复,或 card-body 结构异常。

- [ ] **Step 3: 抽样确认现有 body 可编辑(看 1 张全改 + 1 张轻过的当前结构)**

```bash
cd learning/interview-tools
echo "=== C1 当前 body 头部 ==="
grep -A 3 "从零设计一个 Agent" stealth-source-current.html | head -8
echo "=== C11 当前 body 头部 ==="
grep -A 3 "Agent Safety 怎么做" stealth-source-current.html | head -8
```
Expected: 能看到 `<div class="card-body">` + 现有 `<p>` 段落,确认可改写。

- [ ] **Step 4: 记录锚点到 .p2-anchors.txt**

把 Task 1 Step 2 的 14 个精确 card-title(每行一个)写入 `.p2-anchors.txt`,供 Task 6 assemble 校对。

- [ ] **Step 5: Commit**

```bash
git -C /Users/didi/work/linze-journal add learning/interview-tools/stealth-source-current.html learning/interview-tools/.p2-anchors.txt
git -C /Users/didi/work/linze-journal commit -m "chore(stealth): 备份源+抽取P2 ai 14张卡锚点"
```

---

### Task 2: 重建 check_p2.py + 公共 agent prompt 模板

**Files:**
- Create: `learning/interview-tools/check_p2.py`
- Create: `learning/interview-tools/.p2-prompt-template.md`

**Interfaces:**
- Consumes: `learning/interview-tools/check_mastercard.py`(A 留的复用脚本)
- Produces: `check_p2.py` —— 输入 body 片段路径 + 可选 `--light`,跑校验,全过 exit 0 否则 exit 1;`.p2-prompt-template.md` —— 三 agent 共用 prompt 公共部分

- [ ] **Step 1: 写 check_p2.py(从 check_mastercard.py 复制改造)**

```python
#!/usr/bin/env python3
"""校验 P2 ai 卡 card-body 产物。用法: python3 check_p2.py <body.html> [--light]
全改卡 ≥5 段 <strong>;轻过卡(--light) ≥4 段。
注:§4.2 雷区(Manager≠Claude/GPT、向量≠Chroma 等)因 ai 卡会"提到被拒绝的选项"(如 C10 合法说"不用 Chroma"),
naive 子串检查会误报,故不在本脚本自动检查,改由 Task 7 人工 grep 抽检(读上下文判断误用 vs 合法提及)。"""
import re, sys

light = "--light" in sys.argv
f = sys.argv[1]
html = open(f, encoding="utf-8").read()
errs = []
min_strong = 4 if light else 5

# 1. 段首 <strong>(全改≥5 / 轻过≥4)
strongs = re.findall(r"<strong>[^<]{2,}</strong>", html)
if len(strongs) < min_strong:
    errs.append(f"段首 <strong> 只有 {len(strongs)} 个,需 ≥{min_strong}({'轻过' if light else '全改'})")

# 2. 禁用口语碎嘴
banned = ["说白了", "得说句实话", "我自己比较得意", "这套东西", "你就懂了",
          "被问", "我答", "听着像"]
hit = [w for w in banned if w in html]
if hit:
    errs.append(f"命中口语碎嘴: {hit}")

# 3. ①②③④⑤ 堆叠(连续 4 个以上圈号)
if re.search(r"[①②③④⑤][①②③④⑤][①②③④⑤][①②③④⑤]", html):
    errs.append("①②③④⑤ 堆叠(≥4 连续),速查表腔")

# 4. loop 残留 / html 包裹
if "[loop" in html or "<html" in html.lower() or "<body" in html.lower():
    errs.append("含 loop 残留或 html/body 包裹")

# 5. div 平衡
if html.count("<div") != html.count("</div>"):
    errs.append(f"div 不平衡: <div {html.count('<div')} / </div> {html.count('</div>')}")

# 6. 唯一自动雷区:'6 步闭环'(此短语不存在,任何出现都是错;其余 §4.2 雷区人工抽检)
if "6 步闭环" in html or "6步闭环" in html:
    errs.append("含'6 步闭环'(此说法不存在,§4.2 雷区)")

if errs:
    print("❌ 校验失败:")
    for e in errs: print("  -", e)
    sys.exit(1)
mode = "轻过" if light else "全改"
print(f"✅ 校验通过({len(strongs)} 段 <strong>,{mode})")
```

- [ ] **Step 2: 用坏样例验证脚本能抓错**

```bash
cd learning/interview-tools
printf '<div class="card-body"><p>说白了做6步闭环</p></div>' > /tmp/bad.html
python3 check_p2.py /tmp/bad.html; echo "exit=$?"
```
Expected: 打印 ❌(段首<strong>不足 / 口语碎嘴"说白了" / 含"6步闭环"),exit=1。

- [ ] **Step 3: 写公共 agent prompt 模板 `.p2-prompt-template.md`**

```markdown
你是面试速查卡写作 agent。任务:为 stealth.html 重写/对齐 {N} 张「ai 分类·项目/能力主张卡」的 card-body(只 body,不动 core/title/标签/外层 .card)。

# 必读(按顺序)
1. learning/interview-tools/STEALTH-CARDS-GUIDE.md —— §1(铁律)、§6(技术项目卡风格标尺:declarative、不碎嘴、不堆栈)、§2.2(卡片模板)
2. docs/superpowers/specs/2026-07-21-stealth-p2-ai-mastercards-design.md —— §5(五步模板+硬约束)、§6(本批卡的五步骨架,见下方「本次负责的卡」)、§4.2(正向雷区清单)
3. 现有卡原文: 从 stealth-source-current.html 抽取 card-title="{标题}" 的那张卡,保留 core 和好句、保留已校准数字,把 card-body 改/补五步

# 本次负责的卡
{此处由 Task 3/4/5 填入:卡号 + card-title + spec §6 对应小节的五步要点}

# card-body 五段骨架(每段 <strong>段首领起。</strong> 开头;轻过卡可 4 段)
① 业务问题 + ownership —— 解决什么、不解决会怎样、"我在里面 drive 了什么"(不堆技术栈)
② 本质矛盾 —— 难点本质在哪(非堆功能/非更大模型)⭐本轮重点
③ 关键决策 + 拒绝了什么 —— 每个高杠杆决策讲"为什么选它 + 考虑并拒绝了什么 alternative"
④ 结果 + 怎么验证 —— 指标 + eval/metrics(非 vibes)+ 可复用价值
⑤ 方法论 + 局限 —— 可迁移命名框架 + 诚实边界(局限/下次怎么做)⭐本轮重点

# 风格(§6)
declarative 陈述句;禁口语碎嘴(说白了/得说句实话/我自己比较得意/被问X我答/这套东西/你就懂了);
①② 可内联枚举,不堆 ①②③④⑤;主卡开场不堆技术栈(impact not technology names)。

# §4.2 正向雷区(说了穿帮,必回避——但可"提到并拒绝"这些选项)
Manager 模型=qwen-flash(非 Claude/GPT/Anthropic);12 Agent=9外+3内;失败归因纯规则(非 LLM);自动晋级默认关;Checkpoint 自建16字段;
Code 向量=自研 JSON+内存余弦(非 Chroma);增量=sha256(非 git钩子);Code 无 Diff预览/独立审查Agent/HITL写确认;
prd-tools=Claude Code 插件(/reference+/prd-distill,非 SDD 平台);"6 步闭环"不存在;"20+人团队"软化(1-5人)。
不确定的数字软化("大概/约/小范围验证过")或省略,绝不编百分比/倍数/统计口径。

# 硬约束
- 只产出 {N} 个 card-body 的 HTML 片段,每个从 <div class="card-body"> 到对应 </div>
- 每张卡输出到**指定独立文件**,文件名见下方;**绝对不碰 stealth.html,绝对不碰其他卡**
- 不含 core / card-title / 外层 .card div
- div 平衡;无 loop 残留;无 <html>/<body> 包裹

# 产出
按指定文件名输出,每个文件只含一个 card-body 片段,不要任何解释、不要 ``` 包裹。
```

- [ ] **Step 4: Commit**

```bash
git -C /Users/didi/work/linze-journal add learning/interview-tools/check_p2.py learning/interview-tools/.p2-prompt-template.md
git -C /Users/didi/work/linze-journal commit -m "chore(stealth): P2校验脚本(雷区反转+--light)+公共agent prompt模板"
```

---

### Task 3: Agent-1「Agent 设计内核」(C1-C5,5 全改)

> Task 3/4/5 互相独立(不同卡、不同产物文件),**可并行派 3 个 agent**。

**Files:**
- Create: `learning/interview-tools/.p2-c1-agent-design.html`
- Create: `learning/interview-tools/.p2-c2-memory.html`
- Create: `learning/interview-tools/.p2-c3-working-memory.html`
- Create: `learning/interview-tools/.p2-c4-harness.html`
- Create: `learning/interview-tools/.p2-c5-evolution.html`

**Interfaces:**
- Consumes: `.p2-prompt-template.md`(Task 2)、`stealth-source-current.html`(Task 1)
- Produces: `.p2-c1` ~ `.p2-c5` 五张全改卡 card-body 片段

- [ ] **Step 1: 派 general-purpose agent**

prompt = `.p2-prompt-template.md` 填入:
- `{N}` = `5`(全改,不带 --light)
- 「本次负责的卡」填入(五张,均输出 card-body 片段):
  - **C1 · card-title「从零设计一个 Agent，你的思路是什么」**(输出 `.p2-c1-agent-design.html`)—— spec §6 C1 要点:①不是堆工具是先定"目标可控性"(何时停/谁来批)再配能力,我在 code/prd-tools 两项目从零设计过。②核心矛盾=自主性 vs 可控性(自主权越多越强但越易失控/难debug),本质是定边界非堆功能。③分层(规划/执行/校验)+HITL闸门(拒绝全自主跑完)+工具小而可组合(拒绝一个大工具全包)。④code自验证自修复(max_iter+Readiness)+prd-tools /reference//prd-distill 分阶段;eval=每层可观测/可单测/可回放。⑤「先定可控边界再配能力而非堆工具」+局限(两项目偏研究型/小范围没接大规模真实流量;HITL路径是已知改进)。
  - **C2 · card-title「Agent 的记忆怎么设计：短期、长期、工作记忆」」**(输出 `.p2-c2-memory.html`)—— spec §6 C2 要点:①记忆不是塞越多越好是分层管理生命周期,prd-tools 用 Reference(长期)/Spec(本次任务)/Plan(执行轨迹)三层。②矛盾=召回相关性 vs 上下文成本(全塞相关性高但贵且lost-in-middle),本质是分层+按需注入。③三层划分+按需注入(拒绝全塞context)+结构化优先精确指令(拒绝纯向量模糊召回)。④Reference作压缩层复用省token+Plan可回放断点续;eval=context可控关键信息不丢。⑤「记忆分层+按需注入不是全塞context」+局限(prd-tools记忆为PRD蒸馏定制;通用Agent向量长期记忆我没做)。
  - **C3 · card-title「Agent 的工作记忆怎么管，对话越来越长咋办」」**(输出 `.p2-c3-working-memory.html`)—— spec §6 C3 要点:①长对话/多步任务工作记忆爆掉是通病,Manager 用自建16字段Checkpoint快照。②矛盾=保留执行历史 vs 窗口预算(全留则窗口爆/模型分心,全砍则丢断点),本质是有损压缩+checkpoint。③Checkpoint快照(拒绝裸塞对话历史)+有损摘要+关键槽位保留(拒绝无差别截断)+断点续跑。④16字段快照可恢复+长任务不爆窗口;eval=断点续跑能续上关键状态不丢。⑤「工作记忆=有损压缩+checkpoint不是无差别截断」+局限(16字段为Manager任务流定制;hierarchical summary等通用对话压缩我没深做)。
  - **C4 · card-title「Harness Engineering：Agent 等于 Model 加 Harness」」**(输出 `.p2-c4-harness.html`)—— spec §6 C4 要点:①Agent≠模型,Agent=模型+Harness(工具调度/状态/校验/恢复的工程脚手架),两项目都搭了harness。②矛盾=给模型自由度 vs 加约束护栏(harness太薄则模型乱跑太厚则僵化抵消能力),本质是工程化"可控的自主"。③分层harness(工具/编排/校验)+KSG关键状态门+Ratchet只进不退(拒绝裸调模型等结果)+失败恢复(拒绝失败即终止)。④Manager 39节点+code自验证自修复都是harness落地;eval=失败可恢复状态可观测。⑤「Agent=模型+harness价值在harness不在模型调参」+局限(shadow-only/部分机制是已知改进方向非全量生产)。
  - **C5 · card-title「Agent 自进化闭环怎么设计」」**(输出 `.p2-c5-evolution.html`)—— spec §6 C5 要点:①自进化是Agent从自身运行学习改进,Manager设计了Self-Evolution机制。②矛盾=学习信号 vs 统计可靠性(单次反馈噪声大直接学会把坏经验固化),本质是要统计护栏不是裸学习。③四步闭环(采集/归因/实验/回滚)+失败归因纯规则(拒绝LLM归因不可靠)+shadow-only默认(拒绝直接上线学习结果)。④Manager Self-Evolution跑shadow模式;eval=有hold-out/对照不靠vibes。⑤「自进化必须配统计护栏+shadow不能裸学」+局限(目前shadow-only没接真实流量大规模验证——诚实边界;统计严谨性是后续)。
- agent 必读 spec §6 C1-C5 + §4.2 雷区 + stealth-source-current.html 五张卡原文。
- prompt 末尾写死:"只产出 .p2-c1-agent-design.html / .p2-c2-memory.html / .p2-c3-working-memory.html / .p2-c4-harness.html / .p2-c5-evolution.html 五个文件,禁碰 stealth.html,禁碰其他卡,禁碰 .p2-c6~c14。"

- [ ] **Step 2: 校验五张产物**

```bash
cd learning/interview-tools
for f in .p2-c1-agent-design.html .p2-c2-memory.html .p2-c3-working-memory.html .p2-c4-harness.html .p2-c5-evolution.html; do
  python3 check_p2.py "$f"; echo "  $f exit=$?"
done
```
Expected: 五张都 `✅ 校验通过(≥5 段 <strong>,全改)`,exit=0。若失败,把错误回喂 agent 重产出。

- [ ] **Step 3: 人工风格抽看**

打开五张产物,确认:declarative 不碎嘴、开场不堆技术栈、②本质矛盾+⑤方法论非空话、③每决策有"拒绝了什么"。

- [ ] **Step 4: Commit**

```bash
git -C /Users/didi/work/linze-journal add learning/interview-tools/.p2-c1-agent-design.html learning/interview-tools/.p2-c2-memory.html learning/interview-tools/.p2-c3-working-memory.html learning/interview-tools/.p2-c4-harness.html learning/interview-tools/.p2-c5-evolution.html
git -C /Users/didi/work/linze-journal commit -m "feat(stealth): P2 C1-C5 Agent设计内核 五步骨架(全改)"
```

---

### Task 4: Agent-2「选型与检索决策」(C6-C10,5 全改)

**Files:**
- Create: `learning/interview-tools/.p2-c6-when-agent.html`
- Create: `learning/interview-tools/.p2-c7-framework.html`
- Create: `learning/interview-tools/.p2-c8-paradigm.html`
- Create: `learning/interview-tools/.p2-c9-single-multi.html`
- Create: `learning/interview-tools/.p2-c10-vector.html`

**Interfaces:**
- Consumes: `.p2-prompt-template.md`、`stealth-source-current.html`
- Produces: `.p2-c6` ~ `.p2-c10` 五张全改卡 card-body 片段

- [ ] **Step 1: 派 general-purpose agent**

prompt = 模板填入:
- `{N}` = `5`(全改)
- 「本次负责的卡」:
  - **C6 · card-title「什么场景才该上 Agent，别什么活都套 Agent」」**(输出 `.p2-c6-when-agent.html`)—— spec §6 C6 要点:①不是什么活都套Agent,我有判断框架三层。②矛盾=自主性收益 vs 不可控成本(Agent适合路径不确定/需动态决策;确定路径用workflow更稳更便宜),本质是按不确定性选范式。③判断三层(路径确定→workflow;路径动态/需工具组合→Agent;单轮问答→直接LLM)+拒绝"什么都要Agent"的over-engineering。④Manager走Agent(多步动态)+prd-tools部分workflow化;eval=按场景匹配非一刀切。⑤「按不确定性选范式Agent不是万能」+局限(框架是经验归纳边界case靠判断)。
  - **C7 · card-title「Agent 框架怎么选：LangGraph vs LangChain vs AutoGen vs CrewAI vs Dify vs Coze」」**(输出 `.p2-c7-framework.html`)—— spec §6 C7 要点:①框架选型我为Manager选了LangGraph,我是选型决策者。②矛盾=框架能力 vs 可控性/学习成本(全功能框架抽象高但黑盒;裸写可控但重复造轮),本质是按可控性需求选抽象层级。③LangGraph(状态机显式可控,拒绝LangChain全家桶黑盒/拒绝裸写重复造轮)+六框架矩阵对比。④Manager 39节点状态机用LangGraph显式表达;eval=节点/边可观测可调试。⑤「框架选型按可控性需求选抽象层级」+局限(LangGraph学习曲线;小项目其实不必上重框架)。
  - **C8 · card-title「ReAct vs Plan-and-Execute vs Reflexion，什么时候用哪个」」**(输出 `.p2-c8-paradigm.html`)—— spec §6 C8 要点:①三种Agent范式选型,两项目分别用不同范式。②矛盾=思考-行动耦合度 vs 计划稳定性(ReAct灵活但易发散;Plan-Execute稳但僵;Reflexion靠反思纠偏但慢),本质是按任务可计划性选耦合度。③prd-tools用Plan-Execute(PRD流程可预拆)+code_assistant用轻Reflexion(自验证自修复循环)+拒绝一种范式打天下。④按任务特性匹配范式;eval=各场景行为符合预期。⑤「范式按任务可计划性选不迷信某一种」+局限(我的Reflexion是轻量版非完整论文实现)。
  - **C9 · card-title「单 Agent 还是多 Agent，一个决策树」」**(输出 `.p2-c9-single-multi.html`)—— spec §6 C9 要点:①单/多Agent决策,Manager用了多Agent(9外+3内Supervisor+Worker)。②矛盾=专业化收益 vs 协调成本(多Agent专业化强但协调/通信开销大;单Agent简单但context易混),本质是按专业化+context隔离需求选。③五问决策树(任务可拆?专业差异大?context会混?…)+Manager多Agent(9外能力+3内管理)+拒绝为了多而多。④Manager多Agent架构跑通;eval=专业化分工清晰context不混。⑤「单/多Agent按专业化+context隔离需求选」+局限(多Agent协调成本高简单任务别上)。
  - **C10 · card-title「向量库怎么选——还有我为什么自己写不用 Chroma」」**(输出 `.p2-c10-vector.html`)—— spec §6 C10 要点:①向量库选型我选自研JSON+内存余弦不是Chroma,我是code_assistant检索设计者。②矛盾=通用能力 vs 工程成本/可控性(Chroma功能全但引入依赖+运维,自研轻但能力有限),本质是按规模/场景权衡不是"哪个更先进"。③自研JSON+内存余弦(拒绝Chroma:量小不需要重依赖)+sha256增量(拒绝git钩子:更轻)+text-embedding-v3(现成embedding)。④code仓库规模小自研够用零依赖;eval=召回准增量快。⑤「选型按场景规模权衡不追'更先进'」+局限(自研只在量小才成立规模上去必须上专业向量库;主动说的边界不是藏)。⚠️此卡会合法提到"Chroma"作为被拒绝选项,正常。
- agent 必读 spec §6 C6-C10 + §4.2 雷区 + stealth-source-current.html 五张卡原文。
- prompt 末尾写死:"只产出 .p2-c6-when-agent.html / .p2-c7-framework.html / .p2-c8-paradigm.html / .p2-c9-single-multi.html / .p2-c10-vector.html 五个文件,禁碰 stealth.html 和其他卡,禁碰 .p2-c1~c5 和 .p2-c11~c14。"

- [ ] **Step 2: 校验五张产物**

```bash
cd learning/interview-tools
for f in .p2-c6-when-agent.html .p2-c7-framework.html .p2-c8-paradigm.html .p2-c9-single-multi.html .p2-c10-vector.html; do
  python3 check_p2.py "$f"; echo "  $f exit=$?"
done
```
Expected: 五张都 `✅ 校验通过(≥5 段 <strong>,全改)`,exit=0。

- [ ] **Step 3: 人工风格抽看 + Commit**

```bash
git -C /Users/didi/work/linze-journal add learning/interview-tools/.p2-c6-when-agent.html learning/interview-tools/.p2-c7-framework.html learning/interview-tools/.p2-c8-paradigm.html learning/interview-tools/.p2-c9-single-multi.html learning/interview-tools/.p2-c10-vector.html
git -C /Users/didi/work/linze-journal commit -m "feat(stealth): P2 C6-C10 选型与检索决策 五步骨架(全改)"
```

---

### Task 5: Agent-3「标杆对齐」(C11-C14,4 轻过)

**Files:**
- Create: `learning/interview-tools/.p2-c11-safety.html`
- Create: `learning/interview-tools/.p2-c12-retrieval.html`
- Create: `learning/interview-tools/.p2-c13-refactor.html`
- Create: `learning/interview-tools/.p2-c14-dispatch.html`

**Interfaces:**
- Consumes: `.p2-prompt-template.md`、`stealth-source-current.html`
- Produces: `.p2-c11` ~ `.p2-c14` 四张轻过卡 card-body 片段

- [ ] **Step 1: 派 general-purpose agent(轻过模式)**

prompt = 模板填入,但在模板开头加**轻过专项指令**:
> 「**本次是轻过(4 张已成熟卡)**:保留原文绝大部分,只做三件事——①把②本质矛盾和⑤方法论/局限补到显式(若已隐含则提炼成 `<strong>` 段首);②去掉堆名词/速查表腔;③对齐 declarative 风格。**不要大改、不要推倒重写、保留双项目对照和源码引用**。card-body 可 4 段 `<strong>`。校验用 `--light`(≥4 段)。」

- `{N}` = `4`(轻过,`--light`)
- 「本次负责的卡」:
  - **C11 · card-title「Agent Safety 怎么做——规划层加执行层」」**(输出 `.p2-c11-safety.html`)—— spec §6 C11 要点:现已是五步高级形态(规划层+执行层双项目对照+红线暴露诚实边界)。轻过:补②(Safety本质矛盾=防护 vs 不阻碍正常任务——护栏太严抵消能力太松则失控)显式化;去堆名词;对齐declarative。**保留** prd-tools+code_assistant 双项目对照。
  - **C12 · card-title「向量召回 vs 代码实体图——我两个项目各做了一个」」**(输出 `.p2-c12-retrieval.html`)—— spec §6 C12 要点:双项目对照(code_assistant向量+prd-tools正则实体图)已成熟。轻过:补②(两种检索本质差异=模糊语义匹配 vs 精确结构定位)显式化;对齐风格。**保留**双项目红线。⚠️此卡会合法提到"Chroma/向量",正常。
  - **C13 · card-title「把 39 节点的多智能体编排瘦身重构」」**(输出 `.p2-c13-refactor.html`)—— spec §6 C13 要点:真实Manager重构叙事(genre A非假设性)。轻过+补五步:补①ownership(我是重构主导者)+②(瘦身矛盾=可观测性 vs 复杂度——节点多则可观测但配置爆炸,合并则简但丢单测粒度)显式化。**保留** `managerGraph.graph.ts:67-104` 源码引用 + 拆subgraph/删合并/Critic降级决策。
  - **C14 · card-title「设计通用 Multi-Agent 调度系统（Manager 经验升华）」」**(输出 `.p2-c14-dispatch.html`)—— spec §6 C14 要点:Manager升华到通用模式。轻过+补五步:补②(通用化矛盾=特化优化 vs 通用抽象——太特化不通用太通用失去Manager具体优势)显式化。**保留** `retryBudget.ts`/`failureAttribution.ts` 源码引用 + 五大支柱。
- agent 必读 spec §6 C11-C14 + §4.2 雷区 + stealth-source-current.html 四张卡原文。
- prompt 末尾写死:"只产出 .p2-c11-safety.html / .p2-c12-retrieval.html / .p2-c13-refactor.html / .p2-c14-dispatch.html 四个文件,禁碰 stealth.html 和其他卡,禁碰 .p2-c1~c10。"

- [ ] **Step 2: 校验四张产物(轻过 --light)**

```bash
cd learning/interview-tools
for f in .p2-c11-safety.html .p2-c12-retrieval.html .p2-c13-refactor.html .p2-c14-dispatch.html; do
  python3 check_p2.py "$f" --light; echo "  $f exit=$?"
done
```
Expected: 四张都 `✅ 校验通过(≥4 段 <strong>,轻过)`,exit=0。

- [ ] **Step 3: 人工风格抽看(重点确认没过度改写)**

打开四张产物对比原文,确认:保留双项目对照/源码引用、②⑤已补显式、未推倒重写。

- [ ] **Step 4: Commit**

```bash
git -C /Users/didi/work/linze-journal add learning/interview-tools/.p2-c11-safety.html learning/interview-tools/.p2-c12-retrieval.html learning/interview-tools/.p2-c13-refactor.html learning/interview-tools/.p2-c14-dispatch.html
git -C /Users/didi/work/linze-journal commit -m "feat(stealth): P2 C11-C14 标杆卡轻过对齐(补②⑤显式+去堆名词)"
```

---

### Task 6: 组装 —— Python 锚点 splice 14 张 body(不动 data-g/subOrder/title)

**Files:**
- Create: `learning/interview-tools/assemble_p2.py`
- Modify: `learning/interview-tools/stealth.html`

**Interfaces:**
- Consumes: `.p2-c{1-14}-*.html`(Task 3/4/5)、`.p2-anchors.txt`(Task 1)
- Produces: 改写后的 stealth.html(14 张 body 替换;data-g/subOrder/title 不动)

- [ ] **Step 1: 写 assemble_p2.py**

```python
#!/usr/bin/env python3
"""P2 ai 14 张卡:只替换 card-body(不动 data-g/subOrder/title)。原子写。
标题串已在 Task 1 验证(全角标点精确),直接硬编码。"""
import os

ROOT = "/Users/didi/work/linze-journal/learning/interview-tools/"
src = open(ROOT + "stealth.html", encoding="utf-8").read()

CARDS = [
    ("从零设计一个 Agent，你的思路是什么", ".p2-c1-agent-design.html"),
    ("Agent 的记忆怎么设计：短期、长期、工作记忆", ".p2-c2-memory.html"),
    ("Agent 的工作记忆怎么管，对话越来越长咋办", ".p2-c3-working-memory.html"),
    ("Harness Engineering：Agent 等于 Model 加 Harness", ".p2-c4-harness.html"),
    ("Agent 自进化闭环怎么设计", ".p2-c5-evolution.html"),
    ("什么场景才该上 Agent，别什么活都套 Agent", ".p2-c6-when-agent.html"),
    ("Agent 框架怎么选：LangGraph vs LangChain vs AutoGen vs CrewAI vs Dify vs Coze", ".p2-c7-framework.html"),
    ("ReAct vs Plan-and-Execute vs Reflexion，什么时候用哪个", ".p2-c8-paradigm.html"),
    ("单 Agent 还是多 Agent，一个决策树", ".p2-c9-single-multi.html"),
    ("向量库怎么选——还有我为什么自己写不用 Chroma", ".p2-c10-vector.html"),
    ("Agent Safety 怎么做——规划层加执行层", ".p2-c11-safety.html"),
    ("向量召回 vs 代码实体图——我两个项目各做了一个", ".p2-c12-retrieval.html"),
    ("把 39 节点的多智能体编排瘦身重构", ".p2-c13-refactor.html"),
    ("设计通用 Multi-Agent 调度系统（Manager 经验升华）", ".p2-c14-dispatch.html"),
]

def card_body_range(html, title):
    tidx = html.find(f'card-title">{title}')
    assert tidx > 0, f"找不到 title: {title}"
    bs = html.find('<div class="card-body">', tidx)
    assert bs > 0, f"找不到 card-body: {title}"
    depth, i = 0, bs
    while i < len(html):
        if html[i:i+4] == "<div": depth += 1
        elif html[i:i+6] == "</div>":
            depth -= 1
            if depth == 0: return bs, i + 6
        i += 1
    assert False, f"card-body 不闭合: {title}"

for title, prod in CARDS:
    bs, be = card_body_range(src, title)
    nb = open(ROOT + prod, encoding="utf-8").read()
    assert '<div class="card-body">' in nb, f"{prod} 非法 body 片段"
    src = src[:bs] + nb.rstrip() + src[be:]
print(f"Step1: {len(CARDS)} 张 body 替换完成")

tmp = ROOT + "stealth.html.tmp"
open(tmp, "w", encoding="utf-8").write(src)
os.replace(tmp, ROOT + "stealth.html")
print(f"✅ P2 {len(CARDS)} 张 ai 卡 body 组装完成")
```

- [ ] **Step 2: 跑组装**

```bash
cd learning/interview-tools
python3 assemble_p2.py
```
Expected: 打印 `Step1: 14 张 body 替换完成` + `✅ P2 14 张 ai 卡 body 组装完成`。若 assert 报错(找不到 title),停下:对照 `.p2-anchors.txt` 确认标题串与文件完全一致(全角标点)。

- [ ] **Step 3: 验证卡数/标题/data-g 未误动**

```bash
cd learning/interview-tools
echo "=== ai 卡数(应仍 65,未增删卡) ==="
grep -oE 'data-c="ai"' stealth.html | wc -l
echo "=== 14 张标题仍在(各 1) ==="
python3 - <<'PY'
import re
html = open("stealth.html", encoding="utf-8").read()
titles = ["从零设计一个 Agent","Agent 的记忆怎么设计","Agent 的工作记忆怎么管","Harness Engineering",
"Agent 自进化闭环怎么设计","什么场景才该上 Agent","Agent 框架怎么选","ReAct vs Plan-and-Execute",
"单 Agent 还是多 Agent","向量库怎么选","Agent Safety 怎么做","向量召回 vs 代码实体图",
"把 39 节点的多智能体编排瘦身重构","设计通用 Multi-Agent 调度系统"]
for t in titles:
    print(f"  [{len(re.findall(r'card-title\">'+re.escape(t), html))}] {t}")
PY
echo "=== data-g 组分布未变(各组分母应同 Task 1 备份) ==="
for g in "Agent 基础" "Loop 工程" "RAG 检索" "系统设计"; do
  echo "  $g: $(grep -c "data-g=\"$g\"" stealth.html)"
done
```
Expected: ai 卡数 65;14 张标题各 1;data-g 组计数与备份前一致(Agent 基础 12 / Loop 工程 5 / RAG 检索 8 / 系统设计 8,以 Task 1 备份为准)。若 ai 卡数 ≠65 或标题丢失,`git checkout stealth.html` 回退重查。

- [ ] **Step 4: 浏览器肉眼验收**

`open learning/interview-tools/stealth.html` → AI tab → quickbar 各分组(Agent 基础/Loop 工程/RAG 检索/系统设计)点开,确认 14 张卡五段渲染正常、core 高亮在、无破版。确认其余 51 张卡未受影响。

- [ ] **Step 5: Commit**

```bash
git -C /Users/didi/work/linze-journal add learning/interview-tools/stealth.html learning/interview-tools/assemble_p2.py
git -C /Users/didi/work/linze-journal commit -m "feat(stealth): 组装P2 ai 14张卡body(10全改+4轻过五步骨架)"
```

---

### Task 7: 全局校验 + §4.2 雷区人工抽检 + bump sw.js + push

**Files:**
- Modify: `sw.js`

**Interfaces:**
- Consumes: 改写后的 stealth.html(Task 6)

- [ ] **Step 1: 全局 grep 校验**

```bash
cd learning/interview-tools
echo "=== div 平衡(应相等) ==="
grep -oE '<div[^>]*>' stealth.html | wc -l
grep -oE '</div>' stealth.html | wc -l
echo "=== <script> 完整(开=闭) ==="
grep -c '<script' stealth.html; grep -c '</script>' stealth.html
echo "=== 禁用项残留(应全 0) ==="
grep -cE '说白了|得说句实话|我自己比较得意|\[loop' stealth.html
echo "=== '6 步闭环'全文档(应 0) ==="
grep -cE '6 步闭环|6步闭环' stealth.html
```
Expected: div 开=闭;script 开=闭;禁用项 0;"6 步闭环" 0。

- [ ] **Step 2: §4.2 雷区人工 grep 抽检(读上下文判断误用 vs 合法提及)**

```bash
cd learning/interview-tools
echo "=== 抽 14 张卡所在行段,逐个雷区词看上下文 ==="
echo "--- Claude/GPT/Anthropic(若作 Manager 模型用=误用;作 Claude Code 插件/对比=合法) ---"
grep -nE 'Claude|GPT|Anthropic' stealth.html | head -40
echo "--- Chroma(作'我用的向量库'=误用;作'被拒绝选项/C10'=合法) ---"
grep -n 'Chroma' stealth.html
echo "--- git 钩子(作'增量机制'=误用;作'不是git钩子'=合法) ---"
grep -nE 'git ?钩子|git hook' stealth.html
echo "--- SDD(作'prd-tools 是'=误用) ---"
grep -n 'SDD' stealth.html
echo "--- '20+ 人'/'20多人'硬数(应软化) ---"
grep -nE '20\+ ?人|20多 ?人|二十多 ?人' stealth.html
```
Expected: **人工逐行读上下文**。合法提及(C10 "不用 Chroma"、prd-tools "Claude Code 插件"、C10 "sha256 不是 git 钩子")保留;**误用**(把 Manager 模型说成 Claude/GPT、把向量库说成 Chroma、把 prd-tools 说成 SDD 平台、"20+人"硬数)→ 回 Task 3/4/5 对应 agent 修正后重组装。

- [ ] **Step 3: 看 origin 当前 CACHE_NAME 并 bump**

```bash
cd /Users/didi/work/linze-journal
git fetch origin main 2>/dev/null
echo "=== origin 上的 CACHE_NAME ==="
git show origin/main:sw.js | grep CACHE_NAME
echo "=== 本地当前 ==="
grep CACHE_NAME sw.js
```
Expected: origin = `kb-v324`,本地 = `kb-v324`。把 `sw.js` 里 `CACHE_NAME` 改成 **`kb-v325`**。

- [ ] **Step 4: 确认 remote 是个人账号 + Commit + push**

```bash
cd /Users/didi/work/linze-journal
echo "=== 确认 origin 指向个人账号(zachary-lz-glm) ==="
git remote -v
git add sw.js
git commit -m "chore(stealth): bump CACHE_NAME kb-v324→kb-v325(P2 ai 14张卡五步重构)"
git push origin main
```
若 `git remote -v` 显示 origin 不是个人账号(是公司账号),停下确认正确的个人 remote 名再用 `git push <个人remote> main`。**绝不推公司账号**(memory [[github-account]])。

- [ ] **Step 5: 硬刷新验证**

`open learning/interview-tools/stealth.html` 后硬刷新(Cmd+Shift+R),确认 Service Worker 接管新版、AI tab 各分组 14 张卡显示新 body。

- [ ] **Step 6: 清理临时产物**

```bash
cd learning/interview-tools
rm -f .p2-c1-agent-design.html .p2-c2-memory.html .p2-c3-working-memory.html \
      .p2-c4-harness.html .p2-c5-evolution.html .p2-c6-when-agent.html \
      .p2-c7-framework.html .p2-c8-paradigm.html .p2-c9-single-multi.html \
      .p2-c10-vector.html .p2-c11-safety.html .p2-c12-retrieval.html \
      .p2-c13-refactor.html .p2-c14-dispatch.html \
      .p2-anchors.txt .p2-prompt-template.md stealth-source-current.html
git add -A && git commit -m "chore(stealth): 清理P2重构临时产物(保留check_p2/assemble_p2脚本)" || echo "无变更"
git push origin main
```
**保留** `check_p2.py` 和 `assemble_p2.py`(后续 B/D 子项目可复用思路,不删)。

---

## 自审(对照 spec)

- **Spec 覆盖**: spec §2 范围(14张:10全改+4轻过,51张跳过,零routing)→ Task 1-7 全程基调 + Task 6 Step3 验证(65卡数/标题/data-g未误动);§3.2 全改vs轻过 → Task 2 check脚本 --light 阈值 + Task 3/4(全改不带--light)/Task 5(轻过带--light);§3.3 无routing简化 → Task 6 assemble 只body swap + Global Constraints;§3.4 标题修剪(默认不做)→ Global Constraints + Task 6 不含标题逻辑;§3.5 agent分工5+5+4 → Task 3/4/5;§4 校准复用清单+§4.2雷区 → Global Constraints + Task 2 prompt模板 + Task 7 Step2 人工grep抽检(含脚本不做naive雷区的rationale);§5 五步模板+硬约束 → Task 2 prompt模板;§6 14张卡骨架 → Task 3/4/5 prompt 逐卡填入spec §6要点;§7 多agent流程 → Task 1-7;§8 质量门 → Task 2 脚本+Task 7 grep+Task 3/4/5人工抽看。✅ 全覆盖。
- **Placeholder**: Task 2 prompt模板为实文;Task 3/4/5 每卡给了 spec §6 实际五步要点(①业务/②矛盾/③决策+拒绝/④eval/⑤方法论+局限逐条);Task 6 assemble 脚本为完整可跑代码,14个标题串已在Task 1验证为精确全角串、硬编码;check_p2.py 完整可跑。无 TBD。✅
- **类型/命名一致**: 14 个产物文件名 `.p2-c{1-14}-*.html` 在 Task 3/4/5 产出、Task 6 CARDS 列表、Task 7 清理命令三处一致;14 个 card-title 锚点在 Task 1 验证脚本、Task 6 CARDS 硬编码、Task 6 Step3 验证三处一致(全角标点精确:，：—— ());`--light` 标志在 Task 2 脚本定义、Task 5 使用、Task 5 Step2 校验命令一致;bump 版本号统一 `kb-v325`(Global Constraints + Task 7 Step3/4 + commit message 一致)。✅
- **脚本不做naive雷区的合理性**: spec §7 step2 说 check 加 §4.2 雷区抽检;计划发现 naive 子串会误报合法"被拒绝选项"提及(C10"不用Chroma"、prd-tools"Claude Code插件"),故 check_p2.py 只自动查"6步闭环"(无歧义),其余 §4.2 雷区改 Task 7 Step2 人工grep读上下文。spec 意图(§4.2必须强制)保留,执行方式更可靠。已记入 Global Constraints + Task 2 脚本注释。✅
