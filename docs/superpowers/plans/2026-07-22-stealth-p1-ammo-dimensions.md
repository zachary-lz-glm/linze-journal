# stealth P1 弹药卡补维度 · 实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: 用 superpowers:subagent-driven-development(推荐)或 superpowers:executing-plans 逐 task 执行。步骤用 `- [ ]` 跟踪。

**Goal:** 给 stealth.html 的 69 张机制弹药卡(Manager 13 + Code 18 + PRD 37 + 技术选型 1)"加段补维度"——🅰 极薄/纯机制档 34 张补 ownership+alternative,🅱 半截 STAR/亮点成熟档 35 张补 eval+方法论句;2 张聚合卡 + 速查 + A/C 已改卡不动;零 routing 改动(69 张已有 data-g),只增不删。

**Architecture:** 双层(主陈述卡 A/C 已改 + 本轮弹药卡补维度)。分档判据看 card-body 有无 ownership/alternative 痕迹。4 个 agent 各产本组卡的"新 card-body 片段(原文+加段)"到独立文件 + 主会话改技术选型 602 → check_p1.py 校验(分档维度词 + 只增不删 + 雷区)→ assemble_p1.py 锚点 splice 69 张(不动 data-g/subOrder/title/core)→ 雷区人工 grep 抽检 → bump sw.js kb-v326→kb-v327 + 个人账号 push。

**Tech Stack:** HTML(stealth.html 单页,无构建工具)、Python 3(组装/校验脚本)、grep/bash(验收)。

## Global Constraints

- **范围严格 69 张**:Manager 13 + Code 18 + PRD 37 + 技术选型 1。2 张聚合卡(2526/2551)、速查(615/4221)、A 批 5 张前端主卡、C 批 14 张 ai 卡、三件套主卡(646/796/2335)、无 data-g 老追问卡 **一律不动**。⚠️ Code 4514 物理紧邻 C 批 4529/4540,**禁碰**。
- **零 routing 改动**:69 张已有 data-g,**不加新 data-g、不动 subOrder、不删卡、不改标题/core/data-kw**。assemble 只 body swap。
- **只增不删**:每张在原文 card-body **末尾加一小段**,保留所有原文 `<p>` 好句,改后 body 长度 ≥ 原文。
- **分档补**(spec §3.2):
  - 🅰 极薄/纯机制档(34 张):加"我的取舍"段 = ownership("我在 X 项目里定的是 Y") + alternative("本可以 Z,但拒绝了,因为 W")。
  - 🅱 半截 STAR/亮点成熟档(35 张):加"怎么验证/沉淀"段 = eval(怎么验证/效果,或诚实承认"框架先行没度量"+点"若要度量会怎么做") + 方法论句(拔成可迁移命名判断)。**若该卡 eval/方法论已有其一,只补缺的那个**。
  - 边缘卡:Code 4514(系统设计型,ownership 写"基于 code_assistant 经验推导的设计能力")+ 技术选型 602(方法论已全,只补 ownership 挂回项目)按 spec §6 特殊处理,不机械套档。
- **数字校准复用现有清单**(不派 agent 重读 `agent-main/`):memory + roadmap §5 + `learning/interview-kb/明日面试_预测题校准与匹配分析.md` + 69 张卡现有已校准数字。不确定软化("大概/约/小范围验证过")或省略。**绝不编百分比/提升倍数/团队规模。**
- **§4.1 正向雷区**(写卡 agent 必回避):Manager=qwen-flash 非 Claude/GPT/Anthropic · 12 Agent=9外+3内 · 失败归因纯规则非 LLM · 自动晋级默认关 · Checkpoint 自建16字段 · Code 向量自研 JSON+余弦非 Chroma · 增量 sha256 非 git钩子 · Code 无 Diff预览/独立审查Agent/HITL写确认 · prd-tools 是 Claude Code 插件非 SDD 平台/"6步闭环"不存在 · "20+人"软化(1-5人) · "5h→2h"/"团队模式准确率60%"软化(无严格统计口径)。
  - ⚠️ **check 脚本不做 naive 雷区子串检查**——弹药卡会合法"提到被拒绝的选项"(如"不用 Chroma""Claude Code 插件"),naive grep 误报。雷区由 **Task 9 人工 grep + 读上下文**判断"误用 vs 合法提及"。脚本只自动查"6 步闭环"(此短语不存在,任何出现都错)。
- **§6 declarative 风格**;禁口语碎嘴:说白了 / 得说句实话 / 我自己比较得意 / 被问X我答 / 这套东西 / 你就懂了 / 听着像。**strong 标句首自然词**,不孤立。①②只内联,不堆①②③④⑤。
- **改完 bump `sw.js` 的 `CACHE_NAME`**:**kb-v326 → kb-v327**(bump 前必核 `git show origin/main:sw.js | grep CACHE_NAME`,kb-v325 撞号教训)。
- 用**个人 GitHub 账号**推送(origin = `github-personal:zachary-lz-glm`);本项目 main 工作流,commit main + push 触发 Pages。
- stealth.html 单页大文件,组装用 **Python 锚点替换 + 原子写**,不用多次 Edit。
- agent 产**独立文件**,主会话统一组装,避免并发改同一文件(GUIDE §4.6)。**每 agent prompt 写死「只产指定卡的新 card-body 片段到独立文件,禁碰 stealth.html、禁碰其他卡、禁碰 C 批 4529-4540」**(memory [[agent-scope-constraint]])。

## File Structure

