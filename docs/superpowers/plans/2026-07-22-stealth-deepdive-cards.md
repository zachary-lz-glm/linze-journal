# stealth D 实现细节深挖卡 · 实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: 用 superpowers:subagent-driven-development(推荐)或 superpowers:executing-plans 逐 task 执行。步骤用 `- [ ]` 跟踪。Task 3-6 互相独立(不同项目、不同产物文件),**可并行派 4 个 agent**。

**Goal:** 给 stealth.html proj 的 4 个项目各**新增 1 张「实现细节深挖卡」**(前端 dAction 双求值引擎 / Manager 39节点状态图+probe-before-plan / Code 自研 JSON+余弦向量检索 / PRD reference 6文件 SSOT 蒸馏),Form A 结构化实现卡(数据结构→算法→为什么自研拒绝X→踩坑/诚实边界),各插在该项目主陈述卡正后方;不动 A/B/C/三件套现有卡、不动 subOrder、不动 getGroup。

**Architecture:** 双层+深挖(主陈述五步 / 机制弹药 / **实现深挖**新维度)。4 个 agent 各产 1 张**完整 card** 片段到独立文件(前端无源码靠记忆+现有卡;Manager/Code/PRD 先读 agent-main/prd-tools 源码产事实清单再写)→ check_d.py 校验(四要素+per-project雷区+strong≥4)→ assemble_d.py 按主卡 title 锚点 depth 数到主卡闭合 `</div>`、在其后**插入**(非 body-swap)4 张新卡 → grep/quickbar 校验 → bump sw.js kb-v327→kb-v328 + 个人账号 push。

**Tech Stack:** HTML(stealth.html 单页,无构建工具)、Python 3(组装/校验脚本)、grep/bash(验收)。

## Global Constraints

(全部 verbatim 自 spec `2026-07-22-stealth-deepdive-cards-design.md`,每个 task 隐式包含)

- **形态 = Form A 四要素**:每张 4-5 段,每段 `<strong>领起标签。</strong>` 开头(≥4 段),必含 ①数据结构/形态 ②核心算法/流程 ③为什么自研、拒绝了什么 alternative+代价 ④踩坑+诚实边界(第④项不可省,防纯技术流水账)。可选第⑤段代码引用(文件名/行号,只进 body 不进 title)。
- **§6 declarative 风格**;禁口语碎嘴:说白了 / 得说句实话 / 我自己比较得意 / 被问X我答 / 这套东西 / 你就懂了 / 听着像。①② 只内联枚举,不堆①②③④⑤。
- **数字/spec §4.2 雷区硬回避**:
  - **Manager**:模型是阿里云 **qwen-flash**(非 Claude/GPT/Anthropic);12 Agent = **9 外 + 3 内**(非 8+4);失败归因**纯规则**(非 LLM);**自动晋级默认关**。
  - **Code**:向量检索**自研 JSON+内存余弦**(非 Chroma);增量靠 **sha256**(非 git 钩子);**没有** Diff 预览确认 / 独立审查 Agent / HITL 写确认。
  - **PRD**:prd-tools 是 **Claude Code 插件**(/reference + /prd-distill),非 SDD 平台、不直接生成代码;**"6 步闭环"不存在**;**"20+ 人"软化**(ADR-0005 写 1-5 人);"5h→2h"非严格 AB。
  - 原则:不确定软化("大概/约/小范围验证过")或省略;**绝不编百分比/倍数/团队规模**。agent 项目数字必须核对源码再写;核对不到宁可少写也不编。
- **routing**:4 张都 `data-c="proj"` + 挂各自现有 data-g(前端项目 / Manager 智能体 / Code 智能体 / PRD 工作流);**subOrder 不动**(4 组都已在 subOrder;组内按 DOM 序,插对位置即可);**getGroup 不动**;插在主陈述卡正后方。
- **新卡 title**:面试官口吻问题、**无英文项目名前缀**(禁 "Manager_Agent xxx")、**无文件路径**(代码引用只进 body)。
- **不动现有卡**:A/B/C/三件套已改已补的卡 body 零修改(D 是纯新增)。
- **改完 bump `sw.js` 的 `CACHE_NAME`** kb-v327 → **kb-v328**(看 origin 已部署版本 +1,GUIDE §4.7;kb-v325 撞号教训:bump 前必 `git show origin/main:sw.js | grep CACHE_NAME` 确认基线)。
- 用**个人 GitHub 账号**推送(remote origin 已指向 `github-personal:zachary-lz-glm`,push 命令 `git push origin main`);push 前 `git remote -v` 确认。
- stealth.html 单页大文件,组装用 **Python 锚点插入 + 原子写**,不用多次 Edit。
- agent 产**独立文件**(完整 card 片段),主会话统一组装,避免并发改同一文件(GUIDE §4.6)。
- **每 agent prompt 写死「只产出指定 fragment 文件到独立文件,禁碰 stealth.html、禁碰其他卡、禁碰 GUIDE/README/配置」**(memory [[agent-scope-constraint]])。

## File Structure

| 文件 | 责任 | 动作 |
|------|------|------|
| `learning/interview-tools/stealth.html` | 速查页主体 | 改:插入 4 张深挖卡 |
| `learning/interview-tools/stealth-source-current.html` | 改前源料备份(写卡 agent 读现有卡原文用) | 建 |
| `learning/interview-tools/check_d.py` | 校验深挖卡片段(四要素/per-project雷区/strong≥4/div平衡/禁碎嘴) | 建 |
| `learning/interview-tools/assemble_d.py` | 按主卡 title 锚点 depth 插入 4 张新卡(非 body-swap) | 建 |
| `learning/interview-tools/.d-prompt-template.md` | 4 agent 共用 prompt 公共部分 | 建 |
| `learning/interview-tools/.d-anchors.txt` | 4 主卡 title 原文 + proj 卡数基线 | 建 |
| `learning/interview-tools/.d-front.html` `.d-mgr.html` `.d-code.html` `.d-prd.html` | 4 张完整深挖卡产物(临时) | 建,组装后清理 |
| `sw.js` | Service Worker 缓存版本 | 改:CACHE_NAME kb-v327→kb-v328 |

