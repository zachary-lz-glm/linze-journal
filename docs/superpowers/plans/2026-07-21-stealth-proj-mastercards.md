# stealth Agent 三件套主陈述卡重构 · 实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: 用 superpowers:subagent-driven-development(推荐)或 superpowers:executing-plans 逐 task 执行。步骤用 `- [ ]` 跟踪。

**Goal:** 把 stealth.html 里 Agent 三件套(Manager/Code/PRD)各 1 张主陈述雏形卡的 `card-body` 重写成五步骨架(业务问题/本质矛盾/决策+alternatives/结果+eval/方法论+局限),机制弹药卡 76 张不动。

**Architecture:** 双层(主陈述卡 + 弹药卡)。每项目派 1 个 agent 读源文档产出 `card-body` HTML 到独立文件 → Python 锚点脚本按 `card-title` 替换 3 张雏形的 body(原子写,不动 core/title/data-g/data-kw)→ grep + 雷区抽检校验 → bump `sw.js`。

**Tech Stack:** HTML(stealth.html 单页,无构建工具)、Python 3(组装/校验脚本)、grep/bash(验收)。

## Global Constraints

- **数字沿用现有已校准值**;§1.3 雷区必须回避:
  - Manager:模型是阿里云 **qwen-flash**(非 Claude/GPT);12 Agent = **9 外 + 3 内**;失败归因**纯规则非 LLM**;**自动晋级默认关**;Checkpoint 是**自建 16 字段快照**
  - Code:向量检索是**自研 JSON+内存余弦**(非 Chroma);增量靠 **sha256**(非 git 钩子);**无** Diff 预览用户确认 / 独立审查 Agent / HITL 写确认
  - PRD:prd-tools 真身是 **Claude Code 插件**(/reference + /prd-distill);"prd2code-gen 6 步闭环"**不存在**;"20+ 人团队"软化(ADR-0005 写 1-5 人)
- **§6 declarative 风格**;禁口语碎嘴:说白了 / 得说句实话 / 我自己比较得意 / 被问 X 我答 / 这套东西 / 你就懂了
- **主卡不堆技术栈**:技术名词只在 body 最后一句带过(如「栈:Nuxt4+LangGraph」),不展开;详细栈留给弹药卡
- **标题 / core / data-g / data-kw 不动**(零路由风险)
- **改完 bump `sw.js` 的 `CACHE_NAME`**(kb-vN → kb-vN+1,看 origin 已部署版本 +1,见 GUIDE §4.7)
- 用**个人 GitHub 账号**推送(非公司账号)
- stealth.html 是单页大文件,组装用 **Python 锚点替换 + 原子写**,不用多次 Edit
- agent 产出**独立文件**,主会话统一组装,避免并发改同一文件(GUIDE §4.6)

## File Structure

| 文件 | 责任 | 动作 |
|------|------|------|
| `learning/interview-tools/stealth.html` | 速查页主体 | 改:3 张雏形 card-body |
| `learning/interview-tools/stealth-source-current.html` | 重写前的源料备份 | 建 |
| `learning/interview-tools/check_mastercard.py` | 校验 agent 产物(五段/禁用项/div 平衡) | 建 |
| `learning/interview-tools/assemble_mastercards.py` | 按 card-title 锚点替换 3 张 body | 建 |
| `learning/interview-tools/.mastercard-{manager,code,prd}.html` | 三张主卡 body 产物(临时) | 建,组装后删 |
| `sw.js` | Service Worker 缓存版本 | 改:CACHE_NAME |

---

### Task 1: 备份源 + 抽取三张雏形卡锚点

**Files:**
- Create: `learning/interview-tools/stealth-source-current.html`
- Create: `learning/interview-tools/.mastercard-anchors.txt`

**Interfaces:**
- Produces: `.mastercard-anchors.txt` 含三张雏形卡的 `card-title` 锚点字符串 + `card-body` 起止标记,供 Task 6 组装脚本读取

- [ ] **Step 1: 备份 stealth.html**

```bash
cp learning/interview-tools/stealth.html learning/interview-tools/stealth-source-current.html
```

- [ ] **Step 2: 抽取三张雏形卡锚点并验证唯一**

```bash
cd learning/interview-tools
for t in "这个项目 30 秒怎么说" "这个 Code Agent 到底是什么" "AI工作流完整介绍"; do
  n=$(grep -c "card-title\">$t" stealth.html || true)
  echo "$t => $n 次匹配"
done
```
Expected: 三张各 `1 次匹配`。若某张 ≠1,停下排查(标题被改过或重复)。

- [ ] **Step 3: 记录锚点到文件**