| 文件 | 责任 | 动作 |
|------|------|------|
| `learning/interview-tools/stealth.html` | 速查页主体 | 改:69 张 card-body(末尾加段) |
| `learning/interview-tools/stealth-source-current.html` | 加段前源料备份 | 建(若不存在) |
| `learning/interview-tools/check_p1.py` | 校验 agent 产物(分档维度词 + 只增不删 + 禁用项 + div 平衡) | 建(从 check_p2.py 复制改造) |
| `learning/interview-tools/assemble_p1.py` | 锚点 splice 69 张 body(不动 data-g/subOrder/title/core) | 建(从 assemble_p2.py 复制改造) |
| `learning/interview-tools/.p1-prompt-template.md` | 四 agent 共用 prompt 公共部分 | 建 |
| `learning/interview-tools/.p1-anchors.txt` | 69 张精确 card-title + 分档 | 建 |
| `learning/interview-tools/.p1-{mgr,code,prd-up,prd-down,tech}.html` | 各组新 body 产物(含原文+加段,临时) | 建,组装后删 |
| `sw.js` | Service Worker 缓存版本 | 改:CACHE_NAME kb-v326→kb-v327 |

---

### Task 1: 备份源 + 验证 69 张卡锚点 + 记录分档

**Files:**
- Create: `learning/interview-tools/stealth-source-current.html`(若不存在)
- Create: `learning/interview-tools/.p1-anchors.txt`

**Interfaces:**
- Produces: `.p1-anchors.txt` 含 69 张 card-title(子串形式) + 档位(🅰/🅱) + 所属组,供 Task 8 assemble + Task 3-7 agent 认领

- [ ] **Step 1: 备份 stealth.html**

```bash
cp learning/interview-tools/stealth.html learning/interview-tools/stealth-source-current.html
```

- [ ] **Step 2: 验证 69 张卡都能定位 + 有 card-body**

```bash
cd learning/interview-tools
python3 - <<'PY'
html = open("stealth.html", encoding="utf-8").read()
# (标题子串, 档, 组) —— 档仅供记录,执行 agent 按 spec §2.1 判据复核
cards = [
 # Manager 13
 ("主干链路长什么样", "A", "mgr"),
 ("编排层和专家层怎么分工", "A", "mgr"),
 ("HITL checkpoint 解决什么问题", "B", "mgr"),
 ("Critic 节点和一次 LLM 调用", "A", "mgr"),
 ("managerTask 协议是干嘛", "A", "mgr"),
 ("流式输出和阶段事件怎么走", "A", "mgr"),
 ("多 Agent 出问题怎么定位", "A", "mgr"),
 ("反复用的几个工程模式", "A", "mgr"),
 ("自我进化机制是什么样", "B", "mgr"),
 ("这项目真上生产了吗", "B", "mgr"),
 ("为什么用硬编码状态机", "B", "mgr"),
 ("和市面多 Agent 竞品比", "B", "mgr"),
 ("39 个节点是不是过度设计", "B", "mgr"),
 # Code 18
 ("ReAct", "B", "code"),  # 自测①,标题含 ReAct/Tool Use
 ("为什么必须先做意图路由", "B", "code"),
 ("18 个工具怎么分工", "A", "code"),
 ("语义检索 vs 全量 context", "B", "code"),
 ("静态分析和 Bug 检测怎么做", "A", "code"),
 ("怎么和总管 Agent 共享代码上下文", "A", "code"),
 ("为什么 Diff 是命门", "B", "code"),
 ("防模型乱来", "A", "code"),
 ("改完怎么自动验", "A", "code"),
 ("跑长任务怎么不丢", "A", "code"),
 ("Shadow Patch", "B", "code"),
 ("个性化 RAG", "B", "code"),
 ("AsyncLocalStorage", "A", "code"),
 ("被问", "B", "code"),  # "被问'上线了吗'我怎么答"
 ("和 Cursor", "B", "code"),
 ("opencode", "B", "code"),
 ("18 个工具是不是太多", "B", "code"),
 ("为创业团队设计 Coding Agent", "B", "code"),  # 4514 特殊标
 # PRD 上半 19 (2116-2397)
 ("AI 怎么理解陌生项目", "A", "prd-up"),
 ("PRD 到代码最难的一步", "A", "prd-up"),
 ("SSOT 五条边界规则", "B", "prd-up"),
 ("reference 知识过时怎么办", "B", "prd-up"),
 ("2-3 万字 PRD 打爆 Context", "B", "prd-up"),
 ("团队模式准确率", "B", "prd-up"),
 ("5h→2h", "B", "prd-up"),  # 2213 G4
 ("和 Claude Code init", "B", "prd-up"),
 ("能力面适配器怎么设计", "A", "prd-up"),
 ("BMAD架构", "A", "prd-up"),
 ("双插件体系", "A", "prd-up"),
 ("质量门控", "A", "prd-up"),
 ("Readiness Score", "A", "prd-up"),
 ("PRD摄入", "A", "prd-up"),
 ("Spec和Plan长什么样", "A", "prd-up"),
 ("自验证+自修复循环", "A", "prd-up"),
 ("模板/LLM 双路径", "A", "prd-up"),
 ("端到端原型 → 生产", "B", "prd-up"),
 ("AI工作流怎么优化和迭代", "A", "prd-up"),
 # PRD 下半 18 (2412-2934)
 ("Skill解决什么问题", "B", "prd-down"),
 ("Skill vs 写代码", "B", "prd-down"),
 ("AI知识库的本质定位", "B", "prd-down"),
 ("Tools vs Skill", "B", "prd-down"),
 ("Tool多了识别率下降", "B", "prd-down"),
 ("传统工程思维在AI系统", "A", "prd-down"),
 ("有Claude Code了为什么还要自定义", "B", "prd-down"),
 ("PRD质量卡口", "B", "prd-down"),
 ("代码上下文怎么精准定位", "A", "prd-down"),
 ("证据链机制详解", "A", "prd-down"),
 ("AI工作流在团队怎么落地", "A", "prd-down"),
 ("Skill执行结果不稳定", "A", "prd-down"),
 ("PRD过时或临时改动", "A", "prd-down"),
 ("AI工作流出错了怎么归因", "B", "prd-down"),
 ("AI工作流推广ROI", "B", "prd-down"),
 ("实验组和对照组", "B", "prd-down"),  # 2845,与 2213 撞车
 ("SDD 完整流程", "A", "prd-down"),
 ("Harness 三种引擎", "A", "prd-down"),
 # 技术选型 1
 ("我的技术选型怎么做", "B*", "tech"),  # 602 边缘
]
import re
miss = []; dup = []
for sub, tier, grp in cards:
    matches = list(re.finditer(r'card-title">[^<]*' + re.escape(sub), html))
    if len(matches) == 0:
        miss.append((sub, tier, grp))
    elif len(matches) > 1:
        dup.append((sub, tier, grp))
    else:
        ti = matches[0].start()
        if html.find('<div class="card-body">', ti) < 0:
            miss.append((sub, tier, grp))
print(f"共 {len(cards)} 张,定位失败 {len(miss)} 张,子串在 title 内不唯一 {len(dup)} 张")
for m in miss: print("  ❌缺", m)
for d in dup: print("  ⚠️重", d)
print("ALL OK" if not miss and not dup else "有异常,停下排查(换更长的唯一子串)")
PY
```
Expected: `共 69 张,定位失败 0 张` + `ALL OK`。若某张 ❌,停下排查:标题被改/子串在文中出现多次导致定位错位(换更长的唯一子串)。