---

### Task 1: 备份源 + 验证 4 主卡锚点 + 记录 proj 卡数基线

**Files:**
- Create: `learning/interview-tools/stealth-source-current.html`
- Create: `learning/interview-tools/.d-anchors.txt`

**Interfaces:**
- Produces: `.d-anchors.txt` 含 4 主卡完整 card-title + proj 卡数基线,供 Task 7 组装/校验参考

- [ ] **Step 1: 备份 stealth.html**

```bash
cp learning/interview-tools/stealth.html learning/interview-tools/stealth-source-current.html
```

- [ ] **Step 2: 验证 4 主卡锚点唯一 + 取完整标题**

```bash
cd /Users/didi/work/linze-journal/learning/interview-tools
for t in "最有价值的项目" "30 秒怎么说" "Code Agent 到底是什么" "AI工作流完整介绍"; do
  n=$(grep -c "card-title\">$t" stealth.html)
  echo "$t => $n 次匹配"
done
echo "=== 4 主卡完整 card-title ==="
for t in "最有价值的项目" "30 秒怎么说" "Code Agent 到底是什么" "AI工作流完整介绍"; do
  grep -oE "card-title\">$t[^<]*" stealth.html
done
```
Expected: 4 个锚点各 `1 次匹配`;4 个完整标题(前端=`最有价值的项目：Schema 营销中台`、Manager=`这个项目 30 秒怎么说？`、Code=`这个 Code Agent 到底是什么？`、PRD=`AI工作流完整介绍（面试第一答）`,注意全角标点)。若某锚点 ≠1,停下排查(标题被改/重复)。

- [ ] **Step 3: 记录 proj 卡数基线 + 4 主卡 data-g**

```bash
cd /Users/didi/work/linze-journal/learning/interview-tools
echo "proj 卡数基线: $(grep -oE 'data-c=\"proj\"' stealth.html | wc -l | tr -d ' ')"
echo "=== 4 主卡当前 data-g(确认组名) ==="
for t in "最有价值的项目：Schema 营销中台" "这个项目 30 秒怎么说" "这个 Code Agent 到底是什么" "AI工作流完整介绍"; do
  grep -B0 "card-title\">$t" stealth.html | head -1
done
```
Expected: proj 卡数基线记下(如 101,Task 7 应 = 基线 + 4);4 主卡 data-g 分别为 `前端项目`/`Manager 智能体`/`Code 智能体`/`PRD 工作流`。

- [ ] **Step 4: 写 .d-anchors.txt**

把 4 个完整 card-title 原文 + proj 卡数基线写入 `.d-anchors.txt`。

- [ ] **Step 5: Commit**

```bash
git -C /Users/didi/work/linze-journal add learning/interview-tools/stealth-source-current.html learning/interview-tools/.d-anchors.txt
git -C /Users/didi/work/linze-journal commit -m "chore(stealth): 备份源+抽取D深挖卡4主卡锚点+proj卡数基线"
```

---

### Task 2: 建 check_d.py + 公共 agent prompt 模板

**Files:**
- Create: `learning/interview-tools/check_d.py`
- Create: `learning/interview-tools/.d-prompt-template.md`

**Interfaces:**
- Produces: `check_d.py <片段> --project front|mgr|code|prd` —— 校验单张深挖卡片段,过 exit 0 否则 exit 1;`.d-prompt-template.md` —— 4 agent 共用 prompt 公共部分(执行时填入 spec §6 对应卡骨架)

- [ ] **Step 1: 写 check_d.py**

```python
#!/usr/bin/env python3
"""校验 D 深挖卡产物(Form A 四要素)。用法:
python3 check_d.py <new_card.html> --project front|mgr|code|prd
四要素: 数据结构词 + 算法词 + 拒绝alternative词 + 诚实边界词(各至少1,语义靠人工抽检只 warn)
结构: <strong>领起标签。</strong> 段 ≥ 4
硬约束: 禁口语碎嘴 / 无①②③④⑤堆叠 / div 平衡 / 无'6步闭环'(err)
雷区: per-project warn(Chroma/git钩子/Claude/GPT/20+人 等出现在'拒绝/对比'语境属正常,人工确认)"""
import re, sys, argparse

p = argparse.ArgumentParser()
p.add_argument("new")
p.add_argument("--project", required=True, choices=["front", "mgr", "code", "prd"])
a = p.parse_args()

html = open(a.new, encoding="utf-8").read()
errs, warns = [], []

# 1. 四要素词(各至少命中一个 → warn 不命中,语义靠人工)
DATA = ["数据结构", "结构", "字段", "JSON", "schema", "文件", "节点", "边", "拓扑", "语法", "存的是", "长这样", "协议"]
ALGO = ["算法", "流程", "余弦", "top-k", "topK", "召回", "求值", "蒸馏", "扫描", "匹配", "计算", "检索", "调度", "流转"]
REJECT = ["自研", "拒绝", "本可以", "没选", "而不是", "instead", "不用", "不选", "放弃了", "权衡", "排除了"]
HONESTY = ["没接", "研究型", "诚实", "局限", "上限", "框架先行", "规模", "边界", "代价", "不适用", "原型"]
if not any(w in html for w in DATA): warns.append("未见数据结构词")
if not any(w in html for w in ALGO): warns.append("未见算法/流程词")
if not any(w in html for w in REJECT): warns.append("未见'自研/拒绝alternative'词")
if not any(w in html for w in HONESTY): warns.append("未见诚实边界词(四要素第④项不可省)")

# 2. <strong> 段首 ≥ 4
strongs = re.findall(r"<strong>[^<]{2,}</strong>", html)
if len(strongs) < 4:
    errs.append(f"段首 <strong> 只有 {len(strongs)} 个,需 ≥4(Form A 四要素)")

# 3. 禁口语碎嘴
banned = ["说白了", "得说句实话", "我自己比较得意", "这套东西", "你就懂了", "听着像"]
hit = [w for w in banned if w in html]
if hit: errs.append(f"命中口语碎嘴: {hit}")

# 4. ①②③④⑤ 堆叠
if re.search(r"[①②③④⑤][①②③④⑤][①②③④⑤][①②③④⑤]", html):
    errs.append("①②③④⑤ 堆叠(≥4 连续),速查表腔")

# 5. div 平衡
if html.count("<div") != html.count("</div>"):
    errs.append(f"div 不平衡: <div {html.count('<div')} / </div> {html.count('</div>')}")

# 6. 完整 card 片段校验
if not html.lstrip().startswith("<div class=\"card\""):
    errs.append("片段非完整 card(应以 <div class=\"card\" 开头)")

# 7. 硬雷区 err:'6 步闭环'(全项目)
if "6 步闭环" in html or "6步闭环" in html:
    errs.append("含'6 步闭环'(此说法不存在,§4.2 雷区)")

# 8. per-project 雷区 warn(naive 子串在'拒绝/对比'语境会误报,人工确认)
if a.project == "mgr":
    for w in ["Claude", "GPT-4", "GPT-5", "Anthropic"]:
        if w in html: warns.append(f"Manager 卡出现 {w}(应为 qwen-flash;确认是对比非自述)")
if a.project == "code":
    if "Chroma" in html: warns.append("Code 卡出现 Chroma(自研非Chroma;确认是'不用Chroma'语境)")
    if "git 钩子" in html or "git钩子" in html: warns.append("Code 卡出现 git 钩子(增量靠sha256;确认是'不用git钩子'语境)")
if a.project == "prd":
    if "SDD 平台" in html or "SDD平台" in html: warns.append("PRD 卡出现 SDD 平台(prd-tools是Claude Code插件非SDD)")
    if "20+人" in html or "20+ 人" in html: warns.append("PRD 卡出现 20+人(应软化,ADR-0005写1-5人)")
    if "直接生成代码" in html: warns.append("PRD 卡出现'直接生成代码'(插件不直接生成代码)")

if warns:
    print(f"⚠️ 提示(--project {a.project},语义/语境在即可,不阻塞):")
    for w in warns: print("  -", w)
if errs:
    print(f"❌ 校验失败(--project {a.project}):")
    for e in errs: print("  -", e)
    sys.exit(1)
print(f"✅ 校验通过(--project {a.project},{len(strongs)} 段 <strong>,{len(warns)}条提示)")
```