把三个 `card-title` 原文写入 `.mastercard-anchors.txt`,每行一个,供 Task 6 的组装脚本逐行读取做替换定位。

- [ ] **Step 4: Commit**

```bash
git -C /Users/didi/work/linze-journal add learning/interview-tools/stealth-source-current.html learning/interview-tools/.mastercard-anchors.txt
git -C /Users/didi/work/linze-journal commit -m "chore(stealth): 备份源+抽取主卡锚点"
```

---

### Task 2: 写校验脚本 + 公共 agent prompt 模板

**Files:**
- Create: `learning/interview-tools/check_mastercard.py`
- Create: `learning/interview-tools/.mastercard-prompt-template.md`

**Interfaces:**
- Produces: `check_mastercard.py` —— 输入一个 body 片段文件路径,跑校验,全过 exit 0 否则 exit 1;`.mastercard-prompt-template.md` —— 三张卡共用的 agent prompt 公共部分

- [ ] **Step 1: 写 check_mastercard.py**

```python
#!/usr/bin/env python3
"""校验主陈述卡 card-body 产物。用法: python3 check_mastercard.py <body.html>"""
import re, sys

f = sys.argv[1]
html = open(f, encoding="utf-8").read()
errs = []

# 1. 五段 <strong> 段首(至少 5 个 <strong>...)
strongs = re.findall(r"<strong>[^<]{2,}</strong>", html)
if len(strongs) < 5:
    errs.append(f"段首 <strong> 只有 {len(strongs)} 个,需 ≥5")

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

# 6. 雷区词(粗扫,精确抽检在 Task 7)
if "Chroma" in html:
    errs.append("雷区词 Chroma(Code 向量是自研非 Chroma)")
if re.search(r"prd2code-gen.*6\s*步", html) and "不存在" not in html and "原型" not in html:
    errs.append("prd2code-gen 6 步闭环未软化")

if errs:
    print("❌ 校验失败:")
    for e in errs: print("  -", e)
    sys.exit(1)
print(f"✅ 校验通过({len(strongs)} 段 <strong>)")
```

- [ ] **Step 2: 用坏样例验证脚本能抓错**

```bash
cd learning/interview-tools
printf '<div class="card-body"><p>说白了</p><div></div></div>' > /tmp/bad.html
python3 check_mastercard.py /tmp/bad.html; echo "exit=$?"
```
Expected: 打印 ❌(段首<strong>不足 / 口语碎嘴"说白了" / div 不平衡),exit=1。

- [ ] **Step 3: 写公共 agent prompt 模板 `.mastercard-prompt-template.md`**

