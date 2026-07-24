# stealth.html 综合卡片全面重构 · 实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 把 stealth.html 综合 tab 从"按面试环节分组(28 卡)"重构成"9 张自我陈述主卡 + 弹药·参考(共 22 卡)",每张主卡 CLEAR/L + 证据锚点 + 诚实边界 + 内嵌预判追问清单。

**Architecture:** 备份 → 并行 9 个 agent 各写 1 张主卡 HTML 片段(check 脚本校验)→ Python 锚点脚本原子组装(插 9 / 删 15 / 改 data-g / 改 subOrder)→ grep 终检 → bump sw.js。照搬 D 深挖卡重构的 assemble_d.py / check_d.py 模式。

**Tech Stack:** 纯 HTML(无构建)、Python3 校验/组装脚本、git、Service Worker(sw.js)。

**Spec:** `docs/superpowers/specs/2026-07-24-stealth-comprehensive-mastercards-design.md`(§6 有 9 张主卡完整骨架,实施时必读)

## Global Constraints(每个 task 隐含遵守)

- **⚠️ 顺序前置(最重要)**:本计划改 `stealth.html`,与并行会话的 PRD 模块重构(`feat/prd-module-reorg` 分支)**改同一文件**。实施必须在 PRD 重构**合并/稳定进 stealth.html 之后**进行。动手前先 `git log --oneline -5` + `grep` 确认 emer 卡数与锚点标题与本文档一致(当前基线 emer=28 卡);若 PRD 重构后 stealth.html 结构变了,**重新核对锚点标题与卡数再组装**。
- **风格=口语逐字稿**(对标现有创业3卡 `stealth.html:4700-4733`):第一人称、能直接念。**不用** §6 declarative(`<strong>段首。</strong>` 堆叠)——那是 Agent 技术卡的规矩。少滥用 `<strong>`,禁速查表腔(必背/杀手锏/被问X必答/金句钩子)。
- **9 张主卡**: `data-c="emer" data-g="自我声明"` · 标题序号①-⑨ · 不带英文项目名前缀。
- **数字校准(防穿帮)**:Q9 分档——LangGraph/向量检索/GraphRAG/OpenHands 在"用过/源码"档;**Cursor/Claude Code/OpenAI Agent SDK/MCP 必须明确标"产品体验"档,绝不装"读过源码"**。雷区词(Chroma/git钩子/Claude/GPT/SDD平台/6步闭环/20+人)只在"否定/产品体验"语境出现。所有数字带口径(5h→2h 注 n=5、40%→85% 注 n=10 产物稳定性)。
- **bump `sw.js` 的 `CACHE_NAME`**:看 **origin 已部署版本** +1(不是本地最新 commit 号)。并发时后推者先看 origin 再 +1,防撞号。
- **并发 git 纪律**:改 stealth.html 前 `git status` 确认工作区干净;改完**立刻提交**,别拖(并行会话 `git add` 整文件会扫走你的改动——见 memory `feedback_parallel_review_git_collision`)。
- **路由零风险**:`getGroup` 逻辑不动(仍 `data-g` 优先),只新增/改 `data-g` 值与 `subOrder`。

## File Structure

| 文件 | 责任 | 动作 |
|------|------|------|
| `learning/interview-tools/stealth.html` | 主页(emer 综合模块) | 改:插 9 / 删 15 / 改 data-g / 改 subOrder |
| `learning/interview-tools/check_comprehensive.py` | 9 张主卡片段校验(CLEAR/证据/边界/追问/div/雷区) | 新建 |
| `learning/interview-tools/assemble_comprehensive.py` | 组装:插 9 + 删 15 + 改 data-g + 改 subOrder,原子写 | 新建 |
| `/tmp/comp-card-{1..9}.html` | 9 张主卡片段(agent 产出,组装后可删) | 新建(临时) |
| `learning/interview-tools/stealth-source-current.html` | 重写源料/回退兜底 | 已有(PRD 会话建),Task1 确认/刷新 |
| `learning/interview-tools/sw.js` | Service Worker 缓存版本 | 改 CACHE_NAME +1 |
| `docs/superpowers/specs/2026-07-24-stealth-comprehensive-mastercards-design.md` | spec(§6 九张骨架) | 读(不改) |