> ⚠️ 子串如 `"ReAct"`/`"被问"`/`"opencode"` 较短,若脚本报"定位失败"或assemble 时错位,在该子串前补字符使其唯一(如 `"ReAct / Tool Use"`、`"被问"上线了吗"`、`"了解 opencode"`)。Task 8 assemble 用同样子串,需与此处一致。

- [ ] **Step 3: 记录锚点 + 分档到 .p1-anchors.txt**

把 Step 2 的 69 行(子串 | 档 | 组)写入 `.p1-anchors.txt`(供 Task 3-7 agent 认领 + Task 8 assemble)。格式每行:`组 | 档 | 子串`。

- [ ] **Step 4: Commit**

```bash
git -C /Users/didi/work/linze-journal add learning/interview-tools/stealth-source-current.html learning/interview-tools/.p1-anchors.txt
git -C /Users/didi/work/linze-journal commit -m "chore(stealth): 备份源+抽取P1弹药卡69张锚点+分档"
```

---

### Task 2: 建 check_p1.py + 公共 agent prompt 模板

**Files:**
- Create: `learning/interview-tools/check_p1.py`
- Create: `learning/interview-tools/.p1-prompt-template.md`

**Interfaces:**
- Consumes: `learning/interview-tools/check_p2.py`(复用思路)
- Produces: `check_p1.py` —— `python3 check_p1.py <new_body.html> --orig <orig_body.html> --tier A|B`,校验分档维度词 + 只增不删 + 禁用项 + div 平衡,全过 exit 0 否则 exit 1;`.p1-prompt-template.md` —— 四 agent 共用 prompt 公共部分

- [ ] **Step 1: 写 check_p1.py**

```python
#!/usr/bin/env python3
"""校验 P1 弹药卡"加段补维度"产物。用法:
python3 check_p1.py <new_body.html> --orig <orig_body.html> --tier A|B
A 档(极薄/纯机制): 命中 ownership 词 + alternative 词
B 档(半截STAR/亮点成熟): 命中 eval 词 或 方法论句词
所有档: 改后长度 ≥ 原文*0.85(只增不删) + 禁碎嘴 + 无①②③④⑤堆叠 + div 平衡 + 无'6步闭环'
注:§4.1 其余雷区(Manager≠Claude/GPT、向量≠Chroma 等)因弹药卡会合法"提到被拒绝的选项",
naive 子串检查会误报,不在本脚本自动检查,改由 Task 9 人工 grep 抽检。"""
import re, sys, argparse

p = argparse.ArgumentParser()
p.add_argument("new")
p.add_argument("--orig", required=True)
p.add_argument("--tier", required=True, choices=["A", "B"])
a = p.parse_args()

new = open(a.new, encoding="utf-8").read()
orig = open(a.orig, encoding="utf-8").read()
errs = []

# 1. 只增不删(加段不应使 body 大幅变短)
if len(new) < len(orig) * 0.85:
    errs.append(f"只增不删失败: 新 {len(new)} < 原文 {len(orig)} * 0.85 (疑似删了原文段)")

# 2. 分档维度词
OWNERSHIP = ["我定的是", "我在", "我负责", "我设计", "我做的是", "我 drive", "我主导", "我牵头"]
ALTERNATIVE = ["拒绝", "本可以", "没选", "而不是", "instead", "不选", "放弃了", "权衡过", "排除了"]
EVAL = ["验证", "度量", "怎么知道", "效果", "若要度量", "指标", "测过", "看 ", "回放", "对照"]
METHOD = ["本质是", "本质在于", "下次", "可迁移", "可复用", "方法论", "规律", "套路", "抽象成"]
if a.tier == "A":
    if not any(w in new for w in OWNERSHIP):
        errs.append(f"A 档缺 ownership 词(任一:{OWNERSHIP})")
    if not any(w in new for w in ALTERNATIVE):
        errs.append(f"A 档缺 alternative 词(任一:{ALTERNATIVE})")
else:  # B
    if not (any(w in new for w in EVAL) or any(w in new for w in METHOD)):
        errs.append(f"B 档缺 eval 词 或 方法论句词(EVAL:{EVAL} / METHOD:{METHOD})")

# 3. 禁用口语碎嘴
banned = ["说白了", "得说句实话", "我自己比较得意", "这套东西", "你就懂了", "听着像"]
hit = [w for w in banned if w in new]
if hit:
    errs.append(f"命中口语碎嘴: {hit}")

# 4. ①②③④⑤ 堆叠(连续 4 个以上圈号)
if re.search(r"[①②③④⑤][①②③④⑤][①②③④⑤][①②③④⑤]", new):
    errs.append("①②③④⑤ 堆叠(≥4 连续),速查表腔")

# 5. div 平衡
if new.count("<div") != new.count("</div>"):
    errs.append(f"div 不平衡: <div {new.count('<div')} / </div> {new.count('</div>')}")

# 6. 唯一自动雷区:'6 步闭环'
if "6 步闭环" in new or "6步闭环" in new:
    errs.append("含'6 步闭环'(此说法不存在,§4.1 雷区)")

if errs:
    print(f"❌ 校验失败(--tier {a.tier}):")
    for e in errs: print("  -", e)
    sys.exit(1)
print(f"✅ 校验通过(--tier {a.tier},新 {len(new)} / 原 {len(orig)})")
```

