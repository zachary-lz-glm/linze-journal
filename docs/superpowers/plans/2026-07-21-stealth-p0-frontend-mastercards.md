# stealth P0 老前端项目卡五步重构 · 实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: 用 superpowers:subagent-driven-development(推荐)或 superpowers:executing-plans 逐 task 执行。步骤用 `- [ ]` 跟踪。

**Goal:** 把 stealth.html proj 的 5 张老前端项目卡(STAR/架构决策/推广/前端扎实/事故反思)card-body 改写成五步骨架(业务+ownership/本质矛盾/决策+alternatives/结果+eval/方法论+局限),卡1 改标题「最有价值的项目:Schema 营销中台」+ data-kw 同步,5 张加 `data-g="前端项目"` 聚拢、subOrder 补值;10 张保留卡和 A4/A10/A5-prd 原位不动。

**Architecture:** 双层(主陈述+弹药)。3 个 agent 各产 card-body 片段到独立文件(Agent-Schema 管 卡1+2 / 权益前端 管 卡3+4 / 事故 管 卡5)→ Python 锚点脚本 splice 5 张 body 进 stealth.html + 卡1 改标题/data-kw + 5 张加 data-g + subOrder 补 '前端项目':1.4 → grep + §4 校准抽检校验 → bump sw.js + 个人账号 push。

**Tech Stack:** HTML(stealth.html 单页,无构建工具)、Python 3(组装/校验脚本)、grep/bash(验收)。

## Global Constraints

- **数字按 spec §4 档位**:
  - ✅可说:20+ 活动类型、24 基础组件、30-40 定制组件、400+(组合数)、上线两周→三天、15 分钟回滚
  - ⚠️软化:8国→「七八个」、月均20起→「一二十起」并主动说「无严格统计口径」、35组件→「三十多个」、16模板→「十几个」、95%→「绝大多数」、18个月→「一年半」、月均10bug→「十来个」、接入2周→3天→软化、构建5分钟→30秒→软化
  - ❌绝不编百分比/倍数/统计口径
- **A5 拆分边界**:Schema 引擎「月均十来个 bug→归零」并入卡1④;prd-tools 弯路→突破**留原位**(line 533),不进老前端卡。**5 张老前端卡不该出现** `5h→2h` / `prd-tools` / `prd2code` / `6 步闭环` / `Claude` / `GPT`(那些是 PRD/agent 项目的)
- **§6 declarative 风格**;禁口语碎嘴:说白了 / 得说句实话 / 我自己比较得意 / 被问X我答 / 这套东西 / 你就懂了 / 听着像
- **主卡开场不堆技术栈**(impact not technology names):技术名词只在必要处带过,不展开罗列
- **标题/core/data-kw**:卡1 改(标题 `最有价值项目（STAR逐字稿）` → `最有价值的项目：Schema 营销中台`,data-kw 补问法);其余 4 张 core/标题保留
- **5 张加 `data-g="前端项目"`**;subOrder 加 `'前端项目':1.4`(proj 最前,主力优先)
- **10 张保留卡 body 不动**(A1/A2/A3/A7/A8/BFF挂了/线上事故短/Hybrid/核心竞争力/Schema适用场景);**A4/A10/A5 原位不动**
- **改完 bump `sw.js` 的 `CACHE_NAME`**(看 origin 已部署版本 +1,见 GUIDE §4.7)
- 用**个人 GitHub 账号**推送(非公司账号);push 前 `git remote -v` 确认 origin 指向个人
- stealth.html 单页大文件,组装用 **Python 锚点替换 + 原子写**,不用多次 Edit
- agent 产**独立文件**,主会话统一组装,避免并发改同一文件(GUIDE §4.6)
- **每 agent prompt 写死「只产指定卡的 card-body 片段到独立文件,禁碰 stealth.html、禁碰其他卡」**(memory [[agent-scope-constraint]])

## File Structure