---

### Task 1: 备份 + 核对基线

**Files:**
- Verify: `learning/interview-tools/stealth.html`(emer 卡数=28、锚点标题)
- Refresh: `learning/interview-tools/stealth-source-current.html`

**Interfaces:**
- Produces: `stealth-source-current.html` 作为后续 agent 取"被吸掉旧卡原文"的源料 + 回退兜底。

- [ ] **Step 1: 确认工作区干净 + 当前分支**

Run: `git status && git branch --show-current`
Expected: 工作区干净(或只有本次相关改动)。记录分支名。⚠️ 若在 `feat/prd-module-reorg` 且 PRD 会话未稳定,**停**,等 PRD 合并后再做。

- [ ] **Step 2: 核对 emer 基线卡数**

Run: `grep -oP 'data-c="emer" data-g="[^"]*"' learning/interview-tools/stealth.html | sort | uniq -c`
Expected(PRD 未动综合时): `HR面 6 / 反问 5 / 话术急救 6 / 软技能 10 / 项目数据 1`(共 28)。若数字不符,**先查明**(可能 PRD 已改文件),别盲组装。

- [ ] **Step 3: 刷新备份源**

Run: `cp learning/interview-tools/stealth.html learning/interview-tools/stealth-source-current.html`
(覆盖 PRD 会话旧的备份,确保含最新 stealth.html 作为源料)

- [ ] **Step 4: 抽取被吸掉的 15 张旧卡的锚点标题(供 Task 4 删除用)**

Run(确认每个标题在文件里唯一):
```bash
for t in "优点和缺点" "为什么录用你" "最有成就感的事" "AI 会取代前端吗" \
         "方案推不动" "价值靠什么衡量" "为什么我想要创业状态" \
         "从 0 到 1 让我兴奋在哪" "我为什么主动选创业节奏" \
         "空窗期怎么解释" "最大的失败" "薪资低于预期怎么谈" \
         "手上有其他 offer 吗" "业务方关心什么" "了解 X 吗"; do
  n=$(grep -c "card-title\">$t\|card-title\">[^<]*$t" learning/interview-tools/stealth.html)
  echo "$n  $t"
done
```
Expected: 每行 ≥1。记录每个标题的**精确 card-title 子串**(打开 stealth-source-current.html 核对完整标题文本,如"最大的失败 / 挫折")。这 15 个子串喂给 Task 4 的 assemble 脚本。

- [ ] **Step 5: Commit**

```bash
git add learning/interview-tools/stealth-source-current.html
git commit -m "chore(stealth): 综合重构备份源(emer 28卡基线)"
```

---

### Task 2: 写片段校验脚本 check_comprehensive.py

**Files:**
- Create: `learning/interview-tools/check_comprehensive.py`

**Interfaces:**
- Consumes: 单张主卡 HTML 片段文件路径 + 卡序号(1-9)
- Produces: exit 0=通过 / exit 1=失败,stdout 打印 errs/warns。Task 3 每个 agent 产出后跑它。

- [ ] **Step 1: 写 check_comprehensive.py**