```markdown
你是面试速查卡写作 agent。任务:为 stealth.html 重写一张「项目主陈述卡」的 card-body(只 body,不动 core/title/标签)。

# 必读(按顺序)
1. learning/interview-tools/STEALTH-CARDS-GUIDE.md —— §1(铁律)、§6(Agent 项目卡风格标尺)、§2.2(卡片模板)
2. docs/superpowers/specs/2026-07-21-stealth-proj-mastercards-design.md —— §5(五步模板+硬约束)、§6.{X}(本项目骨架)、§4(校准雷区)、§8(质量门)
3. {说明书路径}
4. learning/interview-kb/明日面试_预测题校准与匹配分析.md —— 校准清单
5. 现有雏形卡原文: 从 stealth-source-current.html 抽取 card-title="{雏形标题}" 的那张卡

# card-body 五段骨架(每段 <strong>段首领起。</strong> 开头)
① 业务问题 + 为什么重要 —— 解决什么、不解决会怎样(lead with impact,不堆技术栈)
② 本质矛盾 —— 难点本质在哪(非模型更大 / 非堆功能)
③ 关键决策 + 拒绝了什么 —— 每个高杠杆决策讲"为什么选它 + 考虑并拒绝了什么 alternative"
④ 结果 + 怎么验证 —— 指标 + eval/metrics(非 vibes)+ 可复用价值
⑤ 方法论 + 局限 —— 可迁移命名框架 + 诚实边界(局限 / 下次怎么做)
技术栈只在 body 最后一句带过(如「栈:Nuxt4+LangGraph」),不展开。

# 风格(§6)
declarative 陈述句;禁口语碎嘴(说白了/得说句实话/我自己比较得意/被问X我答/这套东西);
①② 可内联枚举,不堆 ①②③④⑤。

# 硬约束
- 只产出 card-body 的 HTML(从 <div class="card-body"> 到对应 </div>),不含 core / card-title / 外层 .card div
- 数字沿用雏形卡现有已校准值;§1.3 雷区回避(spec §4 已列)
- div 平衡;无 loop 残留;无 <html>/<body> 包裹

# 产出
只输出 HTML 片段本身,不要任何解释、不要 ``` 包裹。
```

- [ ] **Step 4: Commit**

```bash
git -C /Users/didi/work/linze-journal add learning/interview-tools/check_mastercard.py learning/interview-tools/.mastercard-prompt-template.md
git -C /Users/didi/work/linze-journal commit -m "chore(stealth): 主卡校验脚本+公共agent prompt模板"
```

---

### Task 3: Manager 主卡 agent

> Task 3/4/5 互相独立(不同项目、不同产物文件),**可并行派 3 个 agent**。

**Files:**
- Create: `learning/interview-tools/.mastercard-manager.html`

**Interfaces:**
- Consumes: `.mastercard-prompt-template.md`(Task 2)、`stealth-source-current.html`(Task 1)
- Produces: `.mastercard-manager.html` —— Manager 主卡 card-body 片段

- [ ] **Step 1: 派 general-purpose agent**

prompt = `.mastercard-prompt-template.md` 内容,填入:
- `{说明书路径}` = `learning/ai-projects/Manager-Agent-多智能体编排总管.md`
- `{雏形标题}` = `这个项目 30 秒怎么说?`
- `{X}` = `1`
- 并附 spec §6.1 的五步要点作为该项目的内容骨架(业务问题=多能力入口分散;本质矛盾=编排可信;决策=硬编码状态机拒绝LLM自主/Probe+Health拒绝单层/Critic拒绝单次LLM/HITL拒绝全自动;结果=研究型诚实边界+LangSmith可观测;方法论=编排可信三件套+局限)

agent 必须读 `/Users/didi/work/agent-main/Manager_Agent/` 源码核对数字(spec §4 雷区),产出写入 `.mastercard-manager.html`。

- [ ] **Step 2: 校验产物**

```bash
cd learning/interview-tools
python3 check_mastercard.py .mastercard-manager.html; echo "exit=$?"
```
Expected: `✅ 校验通过(5 段 <strong>)`,exit=0。若失败,把错误回喂 agent 重产出。

- [ ] **Step 3: 人工风格抽看**

打开 `.mastercard-manager.html`,确认:declarative 不碎嘴、技术栈只在末句、②本质矛盾和⑤方法论非空话。

- [ ] **Step 4: Commit**

```bash
git -C /Users/didi/work/linze-journal add learning/interview-tools/.mastercard-manager.html
git -C /Users/didi/work/linze-journal commit -m "feat(stealth): Manager 主陈述卡五步骨架"
```

---

### Task 4: Code 主卡 agent

**Files:**
- Create: `learning/interview-tools/.mastercard-code.html`

**Interfaces:**
- Consumes: `.mastercard-prompt-template.md`、`stealth-source-current.html`
- Produces: `.mastercard-code.html`

- [ ] **Step 1: 派 general-purpose agent**

prompt = 模板填入:
- `{说明书路径}` = `learning/ai-projects/Code-Assist-Agent-工程化代码助手.md`
- `{雏形标题}` = `这个 Code Agent 到底是什么?`
- `{X}` = `2`
- 附 spec §6.2 五步要点(业务问题=缺真能改代码的+写权限=事故;本质矛盾=改得可信非能改;决策=ReAct拒绝Supervisor/语义检索拒绝全量/Diff受控写盘拒绝覆盖/Shadow Patch拒绝固定prompt;结果=800文件demo诚实+sha256静态分析自验自修;方法论=安全在代码路径不在prompt+ReAct/Supervisor按场景+局限)

agent 读 `/Users/didi/work/agent-main/code_assistent_Agent/` 源码核对,产出 `.mastercard-code.html`。

- [ ] **Step 2: 校验产物**

```bash
cd learning/interview-tools
python3 check_mastercard.py .mastercard-code.html; echo "exit=$?"
```
Expected: `✅ 校验通过`,exit=0。

- [ ] **Step 3: 人工风格抽看 + Commit**

```bash
git -C /Users/didi/work/linze-journal add learning/interview-tools/.mastercard-code.html
git -C /Users/didi/work/linze-journal commit -m "feat(stealth): Code 主陈述卡五步骨架"
```

---

### Task 5: PRD 主卡 agent

**Files:**
- Create: `learning/interview-tools/.mastercard-prd.html`

**Interfaces:**
- Consumes: `.mastercard-prompt-template.md`、`stealth-source-current.html`
- Produces: `.mastercard-prd.html`

- [ ] **Step 1: 派 general-purpose agent**

prompt = 模板填入:
- `{说明书路径}` —— PRD 工作流无独立说明书;改指示 agent 读 stealth-source-current.html 里 `data-g="PRD 工作流"` 的 40 张卡作为事实源 + spec §4 PRD 雷区
- `{雏形标题}` = `AI工作流完整介绍(面试第一答)`
- `{X}` = `3`
- 附 spec §6.3 五步要点(业务问题=认知偏差+隐性知识;本质矛盾=结论可不可信非生成;决策=SSOT拒绝冗余/证据链拒绝无引用/多层门控拒绝端到端直出;结果=5h→2h/80%/40→85%有对照实验+20+人软化+6步闭环诚实说不存在;方法论=AI产出可信三支柱+局限60%损耗)

agent 产出 `.mastercard-prd.html`,**特别核对** "20+ 人"软化、"prd2code-gen 6 步闭环"不声称存在(spec §4)。

- [ ] **Step 2: 校验产物**

```bash
cd learning/interview-tools
python3 check_mastercard.py .mastercard-prd.html; echo "exit=$?"
```
Expected: `✅ 校验通过`,exit=0。

- [ ] **Step 3: 人工风格抽看 + Commit**

```bash
git -C /Users/didi/work/linze-journal add learning/interview-tools/.mastercard-prd.html
git -C /Users/didi/work/linze-journal commit -m "feat(stealth): PRD 主陈述卡五步骨架"
```

---

### Task 6: 组装 —— Python 锚点替换 3 张雏形 body

**Files:**
- Create: `learning/interview-tools/assemble_mastercards.py`
- Modify: `learning/interview-tools/stealth.html`

**Interfaces:**
- Consumes: `.mastercard-{manager,code,prd}.html`(Task 3/4/5)、`.mastercard-anchors.txt`(Task 1)
- Produces: 改写后的 stealth.html(3 张雏形 body 被替换)

- [ ] **Step 1: 写 assemble_mastercards.py**

```python
#!/usr/bin/env python3
"""按 card-title 锚点,把三张主卡 body 替换进 stealth.html(原子写)。"""
import re