| 文件 | 责任 | 动作 |
|------|------|------|
| `learning/interview-tools/stealth.html` | 速查页主体 | 改:5 张 card-body + 卡1 标题/data-kw + 5 张 data-g + subOrder |
| `learning/interview-tools/stealth-source-current.html` | 重写前源料备份 | 建 |
| `learning/interview-tools/check_mastercard.py` | 校验 agent 产物(五段/禁用项/div 平衡/雷区) | 建(上轮已删,重建) |
| `learning/interview-tools/assemble_p0.py` | 锚点 splice 5 张 body + data-g + 标题 + subOrder | 建 |
| `learning/interview-tools/.p0-prompt-template.md` | 三 agent 共用 prompt 公共部分 | 建 |
| `learning/interview-tools/.p0-card{1-5}-*.html` | 5 张 body 产物(临时) | 建,组装后删 |
| `sw.js` | Service Worker 缓存版本 | 改:CACHE_NAME |

---

### Task 1: 备份源 + 验证 5 张卡锚点 + 记录 subOrder

**Files:**
- Create: `learning/interview-tools/stealth-source-current.html`
- Create: `learning/interview-tools/.p0-anchors.txt`

**Interfaces:**
- Produces: `.p0-anchors.txt` 含 5 张卡 card-title 原文 + subOrder 现状,供 Task 6 组装脚本参考

- [ ] **Step 1: 备份 stealth.html**

```bash
cp learning/interview-tools/stealth.html learning/interview-tools/stealth-source-current.html
```

- [ ] **Step 2: 验证 5 张卡 card-title 唯一**

```bash
cd learning/interview-tools
for t in "最有价值项目" "架构决策故事" "跨团队推广故事" "怎么证明前端扎实" "线上事故反思"; do
  n=$(grep -c "card-title\">$t" stealth.html)
  echo "$t => $n 次匹配"
done
```
Expected: 五张各 `1 次匹配`。若某张 ≠1,停下排查(标题被改过或重复)。

- [ ] **Step 3: 确认 5 张卡完整标题(精确标点)+ 当前 tag/data-g 状态**

```bash
cd learning/interview-tools
echo "=== 5 张完整 card-title ==="
for t in "最有价值项目" "架构决策故事" "跨团队推广故事" "怎么证明前端扎实" "线上事故反思"; do
  grep -oE "card-title\">$t[^<]*" stealth.html
done
echo "=== 当前 subOrder proj 行(line 4566) ==="
sed -n '4566p' stealth.html
echo "=== 5 张当前是否已有 data-g(应都无) ==="
for t in "最有价值项目" "架构决策故事" "跨团队推广故事" "怎么证明前端扎实" "线上事故反思"; do
  grep -B1 "card-title\">$t" stealth.html | grep -c "data-g" || echo "0"
done
```
Expected: 5 个完整标题(卡1=`最有价值项目（STAR逐字稿）` 全角括号);subOrder proj 行含 `'Schema 项目':8,'产品思维':7` 等;5 张当前 data-g 计数应 0(都靠正则兜底分组)。

- [ ] **Step 4: 记录锚点到 .p0-anchors.txt**

把 5 个 card-title 原文(每行一个)+ subOrder proj 行原文写入 `.p0-anchors.txt`,供 Task 6 的 assemble 脚本校对。

- [ ] **Step 5: Commit**

```bash
git -C /Users/didi/work/linze-journal add learning/interview-tools/stealth-source-current.html learning/interview-tools/.p0-anchors.txt
git -C /Users/didi/work/linze-journal commit -m "chore(stealth): 备份源+抽取P0老前端5张卡锚点"
```

---

### Task 2: 重建 check_mastercard.py + 公共 agent prompt 模板

**Files:**
- Create: `learning/interview-tools/check_mastercard.py`
- Create: `learning/interview-tools/.p0-prompt-template.md`

**Interfaces:**
- Produces: `check_mastercard.py` —— 输入 body 片段文件路径,跑校验,全过 exit 0 否则 exit 1;`.p0-prompt-template.md` —— 三 agent 共用的 prompt 公共部分(执行时填入 spec §6 对应卡骨架)

- [ ] **Step 1: 写 check_mastercard.py**