Create `learning/interview-tools/check_comprehensive.py`:
```python
#!/usr/bin/env python3
"""校验综合主卡片段(口语逐字稿版 CLEAR/L)。用法:
python3 check_comprehensive.py <card.html> --n 1..9
检查: data-g=自我陈述 / 标题带①-⑨序号 / CLEAR四要素词(背景·Leadership·执行·结果各≥1,warn) /
证据锚点词 / 诚实边界词 / 预判追问<ul>≥4条<li> / div平衡 / 完整card /
速查表腔(err) / Q9雷区(Cursor等只在'产品体验'语境,warn)
注:综合主卡是口语逐字稿,不禁'说白了'等口语连接词(那是§6 declarative卡的规矩)。"""
import re, sys, argparse

p = argparse.ArgumentParser()
p.add_argument("new")
p.add_argument("--n", type=int, required=True, choices=range(1, 10))
a = p.parse_args()

html = open(a.new, encoding="utf-8").read()
errs, warns = [], []

# 1. data-g=自我陈述
if 'data-g="自我陈述"' not in html:
    errs.append('缺 data-g="自我陈述"')

# 2. 标题带对应序号
circles = "①②③④⑤⑥⑦⑧⑨"
if circles[a.n - 1] not in html:
    errs.append(f"标题缺序号 {circles[a.n-1]}(第{a.n}张)")

# 3. CLEAR 四要素词(warn,口语逐字稿语义靠人工)
CONTEXT = ["背景", "之前", "那时", "起因", "遇到", "情境", "场景"]
LEADERSHIP = ["我主动", "我选", "我决定", "我想要", "为什么是我", "我牵头", "我主导", "主动选", "我算过", "我的判断"]
EXEC = ["做了", "设计了", "搭了", "三步", "两步", "策略", "具体", "陪跑", "试点", "门禁", "证据链"]
RESULT = ["结果", "变成", "从", "同事", "证据", "数据", "缩短", "验证"]
if not any(w in html for w in CONTEXT): warns.append("未见 Context 词")
if not any(w in html for w in LEADERSHIP): warns.append("未见 Leadership 词(为什么是你)")
if not any(w in html for w in EXEC): warns.append("未见 Execution 词")
if not any(w in html for w in RESULT): warns.append("未见 Results/证据词")

# 4. 诚实边界词(warn,Reflection 段不可省)
HONESTY = ["得说实话", "诚实", "没成", "不理想", "边界", "局限", "原型", "预研", "没接", "在补", "验证期", "小范围", "不是已", "坦白"]
if not any(w in html for w in HONESTY): warns.append("未见诚实边界词(Reflection 段不可省)")

# 5. 预判追问 ≥4 条 <li>
lis = re.findall(r"<li>[^<]", html)
if len(lis) < 4:
    errs.append(f"预判追问 <li> 只有 {len(lis)} 条,需 ≥4")

# 6. 速查表腔(err)
banned = ["必背", "杀手锏", "必答", "金句钩子", "被问.*必答"]
hit = [w for w in banned if re.search(w, html)]
if hit: errs.append(f"命中速查表腔: {hit}")

# 7. div 平衡
if html.count("<div") != html.count("</div>"):
    errs.append(f"div 不平衡: <div {html.count('<div')} / </div> {html.count('</div>')}")

# 8. 完整 card 片段
if not html.lstrip().startswith('<div class="card"'):
    errs.append("片段非完整 card(应以 <div class=\"card\" 开头)")

# 9. 硬雷区 err:6 步闭环
if "6 步闭环" in html or "6步闭环" in html:
    errs.append("含'6 步闭环'(不存在,§4 雷区)")

# 10. Q9(n=9)产品体验档雷区 warn
if a.n == 9:
    for w in ["Cursor", "Claude Code", "Agent SDK", "MCP"]:
        if w in html and "产品体验" not in html and "只用过" not in html and "体验级" not in html:
            warns.append(f"Q9 出现 {w} 但未标'产品体验'(必须分档,防装读过源码)")

if warns:
    print(f"⚠️ 提示(--n {a.n},语义/语境在即可,不阻塞):")
    for w in warns: print("  -", w)
if errs:
    print(f"❌ 校验失败(--n {a.n}):")
    for e in errs: print("  -", e)
    sys.exit(1)
print(f"✅ 校验通过(--n {a.n},{len(lis)} 条追问,{len(warns)}条提示)")
```

- [ ] **Step 2: chmod + 抽测(用一个占位片段确认脚本能跑)**

Run: `chmod +x learning/interview-tools/check_comprehensive.py`
写一个最小合法片段到 /tmp/t.html 跑一次,确认无语法错:
```bash
cat > /tmp/t.html <<'EOF'
<div class="card" data-c="emer" data-g="自我陈述" data-kw="test">
<div class="card-head"><span class="tag emer">t</span><div class="card-title">①t</div></div>
<div class="core">t</div><div class="card-body">
<p>背景之前遇到的情境。</p><p>我主动选的,我决定。</p>
<p>做了三步,设计了证据链。</p><p>结果同事变了,有数据验证。</p>
<p>得说实话:小范围,边界是预研。</p>
<ul class="points"><li>q1?→a</li><li>q2?→a</li><li>q3?→a</li><li>q4?→a</li></ul>
</div></div>
EOF
python3 learning/interview-tools/check_comprehensive.py /tmp/t.html --n 1
```
Expected: `✅ 校验通过(--n 1,4 条追问,0/N条提示)`