- [ ] **Step 2: 用坏样例验证脚本能抓错**

```bash
cd /Users/didi/work/linze-journal/learning/interview-tools
printf '<div class="card"><p>说白了</p><p>6步闭环</p></div>' > /tmp/bad-d.html
python3 check_d.py /tmp/bad-d.html --project code; echo "exit=$?"
```
Expected: 打印 ❌(strong<4 / 口语碎嘴"说白了" / 含"6步闭环" / 四要素词缺失),exit=1。

- [ ] **Step 3: 用好样例验证脚本能放行**

```bash
cd /Users/didi/work/linze-journal/learning/interview-tools
cat > /tmp/good-d.html <<'EOF'
<div class="card" data-c="proj" data-g="Code 智能体" data-kw="向量检索 自研">
<div class="card-head"><span class="tag proj">实现</span><div class="card-title">测试卡</div></div>
<div class="core">自研JSON+余弦——不用Chroma,内存里跑语义召回</div>
<div class="card-body">
<p><strong>数据结构。</strong>JSON 字段结构长这样,存的是 id 和向量。</p>
<p><strong>召回算法。</strong>内存余弦相似度,top-k 召回流程。</p>
<p><strong>为什么自研。</strong>自研不用 Chroma,因为依赖重;代价是规模上限。</p>
<p><strong>踩坑和边界。</strong>研究型没接真实流量,框架先行没大规模度量。</p>
</div>
</div>
EOF
python3 check_d.py /tmp/good-d.html --project code; echo "exit=$?"
```
Expected: 打印 `✅ 校验通过(--project code,4 段 <strong>...)`,exit=0(Chroma 在"不用"语境 → warn 但不阻塞)。

- [ ] **Step 4: 写公共 agent prompt 模板 `.d-prompt-template.md`**