```python
#!/usr/bin/env python3
"""校验 P0 老前端主陈述卡 card-body 产物。用法: python3 check_mastercard.py <body.html>"""
import re, sys

f = sys.argv[1]
html = open(f, encoding="utf-8").read()
errs = []

# 1. 五段 <strong> 段首(至少 5 个)
strongs = re.findall(r"<strong>[^<]{2,}</strong>", html)
if len(strongs) < 5:
    errs.append(f"段首 <strong> 只有 {len(strongs)} 个,需 ≥5(五步骨架)")

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

# 6. P0 老前端卡雷区:不该出现 PRD/agent 项目词(A5 拆分别串味)
poison = ["5h→2h", "prd-tools", "prd2code", "6 步闭环", "6步闭环", "Claude", "GPT-4", "GPT-5"]
phit = [w for w in poison if w in html]
if phit:
    errs.append(f"串入 PRD/agent 项目词(老前端卡不该有): {phit}")

# 7. 硬数字未软化(应已按 §4 软化)
hard = ["8个国", "8国", "月均20起", "95%场景", "18个月", "16个联动"]
hhit = [w for w in hard if w in html]
if hhit:
    errs.append(f"硬数字未软化(§4 要求软化): {hhit}")

if errs:
    print("❌ 校验失败:")
    for e in errs: print("  -", e)
    sys.exit(1)
print(f"✅ 校验通过({len(strongs)} 段 <strong>)")
```

- [ ] **Step 2: 用坏样例验证脚本能抓错**

```bash
cd learning/interview-tools
printf '<div class="card-body"><p>说白了用Claude做5h→2h</p><div></div></div>' > /tmp/bad.html
python3 check_mastercard.py /tmp/bad.html; echo "exit=$?"
```
Expected: 打印 ❌(段首<strong>不足 / 口语碎嘴"说白了" / 串入 Claude + 5h→2h / div 不平衡),exit=1。

- [ ] **Step 3: 写公共 agent prompt 模板 `.p0-prompt-template.md`**

```markdown
你是面试速查卡写作 agent。任务:为 stealth.html 重写 {N} 张「老前端项目主陈述/故事卡」的 card-body(只 body,不动 core/title/标签/外层 .card)。

# 必读(按顺序)
1. learning/interview-tools/STEALTH-CARDS-GUIDE.md —— §1(铁律)、§6(技术项目卡风格标尺:declarative、不碎嘴、不堆栈)、§2.2(卡片模板)
2. docs/superpowers/specs/2026-07-21-stealth-p0-frontend-mastercards-design.md —— §5(五步模板+硬约束)、§6(本批卡的五步骨架,见下方「本次负责的卡」)、§4(校准档位表)
3. 现有卡原文: 从 stealth-source-current.html 抽取 card-title="{标题}" 的那张卡,保留 core 和好句,把 card-body 改五步

# 本次负责的卡
{此处由 Task 3/4/5 填入:卡号 + card-title + spec §6 对应小节的五步要点}

# card-body 五段骨架(每段 <strong>段首领起。</strong> 开头)
① 业务问题 + ownership —— 解决什么、不解决会怎样、"我在里面 drive 了什么"(不堆技术栈)
② 本质矛盾 —— 难点本质在哪(非堆功能/非更大模型)
③ 关键决策 + 拒绝了什么 —— 每个高杠杆决策讲"为什么选它 + 考虑并拒绝了什么 alternative"
④ 结果 + 怎么验证 —— 指标 + eval/metrics(非 vibes)+ 可复用价值
⑤ 方法论 + 局限 —— 可迁移命名框架 + 诚实边界(局限/下次怎么做)

# 风格(§6)
declarative 陈述句;禁口语碎嘴(说白了/得说句实话/我自己比较得意/被问X我答/这套东西/你就懂了);
①② 可内联枚举,不堆 ①②③④⑤。

# 数字硬约束(spec §4)
- ✅可说:20+活动类型、24基础组件、30-40定制组件、400+(组合数非组件数)、上线两周→三天、15分钟回滚
- ⚠️软化:八国→「七八个」、月均20起→「一二十起」并说「无严格统计口径」、35→「三十多个」、16→「十几个」、95%→「绝大多数」、18个月→「一年半」、月均10bug→「十来个」、2周→3天软化、5分钟→30秒软化
- ❌绝不编百分比/倍数;绝不出现 5h→2h/prd-tools/prd2code/6步闭环/Claude/GPT(那是 PRD/agent 项目的,老前端卡不该有)

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
git -C /Users/didi/work/linze-journal add learning/interview-tools/check_mastercard.py learning/interview-tools/.p0-prompt-template.md
git -C /Users/didi/work/linze-journal commit -m "chore(stealth): P0校验脚本+公共agent prompt模板"
```