- [ ] **Step 3: Commit**

```bash
git add learning/interview-tools/check_comprehensive.py
git commit -m "feat(stealth): 综合主卡片段校验脚本 check_comprehensive.py"
```

---

### Task 3: 并行写 9 张自我陈述主卡

**Files:**
- Create: `/tmp/comp-card-{1..9}.html`(9 个,组装后可删)

**Interfaces:**
- Consumes: spec §6.1-§6.9 骨架 + `stealth-source-current.html` 里被吸掉旧卡的原文 + `check_comprehensive.py`
- Produces: 9 个完整 `<div class="card" data-c="emer" data-g="自我陈述">` 片段(每个过 check)

> 用 superpowers:dispatching-parallel-agents(或 Workflow)并行派 9 个 agent,**每张一个**。每个 agent prompt 用下面的模板,填该卡的 `{{SPEC_SECTION}}` / `{{SOURCE_CARDS}}` / `{{N}}`。

**主卡映射表(喂给各 agent):**

| N | 序号 | 标题 | spec 骨架 | 并入旧卡(从 stealth-source-current.html 取原文) | 输出 |
|---|------|------|-----------|------|------|
| 1 | ① | 为什么看机会/为什么离开滴滴 | §6.1 | open离职原因+动机收尾 + emer空窗期 | /tmp/comp-card-1.html |
| 2 | ② | 你的核心竞争力/优缺点 | §6.2 | emer优点和缺点 + 为什么录用你 | /tmp/comp-card-2.html |
| 3 | ③ | AI时代的职业规划/你想做什么 | §6.3 | open职业规划+精力分配 + emerAI会取代前端吗 | /tmp/comp-card-3.html |
| 4 | ④ | 手里offer/薪资怎么谈 | §6.4 | emer手上有其他offer吗 + 薪资低于预期 | /tmp/comp-card-4.html |
| 5 | ⑤ | 对创业的想法/想要什么状态 | §6.5 | emer创业3卡(为什么想要/从0到1兴奋/为什么主动选) | /tmp/comp-card-5.html |
| 6 | ⑥ | 最有成就感的事 | §6.6 | emer最有成就感的事 | /tmp/comp-card-6.html |
| 7 | ⑦ | 你关注业务指标吗/怎么挂钩 | §6.7 | emer价值靠什么衡量 + 业务方关心什么 | /tmp/comp-card-7.html |
| 8 | ⑧ | 最大的困难/怎么解决的 | §6.8 | emer最大的失败挫折 + 方案推不动 | /tmp/comp-card-8.html |
| 9 | ⑨ | 行业洞察/你深度了解过哪些方案 | §6.9 | emer反问4卡(快手/动念/B端/同类工具)+ 了解X吗 | /tmp/comp-card-9.html |

**Agent prompt 模板(每张填入对应值):**