```markdown
你是面试速查卡写作 agent。任务:为 stealth.html **新增 1 张「实现细节深挖卡」**(完整 card,从 <div class="card"> 到对应 </div>)。

# 必读(按顺序)
1. learning/interview-tools/STEALTH-CARDS-GUIDE.md —— §1(铁律)、§6(技术项目卡风格标尺:declarative、不碎嘴、不堆栈)、§2.2(卡片模板)
2. docs/superpowers/specs/2026-07-22-stealth-deepdive-cards-design.md —— §5(Form A 四要素模板+硬约束)、§6(本卡骨架,见下方「本次负责的卡」)、§4.2(雷区)
3. {源码/素材:见下方「事实来源」,先读再写;agent 项目必须核对源码数字,核对不到就软化或省略,绝不编}
4. 现有卡原文: 从 stealth-source-current.html 读该项目主陈述卡,确认深挖卡**不重复**主卡已覆盖内容(主卡讲决策层,深挖落到实现层)

# 本次负责的卡
{此处由 Task 3/4/5/6 填入:项目 + data-g + 主题 + spec §6 对应小节四要素要点 + 雷区}

# Form A 四要素骨架(每段 <strong>领起标签。</strong> 开头,共 4-5 段)
① 数据结构 / 形态 —— 长什么样(JSON schema / 6文件结构 / graph节点边 / dAction语法)
② 核心算法 / 流程 —— 怎么跑(余弦 top-k / 蒸馏流程 / probe→plan / 双求值)
③ 为什么自研、拒绝了什么 —— 自研 X(拒绝 Y 因为 Z,代价 W)。CLEAR 的 L + 三段推理链
④ 踩坑 + 诚实边界 —— eval/局限(没接真实流量/研究型/规模上限/框架先行没度量)。**第④项不可省**
[可选]⑤ 代码在哪 —— `file.ts:行号`(只进 body,不进 title)

# 完整 card 片段格式
<div class="card" data-c="proj" data-g="{组}" data-kw="{关键词,含'具体实现 数据结构 怎么设计的 讲讲细节' + 主题词}">
  <div class="card-head"><span class="tag proj">实现</span><div class="card-title">{面试官口吻问题,无英文项目名前缀,无文件路径}</div></div>
  <div class="core">{一句带机制名+关键取舍的浓缩}</div>
  <div class="card-body">
    <p><strong>数据结构 / 形态。</strong>……</p>
    <p><strong>核心算法 / 流程。</strong>……</p>
    <p><strong>为什么自研、拒绝了什么。</strong>……</p>
    <p><strong>踩坑和边界。</strong>……</p>
    [可选]<p><strong>代码在哪。</strong>……</p>
  </div>
</div>

# 风格(§6)
declarative 陈述句;禁口语碎嘴(说白了/得说句实话/我自己比较得意/被问X我答/这套东西/你就懂了/听着像);
①② 可内联枚举,不堆①②③④⑤;strong 标句首自然词。

# 数字硬约束(spec §4.2,逐项目雷区见下方)
不确定软化("大概/约/小范围验证过")或省略;绝不编百分比/倍数/团队规模。

# 硬约束
- 只产出**1 个完整 card 片段**到**指定独立文件**;绝对不碰 stealth.html、其他卡、GUIDE/README/配置/任何其他文件
- div 平衡;无 loop 残留;无 <html>/<body> 包裹

# 产出
按指定文件名输出 1 个完整 card 片段,不要任何解释、不要 ``` 包裹。
```

- [ ] **Step 5: Commit**

```bash
git -C /Users/didi/work/linze-journal add learning/interview-tools/check_d.py learning/interview-tools/.d-prompt-template.md
git -C /Users/didi/work/linze-journal commit -m "chore(stealth): D深挖卡校验脚本check_d.py+公共agent prompt模板"
```

---

### Task 3: Agent-前端 dAction 双求值引擎(无源码)

> Task 3/4/5/6 互相独立,**可并行**。

**Files:**
- Create: `learning/interview-tools/.d-front.html`

**Interfaces:**
- Consumes: `.d-prompt-template.md`(Task 2)、`stealth-source-current.html`(Task 1)、A spec §6.4
- Produces: `.d-front.html` —— 1 张完整深挖卡(前端 dAction 双求值引擎)

- [ ] **Step 1: 派 general-purpose agent(或 inline 执行)**

prompt = `.d-prompt-template.md` 填入:
- 「事实来源」:`docs/superpowers/specs/2026-07-21-stealth-p0-frontend-mastercards-design.md` §6.4(卡4「怎么证明前端扎实」要点:联动 DSL dAction+injectDActions 双求值、虚拟滚动、Rollup tree-shaking)+ `stealth-source-current.html` 现有卡「最有价值的项目:Schema 营销中台」(2860)和「怎么证明前端扎实」(2896)原文。**无外部源码**,靠这些素材+记忆,数字一律⚠️软化。
- 「本次负责的卡」:
  - **data-g=`前端项目`**,主题:联动 DSL dAction + 双求值渲染引擎。spec §6.1 四要素要点:①数据结构:dAction 联动 DSL——组件依赖从命令式 if-else 变声明式模板表达式(组件A的值→组件B的disabled/选项),联动引用/循环依赖/字段类型可静态校验。②核心算法:injectDActions 双求值——渲染期先求值出初始状态(解决 SSR 初始态不对,不用等前端 JS 加载),运行期再求值响应用户操作;联动走精确更新(只重渲染受影响组件,非全量)。③为什么自研/拒绝:从零设计渲染引擎(拒绝现成 Formily/Ajv:联动描述力不够/黑盒/双求值做不到);虚拟滚动+按需渲染(拒绝全量重渲染:400+组件卡死);Rollup+tree-shaking(拒绝整包)。④踩坑/边界:这套引擎为**配置类页面**设计,不直接迁移 C 端自由布局/数据大屏;400+是组合数非组件数;为内部国际化业务设计(诚实:非公开 C 端真实流量产品)。
  - **title 建议**:`联动引擎怎么从零造的：dAction 双求值`(dAction 是术语非项目名,允许)。
  - **不重复主卡**:2860 主卡已讲"配置表达力 vs 可控性"决策层、双端解析架构决策;深挖只落到 dAction DSL 语法 + 双求值引擎实现层。
- **数字档**:400+(组合数 ✅)/ 24基础·30-40定制组件(✅)/ 35动态渲染(⚠️"三十多个")。
- prompt 末尾写死:"只产出 `.d-front.html` 一个完整 card 片段,禁碰 stealth.html、其他卡、GUIDE/README/配置/任何其他文件。"

- [ ] **Step 2: 校验产物**

```bash
cd /Users/didi/work/linze-journal/learning/interview-tools
python3 check_d.py .d-front.html --project front; echo "exit=$?"
```
Expected: `✅ 校验通过(--project front,4+ 段 <strong>...)`,exit=0。若失败,把错误回喂 agent 重产出。

- [ ] **Step 3: 人工风格抽看**

打开 `.d-front.html` 确认:declarative 不碎嘴、四要素齐全(尤其④诚实边界非空)、不堆技术栈、不重复主卡决策层内容。

- [ ] **Step 4: Commit**

```bash
git -C /Users/didi/work/linze-journal add learning/interview-tools/.d-front.html
git -C /Users/didi/work/linze-journal commit -m "feat(stealth): D前端深挖卡 dAction双求值渲染引擎"
```

---

### Task 4: Agent-Manager 39节点状态图 + probe-before-plan(读源码)

**Files:**
- Create: `learning/interview-tools/.d-mgr.html`

**Interfaces:**
- Consumes: `.d-prompt-template.md`、`stealth-source-current.html`、Manager_Agent 源码
- Produces: `.d-mgr.html` —— 1 张完整深挖卡(Manager 39节点 graph + probe-before-plan)

- [ ] **Step 1: 派 general-purpose agent —— 先读源码产事实清单**

prompt 先要求 agent 读以下源码,产出《真实事实 + ✅⚠️❌清单》(graph 拓扑结构、节点/边/条件边、probe 具体探什么、managerTask 关键字段、"39"是否准确),再据此写卡:
- `agent-main/Manager_Agent/server/utils/managerGraph.graph.ts`(主 graph 定义)
- `agent-main/Manager_Agent/server/utils/managerGraph.*.ts`(probe/plan/route/execute/synth/critic/finalize 等节点文件,按 graph.ts 引用展开)
- `agent-main/Manager_Agent/shared/routeAgentOrder.ts`
- 辅以 `learning/ai-projects/Manager-Agent-多智能体编排总管.md` + `learning/interview-kb/明日面试_预测题校准与匹配分析.md`

prompt = `.d-prompt-template.md` 填入:
- 「事实来源」:上述源码(核对数字,核对不到软化)。
- 「本次负责的卡」:
  - **data-g=`Manager 智能体`**,主题:39节点状态图 + probe-before-plan 工程实现。spec §6.2 四要素要点:①数据结构:graph 拓扑(节点/边/条件边),每个节点对应一个显式决策或坑,managerTask 协议在节点间流转(字段结构待源码核实)。②核心算法:probe-before-plan——先并行探一遍下游(9外3内 Agent 能力/真实状态)再让模型 plan,否则模型脑补下游状态;硬编码状态机驱动,非 LLM 自主流转。③为什么自研/拒绝:用硬编码状态机(拒绝 LLM 自主流转:可控/可观测/可单测/每条边能讲清);probe 排 plan 前(拒绝直接 plan:模型脑补)。④踩坑/边界:39 是结果非设计目标(每个节点对应一个显式决策/坑);本质研究型没接真实流量;自动晋级默认关;失败归因纯规则非 LLM。
  - **title 建议**:`39 节点状态图是怎么搭出来的`。
  - **不重复主卡/弹药卡**:646 主卡(30秒定位)、658(主干链路流程)、703(managerTask 协议是什么)、795(39是不是过度设计)。深挖只落到 graph 拓扑怎么设计 + probe-before-plan 的工程实现,不复述链路/协议/复杂度。
- **雷区**:qwen-flash 非 Claude/GPT/Anthropic · 12Agent=9外3内 · 失败归因纯规则 · 自动晋级默认关。"39"若源码核实不准→软化"几十个节点"。
- prompt 末尾写死:"先读指定源码产事实清单(可写到思考,不产额外文件);再只产出 `.d-mgr.html` 一个完整 card 片段;禁碰 stealth.html、其他卡、GUIDE/README/配置、**禁修改 agent-main 任何文件(只读)**、禁产其他文件。"

- [ ] **Step 2: 校验产物**

```bash
cd /Users/didi/work/linze-journal/learning/interview-tools
python3 check_d.py .d-mgr.html --project mgr; echo "exit=$?"
```
Expected: `✅ 校验通过(--project mgr,...)`,exit=0。若 Claude/GPT warn 命中,人工确认是对比非自述。

- [ ] **Step 3: 人工风格抽看 + 数字核对**

确认:declarative 不碎嘴、四要素齐全、graph/probe 落到实现层不重复 658/703/795、数字与源码事实清单一致("39"已核实或软化)、雷区回避。

- [ ] **Step 4: Commit**

```bash
git -C /Users/didi/work/linze-journal add learning/interview-tools/.d-mgr.html
git -C /Users/didi/work/linze-journal commit -m "feat(stealth): D Manager深挖卡 39节点状态图+probe-before-plan(读源码核对)"
```

---

### Task 5: Agent-Code 自研 JSON+余弦向量检索(读源码)

**Files:**
- Create: `learning/interview-tools/.d-code.html`

**Interfaces:**
- Consumes: `.d-prompt-template.md`、`stealth-source-current.html`、code_assistent_Agent 源码
- Produces: `.d-code.html` —— 1 张完整深挖卡(Code 自研向量检索)

- [ ] **Step 1: 派 general-purpose agent —— 先读源码产事实清单**

agent 读以下源码产《真实事实清单》(JSON 结构、余弦实现、sha256 增量粒度、top-k、embedding 来源/维度),再写卡:
- `agent-main/code_assistent_Agent/server/services/vectorSearch.ts`
- `agent-main/code_assistent_Agent/server/utils/code_experience_vectors.ts`
- `agent-main/code_assistent_Agent/stores/codeStore.ts`(sha256)
- `agent-main/code_assistent_Agent/server/utils/files.ts`(sha256)
- 辅以 `learning/ai-projects/Code-Assist-Agent-工程化代码助手.md` + 校准文档

prompt = `.d-prompt-template.md` 填入:
- 「事实来源」:上述源码。
- 「本次负责的卡」:
  - **data-g=`Code 智能体`**,主题:自研 JSON+内存余弦向量检索。spec §6.3 四要素要点:①数据结构:JSON 存 {id/向量/text/sha256},全量加载进内存(code_experience_vectors 真实字段待源码核实)。②核心算法:内存余弦相似度,top-k 召回;sha256 比对文件内容,变了才重算向量(增量)。③为什么自研/拒绝:自研 JSON+余弦(拒绝 Chroma 等向量库:依赖重、研究型规模小、零依赖更可控);sha256 增量(拒绝 git 钩子/全量重算:全量贵、git 钩子耦合仓库)。④踩坑/边界:研究型没接真实流量;内存全量算有规模上限(诚实承认,点"若上量会换近似检索/落库");召回质量小范围验证过非大规模 benchmark。
  - **title 建议**:`向量检索为什么不用 Chroma、自研怎么实现`(Chroma 在 title 是"不用"语境,允许)。
  - **不重复主卡/弹药卡**:809 主卡(Code Agent 整体定位)、858(语义检索 vs 全量 context 取舍)、964(AsyncLocalStorage)。深挖只落到自研向量检索的数据结构+余弦算法+sha256 增量实现,不复述取舍/上下文。
- **雷区**:自研非 Chroma · 增量 sha256 非 git 钩子 · 无 Diff 预览确认/独立审查 Agent/HITL 写确认。
- prompt 末尾写死:"先读指定源码产事实清单;再只产出 `.d-code.html`;禁碰 stealth.html/其他卡/GUIDE/配置、**禁改 agent-main(只读)**、禁产其他文件。"

- [ ] **Step 2: 校验产物**

```bash
cd /Users/didi/work/linze-journal/learning/interview-tools
python3 check_d.py .d-code.html --project code; echo "exit=$?"
```
Expected: `✅ 校验通过(--project code,...)`,exit=0。Chroma warn 命中是预期(确认是"不用 Chroma"语境)。

- [ ] **Step 3: 人工风格抽看 + 数字核对**

确认:四要素齐全、数据结构/算法与源码一致、雷区回避(Chroma 仅"不用"语境、增量是 sha256 非 git 钩子)、不重复 809/858/964。

- [ ] **Step 4: Commit**

```bash
git -C /Users/didi/work/linze-journal add learning/interview-tools/.d-code.html
git -C /Users/didi/work/linze-journal commit -m "feat(stealth): D Code深挖卡 自研JSON+余弦向量检索(读源码核对)"
```

---

### Task 6: Agent-PRD reference 6文件 SSOT 蒸馏(读源码)

**Files:**
- Create: `learning/interview-tools/.d-prd.html`

**Interfaces:**
- Consumes: `.d-prompt-template.md`、`stealth-source-current.html`、prd-tools 源码
- Produces: `.d-prd.html` —— 1 张完整深挖卡(PRD reference 6文件蒸馏)

- [ ] **Step 1: 派 general-purpose agent —— 先读源码产事实清单**

agent 读以下源码产《真实事实清单》(/reference 命令实现、6 个领域文件具体是哪 6 个 + schema、/prd-distill 流程、"6"是否准确),再写卡:
- `/Users/didi/work/prd-tools/plugins/`(找 /reference、/prd-distill 命令实现)
- `/Users/didi/work/prd-tools/docs/`、`/Users/didi/work/prd-tools/README.md`、`CLAUDE.md`
- 辅以校准文档 + memory `reference_prd_to_code_projects.md`

prompt = `.d-prompt-template.md` 填入:
- 「事实来源」:上述源码。
- 「本次负责的卡」:
  - **data-g=`PRD 工作流`**,主题:/reference 6文件 SSOT 怎么蒸馏。spec §6.4 四要素要点:①数据结构:6 个领域文件每个存什么(待源码核实具体哪 6 个+schema),单一事实源原则——同一事实只存一处。②核心算法:/reference 命令怎么扫项目→蒸馏→6 文件;/prd-distill 怎么消费 6 文件出计划;每个事实只存一处(散多处=AI 挑顺口的用=编造空间)。③为什么自研/拒绝:单一事实源(拒绝多处冗余存储:AI 编造);6 文件按领域切(拒绝一个大文件/全量塞 PRD:打爆 context);Claude Code 插件形态(拒绝独立 SDD 平台:轻量、复用 CC 能力)。④踩坑/边界:团队模式 Pull-based 禁止主动搜源码→准确率 60% 损耗(对单仓 80%);"5h→2h"是前后工时非严格 AB;团队规模按 ADR-0005 是 1-5 人小范围试用。
  - **title 建议**:`reference 蒸馏的 6 个文件怎么来的`。
  - **不重复主卡**:2380 主卡(面试第一答)已点名"6文件/8证据类型/Readiness 85-60-60/negative_code_search"。深挖只落到 /reference 这 6 个文件具体怎么蒸馏(命令流程+文件 schema+单一事实源怎么保证),**不复述证据链/门控/Readiness**(留主卡)。
- **雷区**:插件非 SDD 平台 · "6 步闭环"不存在(err) · 不直接生成代码 · "20+ 人"软化 · 5h→2h 非严格 AB。"6"若源码核实不准→软化"几个领域文件"。
- prompt 末尾写死:"先读指定源码产事实清单;再只产出 `.d-prd.html`;禁碰 stealth.html/其他卡/GUIDE/配置、**禁改 prd-tools(只读)**、禁产其他文件。"

- [ ] **Step 2: 校验产物**

```bash
cd /Users/didi/work/linze-journal/learning/interview-tools
python3 check_d.py .d-prd.html --project prd; echo "exit=$?"
```
Expected: `✅ 校验通过(--project prd,...)`,exit=0。SDD/20+人/直接生成代码 warn 若命中→人工确认已软化/在拒绝语境。

- [ ] **Step 3: 人工风格抽看 + 数字核对**

确认:四要素齐全、6 文件结构/蒸馏流程与源码一致("6"已核实或软化)、雷区回避(无"6步闭环"、无 SDD 平台自述、"20+人"软化)、不重复主卡证据链/门控/Readiness。

- [ ] **Step 4: Commit**

```bash
git -C /Users/didi/work/linze-journal add learning/interview-tools/.d-prd.html
git -C /Users/didi/work/linze-journal commit -m "feat(stealth): D PRD深挖卡 reference 6文件SSOT蒸馏(读源码核对)"
```

---

### Task 7: 组装 —— assemble_d.py 按主卡锚点 depth 插入 4 张新卡

**Files:**
- Create: `learning/interview-tools/assemble_d.py`
- Modify: `learning/interview-tools/stealth.html`

**Interfaces:**
- Consumes: `.d-front.html` `.d-mgr.html` `.d-code.html` `.d-prd.html`(Task 3-6)、`.d-anchors.txt`(Task 1)
- Produces: 改写后的 stealth.html(4 张深挖卡插在各自主卡正后方)

- [ ] **Step 1: 写 assemble_d.py**

```python
#!/usr/bin/env python3
"""D 深挖卡:把 4 张新深挖卡(完整 card)插到各自主陈述卡正后方。原子写。
锚点:主卡 card-title 子串(唯一)→ 定位主卡开标签 → depth 数到主卡闭合 </div> → 在其后插入新卡。"""
import re, os, sys