---

### Task 3: Agent-Schema(卡1 STAR + 卡2 架构决策)

> Task 3/4/5 互相独立(不同卡、不同产物文件),**可并行派 3 个 agent**。

**Files:**
- Create: `learning/interview-tools/.p0-card1-star.html`
- Create: `learning/interview-tools/.p0-card2-decision.html`

**Interfaces:**
- Consumes: `.p0-prompt-template.md`(Task 2)、`stealth-source-current.html`(Task 1)
- Produces: `.p0-card1-star.html`、`.p0-card2-decision.html` —— 两张卡的 card-body 片段

- [ ] **Step 1: 派 general-purpose agent**

prompt = `.p0-prompt-template.md` 填入:
- `{N}` = `2`
- 「本次负责的卡」填入(两张):
  - **卡1 · card-title「最有价值项目（STAR逐字稿）」**(输出到 `.p0-card1-star.html`)—— spec §6.1 五步要点:①国际化营销20+活动×七八国多城,if-else上万行,月均一二十起问题(无严格统计口径),新活动前端两周;**我是前端负责人**。②项目层矛盾:配置表达力 vs 可控性,把命令式硬编码联动抽象成声明式可静态校验配置不牺牲表达力。③Schema驱动(拒绝低代码:B端设计稿少/联动描述不了)、双端解析(拒绝单端:SSR初始状态不对)、联动DSL dAction(拒绝命令式if-else:不可静态校验)。④零开发/两周→三天/月均二十→接近零;并入A5拆出的「Schema引擎月均十来个bug→归零」;eval=静态校验+灰度+reason tag监控三层。⑤「声明式配置驱动:人依赖配置非代码」+局限(Schema天花板:拖拽/实时协作仍写代码;只适用配置类页面)。
  - **卡2 · card-title「架构决策故事：为什么选Schema？」」**(输出到 `.p0-card2-decision.html`)—— spec §6.2 五步要点:①存量if-else维护失控(月均二十起),**我是技术决策者**。②决策层矛盾:抽象层级选哪层——硬编码太低失控、低代码太高表达力不够,需介于其间的声明式抽象。③(现有最完整)三选项+排除①②+Schema权衡+代价(学习曲线一周/天花板)。④月均二十→接近零,静态校验可追溯。⑤「架构决策核心是取舍:记录排除什么+代价,不是记录选了什么」+局限(Schema天花板)。
- agent 必读 spec §6.1/§6.2 + §4 校准表 + stealth-source-current.html 两张卡原文。
- **关键约束:卡1②(项目层"配置vs可控")与卡2②(决策层"抽象层级")必须不重叠**——agent 统筹两张时注意分工。
- prompt 末尾写死:"只产出 .p0-card1-star.html 和 .p0-card2-decision.html 两个文件,禁碰 stealth.html,禁碰其他卡,禁碰 .p0-card3/4/5。"

- [ ] **Step 2: 校验两张产物**

```bash
cd learning/interview-tools
python3 check_mastercard.py .p0-card1-star.html; echo "exit=$?"
python3 check_mastercard.py .p0-card2-decision.html; echo "exit=$?"
```
Expected: 两张都 `✅ 校验通过(5 段 <strong>)`,exit=0。若失败,把错误回喂 agent 重产出。

- [ ] **Step 3: 人工风格抽看**

打开两张产物,确认:declarative 不碎嘴、技术栈不堆、卡1②与卡2②不重叠、⑤方法论非空话。

- [ ] **Step 4: Commit**

```bash
git -C /Users/didi/work/linze-journal add learning/interview-tools/.p0-card1-star.html learning/interview-tools/.p0-card2-decision.html
git -C /Users/didi/work/linze-journal commit -m "feat(stealth): P0卡1 Schema主陈述+卡2架构决策 五步骨架"
```

---

### Task 4: Agent-权益前端(卡3 推广 + 卡4 前端扎实)

**Files:**
- Create: `learning/interview-tools/.p0-card3-promote.html`
- Create: `learning/interview-tools/.p0-card4-frontend.html`

**Interfaces:**
- Consumes: `.p0-prompt-template.md`、`stealth-source-current.html`
- Produces: `.p0-card3-promote.html`、`.p0-card4-frontend.html`