```
你是面试速查卡写作专家。任务:为 stealth.html 综合 tab 写第 {{N}} 张自我陈述主卡,产出【可直接粘贴的完整 HTML 片段】写到 /tmp/comp-card-{{N}}.html。

【必读】
1. 设计文档:docs/superpowers/specs/2026-07-24-stealth-comprehensive-mastercards-design.md —— 读 §5(主卡模板)+ §6.{{SECTION}}(本卡完整骨架:core/CLEAR四段/证据/边界/追问)+ §4(校准料:Q9分档/Q8主线/数字雷区)。严格按 §6.{{SECTION}} 的骨架写。
2. 写作指南:learning/interview-tools/STEALTH-CARDS-GUIDE.md §1(铁律)+ §2.2(卡片 HTML 模板)。
3. 风格标尺:口语逐字稿,对标 stealth-source-current.html 里「为什么我想要创业状态」「从 0 到 1 让我兴奋在哪」「我为什么主动选创业节奏」3 张卡(第一人称、能直接念、自然连接词)。禁 §6 declarative 碎嘴堆叠、禁速查表腔(必背/杀手锏/被问X必答)。
4. 源料:从 stealth-source-current.html 取这些旧卡的原文,把精华并入本卡:{{SOURCE_CARDS}}(按 card-title 定位)。并入后旧卡会删,所以精华要全吸收进主卡。

【硬约束】
- 完整 <div class="card" data-c="emer" data-g="自我陈述" data-kw="..."> 开头(data-kw 覆盖这道题各种问法)。
- card-title 带序号 {{CIRCLE}} 且不带英文项目名前缀。
- core:一句口语化金色钩子(30 秒能念)。
- body 顺序:【背景+为什么是你(Context+Leadership)】→【怎么做(Execution)】→【结果+证据锚点(Results,挂可追溯证据/已校准数字)】→【反思/诚实边界(Reflection:局限/没做成/下次)】→【预判追问 <ul class="points"> ≥4 条,每条"问?→ 一句话答 或 → 指向弹药·XX卡"】。
- 数字带口径(5h→2h 注 n=5;40%→85% 注 n=10 产物稳定性);雷区词(Chroma/git钩子/Claude/GPT/SDD/6步闭环/20+人)只在"否定/产品体验"语境。
- Q9(第9张)特例:LangGraph/向量检索/GraphRAG/OpenHands=用过或源码档;Cursor/Claude Code/Agent SDK/MCP **必须明标"产品体验"档,绝不装读过源码**。

【产出】
只写 HTML 片段(到 </div> 闭合),无 html/body 包裹、无 markdown。写完自查 div 平衡、追问≥4条。

【自检】
写完跑:python3 learning/interview-tools/check_comprehensive.py /tmp/comp-card-{{N}}.html --n {{N}},必须 ✅ 通过(err=0)。warn 可有(语义在即可)。不通过就改到通过。
```

- [ ] **Step 1: 并行派 9 个 agent**(每张一个,用上面模板填值;循环序号子串 ①-⑨)

dispatch 9 agents → 各产出 /tmp/comp-card-{1..9}.html。

- [ ] **Step 2: 逐张跑 check_comprehensive.py**

Run:
```bash
for n in 1 2 3 4 5 6 7 8 9; do
  echo "=== card $n ==="
  python3 learning/interview-tools/check_comprehensive.py /tmp/comp-card-$n.html --n $n
done
```
Expected: 9 张全 `✅ 校验通过`。err≠0 的退回 agent 改到通过。

- [ ] **Step 3: 人工抽检 Q9 分档 + 数字雷区**

Run: `grep -nE "Cursor|Claude Code|Agent SDK|MCP|Chroma|git 钩子|6 步闭环|20\+人" /tmp/comp-card-9.html`
Expected: Cursor/Claude Code/Agent SDK/MCP 行附近有"产品体验/只用过/体验级"字样;Chroma/git钩子等只在"不用/否定"语境。不符退回改。

- [ ] **Step 4: Commit(9 个片段)**

```bash
mkdir -p /tmp  # 片段在 /tmp 不进 git;此处记录已产出
# 片段是临时产物,不单独 commit(组装后 stealth.html 才提交)。记录 9 张已校验通过即可。
echo "9 张主卡片段已校验通过,待 Task 5 组装"
```

---

### Task 4: 写组装脚本 assemble_comprehensive.py

**Files:**
- Create: `learning/interview-tools/assemble_comprehensive.py`

**Interfaces:**
- Consumes: `/tmp/comp-card-{1..9}.html` + `stealth.html`(当前)+ Task1 抽取的 15 个删除锚点标题
- Produces: 原子改写 `stealth.html`(插 9 / 删 15 / 改 3 张 data-g / 改 subOrder)

- [ ] **Step 1: 写 assemble_comprehensive.py**