ROOT = "/Users/didi/work/linze-journal/learning/interview-tools/"
HTML = ROOT + "stealth.html"

# (主卡 card-title 子串, 新卡 fragment 文件)
INSERTS = [
    ("最有价值的项目：Schema 营销中台", ".d-front.html"),   # 前端项目
    ("这个项目 30 秒怎么说", ".d-mgr.html"),                # Manager 智能体
    ("Code Agent 到底是什么", ".d-code.html"),              # Code 智能体
    ("AI工作流完整介绍", ".d-prd.html"),                    # PRD 工作流
]

html = open(HTML, encoding="utf-8").read()
problems = []

for title_sub, frag in INSERTS:
    pat = 'card-title">' + title_sub
    idxs = [m.start() for m in re.finditer(re.escape(pat), html)]
    if len(idxs) != 1:
        problems.append((frag, f"主卡锚点匹配{len(idxs)}次,应1: {title_sub!r}")); continue
    tidx = idxs[0]
    o = html.rfind('<div class="card"', 0, tidx)
    if o < 0:
        problems.append((frag, "找不到主卡开标签")); continue
    # depth 数到主卡闭合
    depth, i, close_end = 0, o, None
    while i < len(html):
        if html[i:i+4] == '<div':
            depth += 1; i = html.find('>', i) + 1
        elif html[i:i+6] == '</div>':
            depth -= 1; i += 6
            if depth == 0:
                close_end = i; break
        else:
            i += 1
    if close_end is None:
        problems.append((frag, "主卡未闭合")); continue
    new_card = open(ROOT + frag, encoding="utf-8").read().strip()
    if not new_card.startswith('<div class="card"'):
        problems.append((frag, "片段非完整 card")); continue
    if new_card.count('<div') != new_card.count('</div>'):
        problems.append((frag, "片段 div 不平衡")); continue
    html = html[:close_end] + "\n" + new_card + "\n" + html[close_end:]
    print(f"插入: {frag} → 主卡「{title_sub}」后")