- [ ] **Step 1: 派 general-purpose agent**

prompt = 模板填入:
- `{N}` = `2`
- 「本次负责的卡」:
  - **卡3 · card-title「跨团队推广故事：组件库如何从1到8？」」**(输出到 `.p0-card3-promote.html`)—— spec §6.3 要点:①权益SDK最早只服务国际化,其他七八个团队各搞各的重复开发;**我是SDK owner**。②推广阻力不是技术是信任——方案好坏 vs 别人愿不愿用,本质降低他人采纳风险。③推广三步(试点痛点最大业务/沉淀接入文档/试点数据内部分享),拒绝"写README等别人来用";Register注册模式拒绝"通用不够就fork改"。④接入工作量两周→三四天,从1→8团队。⑤「推广=试点数据说服>文档说服;Register让自定义与通用共存防fork」+局限(推广靠试点意愿,非所有团队都主动)。
  - **卡4 · card-title「怎么证明前端扎实？」」**(输出到 `.p0-card4-frontend.html`)—— spec §6.4 要点:①证明前端底子,**我从零设计了Schema渲染引擎**。②难点不是用现成Formily/Ajv(那是调API),是从零设计联动DSL+injectDActions双求值——渲染引擎级架构 vs 调API写页面。③联动DSL+双求值(拒绝现成Formily:描述力不够/黑盒)、虚拟滚动+按需渲染(拒绝全量重渲染:四百+组件卡)、Rollup+tree-shaking(拒绝整包)。④四百+组件配置页流畅(虚拟滚动只渲染视口内)、联动精确更新非全量。⑤「前端扎实的证据是从零设计引擎非用轮子;性能靠精确更新非全量重渲染」+局限(引擎为配置类页面设计,不直接迁移C端自由布局)。
- prompt 末尾写死:"只产出 .p0-card3-promote.html 和 .p0-card4-frontend.html,禁碰 stealth.html 和其他卡。"

- [ ] **Step 2: 校验两张产物**

```bash
cd learning/interview-tools
python3 check_mastercard.py .p0-card3-promote.html; echo "exit=$?"
python3 check_mastercard.py .p0-card4-frontend.html; echo "exit=$?"
```
Expected: 两张 `✅ 校验通过`,exit=0。

- [ ] **Step 3: 人工风格抽看 + Commit**

```bash
git -C /Users/didi/work/linze-journal add learning/interview-tools/.p0-card3-promote.html learning/interview-tools/.p0-card4-frontend.html
git -C /Users/didi/work/linze-journal commit -m "feat(stealth): P0卡3推广+卡4前端扎实 五步骨架"
```

---

### Task 5: Agent-事故(卡5 事故反思)

**Files:**
- Create: `learning/interview-tools/.p0-card5-accident.html`

**Interfaces:**
- Consumes: `.p0-prompt-template.md`、`stealth-source-current.html`
- Produces: `.p0-card5-accident.html`

- [ ] **Step 1: 派 general-purpose agent**

prompt = 模板填入:
- `{N}` = `1`
- 「本次负责的卡」:
  - **卡5 · card-title「线上事故反思 + 基础设施架构判断」」**(输出到 `.p0-card5-accident.html`)—— spec §6.5 要点:①**我经历过yarn.lock事故**(解析器自动升级导致构建全挂,十几分钟回滚),主导复盘。②事故处理本质不是"快速修",是"快速止血+根因(追机制不追责)+流程改进"——救火vs防火;容灾本质是物理距离非机房数(两地同区域=假容灾)。③(现有)事故三部曲+两地部署判断+补偿四项(降级/多级监控/预案演练/客户端容错)。④yarn.lock事故十几分钟回滚;复盘三件事(yarn.lock入git保护/CI lockfile diff/依赖升级staging验证)。⑤事故三部曲=方法论;**局限(诚实)**:我的事故是构建级(构建挂)非用户级(数据丢失/资损)别夸大;容灾判断是理论推演非我亲自架构的生产容灾。
- prompt 末尾写死:"只产出 .p0-card5-accident.html,禁碰 stealth.html 和其他卡。"

- [ ] **Step 2: 校验产物**