ROOT = "/Users/didi/work/linze-journal/learning/interview-tools/"
src = open(ROOT + "stealth.html", encoding="utf-8").read()

# (雏形 card-title 原文, 产物文件)
JOBS = [
    ("这个项目 30 秒怎么说?", ".mastercard-manager.html"),
    ("这个 Code Agent 到底是什么?", ".mastercard-code.html"),
    ("AI工作流完整介绍(面试第一答)", ".mastercard-prd.html"),
]

def replace_body(html, title_anchor, new_body):
    """定位含该 card-title 的 card 块,替换其 card-body。"""
    # card-body 起: <div class="card-body"> ... 到该 card 的闭合
    # 策略: 找到 card-title 锚点所在 card,取其 card-body 段
    tidx = html.find(f'card-title">{title_anchor}')
    assert tidx > 0, f"找不到锚点: {title_anchor}"
    body_start = html.find('<div class="card-body">', tidx)
    assert body_start > 0, f"找不到 card-body 起点: {title_anchor}"
    # card-body 闭合 = 从 body_start 起深度匹配 </div>
    depth, i = 0, body_start
    while i < len(html):
        if html[i:i+4] == "<div": depth += 1
        elif html[i:i+6] == "</div>":
            depth -= 1
            if depth == 0:
                body_end = i + 6
                break
        i += 1
    return html[:body_start] + new_body.rstrip() + html[body_end:]

for title, prod in JOBS:
    new_body = open(ROOT + prod, encoding="utf-8").read()
    assert '<div class="card-body">' in new_body, f"{prod} 不是合法 body 片段"
    src = replace_body(src, title, new_body)

tmp = ROOT + "stealth.html.tmp"
open(tmp, "w", encoding="utf-8").write(src)
import os; os.replace(tmp, ROOT + "stealth.html")
print("✅ 已替换 3 张主卡 body")
```

- [ ] **Step 2: 跑组装**

```bash
cd learning/interview-tools
python3 assemble_mastercards.py
```
Expected: `✅ 已替换 3 张主卡 body`。若 assert 报错(找不到锚点/body),停下排查锚点字符串是否与文件完全一致。

- [ ] **Step 3: 验证 core/title/data-g 未变 + 卡数不变**

```bash
cd learning/interview-tools
echo "proj 卡数(应仍 104):"
grep -oE 'data-c="proj"' stealth.html | wc -l
echo "三张雏形标题仍在:"
for t in "这个项目 30 秒怎么说" "这个 Code Agent 到底是什么" "AI工作流完整介绍"; do
  grep -c "card-title\">$t" stealth.html