- [ ] **Step 2: 用坏样例验证脚本能抓错**

```bash
cd learning/interview-tools
# 原文(模拟一张极薄卡)
printf '<div class="card-body"><p>六个文件枚举。</p></div>' > /tmp/orig.html
# A 档坏样例:没补 ownership/alternative + 变短 + 碎嘴
printf '<div class="card-body"><p>说白了删了。</p></div>' > /tmp/bad.html
python3 check_p1.py /tmp/bad.html --orig /tmp/orig.html --tier A; echo "exit=$?"
```
Expected: ❌(只增不删失败 + A 档缺 ownership + A 档缺 alternative + 口语碎嘴"说白了"),exit=1。

- [ ] **Step 3: 写公共 agent prompt 模板 `.p1-prompt-template.md`**

```markdown
你是面试速查卡写作 agent。任务:为 stealth.html 的 {N} 张「{组名}·机制弹药卡」**在原文 card-body 末尾加一小段补维度**(只加段,保留原文所有 <p>,不动 core/title/标签/外层 .card/data-g)。

# 必读(按顺序)
1. learning/interview-tools/STEALTH-CARDS-GUIDE.md —— §1(铁律)、§6(技术项目卡风格:declarative、不碎嘴、不堆栈、strong 标句首自然词)、§2.2(卡片模板)
2. docs/superpowers/specs/2026-07-22-stealth-p1-ammo-dimensions-design.md —— §5(两档补维度模板+硬约束)、§2.1(本组卡的分档表,看「本次负责的卡」)、§4.1(正向雷区清单)、§6(边界卡特殊处理)
3. 现有卡原文:从 stealth-source-current.html 抽 card-title 含"{子串}"的那张,**保留 card-body 里所有原文 <p> 好句**,只在末尾加一小段

# 分档补法(spec §3.2/§5)
- 🅰 极薄/纯机制档:加"我的取舍"段 = ownership("我在 X 项目里定的是 Y")+ alternative("本可以 Z,但拒绝了,因为 W")。
- 🅱 半截STAR/亮点成熟档:加"怎么验证/沉淀"段 = eval(怎么验证/效果,或诚实"框架先行没度量,若要度量会按 V 做")+ 方法论句(拔成可迁移命名判断)。若 eval/方法论已有其一,只补缺的。

# 产物格式(写入指定独立文件,禁碰 stealth.html)
每张卡用标记包裹,assemble 按标记解析:
<!-- P1CARD: {该卡 card-title 子串} -->
<div class="card-body">
{原文所有 <p> 段落,原样保留}
{新增的一小段:<p><strong>段首领起。</strong>…</p>}
</div>
<!-- /P1CARD -->

# 铁律
- **只增不删**:原文 <p> 全保留,新 body 长度 ≥ 原文。
- **§6 declarative 风格**,禁碎嘴(说白了/得说句实话/我自己比较得意/这套东西/你就懂了/听着像)。
- **数字按 §4.1 软化**(不确定软化/省略),绝不编百分比/倍数/团队规模。
- **§4.1 雷区回避**:Manager=qwen-flash 非 Claude/GPT · 12Agent=9外+3内 · 失败归因纯规则 · 向量自研 JSON+余弦非 Chroma · 增量 sha256 · prd-tools 是 Claude Code 插件非 SDD/"6步闭环"不存在 · "20+人"软化。
- ⚠️ 弹药卡会合法"提到被拒绝的选项"(如"不用 Chroma""Claude Code 插件"),这是 alternative 的正常写法,不是雷区误用——区分"我说我用 Chroma"(错) vs "我没选 Chroma"(对)。

# 本次负责的卡
{此处由 Task 3/4/5/6 填入:该组每张卡的 子串 | 档 | 五步维度补什么(从 spec §2.1 表取)}
```

- [ ] **Step 4: Commit**

```bash
git -C /Users/didi/work/linze-journal add learning/interview-tools/check_p1.py learning/interview-tools/.p1-prompt-template.md
git -C /Users/didi/work/linze-journal commit -m "chore(stealth): 建check_p1.py(分档维度+只增不删)+P1 agent prompt模板"
```

---

### Task 3: Agent-1 Manager 13 张

**Files:**
- Create: `learning/interview-tools/.p1-mgr.html`(13 张新 body,含原文+加段)

**Interfaces:**
- Consumes: `.p1-prompt-template.md`、`stealth-source-current.html`、spec §2.1 Manager 表、`check_p1.py`
- Produces: `.p1-mgr.html` —— 13 张卡新 card-body(<!-- P1CARD --> 标记包裹),供 Task 8 assemble

- [ ] **Step 1: 派 Agent-1 产 .p1-mgr.html**

用 `.p1-prompt-template.md` 公共部分 + 填入本次负责的卡(从 `.p1-anchors.txt` 的 mgr 行 + spec §2.1 Manager 表):

13 张 = 🅰 7(主干链路/编排层专家分工/Critic vs LLM/managerTask 协议/流式输出阶段事件/多Agent可观测性/反复用工程模式)+ 🅱 6(HITL checkpoint/自我进化机制/这项目真上生产了吗/为什么硬编码状态机/和市面竞品比/39节点是否过度设计)。