Create `learning/interview-tools/assemble_comprehensive.py`:
```python
#!/usr/bin/env python3
"""综合重构组装:插 9 张主卡 + 删 15 张旧卡 + 改 3 张 residue 的 data-g + 改 subOrder。原子写。
锚点:
  插入点: <!-- ==================== 综合模块 v2 ==================== --> 后(emer 顶部,主卡置首)
  删除:按 card-title 子串 → rfind <div class="card" → depth 数到闭合 </div> → 切除整块
  data-g 改:入职规划 软技能→HR·行为面;上级冲突/加班 HR面→HR·行为面
  subOrder:加'自我陈述':0.5,删'软技能',改'HR面'→'HR·行为面'"""
import re, os, sys

ROOT = "/Users/didi/work/linze-journal/learning/interview-tools/"
HTML = ROOT + "stealth.html"

# 待删 15 张旧卡 card-title 子串(精确,Task1 Step4 核对过)。若 PRD 改过 stealth.html,先重新核对!
DELETE_TITLES = [
    "优点和缺点", "为什么录用你", "最有成就感的事", "AI 会取代前端吗",
    "方案推不动", "价值靠什么衡量", "为什么我想要创业状态",
    "从 0 到 1 让我兴奋在哪", "我为什么主动选创业节奏",
    "空窗期怎么解释", "最大的失败", "薪资低于预期怎么谈",
    "手上有其他 offer 吗", "业务方关心什么", "了解 X 吗",
]

html = open(HTML, encoding="utf-8").read()
problems = []

# --- A. 删 15 张旧卡 ---
def find_card_block(h, title_sub):
    """返回 (start, end) 卡片 <div...>...</div> 闭区间;找不到返回 None。"""
    pat = 'card-title">' + title_sub
    idxs = [m.start() for m in re.finditer(re.escape(pat), h)]
    if len(idxs) != 1:
        return None, f"删:锚点'{title_sub}'匹配{len(idxs)}次,应1"
    o = h.rfind('<div class="card"', 0, idxs[0])
    if o < 0:
        return None, f"删:找不到'{title_sub}'的开标签"
    depth, i, close_end = 0, o, None
    while i < len(h):
        if h[i:i+4] == '<div':
            depth += 1; i = h.find('>', i) + 1
        elif h[i:i+6] == '</div>':
            depth -= 1; i += 6
            if depth == 0:
                close_end = i; break
        else:
            i += 1
    if close_end is None:
        return None, f"删:'{title_sub}'未闭合"
    return (o, close_end), None

for t in DELETE_TITLES:
    blk, err = find_card_block(html, t)
    if err:
        problems.append(err); continue
    html = html[:blk[0]] + html[blk[1]:]
    print(f"删除: {t}")

if problems:
    print("❌ 删除锚点问题,未写文件:"); [print("  -", p) for p in problems]; sys.exit(1)

# --- B. 改 3 张 residue 的 data-g ---
# 入职规划: 软技能→HR·行为面;上级冲突、加班: HR面→HR·行为面
for t, old_g, new_g in [
    ("入职前 3 个月怎么规划", "软技能", "HR·行为面"),
    ("和上级意见冲突", "HR面", "HR·行为面"),
    ("怎么看待加班", "HR面", "HR·行为面"),
]:
    blk, err = find_card_block(html, t)
    if err:
        problems.append(f"data-g改:{err}"); continue
    block = html[blk[0]:blk[1]]
    if f'data-g="{old_g}"' not in block:
        problems.append(f"data-g改:'{t}' 当前非 data-g=\"{old_g}\"(可能已改/PRD动过)"); continue
    block = block.replace(f'data-g="{old_g}"', f'data-g="{new_g}"', 1)
    html = html[:blk[0]] + block + html[blk[1]:]
    print(f"改 data-g: {t}  {old_g}→{new_g}")

if problems:
    print("❌ data-g 改问题,未写文件:"); [print("  -", p) for p in problems]; sys.exit(1)

# --- C. 插 9 张主卡(emer 顶部,综合模块 v2 标记后) ---
frag_all = "\n".join(
    open(f"/tmp/comp-card-{n}.html", encoding="utf-8").read().strip()
    for n in range(1, 10)
)
marker = "<!-- ==================== 综合模块 v2 ==================== -->"
if html.count(marker) != 1:
    problems.append(f"插入标记匹配{html.count(marker)}次,应1")
else:
    mi = html.index(marker) + len(marker)
    html = html[:mi] + "\n" + frag_all + "\n" + html[mi:]
    print("插入: 9 张自我陈述主卡 → 综合模块 v2 顶部")

# --- D. 改 subOrder ---
old_sub = "'项目数据':1,'软技能':2,'HR面':3,'反问':4,'话术急救':5"
new_sub = "'自我陈述':0.5,'项目数据':1,'HR·行为面':3,'反问':4,'话术急救':5"
if old_sub not in html:
    problems.append(f"subOrder 原串未找到(可能 PRD 改过):\n  {old_sub}")
else:
    html = html.replace(old_sub, new_sub, 1)
    print("改 subOrder: +自我陈述, -软技能, HR面→HR·行为面")

if problems:
    print("❌ 组装问题,未写文件:"); [print("  -", p) for p in problems]; sys.exit(1)

# --- E. 完整性断言 + 原子写 ---
assert html.count("<div") == html.count("</div>"), f"全文 div 不平衡: {html.count('<div')}/{html.count('</div>')}"
assert "<script>" in html and "</script>" in html, "script 残缺"
tmp = HTML + ".tmp"
open(tmp, "w", encoding="utf-8").write(html)
os.replace(tmp, HTML)
print("✅ 综合重构组装完成")
```