done
echo "三张 core 仍在(各打印 core):"
grep -A1 'card-title">这个项目 30 秒怎么说' stealth.html | grep core || true
```
Expected: proj 卡数 104;三标题各 1;core 行仍在(未被改)。若卡数 ≠104 或标题丢失,`git checkout stealth.html` 回退重查。

- [ ] **Step 4: 浏览器肉眼验收**

`open learning/interview-tools/stealth.html`,项目 tab → 三张主卡,展开看五段渲染正常、core 高亮在、无破版。

- [ ] **Step 5: Commit**

```bash
git -C /Users/didi/work/linze-journal add learning/interview-tools/stealth.html learning/interview-tools/assemble_mastercards.py
git -C /Users/didi/work/linze-journal commit -m "feat(stealth): 组装三张主陈述卡body进速查页"
```

---

### Task 7: 全局校验 + 雷区抽检 + bump sw.js + push

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
echo "=== <script> 完整(应偶数个、末尾有 </script>) ==="
grep -c '<script' stealth.html; grep -c '</script>' stealth.html
echo "=== 禁用项残留(应全 0) ==="
grep -cE '说白了|得说句实话|我自己比较得意|\[loop' stealth.html
echo "=== data-g 路由未变(三组各 14/19/40) ==="
grep -oE 'data-g="(Manager 智能体|Code 智能体|PRD 工作流)"' stealth.html | sort | uniq -c
```
Expected: div 开=闭;script 开=闭;禁用项 0;data-g 三组数不变。

- [ ] **Step 2: §1.3 雷区数字抽检(三张主卡)**

```bash
cd learning/interview-tools
echo "=== Manager 雷区(以下应 0 命中) ==="
grep -cE 'Claude|GPT-4|GPT-5' stealth.html   # Manager 模型是 qwen-flash,主卡不该出现 Claude/GPT
echo "=== Code 雷区 ==="
grep -c 'Chroma' stealth.html                 # 应 0
echo "=== PRD 雷区(6步闭环要么不提要么带'不存在/原型') ==="
grep -oE 'prd2code-gen[^。，]{0,20}' stealth.html | head
```
逐项确认: 不穿帮。若命中,回到对应 Task 的 agent 重产出。

- [ ] **Step 3: 看 origin 当前 CACHE_NAME 并 bump**

```bash
cd /Users/didi/work/linze-journal
git fetch origin main 2>/dev/null
echo "=== origin 上的 CACHE_NAME ==="
git show origin/main:sw.js | grep CACHE_NAME || echo "(origin 无 sw.js,看本地)"
echo "=== 本地当前 ==="
grep CACHE_NAME sw.js
```
把 `sw.js` 里 `CACHE_NAME` 的 `kb-vN` 改成 `origin 已部署版本 + 1`(GUIDE §4.7:看 origin 不是本地最新 commit)。

- [ ] **Step 4: Commit + push(个人账号)**

```bash
cd /Users/didi/work/linze-journal
git add sw.js
git commit -m "chore(stealth): bump CACHE_NAME kb-vN→vN+1(三张主陈述卡重构)"
git push origin main
```

- [ ] **Step 5: 硬刷新验证**

`open` stealth.html 后硬刷新(Cmd+Shift+R),确认 Service Worker 接管新版、三张主卡显示新 body。

- [ ] **Step 6: 清理临时产物(可选)**

```bash
cd learning/interview-tools
rm -f .mastercard-manager.html .mastercard-code.html .mastercard-prd.html \
      .mastercard-anchors.txt .mastercard-prompt-template.md \
      stealth-source-current.html check_mastercard.py assemble_mastercards.py
git add -A && git commit -m "chore(stealth): 清理主卡重构临时产物" || echo "无变更"
git push origin main
```
(保留 `stealth-source-current.html` 也行,作回退源料;按需。)

---

## 自审(对照 spec)

- **Spec 覆盖**: spec §3 双层 → 全计划基调;§4 雷区 → Task 2 脚本+Task 7 抽检;§5 五步模板+硬约束 → Task 2 prompt 模板;§6 三件套骨架 → Task 3/4/5;§7 多 agent 流程 → Task 1-7;§8 质量门 → Task 2 脚本+Task 7 grep+Task 3/4/5 人工抽看。✅ 全覆盖。
- **Placeholder**: agent prompt 模板为实文;三个 agent task 的项目特定部分给了实际说明书路径/雏形标题/spec §6.X 要点。无 TBD。✅
- **一致性**: 三个产物文件名 `.mastercard-{manager,code,prd}.html` 在 Task 3/4/5 产出、Task 6 消费,命名一致;锚点字符串三处一致。✅