```bash
cd learning/interview-tools
python3 check_mastercard.py .p0-card5-accident.html; echo "exit=$?"
```
Expected: `✅ 校验通过`,exit=0。

- [ ] **Step 3: 人工风格抽看 + Commit**

```bash
git -C /Users/didi/work/linze-journal add learning/interview-tools/.p0-card5-accident.html
git -C /Users/didi/work/linze-journal commit -m "feat(stealth): P0卡5事故反思 五步骨架"
```

---

### Task 6: 组装 —— Python 锚点 splice 5 张 body + data-g + 标题 + subOrder

**Files:**
- Create: `learning/interview-tools/assemble_p0.py`
- Modify: `learning/interview-tools/stealth.html`

**Interfaces:**
- Consumes: `.p0-card{1-5}-*.html`(Task 3/4/5)
- Produces: 改写后的 stealth.html(5 张 body 替换 + 卡1 标题/data-kw + 5 张 data-g + subOrder 补值)

- [ ] **Step 1: 写 assemble_p0.py**

```python
#!/usr/bin/env python3
"""P0 老前端 5 张卡:替换 body + 卡1改标题/data-kw + 5张加 data-g + subOrder补值。原子写。
顺序:先替换 body(用原 title 定位)→ 加 data-g → subOrder → 最后改卡1 title(改完不再用 title 定位)。"""
import re, os

ROOT = "/Users/didi/work/linze-journal/learning/interview-tools/"
src = open(ROOT + "stealth.html", encoding="utf-8").read()

TITLES = [
    "最有价值项目（STAR逐字稿）",
    "架构决策故事：为什么选Schema？",
    "跨团队推广故事：组件库如何从1到8？",
    "怎么证明前端扎实？",
    "线上事故反思 + 基础设施架构判断",
]
BODIES = [
    ".p0-card1-star.html",
    ".p0-card2-decision.html",
    ".p0-card3-promote.html",
    ".p0-card4-frontend.html",
    ".p0-card5-accident.html",
]
CARD1_OLD_TITLE = TITLES[0]
CARD1_NEW_TITLE = "最有价值的项目：Schema 营销中台"
CARD1_NEW_KW = "最有价值的项目 最得意的项目 介绍下你的项目 Schema 营销中台 最有成就感 STAR 项目陈述 前端负责人"
DATA_G = "前端项目"

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

def card_open_tag_range(html, title):
    tidx = html.find(f'card-title">{title}')
    assert tidx > 0
    o = html.rfind('<div class="card"', 0, tidx)
    assert o >= 0, f"找不到 card 开标签: {title}"
    e = html.find('>', o)
    assert e > 0
    return o, e + 1

# Step 1: 替换 5 张 body(title 未改,定位安全)
for title, prod in zip(TITLES, BODIES):
    bs, be = card_body_range(src, title)
    nb = open(ROOT + prod, encoding="utf-8").read()
    assert '<div class="card-body">' in nb, f"{prod} 非法 body 片段"
    src = src[:bs] + nb.rstrip() + src[be:]
print("Step1: 5 张 body 替换完成")

# Step 2: 5 张加 data-g="前端项目"(若没有)
for title in TITLES:
    o, e = card_open_tag_range(src, title)
    tag = src[o:e]
    if "data-g=" not in tag:
        newtag = tag.replace('data-c="proj"', f'data-c="proj" data-g="{DATA_G}"', 1)
        assert newtag != tag, f"{title} 加 data-g 失败(找不到 data-c=\"proj\")"
        src = src[:o] + newtag + src[e:]
print("Step2: 5 张加 data-g=前端项目")

# Step 3: subOrder 加 '前端项目':1.4
assert "'前端项目':" not in src, "subOrder 已含 前端项目,检查是否重复运行"
assert src.replace("'Schema 项目':8", "'前端项目':1.4,'Schema 项目':8", 1) != src, "找不到 subOrder 'Schema 项目':8 锚点"
src = src.replace("'Schema 项目':8", "'前端项目':1.4,'Schema 项目':8", 1)
print("Step3: subOrder 加 前端项目:1.4")

# Step 4: 卡1 改 title + data-kw(最后做,之后不再用 title 定位)
o, e = card_open_tag_range(src, CARD1_OLD_TITLE)
tag = src[o:e]
newtag = re.sub(r'data-kw="[^"]*"', f'data-kw="{CARD1_NEW_KW}"', tag, 1)
assert newtag != tag, "卡1 data-kw 替换失败"
src = src[:o] + newtag + src[e:]
old_t = f'card-title">{CARD1_OLD_TITLE}</div>'
assert old_t in src, "卡1 旧标题找不到"
src = src.replace(old_t, f'card-title">{CARD1_NEW_TITLE}</div>', 1)
print("Step4: 卡1 改标题+data-kw")

tmp = ROOT + "stealth.html.tmp"
open(tmp, "w", encoding="utf-8").write(src)
os.replace(tmp, ROOT + "stealth.html")
print("✅ P0 5 张老前端卡组装完成")
```