prompt 写死:**只产 .p1-mgr.html(13 张 body 片段),禁碰 stealth.html、禁碰其他组卡、禁碰 C 批 4529-4540**。Agent 必读 GUIDE + spec §5/§2.1/§4.1/§6 + stealth-source-current.html 各卡原文。

- [ ] **Step 2: 逐张抽原文 + check 校验**

```bash
cd learning/interview-tools
# 对每张:从 source 抽原文 body,从产物抽新 body,按档跑 check
python3 - <<'PY'
import re, subprocess, sys
src = open("stealth-source-current.html", encoding="utf-8").read()
prod = open(".p1-mgr.html", encoding="utf-8").read()
subs = ["主干链路长什么样","编排层和专家层怎么分工","HITL checkpoint 解决什么问题",
        "Critic 节点和一次 LLM 调用","managerTask 协议是干嘛","流式输出和阶段事件怎么走",
        "多 Agent 出问题怎么定位","反复用的几个工程模式","自我进化机制是什么样",
        "这项目真上生产了吗","为什么用硬编码状态机","和市面多 Agent 竞品比","39 个节点是不是过度设计"]
tiers = ["A","A","B","A","A","A","A","A","B","B","B","B","B"]
def body_of(html, sub):
    i = html.find(sub); j = html.find('<div class="card-body">', i)
    k = html.find('</div>', j)  # 简化:第一个 </div>;Agent 产物结构规整可用
    return html[j:k+len('</div>')]
ok = True
for sub, t in zip(subs, tiers):
    ob = body_of(src, sub); nb = body_of(prod, sub)
    open("/tmp/o.html","w",encoding="utf-8").write(ob)
    open("/tmp/n.html","w",encoding="utf-8").write(nb)
    r = subprocess.run(["python3","check_p1.py","/tmp/n.html","--orig","/tmp/o.html","--tier",t],
                       capture_output=True, text=True)
    flag = "✅" if r.returncode==0 else "❌"
    if r.returncode: ok = False
    print(flag, t, sub, "::", r.stdout.strip() or r.stderr.strip())
print("ALL OK" if ok else "有失败,修产物重跑")
PY
```
Expected: 13 行全 ✅。❌ 的卡按报错修 `.p1-mgr.html` 对应段(补缺失维度词 / 补回被删原文 / 去碎嘴)重跑,直到全 ✅。

> 注:`body_of` 用第一个 `</div>` 是简化定位;若某张 body 内嵌套 div 导致截断错误,改用手动核对或让 assemble(Task 8)用 card-title 锚点完整切分后回灌校验。

- [ ] **Step 3: Commit 产物**

```bash
git -C /Users/didi/work/linze-journal add learning/interview-tools/.p1-mgr.html
git -C /Users/didi/work/linze-journal commit -m "feat(stealth): P1 Manager 13张弹药卡加段补维度(A档7+B档6)"
```

---

### Task 4: Agent-2 Code 18 张(含 4514 特殊标)

**Files:**
- Create: `learning/interview-tools/.p1-code.html`

**Interfaces:**
- Consumes: 同 Task 3(换 Code 组)
- Produces: `.p1-code.html` —— 18 张新 body

- [ ] **Step 1: 派 Agent-2 产 .p1-code.html**