- [ ] **Step 2: chmod + 自检(脚本本身无语法错)**

Run: `chmod +x learning/interview-tools/assemble_comprehensive.py && python3 -c "import ast; ast.parse(open('learning/interview-tools/assemble_comprehensive.py').read()); print('语法 OK')" `
Expected: `语法 OK`

- [ ] **Step 3: Commit**

```bash
git add learning/interview-tools/assemble_comprehensive.py
git commit -m "feat(stealth): 综合重构组装脚本 assemble_comprehensive.py(插9/删15/改data-g/subOrder)"
```

---

### Task 5: 组装 + 终检 + bump sw.js + 提交

**Files:**
- Modify: `learning/interview-tools/stealth.html`(由脚本原子改)
- Modify: `learning/interview-tools/sw.js`(CACHE_NAME +1)

**Interfaces:**
- Consumes: Task3 的 9 片段 + Task4 脚本

- [ ] **Step 1: 跑组装脚本**

Run: `python3 learning/interview-tools/assemble_comprehensive.py`
Expected: 末行 `✅ 综合重构组装完成`,中间打印 15 行"删除:"+ 3 行"改 data-g:"+ "插入:"+ "改 subOrder:"。任何 `❌` 立即停,按提示修(多半是 PRD 改过 stealth.html 导致锚点/串失配 → 回 Task1 重核锚点)。

- [ ] **Step 2: grep 终检 emer 结构**

Run: `grep -oP 'data-c="emer" data-g="[^"]*"' learning/interview-tools/stealth.html | sort | uniq -c`
Expected: `自我陈述 9 / 项目数据 1 / HR·行为面 3 / 反问 5 / 话术急救 4`(共 22)。不是这个就停排查。

- [ ] **Step 3: grep 终检 主卡序号 + data-g + 无英文项目名标题**

Run:
```bash
echo "=== 9 张主卡序号 ===" && grep -oP 'data-g="自我陈述"[^>]*>.*?card-title">\K[①②③④⑤⑥⑦⑧⑨]' learning/interview-tools/stealth.html | tr '\n' ' '
echo "" && echo "=== 全文 div 平衡 ===" && python3 -c "h=open('learning/interview-tools/stealth.html').read();print('<div',h.count('<div'),'</div>',h.count('</div>'),'OK' if h.count('<div')==h.count('</div>') else 'BAD')"
echo "=== 自我陈述组无英文项目名前缀标题 ===" && grep -oP 'data-g="自我陈述".*?card-title">\K[^<]+' learning/interview-tools/stealth.html
```
Expected: 序号 `① ② ③ ④ ⑤ ⑥ ⑦ ⑧ ⑨` 各一次;div 平衡 OK;9 个标题无 "Manager_/code_/prd-tools" 前缀。

- [ ] **Step 4: grep 终检 雷区(只在否定/产品体验语境)**