- [ ] **Step 2: 跑组装**

```bash
cd learning/interview-tools
python3 assemble_p0.py
```
Expected: 打印 Step1-4 + `✅ P0 5 张老前端卡组装完成`。若 assert 报错(找不到锚点),停下排查:对照 `.p0-anchors.txt` 确认标题字符串与文件完全一致(全角括号/标点)。

- [ ] **Step 3: 验证 core/title/data-g/subOrder/卡数**

```bash
cd learning/interview-tools
echo "=== proj 卡数(应仍 101,未增删卡) ==="
grep -oE 'data-c="proj"' stealth.html | wc -l
echo "=== 5 张 data-g=前端项目(应 5) ==="
grep -c 'data-g="前端项目"' stealth.html
echo "=== 卡1 新标题在、旧标题不在 ==="
grep -c 'card-title">最有价值的项目：Schema 营销中台' stealth.html
grep -c 'card-title">最有价值项目（STAR逐字稿）' stealth.html
echo "=== 其余 4 张标题仍在 ==="
for t in "架构决策故事：为什么选Schema" "跨团队推广故事：组件库如何从1到8" "怎么证明前端扎实" "线上事故反思"; do
  grep -c "card-title\">$t" stealth.html
done
echo "=== subOrder 含 前端项目:1.4 ==="
grep -c "'前端项目':1.4" stealth.html
echo "=== A4/A10/A5 原位未动(标题仍在) ==="
grep -c 'card-title">从 PRD 到上线' stealth.html
grep -c 'card-title">AI 工程怎么保证可靠性' stealth.html
grep -c 'card-title">最有技术挑战' stealth.html
```
Expected: proj 卡数 101;data-g=前端项目 5;卡1 新标题 1、旧标题 0;其余 4 标题各 1;subOrder 前端项目:1.4 为 1;A4/A10/A5 标题各 1(未动)。若卡数 ≠101 或标题丢失,`git checkout stealth.html` 回退重查。

- [ ] **Step 4: 浏览器肉眼验收**

`open learning/interview-tools/stealth.html` → 项目 tab → quickbar 应出现「前端项目」子分组,点开看 5 张卡五段渲染正常、core 高亮在、卡1 标题已变、无破版。确认 A4/A10/A5 仍在原分组(AI 总览/Schema 项目)未被误移。

- [ ] **Step 5: Commit**

```bash
git -C /Users/didi/work/linze-journal add learning/interview-tools/stealth.html learning/interview-tools/assemble_p0.py
git -C /Users/didi/work/linze-journal commit -m "feat(stealth): 组装P0老前端5张卡body+data-g=前端项目+卡1改标题"
```

---