prompt 公共部分 + 本次卡(`.p1-anchors.txt` code 行 + spec §2.1 Code 表):
18 张 = 🅰 7(18工具分工/静态分析Bug检测/共享代码上下文/防模型乱来/改完自动验/跑长任务Checkpoint/AsyncLocalStorage)+ 🅱 11(ReAct循环/意图路由/语义检索vs全量/ Diff命门/Shadow Patch/个性化RAG/被问上线了吗/和Cursor比/opencode/18工具是否太多/**4514 系统设计型**)。

**4514 特殊标**(spec §6):它是"如果让你设计 Coding Agent"的系统设计答题,ownership 写"基于 code_assistant 经验推导的设计能力"(非"我做过"),方法论句点明"这是设计题不是实战复盘"。

prompt 写死:**只产 .p1-code.html(18 张),禁碰 stealth.html、其他组卡、C 批 4529-4540**。

- [ ] **Step 2: 逐张 check 校验**

同 Task 3 Step 2,subs 换成 18 个 Code 子串、tiers 换成 `["B","B","A","B","A","A","B","A","A","A","B","B","A","B","B","B","B","B"]`(对应 808B/820B/831A/842B/853A/864A/875B/887A/898A/908A/918B/928B/939A/950B/960B/970B/981B/4514B)。全 ✅。

- [ ] **Step 3: Commit 产物**

```bash
git -C /Users/didi/work/linze-journal add learning/interview-tools/.p1-code.html
git -C /Users/didi/work/linze-journal commit -m "feat(stealth): P1 Code 18张弹药卡加段补维度(A档7+B档11,含4514系统设计标)"
```

---

### Task 5: Agent-3 PRD 上半 19 张(行号 2116-2397)

**Files:**
- Create: `learning/interview-tools/.p1-prd-up.html`

**Interfaces:**
- Consumes: 同 Task 3(换 PRD 上半组)
- Produces: `.p1-prd-up.html` —— 19 张新 body

- [ ] **Step 1: 派 Agent-3 产 .p1-prd-up.html**

prompt 公共部分 + 本次卡(`.p1-anchors.txt` prd-up 行 + spec §2.1 PRD 表):
19 张(2116/2124/2155/2167/2182/2197/2213/2230/2271/2280/2291/2302/2313/2324/2347/2357/2369/2382/2397)= 🅰 11 + 🅱 8。

**撞车卡 2213**(spec §6):2213「5h→2h 怎么度量」与 2845 撞车。2213 答"度量方法论(怎么设指标)",末尾点一句"实验组对照组怎么设见另一张卡"。不合并。

prompt 写死:**只产 .p1-prd-up.html(19 张),禁碰 stealth.html、其他组卡**。

- [ ] **Step 2: 逐张 check 校验**

同 Task 3 Step 2,subs 用 `.p1-anchors.txt` prd-up 的 19 子串,tiers 按表(A/B)。全 ✅。

- [ ] **Step 3: Commit 产物**

```bash
git -C /Users/didi/work/linze-journal add learning/interview-tools/.p1-prd-up.html
git -C /Users/didi/work/linze-journal commit -m "feat(stealth): P1 PRD上半19张弹药卡加段补维度(A档11+B档8)"
```

---

### Task 6: Agent-4 PRD 下半 18 张(行号 2412-2934)

**Files:**
- Create: `learning/interview-tools/.p1-prd-down.html`

**Interfaces:**
- Consumes: 同 Task 3(换 PRD 下半组)
- Produces: `.p1-prd-down.html` —— 18 张新 body

- [ ] **Step 1: 派 Agent-4 产 .p1-prd-down.html**

prompt 公共部分 + 本次卡(`.p1-anchors.txt` prd-down 行 + spec §2.1 PRD 表):
18 张(2412/2423/2443/2454/2467/2479/2570/2629/2640/2651/2661/2671/2701/2747/2845/2921/2934 + 2499)= 🅰 9 + 🅱 9。

**撞车卡 2845**(spec §6):2845「实验组对照组」与 2213 撞车。2845 答"数据素养(实验组对照组怎么设)",末尾点一句"度量指标体系见另一张卡"。不合并。

**⚠️ 物理相邻**:2921(SDD)/2934(Harness)附近无 C 批卡,但 PRD 下半改时注意只动这 18 张锚点。

prompt 写死:**只产 .p1-prd-down.html(18 张),禁碰 stealth.html、其他组卡**。

- [ ] **Step 2: 逐张 check 校验**

同 Task 3 Step 2,subs 用 prd-down 18 子串,tiers 按表。全 ✅。

- [ ] **Step 3: Commit 产物**

```bash
git -C /Users/didi/work/linze-journal add learning/interview-tools/.p1-prd-down.html
git -C /Users/didi/work/linze-journal commit -m "feat(stealth): P1 PRD下半18张弹药卡加段补维度(A档9+B档9)"
```

---

### Task 7: 技术选型 602(主会话单张,边缘卡)

**Files:**
- Create: `learning/interview-tools/.p1-tech.html`
- Reference: `stealth-source-current.html` 中 card-title 含"我的技术选型怎么做"的卡

**Interfaces:**
- Consumes: spec §6(602 特殊处理)
- Produces: `.p1-tech.html` —— 1 张新 body

- [ ] **Step 1: 主会话直接改 602(不开 agent,单张)**

602 是"方法论型弹药"(spec §6):方法论四步已完整 + 有 Schema 举例 + 诚实边界,**不补方法论句**,只补 ownership——把通用方法论挂回项目实例。

读 stealth-source-current.html 中 602 的 card-body,保留全部原文 `<p>`,末尾加一段:
```
<p><strong>挂回我的项目。</strong>这不是通用答题,我 Schema 选型(if-else/低代码/Schema 驱动三选一)就是走这套——先定场景(B 端配置页)、过四约束、列候选对比、ADR 化决策;code_assistant 向量库选型同理(自研 JSON+余弦 vs Chroma,按量小权衡)。这套方法论是我两个项目反复验证过的肌肉记忆。</p>
```
写入 `.p1-tech.html`(P1CARD 标记包裹,子串="我的技术选型怎么做")。

> 这段是骨架,执行时核对 spec §4.1 雷区(向量自研非 Chroma 是合法 alternative 提及,不是误用)+ 口语化润色,数字软化。

- [ ] **Step 2: check 校验(B 档,但因只补 ownership,放宽——手动确认 ownership 词命中即可)**

```bash
cd learning/interview-tools
# 602 是边缘卡,check --tier B 会要 eval/方法论词,但它方法论已有;改用 --tier A 验 ownership+alternative 命中
python3 - <<'PY'
src = open("stealth-source-current.html", encoding="utf-8").read()
prod = open(".p1-tech.html", encoding="utf-8").read()
sub = "我的技术选型怎么做"
i = src.find(sub); j = src.find('<div class="card-body">', i); k = src.find('</div>', j)
ob = src[j:k+len('</div>')]
pi = prod.find(sub); pj = prod.find('<div class="card-body">', pi); pk = prod.find('</div>', pj)
nb = prod[pj:pk+len('</div>')]
open("/tmp/o.html","w",encoding="utf-8").write(ob)
open("/tmp/n.html","w",encoding="utf-8").write(nb)
print("新",len(nb),"原",len(ob),"=> 只增不删", "✅" if len(nb)>=len(ob)*0.85 else "❌")
PY
# 雷区 + div 平衡 + 碎嘴 用 check --tier A 跑(确认 ownership/alternative 命中 + 无雷区)
python3 check_p1.py /tmp/n.html --orig /tmp/o.html --tier A; echo "exit=$?"
```
Expected: 只增不删 ✅ + check --tier A 通过(ownership 词"我在/我 Schema"命中 + alternative"vs"相关词——若 alternative 词未命中,因 602 重点是 ownership,可在新段补"而不是 X"满足)。exit=0。

- [ ] **Step 3: Commit 产物**

```bash
git -C /Users/didi/work/linze-journal add learning/interview-tools/.p1-tech.html
git -C /Users/didi/work/linze-journal commit -m "feat(stealth): P1 技术选型602补ownership挂回项目(方法论型边缘卡)"
```

---

### Task 8: assemble_p1.py + 组装 69 张

**Files:**
- Create: `learning/interview-tools/assemble_p1.py`
- Modify: `learning/interview-tools/stealth.html`(69 张 card-body swap)

**Interfaces:**
- Consumes: `.p1-mgr.html`/`.p1-code.html`/`.p1-prd-up.html`/`.p1-prd-down.html`/`.p1-tech.html`(共 69 张新 body)+ `.p1-anchors.txt`(69 子串)
- Produces: stealth.html 69 张 card-body 已替换(原文→原文+加段),data-g/subOrder/title/core 不变

- [ ] **Step 1: 写 assemble_p1.py**

```python
#!/usr/bin/env python3
"""组装 P1 弹药卡:把 5 个产物文件的 69 张新 card-body,按 card-title 子串锚点
替换进 stealth.html(只换 card-body,不动 data-g/subOrder/title/core)。原子写。
产物文件用 <!-- P1CARD: {子串} --> ... <!-- /P1CARD --> 标记,内含完整新 card-body。"""
import re, sys

HTML = "learning/interview-tools/stealth.html"
PROD = ["learning/interview-tools/.p1-mgr.html",
        "learning/interview-tools/.p1-code.html",
        "learning/interview-tools/.p1-prd-up.html",
        "learning/interview-tools/.p1-prd-down.html",
        "learning/interview-tools/.p1-tech.html"]

# 1. 解析产物: 子串 -> 新 card-body(含 <div class="card-body">...</div>)
new_bodies = {}
for f in PROD:
    txt = open(f, encoding="utf-8").read()
    for m in re.finditer(r"<!-- P1CARD: (.+?) -->\s*(<div class=\"card-body\">.*?</div>)\s*<!-- /P1CARD -->",
                         txt, re.S):
        sub = m.group(1).strip()
        new_bodies[sub] = m.group(2)

html = open(HTML, encoding="utf-8").read()
orig_html = html
replaced = 0
missing = []

for sub, new_body in new_bodies.items():
    # 锚点:子串必须出现在某个 card-title 内且唯一(避免短子串在 body 里误匹配错位)
    matches = list(re.finditer(r'card-title">[^<]*' + re.escape(sub), html))
    if len(matches) != 1:
        missing.append((sub, f"title 匹配 {len(matches)} 次,应 1")); continue
    ti = matches[0].start()
    bi = html.find('<div class="card-body">', ti)
    be = html.find('</div>', bi) + len('</div>')
    old = html[bi:be]
    if old == new_body:
        continue  # 无变化
    html = html[:bi] + new_body + html[be:]
    replaced += 1

if missing:
    print("❌ 产物里有锚点在 stealth.html 找不到:", missing)
    sys.exit(1)

# div 平衡 + script 完整快检
assert html.count("<div") == html.count("</div>"), "div 不平衡"
assert "<script>" in html and "</script>" in html, "script 残缺"

open(HTML, "w", encoding="utf-8").write(html)
print(f"✅ 组装完成:替换 {replaced} 张 card-body(共 {len(new_bodies)} 张锚点,产物文件数 {len(PROD)})")
```

- [ ] **Step 2: 先 dry-run 确认锚点都能定位(注释掉写文件那行,跑解析)**

```bash
cd learning/interview-tools
# 解析产物数 + 确认每个锚点子串在 stealth.html 的 card-title 内唯一(与 assemble 同逻辑)
python3 - <<'PY'
import re
PROD = [".p1-mgr.html",".p1-code.html",".p1-prd-up.html",".p1-prd-down.html",".p1-tech.html"]
subs=[]
for f in PROD:
    t=open(f,encoding="utf-8").read()
    subs += [m.strip() for m in re.findall(r"<!-- P1CARD: (.+?) -->", t)]
print(f"产物解析出 {len(subs)} 张")
assert len(subs)==69, f"应为 69 张,实际 {len(subs)}"
html=open("stealth.html",encoding="utf-8").read()
bad=[(s, len(re.findall(r'card-title">[^<]*'+re.escape(s), html))) for s in subs]
bad=[b for b in bad if b[1]!=1]
print("锚点 title 匹配异常:", bad if bad else "无 ✅ (每个子串在 card-title 内唯一)")
PY
```
Expected: `产物解析出 69 张` + `锚点缺失: 无 ✅`。若有缺失,核对子串(Task 1 Step 2 的唯一性提醒)。

- [ ] **Step 3: 正式组装**

```bash
cd learning/interview-tools
python3 assemble_p1.py
```
Expected: `✅ 组装完成:替换 N 张 card-body(共 69 张锚点,产物文件数 5)`。

- [ ] **Step 4: 抽样核对 3 张(1 张 A 档 + 1 张 B 档 + 602)组装正确**

```bash
cd learning/interview-tools
for sub in "主干链路长什么样" "Shadow Patch" "我的技术选型怎么做"; do
  echo "=== $sub ==="
  grep -A 12 "$sub" stealth.html | head -16
done
```
Expected: 每张看到原文 `<p>` 段 + 末尾新增的"我的取舍"/"怎么验证·沉淀"/"挂回我的项目"段;data-g/core/title 未变。

- [ ] **Step 5: Commit 组装结果**

```bash
git -C /Users/didi/work/linze-journal add learning/interview-tools/stealth.html learning/interview-tools/assemble_p1.py
git -C /Users/didi/work/linze-journal commit -m "feat(stealth): 组装P1弹药卡69张加段补维度body assemble_p1.py"
```

---

### Task 9: 雷区人工 grep 抽检 + 结构校验

**Files:**
- Read/verify: `learning/interview-tools/stealth.html`

**Interfaces:**
- Consumes: spec §4.1 雷区清单 + stealth.html

- [ ] **Step 1: div 平衡 + script 完整**

```bash
cd learning/interview-tools
python3 - <<'PY'
html=open("stealth.html",encoding="utf-8").read()
print("<div>",html.count("<div")," </div>",html.count("</div>"),"=>","平衡✅" if html.count("<div")==html.count("</div>") else "不平衡❌")
print("<script>",html.count("<script>")," </script>",html.count("</script>"))
PY
```
Expected: div 平衡✅;script 标签成对。

- [ ] **Step 2: §4.1 雷区 grep(读上下文判断误用 vs 合法提及)**

```bash
cd learning/interview-tools
echo "=== '6步闭环'(必须 0) ==="; grep -c "6步闭环\|6 步闭环" stealth.html
echo "=== Manager 被说成 Claude/GPT/Anthropic 的模型(读上下文) ==="; grep -n "Manager.*\(Claude\|GPT\|Anthropic\)\|\(Claude\|GPT\|Anthropic\).*Manager" stealth.html | head
echo "=== '我用 Chroma'(误用;合法是'没用/没选 Chroma') ==="; grep -n "Chrom" stealth.html | head
echo "=== '20+人\|20+ 人\|二十多人'硬数(应软化) ==="; grep -n "20+人\|20+ 人\|二十多人\|20多个人" stealth.html | head
```
Expected: "6步闭环" = 0;其余 grep 结果逐条读上下文——合法提及(如"我没选 Chroma""Manager 用 qwen-flash 不是 Claude")保留;误用(如"我用 Chroma""Manager 是 Claude")修。

- [ ] **Step 3: 抽 5 张(跨组)人工读 body,确认补维度合理 + 只增不删**

```bash
cd learning/interview-tools
for sub in "Critic 节点和一次 LLM 调用" "Shadow Patch" "SSOT 五条边界规则" "实验组和对照组" "我的技术选型怎么做"; do
  echo "=== $sub ==="; grep -A 14 "$sub" stealth.html | head -18; echo
done
```
Expected: 5 张都看到原文段保留 + 末尾新增段补了对应维度(A 档 ownership+alternative / B 档 eval+方法论 / 602 ownership);撞车卡 2213/2845 互相点名;4514 标注"设计题"。若发现某张维度补错/删了原文,回对应 Task 修产物重 assemble。

- [ ] **Step 4: 若 Step 1-3 有修复,Commit**

```bash
git -C /Users/didi/work/linze-journal add -A learning/interview-tools/
git -C /Users/didi/work/linze-journal commit -m "fix(stealth): P1弹药卡雷区抽检修复(若有)" || echo "无修复,跳过"
```

---

### Task 10: bump sw.js + 个人账号 push + 清理临时产物

**Files:**
- Modify: `sw.js`(CACHE_NAME kb-v326→kb-v327)
- Delete: `.p1-*.html`/`.p1-anchors.txt`/`.p1-prompt-template.md`/`stealth-source-current.html`(临时产物,保留 check_p1.py/assemble_p1.py 复用)

**Interfaces:**
- Consumes: origin/main 当前 CACHE_NAME(必核)

- [ ] **Step 1: 核 origin 已部署版本**

```bash
cd /Users/didi/work/linze-journal
git show origin/main:sw.js | grep CACHE_NAME
grep -m1 CACHE_NAME sw.js
```
Expected: origin = `kb-v326`(本地也是)。若 origin 已被别的提交 bump 到更高,**取 max + 1**(kb-v325 撞号教训)。

- [ ] **Step 2: bump CACHE_NAME kb-v326 → kb-v327**

```bash
cd /Users/didi/work/linze-journal
sed -i '' "s/const CACHE_NAME = 'kb-v326';/const CACHE_NAME = 'kb-v327';/" sw.js
grep -m1 CACHE_NAME sw.js
```
Expected: `const CACHE_NAME = 'kb-v327';`。(若 Step 1 发现 origin 已 >326,改成对应 +1。)

- [ ] **Step 3: 清理临时产物(保留 check_p1.py + assemble_p1.py 供复用)**

```bash
cd learning/interview-tools
rm -f .p1-mgr.html .p1-code.html .p1-prd-up.html .p1-prd-down.html .p1-tech.html .p1-anchors.txt .p1-prompt-template.md stealth-source-current.html
ls check_p1.py assemble_p1.py  # 确认复用脚本保留
```

- [ ] **Step 4: Commit + 个人账号 push**

```bash
cd /Users/didi/work/linze-journal
git add -A
git commit -m "chore(stealth): bump CACHE_NAME kb-v326→kb-v327(P1弹药卡69张加段补维度)

清理临时产物(保留check_p1/assemble_p1脚本)"
git push github-personal:zachary-lz-glm main
```
Expected: push 成功,触发 GitHub Pages。

- [ ] **Step 5: 验证线上(等 Pages 部署后)**

```bash
cd /Users/didi/work/linze-journal
# 拉 origin 确认 CACHE_NAME 已是 kb-v327
git show origin/main:sw.js | grep CACHE_NAME
```
Expected: origin `kb-v327`。线上访问确认弹药卡补维度生效、无旧缓存。

---

## Self-Review(plan 自查,已完成)

- **Spec 覆盖**:spec §2.1(69 张分档)→ Task 1 锚点+Task 3-7 各组;§3.2 分档补法→ Task 2 模板+check;§4.1 雷区→ Task 9;§5 两档模板→ Task 2 模板;§6 边界(4514/602/撞车卡)→ Task 4/7/5/6;§7 流程→ Task 1-10。✅ 无遗漏。
- **Placeholder**:check_p1.py/assemble_p1.py/agent prompt 均完整代码,无 TBD。✅
- **类型/命名一致**:`.p1-*` 产物文件名、P1CARD 标记、子串锚点在 Task 1/2/8 一致。✅
- **已知简化点**(已在对应 Step 标注):Task 3/4/5/6 Step 2 的 `body_of` 用第一个 `</div>` 截断,若 body 嵌套 div 可能截断错误——assemble(Task 8)用完整 P1CARD 标记切分,回灌校验更稳;若 check 阶段截断报错,手动核对或延到 assemble 后校验。