Run: `grep -nE "Chroma|git 钩子|6 步闭环|SDD 平台|20\+人|Claude|GPT-[0-9]" learning/interview-tools/stealth.html | grep "自我陈述\|comp-card" || echo "主卡区无裸雷区词"`
Expected: 主卡区雷区词都带"不用/否定/产品体验"语境(人工扫一眼 9 张)。

- [ ] **Step 5: 确认 subOrder 已更新**

Run: `grep -n "自我陈述.*项目数据.*HR·行为面" learning/interview-tools/stealth.html`
Expected: 命中 subOrder 那行,含 `'自我陈述':0.5,...'HR·行为面':3,...`,且无 `'软技能'` 残留。

- [ ] **Step 6: bump sw.js CACHE_NAME(看 origin +1)**

Run:
```bash
echo "=== origin 当前 ===" && git fetch -q origin 2>/dev/null; grep "CACHE_NAME" learning/interview-tools/sw.js
```
看 origin/学习本地当前 CACHE_NAME(如 kb-v335),+1 → kb-v336。若并发会话已 bump 到更高,取最高 +1。
Edit `learning/interview-tools/sw.js`: `const CACHE_NAME = 'kb-v335'` → `kb-v336`(按实际 origin 版本 +1)。

- [ ] **Step 7: 硬刷新验证(人工)**

本地开 stealth.html(或推送后 GitHub Pages),硬刷新让新 SW 接管:
- 综合 tab 显示 9 张自我陈述主卡(①-⑨)在最前 + 弹药组(项目数据/HR·行为面/反问/话术急救)。
- quickbar 二级按钮出现 `自我陈述` / `HR·行为面`。
- 搜"看机会/竞争力/创业/成就感/行业洞察"等命中对应主卡。
- 被删的 15 张旧卡不再出现(如搜"空窗期/优点和缺点"应无独立卡,内容已在主卡)。

- [ ] **Step 8: Commit + 推送**

```bash
git add learning/interview-tools/stealth.html learning/interview-tools/sw.js
git status   # 确认只这两个文件 + 无并行会话的串入
git commit -m "feat(stealth): 综合卡片全面重构 — 9张自我陈述主卡(CLEAR/L+证据+诚实边界+预判追问) + emer重排28→22(吸15入主卡/留13弹药) + 自我陈述组置首 + HR面→HR·行为面收编residue + sw kb-vN"
git push origin HEAD   # 推当前分支(按实际分支名)
```

- [ ] **Step 9: 清理临时片段**

Run: `rm -f /tmp/comp-card-{1..9}.html /tmp/t.html`

---

## Self-Review(plan 自审,已完成)

- **Spec 覆盖**:§1背景/§2范围/§3架构(双层/9问/内嵌追问/口语/open不动)→ 全计划体现;§4校准(Q9分档/Q8主线/数字雷区)→ Task2 check + Task3 prompt + Task5 grep;§5主卡模板→ Task3 prompt;§6九骨架→ Task3 映射表+prompt 读 spec;§7分组变更(28→22/吸15/HR·行为面/subOrder)→ Task4 脚本 + Task5 grep;§8流程→ Tasks 1-5;§9质量门→ Task2 check + Task5 grep;§10 YAGNI→ 未引入额外;§11拍板(Q3工程化/应用、Q4真实offer状态、组名、9 agent)→ Task3 prompt + Global Constraints。✓ 无遗漏。
- **占位符**:check/assemble 脚本含完整可运行代码;9 卡用参数化 prompt 模板 + 映射表(spec §6 是已提交的完整骨架,非占位)。sw.js 版本号 Task5 Step6 按 origin 实测 +1(非写死)。✓
- **类型一致**:data-g 值"自我陈述"/"HR·行为面" 在 check/assemble/grep/commit 全链路一致;15 个删除标题、3 个 data-g 改标题在 Task1/Task4 一致。✓
- **已知执行注意**:assemble 脚本的 subOrder 原串、15 删除锚点、3 data-g 标题都依赖 stealth.html 当前文本——若 PRD 重构先改了文件,Task1 Step2/Step4 会报错,届时按实际文本更新 assemble 脚本里的字符串常量。Global Constraints 已置顶警告。