### Task 7: 全局校验 + §4 校准抽检 + bump sw.js + push

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
echo "=== 5 张老前端卡未串入 PRD/agent 词(应 0) ==="
grep -cE '5h→2h|prd-tools|prd2code|6 步闭环' stealth.html
```
Expected: div 开=闭;script 开=闭;禁用项 0;PRD/agent 词 0(全文档;若命中说明串味,回 Task 3/4/5 对应 agent 重产出)。

- [ ] **Step 2: §4 校准抽检(5 张老前端卡的数字)**

```bash
cd learning/interview-tools
echo "=== 硬数字不应出现(应 0) ==="
grep -cE '8个国|8国|月均20起|95%场景|18个月|16个联动' stealth.html
echo "=== 软化措辞应在(抽样,应 ≥1) ==="
grep -oE '七八个|一二十起|一年半|十几个联动|绝大多数' stealth.html | sort | uniq -c
```
Expected: 硬数字 0;软化措辞有命中。若硬数字命中,回对应 agent 软化后重组装。

- [ ] **Step 3: 看 origin 当前 CACHE_NAME 并 bump**

```bash
cd /Users/didi/work/linze-journal
git fetch origin main 2>/dev/null
echo "=== origin 上的 CACHE_NAME ==="
git show origin/main:sw.js | grep CACHE_NAME || echo "(origin 无 sw.js,看本地)"
echo "=== 本地当前 ==="
grep CACHE_NAME sw.js
```
把 `sw.js` 里 `CACHE_NAME` 的 `kb-vN` 改成 `origin 已部署版本 + 1`(GUIDE §4.7:看 origin 不是本地最新 commit。上一个已部署版本是 kb-v323,本次应为 kb-v324,但以 origin 实际为准 +1)。

- [ ] **Step 4: 确认 remote 是个人账号 + Commit + push**

```bash
cd /Users/didi/work/linze-journal
echo "=== 确认 origin 指向个人账号(zachary-lz-glm) ==="
git remote -v
git add sw.js
git commit -m "chore(stealth): bump CACHE_NAME kb-vN→vN+1(P0老前端5张卡五步重构)"
git push origin main
```
若 `git remote -v` 显示 origin 不是个人账号(是公司账号),停下确认正确的个人 remote 名(如 `github-personal`)再用 `git push <个人remote> main`。**绝不推公司账号**(memory [[github-account]])。

- [ ] **Step 5: 硬刷新验证**

`open learning/interview-tools/stealth.html` 后硬刷新(Cmd+Shift+R),确认 Service Worker 接管新版、项目 tab 出现「前端项目」分组、5 张卡显示新 body、卡1 新标题。

- [ ] **Step 6: 清理临时产物(可选)**

```bash
cd learning/interview-tools
rm -f .p0-card1-star.html .p0-card2-decision.html .p0-card3-promote.html \
      .p0-card4-frontend.html .p0-card5-accident.html \
      .p0-anchors.txt .p0-prompt-template.md stealth-source-current.html
git add -A && git commit -m "chore(stealth): 清理P0重构临时产物" || echo "无变更"
git push origin main
```
**保留** `check_mastercard.py` 和 `assemble_p0.py`(后续 B/C/D 子项目可复用思路,不删)。

---

## 自审(对照 spec)

- **Spec 覆盖**: spec §2 范围(5张套五步+10保留+A4/A10/A5不动)→ Task 1-7 全程基调 + Task 6 Step3 验证;§3.3 data-g=前端项目+subOrder → Task 6 Step1脚本+Step3验证;§3.4 卡1改标题/data-kw → Task 6 Step1脚本+Step3验证;§3.5 卡1/卡2②分工 → Task 3 prompt 注明;§4 校准档位 → Task 2 脚本检查+Task 7 Step2 抽检;§5 五步模板+硬约束 → Task 2 prompt 模板;§6 五张卡骨架 → Task 3/4/5;§7 多 agent 流程 → Task 1-7;§8 质量门 → Task 2 脚本+Task 7 grep+Task 3/4/5 人工抽看。✅ 全覆盖。
- **Placeholder**: Task 2 prompt 模板为实文;Task 3/4/5 的卡骨架给了 spec §6 实际要点(业务问题/矛盾/决策/结果/方法论逐条);Task 6 assemble 脚本为完整可跑代码;subOrder 值 1.4 已写实。无 TBD。✅
- **类型/命名一致**: 5 个产物文件名 `.p0-card{1-5}-*.html` 在 Task 3/4/5 产出、Task 6 BODIES 列表消费,命名一致;5 个 card-title 锚点在 Task 1 验证、Task 6 TITLES 列表、Task 7 grep 一致(全角括号/标点);subOrder '前端项目':1.4 在 Task 6 脚本和 Task 7 验证一致。✅
- **A5 拆分边界**: spec §2.1 要求 A5 的 Schema 部分(月均十来个bug→归零)并入卡1④、prd-tools 部分留原位 → Task 3 卡1骨架注明"并入A5拆出的Schema引擎bug→归零";Task 2 脚本+Task 7 grep 防止 prd-tools/5h→2h 串入老前端卡。✅