if problems:
    print("❌ 锚点/片段问题,未写文件:")
    for f, p in problems: print(f"  - {f}: {p}")
    sys.exit(1)

assert html.count('<div') == html.count('</div>'), f"全文 div 不平衡: {html.count('<div')}/{html.count('</div>')}"
assert '<script>' in html and '</script>' in html, "script 残缺"
tmp = HTML + ".tmp"
open(tmp, "w", encoding="utf-8").write(html)
os.replace(tmp, HTML)
print("✅ D 4 张深挖卡插入完成")
```

- [ ] **Step 2: 跑组装**

```bash
cd /Users/didi/work/linze-journal/learning/interview-tools
python3 assemble_d.py
```
Expected: 打印 4 行「插入: ...」+ `✅ D 4 张深挖卡插入完成`。若 assert/锚点报错,停下:对照 `.d-anchors.txt` 确认主卡 title 子串与文件完全一致(全角标点);`git checkout stealth.html` 回退重查。

- [ ] **Step 3: 验证插入结果**

```bash
cd /Users/didi/work/linze-journal/learning/interview-tools
echo "=== proj 卡数(应 = Task1 基线 + 4) ==="
grep -oE 'data-c="proj"' stealth.html | wc -l
echo "=== 4 张新深挖卡标题各在(应各 1) ==="
for t in "联动引擎怎么从零造的" "39 节点状态图是怎么搭出来的" "向量检索为什么不用 Chroma" "reference 蒸馏的 6 个文件怎么来的"; do
  echo "$t => $(grep -c "card-title\">$t" stealth.html)"
done
echo "=== 4 张新卡 data-g 对 ==="
for t in "联动引擎怎么从零造的" "39 节点状态图" "向量检索为什么不用 Chroma" "reference 蒸馏的 6 个文件"; do
  grep -B2 "card-title\">$t" stealth.html | grep -oE 'data-g="[^"]*"'
done
echo "=== 4 主卡标题仍在(未被破坏,应各 1) ==="
for t in "最有价值的项目：Schema 营销中台" "这个项目 30 秒怎么说" "这个 Code Agent 到底是什么" "AI工作流完整介绍"; do
  echo "$t => $(grep -c "card-title\">$t" stealth.html)"
done
echo "=== div 平衡(应相等) ==="
echo "<div: $(grep -oE '<div[^>]*>' stealth.html | wc -l | tr -d ' ')  </div>: $(grep -oE '</div>' stealth.html | wc -l | tr -d ' ')"
```
Expected: proj 卡数 = 基线+4;4 新标题各 1;4 新卡 data-g 依次为 前端项目/Manager 智能体/Code 智能体/PRD 工作流;4 主卡标题各 1(未被破坏);div 开=闭。若不对,`git checkout stealth.html` 回退重查。

- [ ] **Step 4: 浏览器肉眼验收**

`open learning/interview-tools/stealth.html` → 项目 tab → quickbar 4 个组里,每张深挖卡显示在该项目主卡**正后方**、core 高亮在、四段渲染正常、无破版。tab 角标计数正确。

- [ ] **Step 5: Commit**

```bash
git -C /Users/didi/work/linze-journal add learning/interview-tools/stealth.html learning/interview-tools/assemble_d.py
git -C /Users/didi/work/linze-journal commit -m "feat(stealth): 组装D深挖卡4张(插主卡正后方,非body-swap,subOrder不动)"
```

---

### Task 8: 全局校验 + 雷区/数字抽检 + bump sw.js + push + 清理

**Files:**
- Modify: `sw.js`

**Interfaces:**
- Consumes: 改写后的 stealth.html(Task 7)

- [ ] **Step 1: 全局 grep 校验**

```bash
cd /Users/didi/work/linze-journal/learning/interview-tools
echo "=== div 平衡 + script 完整 ==="
echo "<div: $(grep -oE '<div[^>]*>' stealth.html | wc -l | tr -d ' ')  </div>: $(grep -oE '</div>' stealth.html | wc -l | tr -d ' ')"
echo "script 开:$(grep -c '<script' stealth.html) 闭:$(grep -c '</script>' stealth.html)"
echo "=== 禁用项残留(应 0) ==="
grep -cE '说白了|得说句实话|我自己比较得意|\[loop' stealth.html
echo "=== '6 步闭环' 全文档(应 0) ==="
grep -cE '6 步闭环|6步闭环' stealth.html
```
Expected: div 开=闭;script 开=闭;禁用项 0;6步闭环 0。若命中,回 Task 3-6 对应 agent 重产出 + 重组装。

- [ ] **Step 2: per-project 雷区语境抽检**

```bash
cd /Users/didi/work/linze-journal/learning/interview-tools
echo "=== Code 卡:Chroma 只在'不用'语境(打印所在行人工确认) ==="
grep -nE 'Chroma' stealth.html
echo "=== Code 卡:git 钩子只在'不用'语境 ==="
grep -nE 'git ?钩子' stealth.html
echo "=== Manager 卡:无 Claude/GPT 自述模型(应为空) ==="
grep -nE 'Claude|GPT-4|GPT-5|Anthropic' stealth.html | grep -iE 'manager|总管|编排' || echo "(Manager 区无 Claude/GPT 自述 ✓)"
echo "=== PRD 卡:无 SDD 平台自述 / 无 20+人硬数 ==="
grep -nE 'SDD ?平台|20\+ ?人' stealth.html || echo "(无 SDD平台/20+人 ✓)"
```
Expected: Chroma/git钩子 命中行均在"不用/拒绝"语境内;Manager 区无 Claude/GPT 作自述模型;无 SDD 平台自述、无"20+人"硬数。不符合→回对应 agent 软化/改语境后重组装。

- [ ] **Step 3: 看 origin 当前 CACHE_NAME 并 bump kb-v327→kb-v328**

```bash
cd /Users/didi/work/linze-journal
git fetch origin main 2>/dev/null
echo "=== origin 上的 CACHE_NAME(应为 kb-v327) ==="
git show origin/main:sw.js | grep CACHE_NAME
echo "=== 本地当前 ==="
grep CACHE_NAME sw.js
```
确认 origin = `kb-v327`(spec 基线)。把 `sw.js` 里 `CACHE_NAME` 的 `'kb-v327'` 改成 `'kb-v328'`(origin +1)。

- [ ] **Step 4: 确认 remote 个人账号 + Commit + push**

```bash
cd /Users/didi/work/linze-journal
echo "=== 确认 origin 指向个人账号(zachary-lz-glm) ==="
git remote -v | head -1
git add sw.js
git commit -m "chore(stealth): bump CACHE_NAME kb-v327→kb-v328(D深挖卡4张:前端dAction/Manager graph/Code自研向量/PRD reference)"
git push origin main
```
若 `git remote -v` 显示 origin 非个人账号(是公司账号),停下确认正确 remote 名再用 `git push <个人remote> main`。**绝不推公司账号**(memory [[github-account]])。

- [ ] **Step 5: 硬刷新验证**

`open learning/interview-tools/stealth.html` 后硬刷新(Cmd+Shift+R),确认 SW 接管新版、项目 tab 4 个组里各多 1 张深挖卡、显示在主卡正后方。

- [ ] **Step 6: 清理临时产物**

```bash
cd /Users/didi/work/linze-journal/learning/interview-tools
rm -f .d-front.html .d-mgr.html .d-code.html .d-prd.html .d-anchors.txt .d-prompt-template.md stealth-source-current.html
git add -A && git commit -m "chore(stealth): 清理D深挖卡临时产物" || echo "无变更"
git push origin main
```
**保留** `check_d.py` 和 `assemble_d.py`(后续子项目可复用,不删)。

---

## 自审(对照 spec)

- **Spec 覆盖**: spec §2.1(4 张新增卡+锚点)→ Task 1 验证锚点 + Task 7 插入;§3.1 Form A 四要素 → Task 2 check_d.py 四要素词 + .d-prompt-template 骨架;§3.3 插主卡正后方/subOrder 不动 → Task 7 assemble_d.py(插入非 body-swap)+ Step3 验证 subOrder 未动(无 subOrder 改动代码);§4.1 分项目源码核对(Manager/Code/PRD 读源码、前端无源码)→ Task 3(素材)/4/5/6(读源码产事实清单);§4.2 雷区 → Task 2 check_d.py per-project 雷区 + Task 8 Step2 语境抽检;§5 四要素模板+硬约束 → Task 2 prompt 模板;§6 四张卡骨架 → Task 3/4/5/6;§7 多 agent 流程 → Task 1-8;§8 质量门 → Task 2 脚本 + Task 7/8 grep + Task 3-6 人工抽看。✅ 全覆盖。
- **Placeholder**: Task 2 check_d.py / assemble_d.py 为完整可跑代码(已好坏样例自检);Task 3-6 每卡给了 spec §6 实际四要素要点(逐条)+ 源码路径 + 雷区 + title 建议 + 不重复边界,非 TBD;4 主卡锚点子串 + 4 新卡 title 全写实。✅
- **类型/命名一致**: 4 fragment 文件名 `.d-front/.d-mgr/.d-code/.d-prd.html` 在 Task 3-6 产出、Task 7 INSERTS 列表消费,一致;4 主卡 title 子串在 Task 1 验证、Task 7 INSERTS、Task 8 grep 一致;4 新卡 title 在 Task 3-6 建议、Task 7 Step3 验证、Task 8 grep 一致;check_d.py `--project front|mgr|code|prd` 在 Task 2 定义、Task 3-6 调用一致;kb-v327→kb-v328 在 Task 8 + Global Constraints 一致。✅
- **D vs A 关键差异已落实**: fragment 是**完整 card**(Task 2 模板 + check_d.py 校验 `startswith('<div class="card"')`)非 body-only;assemble_d.py 是**插入**(Task 7 depth 数到主卡闭合)非 body-swap;3 张 agent 项目卡**读源码产事实清单**(Task 4/5/6 Step1)非复用清单;subOrder **不动**(Task 7 无 subOrder 代码)。✅
