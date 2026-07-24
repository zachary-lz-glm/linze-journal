# stealth PRD 工作流模块重构 · Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: 用 superpowers:subagent-driven-development(推荐)或 superpowers:executing-plans 逐 task 执行。步骤用 `- [ ]` 跟踪。**Task 5–13(9 个模块产出)互相独立(不同 fragment 文件),可并行派 agent**;Task 3/4 也可并行(一个联网拉方法论、一个读源码);Task 1/2 先行(产出后续 task 共用的锚点/脚本/模板)。

**Goal:** 把 stealth.html `data-g="PRD 工作流"` 的 42 张散卡(含 proj 根的 A10 端到端主卡)重组成**入口总览 + 8 主题模块**共 9 簇、≈55 张,每模块 = 1 张 Form A 深挖主卡 + 精修弹药(去重合并)+ 1 张追问库卡;源码核对 + 外部方法论预判追问;routing/subOrder 零改动,组内 DOM 序重排。

**Architecture:** 单组+主题分区。9 个模块 agent 各产**独立 fragment 文件**(主卡/补缺/追问库/重写卡),现有弹药由 assemble 脚本**按 title 原样抽取**(不重写防漂移);`assemble_prd.py` = 抽取全部 PRD 卡 + A10 → 删旧 → 按 LAYOUT 表重排成连续块插入 AI 模块锚点前(首卡加 `.card.master`);`check_prd.py` 校验三类卡型(master Form A / followup points / gap 基础)+ PRD 雷区。bump sw.js kb-v335→kb-v336(看 origin +1)。

**Tech Stack:** HTML(stealth.html 单页,无构建)、Python 3(组装/校验)、grep/bash(验收)、WebFetch(拉外部方法论)。

## Global Constraints

(全部 verbatim 自 spec `2026-07-24-stealth-prd-module-reorg-design.md`,每个 task 隐式包含)

- **结构 = 单组+主题分区**:`PRD 工作流` 一个 quickbar 按钮不变,subOrder 1.7 / getGroup / quickbar 按钮数**全不动**;组内按 9 簇 DOM 序重排(显示 = 组内 DOM 序)。
- **模块主卡 = Form A 四要素**:4-5 段,每段 `<strong>领起标签。</strong>` 开头(≥4 段),必含 ①数据结构/形态 ②算法/流程 ③为何自研、拒绝什么 alternative+代价 ④踩坑+诚实边界(第④不可省)。首卡由 assemble 加 `class="card master"`(agent 写普通 `class="card"`)。
- **追问库卡**:`<ul class="points">` 列 ≥6 条「预判追问 + 一句话答案」,tag=`追问`,挂簇尾。答案对照源码,不照搬通用答案。
- **§6 declarative 风格**;禁口语碎嘴:说白了/得说句实话/我自己比较得意/被问X我答/这套东西/你就懂了/听着像。①② 只内联枚举,不堆①②③④⑤。
- **PRD 雷区**:`6 步闭环`/`6步闭环` 硬 err(不存在);`SDD 平台`/`20+人`/`直接生成代码` warn(只在"不用/拒绝/对比"否定语境可出现,人工确认);prd-tools 是 Claude Code 插件非 SDD 平台、不直接生成代码;团队规模软化 ADR-0005 "约 1–5 人";"端到端"必带"个人原型探索、非生产级闭环";"5h→2h"是前后工时非严格 AB。
- **源码核对**:新主卡/补缺/追问库答案派 agent 读 `/Users/didi/work/prd-to-code` + `/Users/didi/work/prd2code-gen` + `/Users/didi/work/prd-tools` 产 ✅⚠️❌清单再写;核对不到的数字软化或省略,绝不编。
- **新卡 title**:面试官口吻问题、无英文项目名前缀、无文件路径(代码引用只进 body)。
- **routing 零改动**:所有新/重写卡 `data-c="proj"` + `data-g="PRD 工作流"`;现有弹药 assemble 原样抽取(data-g 已是 PRD 工作流,不动)。
- **改完 bump `sw.js` 的 `CACHE_NAME`** kb-v335 → **kb-v336**(执行时先 `git show origin/main:sw.js | grep CACHE_NAME` 确认基线 +1;GUIDE §4.7 撞号教训)。
- 用**个人 GitHub 账号**推送(push 前 `git remote -v` 确认指向 `zachary-lz-glm`,**绝不推公司账号**)。
- stealth.html 单页大文件,组装用 **Python 锚点 + 原子写**,不用多次 Edit;agent 产独立 fragment,主会话统一组装(并发改同文件防护,GUIDE §4.6)。
- **每 agent prompt 写死「只产出指定 fragment 文件,禁碰 stealth.html、禁碰其他卡、禁碰 GUIDE/README/配置、禁改源码项目(只读)」**(memory [[agent-scope-constraint]])。

## ⚠️ 源码核对修正(2026-07-24 · Task 4 产出 · 覆盖映射表冲突)

源码核对 `learning/interview-tools/.prd-facts.md` 发现以下口径与映射表/简历/现有卡冲突,**写卡一律以 .prd-facts.md 为准**:

1. **MCP 不是"踩坑放弃",是从未实现**(ADR-0009 列未来路线 Phase 5)。③主卡「为何自研」写:选 Skill(纯 Markdown)形态而非 MCP Server,因 MCP 过早实现维护成本高、分散 MVP 重点。**禁写"踩过 MCP 的坑/两周发现不行"**。(A5 卡 line546 有此叙事但出本 reorg 范围,已标记给用户。)
2. **"60% 准确率"❌** = readiness warning 阈值,非准确率。②的 `2309` → **重写** `.prd-m2-loss.html`:损耗在 PRD 长尾细节(数值/枚举/边界)向 IR 转译;靠 source_blocks+evidence+coverage gate 防漏,别报百分比。
3. **"map-reduce"❌** 源码未用(2293 core 有此词)。②的 `2293` → **重写** `.prd-m2-context.html`:图片分批并行(≤8张)+ 代码扫描三阶段(Reference 路由→补充扫描→汇总)+ context-pack ≤800 行。
4. **auto-tune 无 llm-judge**❌ 评分是 deterministic 5 维规则(scorer.ts)。⑤的 `2534` → **重写** `.prd-m5-eval.html`:auto-tune = registry(用例注册)+ scorer(5维确定性)+ gap-analyzer + pattern-detector + loop-controller + bmad-optimizer(对抗评审)。**禁"LLM-as-Judge"**。
5. **"Tool 识别率"❌** 源码无此指标(2609 premise)。⑦的 `2609` → **重写** `.prd-m7-stability.html`:prd-tools 纯 Skill 无 function-calling 识别率问题;输出稳定靠确定性优先(模板0token)+4类校验+3次差异重试+A→B→A 震荡检测。
6. **"6 yaml"⚠️ 不严谨**:①主卡用"5 数据 yaml(01-codebase/02-coding-rules/03-contracts/04-routing-playbooks/05-domain)+ project-profile + 00-portal 导航;index 4 文件(entities/edges/inverted-index/manifest)"。自研索引 = "正则扫描的实体+倒排索引辅助层"(非知识图谱/AST/向量)。
7. **R01/R02 不是"稳定提升14分"⚠️**:班次签到 case +14(54→68);油站清理数据泄露后真实 +9(38→47),泄露虚高 +35;benchmark oracle gasstation 单 case 97。⑤ m5-5h2h 按此诚实写。
8. **"7层幻觉防御"❌**(ADR-0011 废弃未落地)。`2671` 说"四层"(证据链/negative search/Spec Review/Readiness,均真实机制)✅ 保留;主卡/追问**勿提"7层"**,用"多层"列真实机制。

**assemble LAYOUT 已同步**:②`keep 2-3万字`→`frag .prd-m2-context`、`keep 团队模式准确率60`→`frag .prd-m2-loss`;⑤`keep AI工作流怎么优化`→`frag .prd-m5-eval`;⑦`keep Tool多了识别率`→`frag .prd-m7-stability`。Fragment 22→26(②+2/⑤+1/⑦+1 重写),keep-verbatim 32→28;最终 PRD-g 仍 55。

---

## File Structure

| 文件 | 责任 | 动作 |
|------|------|------|
| `learning/interview-tools/stealth.html` | 速查页主体 | 改:删 42 张旧 PRD 卡 + A10 旧位 → 插 9 簇重排块 |
| `learning/interview-tools/stealth-source-current.html` | 改前源料(agent 读现有卡原文) | 建 |
| `learning/interview-tools/check_prd.py` | 校验三类卡型 + PRD 雷区 | 建 |
| `learning/interview-tools/assemble_prd.py` | 抽取+删旧+按 LAYOUT 重排+插 A10+加 master 类 | 建 |
| `learning/interview-tools/.prd-prompt-template.md` | 模块 agent 共用 prompt 公共部分 | 建 |
| `learning/interview-tools/.prd-anchors.txt` | 全部 PRD 卡 + A10 完整 title + proj/PRD 卡数基线 | 建 |
| `learning/interview-tools/.prd-facts.md` | 源码核对的事实+✅⚠️❌清单(全模块共享) | 建 |
| `learning/interview-tools/.prd-followup-sources.md` | 5 个外部方法论蒸馏的 per-module 追问种子 | 建 |
| `learning/interview-tools/.prd-m*.html` | 22 个 fragment 产物(主卡/补缺/追问库/重写卡) | 建,组装后清理 |
| `learning/interview-tools/stealth.html` 的 `<style>` | 加 `.card.master` 规则 | 改 |
| `sw.js` | SW 缓存版本 | 改:kb-v335→kb-v336 |

---

## 模块映射总表(驱动 Task 5–13 + assemble LAYOUT)

> 「主卡四要素」= 该模块新主卡 Fragment A 要写的 4 段要点。「新 frag」= 该模块要产的 fragment 文件。「原样留」= assemble 按 title 抽取、不重写。「并入/删」= 合并消失的旧卡。

| 模块 | data-g tag | 主卡四要素(新 `.prd-mN-master.html`) | 新 frag(除主卡) | 原样留(title 子串) | 并入/删 |
|---|---|---|---|---|---|
| **入口·总览** | 总览 | (重写 `.prd-entry.html`)吸收 2456,5 段保留,补 8 模块主卡 cross-ref | — | `prd-tools 4个王牌素材`(2696) | 删 `AI工作流完整介绍`(2456) |
| **① reference** | ◆ reference | ①6 yaml 各存什么+自研实体/倒排索引 schema ②/reference 6 Phase 顺序产出+后生成查先生成去重、按需路由非全量塞 ③自研索引(受 GraphRAG 启发,非 Neo4j 非 AST;拒绝全量塞 context 打爆;拒绝纯向量做精确路由) ④Pull-based 禁主动搜源码→60%损耗;eval 债没建 labeled recall@K;冷启动需人工引导 | `.prd-m1-coldstart.html`(冷启动)、`.prd-m1-followup.html` | `AI知识库的本质定位`(2583)、`/reference 蒸馏出来的 6 个文件`(2467)、`reference 知识过时`(2277) | 删 `AI 怎么理解陌生项目`(2223,并入主卡) |
| **② PRD 蒸馏** | ◆ 蒸馏 | ①11 步流水线每步产出可追溯 ②能力面适配器→摄入→证据账本→AR标注→reference 路由→源码精读→契约差异→Spec(硬停人确认)→Plan→AI 五项自评→门禁脚本 ③硬停人确认=质量责任;每步产出是下步输入,链条断可定位;拒绝一次性出 plan ④2-3万字打爆 context→chunking+map-reduce;变更分类最难(不知现状无法判新增/改/删);60%损耗在 Pull-based | `.prd-m2-followup.html` | `PRD 到代码最难的一步`(2232)、`2-3万字 PRD`(2293)、`团队模式准确率 60%`(2309)、`PRD摄入：多格式`(2444)、`Spec和Plan长什么样`(2480) | — |
| **③ 架构** | ◆ 架构 | ①双插件(Reference 建库 + PRD 蒸馏,上下文隔离)+ 能力面适配器 ②适配器把 PRD 需求点映射到代码能力面;按需加载 ③拆双插件=上下文隔离/Context Engineering;放弃 MCP(A5 弯路:单次调用瓶颈,需求分析需多轮) ④双插件增协调成本;适配器对新项目需配置 | `.prd-m3-followup.html` | `双插件体系`(2408)、`能力面适配器`(2386)、`传统工程思维`(2622) | — (BMAD 2396 移到 ④) |
| **④ 对比** | ◆ 对比 | ①定位差异化(已有项目几万行 vs Cursor/Windsurf 从 0 到 1) ②证据层/可追溯(每条结论挂源码 vs CC init 无证据链) ③不做成 IDE 插件=轻量 CC 插件复用 CC 能力、团队级可推广 ④Cursor 交互强;Devin autonomous 不可控;prd-tools 聚焦计划不生成代码 | `.prd-m4-followup.html` | `和 Claude Code init`(2344)、`有Claude Code了`(2643)、`BMAD架构`(2396) | — (3087 移到 ⑥) |
| **⑤ SSOT/证据链/门禁/评估** | ◆ 质量 | ①SSOT(每条事实只存一处,别处 ID 引用) ②证据链 8 类+置信度+negative_code_search 负向证据;门禁 Readiness 五维加权 85/60 降级 + Spec Review Gate 硬停 ③多处冗余=AI 编造空间;不可追溯结论错误成本高;一次性出 plan 不可控 ④eval 债没 labeled query set 测 recall@K/nDCG;5h→2h 前后工时非严格 AB;R01/R02 54→68 量化 reference 价值 | `.prd-m5-5h2h.html`(合并 2326+3010)、`.prd-m5-gate.html`(重写 2420 吸收 2810)、`.prd-m5-followup.html` | `SSOT 五条边界规则`(2264)、`证据链机制详解`(2787)、`Readiness Score`(2432)、`AI工作流怎么优化`(2534) | 删 `2326`+`3010`(并入 m5-5h2h)、删 `2810`(并入 m5-gate) |
| **⑥ 端到端** | ◆ 端到端 | (无新主卡)A10 搬入作主卡 | `.prd-m6-followup.html` | **A10**`从 PRD 到上线的完整链路`(579,搬入+加 data-g)、`端到端原型：自验证`(2491)、`端到端原型：模板/LLM`(2504)、`端到端原型 → 生产`(2518)、`Harness 三种引擎`(3101)、`SDD 完整流程`(3087) | — |
| **⑦ 实现深坑** | ◆ 实现 | ①踩坑清单(MCP 不行/识别率下降/幻觉/上下文漏文件/工错流) ②转向 Agent+Skill;动态激活工具降识别率;四层防线防幻觉;三轮检索不漏;产物侧拦截 ③每坑根因+拒绝的 alternative ④研究型没接真实流量;小范围验证 | `.prd-m7-skilltools.html`(合并 2550+2562+2595)、`.prd-m7-errorleak.html`(工错流)、`.prd-m7-followup.html` | `Tool多了识别率`(2609)、`幻觉怎么答`(2671)、`代码上下文怎么定位`(2775)、`AI工作流出错了怎么归因`(2852)、`PRD过时或临时改动`(2821) | 删 `2550`+`2562`+`2595`(并入 m7-skilltools) |
| **⑧ 推广落地** | ◆ 推广 | ①怎么推(小范围试点→ROI 量化→赋能不替代) ②阻力(质量责任划分/各人工具偏好/信任/学习成本) ③解法(停 PRD→Plan 低风险环节先推;人工确认才开发;王牌 case 示范) ④诚实:1-5 人小范围 ADR-0005;没全员铺开;渐进推广 | `.prd-m8-resistance.html`(推广阻力)、`.prd-m8-followup.html` | `AI工作流推广ROI`(2899)、`PRD质量卡口`(2715)、`AI工作流在团队怎么落地`(2799) | — |

**Fragment 清单(22 个)**:entry ×1 · m1(master/coldstart/followup) · m2(followup) · m3(followup) · m4(followup) · m5(5h2h/gate/followup) · m6(followup) · m7(skilltools/errorleak/followup) · m8(resistance/followup)。
**原样留(32)**:见各模块行。**删(8)**:2456/2223/2326/3010/2810/2550/2562/2595。**A10 搬入(+1)**。**新主卡 7**(①②③④⑤⑦⑧,⑥ 用 A10)+**追问库 8**+**补缺 3**(冷启动/工错流/推广阻力)+**重写 2**(entry/2420→m5-gate)= 55 张。

---

### Task 1: 备份源 + 抽取全部 PRD 卡/A10 锚点 + 记录基线

**Files:**
- Create: `learning/interview-tools/stealth-source-current.html`
- Create: `learning/interview-tools/.prd-anchors.txt`

**Interfaces:**
- Produces: `.prd-anchors.txt` 含 42 张 PRD 卡 + A10 完整 card-title + proj/PRD 卡数基线,供 Task 14 assemble 抽取/校验

- [ ] **Step 1: 备份 stealth.html**

```bash
cp learning/interview-tools/stealth.html learning/interview-tools/stealth-source-current.html
```

- [ ] **Step 2: 抽取全部 PRD 卡 + A10 完整 title + 验证唯一**

```bash
cd /Users/didi/work/linze-journal/learning/interview-tools
python3 - <<'PY'
import re
src=open('stealth.html',encoding='utf-8').read().splitlines()
out=[]
for i,l in enumerate(src,1):
    if 'data-g="PRD 工作流"' in l or '从 PRD 到上线的完整链路' in l:
        tag=title=''
        for j in range(i,min(i+5,len(src))):
            m=re.search(r'class="tag[^"]*">([^<]*)<',src[j-1]);  tag=tag or (m.group(1).strip() if m else '')
            m=re.search(r'card-title">([^<]*)<',src[j-1]); title=title or (m.group(1).strip() if m else '')
        out.append((i,tag,title))
# 唯一性
from collections import Counter
c=Counter(t for _,_,t in out)
dups=[t for t,n in c.items() if n>1]
print(f"PRD+A10 卡数: {len(out)}; 重复 title: {dups}")
for i,tag,title in out: print(f"{i:5d} [{tag:6s}] {title}")
PY
```
Expected: `PRD+A10 卡数: 43; 重复 title: []`。43 张 = 42 PRD-g + A10。无重复 title。若有重复,停下排查(子串歧义)。

- [ ] **Step 3: 记录基线**

```bash
cd /Users/didi/work/linze-journal/learning/interview-tools
echo "proj 卡数基线: $(grep -oE 'data-c="proj"' stealth.html | wc -l | tr -d ' ')"
echo "PRD-g 卡数基线: $(grep -oE 'data-g=\"PRD 工作流\"' stealth.html | wc -l | tr -d ' ')"
echo "A10 当前 data-g(应为空=proj 根): $(grep -B2 '从 PRD 到上线的完整链路' stealth.html | grep -oE 'data-g=\"[^\"]*\"' | head -1 || echo '(无 data-g,在 proj 根)')"
```
Expected: proj 卡数基线记下(Task 15 应 = 基线 −8 删 +20 新 +0[A10 已在 proj]= 基线+12);PRD-g 基线 = 42(Task 15 应 = 42 −8 +20 +1[A10 加 data-g]= 55);A10 当前无 data-g。

- [ ] **Step 4: 写 .prd-anchors.txt**

把 Step 2 输出(43 张完整 title)+ Step 3 基线写入 `.prd-anchors.txt`。

- [ ] **Step 5: Commit**

```bash
git -C /Users/didi/work/linze-journal add learning/interview-tools/stealth-source-current.html learning/interview-tools/.prd-anchors.txt
git -C /Users/didi/work/linze-journal commit -m "chore(stealth): 备份源+抽取PRD模块43卡锚点+卡数基线"
```

---

### Task 2: 建 check_prd.py + 公共 agent prompt 模板

**Files:**
- Create: `learning/interview-tools/check_prd.py`
- Create: `learning/interview-tools/.prd-prompt-template.md`

**Interfaces:**
- Produces: `check_prd.py <frag> --type master|followup|gap`(过 exit 0 否则 exit 1);`.prd-prompt-template.md`(9 agent 共用 prompt,填模块行即用)

- [ ] **Step 1: 写 check_prd.py**

```python
#!/usr/bin/env python3
"""校验 PRD 模块重构产物。用法:
python3 check_prd.py <frag.html> --type master|followup|gap
  master  = 模块主卡/重写卡(Form A 四要素 + <strong>段 ≥4)
  followup= 追问库卡(<ul class="points"> + <li> ≥6)
  gap     = 补缺弹药卡(基础结构)
公共硬约束: 禁口语碎嘴 / 无①②③④⑤堆叠 / div 平衡 / 完整card / 无'6步闭环'(err)
PRD 雷区 warn: SDD平台 / 20+人 / 直接生成代码(否定语境 OK,人工确认)"""
import re, sys, argparse

p = argparse.ArgumentParser()
p.add_argument("new")
p.add_argument("--type", required=True, choices=["master", "followup", "gap"])
a = p.parse_args()
html = open(a.new, encoding="utf-8").read()
errs, warns = [], []

# 公共: 完整 card
if not html.lstrip().startswith('<div class="card"'):
    errs.append("片段非完整 card(应以 <div class=\"card\" 开头)")
# 公共: div 平衡
if html.count("<div") != html.count("</div>"):
    errs.append(f"div 不平衡: <div {html.count('<div')} / </div> {html.count('</div>')}")
# 公共: 禁口语碎嘴
banned = ["说白了", "得说句实话", "我自己比较得意", "这套东西", "你就懂了", "听着像"]
hit = [w for w in banned if w in html]
if hit: errs.append(f"命中口语碎嘴: {hit}")
# 公共: ①②③④⑤ 堆叠
if re.search(r"[①②③④⑤][①②③④⑤][①②③④⑤][①②③④⑤]", html):
    errs.append("①②③④⑤ 堆叠(≥4 连续),速查表腔")
# 公共: 硬雷区 '6 步闭环'
if "6 步闭环" in html or "6步闭环" in html:
    errs.append("含'6 步闭环'(不存在,雷区)")
# 公共: data-g 必须是 PRD 工作流
if 'data-g="PRD 工作流"' not in html:
    errs.append("缺 data-g=\"PRD 工作流\"")

# type 专属
strongs = re.findall(r"<strong>[^<]{2,}</strong>", html)
if a.type == "master":
    DATA = ["数据结构","结构","字段","JSON","schema","文件","节点","边","拓扑","语法","存的是","长这样","协议","流水线","步骤"]
    ALGO = ["算法","流程","余弦","top-k","召回","求值","蒸馏","扫描","匹配","计算","检索","调度","流转","路由"]
    REJECT = ["自研","拒绝","本可以","没选","而不是","不用","不选","放弃了","权衡","排除了","放弃"]
    HONESTY = ["没接","研究型","诚实","局限","上限","框架先行","规模","边界","代价","不适用","原型","债","小范围"]
    if not any(w in html for w in DATA): warns.append("未见数据结构词")
    if not any(w in html for w in ALGO): warns.append("未见算法/流程词")
    if not any(w in html for w in REJECT): warns.append("未见'自研/拒绝alternative'词")
    if not any(w in html for w in HONESTY): warns.append("未见诚实边界词(四要素第④项不可省)")
    if len(strongs) < 4:
        errs.append(f"master 段首 <strong> 只有 {len(strongs)} 个,需 ≥4(Form A)")
elif a.type == "followup":
    if '<ul class="points">' not in html and '<ul class="points' not in html:
        errs.append("追问库卡缺 <ul class=\"points\">")
    nli = len(re.findall(r"<li>", html))
    if nli < 6:
        errs.append(f"追问库卡 <li> 只有 {nli} 条,需 ≥6")
elif a.type == "gap":
    if len(strongs) < 2:
        warns.append("gap 卡 <strong> 段偏少(建议 ≥2,非硬)")

# PRD 雷区 warn(全 type)
for w in ["SDD 平台", "SDD平台"]:
    if w in html: warns.append(f"出现 {w}(prd-tools 是 CC 插件非 SDD 平台;确认是对比/否定语境)")
if "20+人" in html or "20+ 人" in html: warns.append("出现 20+人(应软化 ADR-0005 1-5 人)")
if "直接生成代码" in html: warns.append("出现'直接生成代码'(插件不直接生成代码;确认语境)")

if warns:
    print(f"⚠️ 提示(--type {a.type},语义/语境在即可,不阻塞):")
    for w in warns: print("  -", w)
if errs:
    print(f"❌ 校验失败(--type {a.type}):")
    for e in errs: print("  -", e)
    sys.exit(1)
extra = f",{len(strongs)} 段 <strong>" if a.type!="followup" else f",{len(re.findall(r'<li>',html))} 条追问"
print(f"✅ 校验通过(--type {a.type}{extra},{len(warns)}条提示)")
```

- [ ] **Step 2: 坏样例验证抓错**

```bash
cd /Users/didi/work/linze-journal/learning/interview-tools
printf '<div class="card" data-g="PRD 工作流"><p>说白了</p><p>6步闭环</p></div>' > /tmp/bad-p.html
python3 check_prd.py /tmp/bad-p.html --type master; echo "exit=$?"
```
Expected: ❌(碎嘴"说白了"/含"6步闭环"/master strong<4),exit=1。

- [ ] **Step 3: 好样例验证放行**

```bash
cd /Users/didi/work/linze-journal/learning/interview-tools
cat > /tmp/good-master.html <<'EOF'
<div class="card" data-c="proj" data-g="PRD 工作流" data-kw="测试 master 数据结构 算法">
<div class="card-head"><span class="tag proj">◆ 测试</span><div class="card-title">测试主卡</div></div>
<div class="core">自研数据结构——不用 SDD 平台,流程可追溯</div>
<div class="card-body">
<p><strong>数据结构。</strong>JSON schema 长这样,存的是字段。</p>
<p><strong>算法流程。</strong>扫描匹配,蒸馏检索调度。</p>
<p><strong>为什么自研。</strong>自研不用现成的,代价是规模上限。</p>
<p><strong>踩坑和边界。</strong>研究型没接真实流量,框架先行没度量。</p>
</div></div>
EOF
python3 check_prd.py /tmp/good-master.html --type master; echo "exit=$?"
cat > /tmp/good-fu.html <<'EOF'
<div class="card" data-c="proj" data-g="PRD 工作流" data-kw="追问 测试">
<div class="card-head"><span class="tag proj">追问</span><div class="card-title">测试追问库</div></div>
<div class="core">本模块高频追问 + 一句话答案</div>
<div class="card-body"><ul class="points">
<li><strong>Q1?</strong> 答1</li><li><strong>Q2?</strong> 答2</li><li><strong>Q3?</strong> 答3</li>
<li><strong>Q4?</strong> 答4</li><li><strong>Q5?</strong> 答5</li><li><strong>Q6?</strong> 答6</li>
</ul></div></div>
EOF
python3 check_prd.py /tmp/good-fu.html --type followup; echo "exit=$?"
```
Expected: master `✅ 校验通过(--type master,4 段 <strong>...)` exit=0(SDD 平台 warn 命中是预期,不阻塞);followup `✅(...,6 条追问)` exit=0。

- [ ] **Step 4: 写公共 agent prompt 模板 `.prd-prompt-template.md`**

```markdown
你是面试速查卡写作 agent。任务:为 stealth.html **PRD 工作流模块重构**产出指定 fragment(完整 card,从 <div class="card"> 到对应 </div>)。

# 必读(按顺序)
1. learning/interview-tools/STEALTH-CARDS-GUIDE.md —— §1(铁律)、§6(技术项目卡 declarative 风格:不碎嘴、不堆栈)、§7(Form A 四要素)、§2.2(卡片模板)
2. docs/superpowers/specs/2026-07-24-stealth-prd-module-reorg-design.md —— §3(本模块映射)、§5(源码核对)、§7(雷区)、§8(卡型风格)
3. learning/interview-tools/.prd-facts.md —— 源码核对的真事实 + ✅⚠️❌清单(数字以此为准,核对不到软化或省略,绝不编)
4. learning/interview-tools/.prd-followup-sources.md —— 追问库卡用它挑本模块预判追问(答案再对照 .prd-facts.md 核对,不照搬通用答案)
5. 现有卡原文: 从 stealth-source-current.html 读相关卡,确认不重复(主卡讲决策层,深挖落到实现层)

# 本次负责的 fragment
{由模块 task 填入:fragment 文件名 + --type(master/followup/gap)+ data-g tag + 主卡四要素要点(见映射表)/或追问库主题/或补缺卡主题 + title 建议 + 不重复边界}

# Form A 四要素骨架(仅 master/gap 用;每段 <strong>领起标签。</strong> 开头,共 4-5 段)
① 数据结构 / 形态 —— 长什么样
② 核心算法 / 流程 —— 怎么跑
③ 为什么自研、拒绝了什么 —— 自研 X(拒绝 Y 因为 Z,代价 W)。CLEAR 的 L + 三段推理链
④ 踩坑 + 诚实边界(eval/局限/原型/债)。**第④项不可省**

# 追问库骨架(仅 followup 用)
<div class="card-body"><ul class="points">
<li><strong>追问短句?</strong> 一句话答案(对照 .prd-facts.md)</li>
... ≥6 条
</ul></div>

# 完整 card 片段格式(所有 type)
<div class="card" data-c="proj" data-g="PRD 工作流" data-kw="{关键词,含各种问法 + 主题词}">
  <div class="card-head"><span class="tag proj">{tag}</span><div class="card-title">{面试官口吻问题,无英文项目名,无文件路径}</div></div>
  <div class="core">{一句带机制名+关键取舍的浓缩}</div>
  <div class="card-body">...</div>
</div>

# 风格(§6/§7)
declarative;禁口语碎嘴(说白了/得说句实话/我自己比较得意/被问/这套东西/你就懂了/听着像);①② 可内联不堆①②③④⑤;strong 标句首自然词;首卡 master 类由 assemble 加(agent 写普通 class="card")。

# PRD 雷区(§7)
'6 步闭环'绝不可出现;SDD 平台/20+人/直接生成代码 只在"不用/拒绝/对比"否定语境;团队规模软化"约 1–5 人"(ADR-0005);"端到端"带"个人原型探索、非生产级闭环";"5h→2h"是前后工时非严格 AB。

# 硬约束
- 只产出**指定 fragment 文件**;绝对不碰 stealth.html、其他卡、GUIDE/README/配置、**禁改 prd-to-code/prd2code-gen/prd-tools 源码(只读)**、禁产其他文件
- div 平衡;无 loop 残留;无 <html>/<body> 包裹;不输出解释、不输出 ``` 包裹
```

- [ ] **Step 5: Commit**

```bash
git -C /Users/didi/work/linze-journal add learning/interview-tools/check_prd.py learning/interview-tools/.prd-prompt-template.md
git -C /Users/didi/work/linze-journal commit -m "chore(stealth): PRD模块重构校验脚本check_prd.py+公共agent prompt模板"
```

---

### Task 3: 拉外部方法论 → `.prd-followup-sources.md`(追问库种子)

> 与 Task 4 可并行。

**Files:**
- Create: `learning/interview-tools/.prd-followup-sources.md`

**Interfaces:**
- Produces: `.prd-followup-sources.md` —— 按 8 模块归类的预判追问种子(供 Task 5-13 追问库卡挑用)

- [ ] **Step 1: 派 general-purpose agent 联网拉 5 源 + 按模块归类**

prompt 要点:
- 用 WebFetch 拉:
  - https://myengineeringpath.dev/interview-guide/ (11 段模板 + 105 追问)
  - https://github.com/alexeygrigorev/ai-engineering-field-guide/blob/main/interview/questions/03-project-deep-dive.md (项目深挖题)
  - https://github.com/zsc/interview_tutorial (5-Why 深度追问)
  - https://juejin.cn/post/7644082483090587658 (证据链:可追问/可验证/可复盘)
  - https://www.pivotjourneys.com/blog/star-format-interview-prep-clear-is-better (CLEAR: Context/Leadership/Execution/Accomplishment-Results)
- 产出 `.prd-followup-sources.md`:把拉到的追问/方法论**按 8 模块**(reference/蒸馏/架构/对比/质量/端到端/实现/推广)归类,每模块列 8-12 条**适配 PRD 工作流项目**的预判追问(不要照搬通用问,改写成会问 prd-tools 的问法)+ 标注源自哪个 URL。
- 末尾写死:"只产出 `.prd-followup-sources.md`,禁碰 stealth.html/其他文件。"

- [ ] **Step 2: 人工抽看**

确认每模块 ≥8 条追问、问法是"会问 prd-tools 的"(如"你的 reference 和 RAG 有什么区别""5h→2h 怎么测的"而非通用"讲讲你的项目")、5 源都标了出处。

- [ ] **Step 3: Commit**

```bash
git -C /Users/didi/work/linze-journal add learning/interview-tools/.prd-followup-sources.md
git -C /Users/didi/work/linze-journal commit -m "feat(stealth): PRD追问库种子-5外部方法论按8模块归类"
```

---

### Task 4: 读 PRD 源码 → `.prd-facts.md`(全模块事实清单)

> 与 Task 3 可并行。

**Files:**
- Create: `learning/interview-tools/.prd-facts.md`

**Interfaces:**
- Produces: `.prd-facts.md` —— prd-to-code + prd2code-gen + prd-tools 源码核对的真事实 + ✅⚠️❌清单,按 8 模块组织

- [ ] **Step 1: 派 general-purpose agent 读源码产事实清单**

prompt 要点:
- 读(只读,禁改):
  - `/Users/didi/work/prd-to-code`(/reference、/prd-distill 命令实现、6 yaml、门禁脚本、Readiness)
  - `/Users/didi/work/prd2code-gen`(/build-reference、/prd-distill、/bff-gen、双路径、校验、震荡检测、eval/auto-tune)
  - `/Users/didi/work/prd-tools`(README/CLAUDE.md/docs)
  - 辅以 `learning/ai-projects/`、`learning/interview-kb/明日面试_预测题校准与匹配分析.md`、memory `reference_prd_to_code_projects.md`
- 产 `.prd-facts.md`,按 8 模块组织,每条标 ✅(源码硬编可说)/⚠️(软化)/❌(别说):
  - reference:6 yaml 各存什么、自研实体/倒排索引实现、6 Phase、"6"是否准确、Pull-based vs 主动搜、冷启动怎么做
  - 蒸馏:11 步具体、每步产出、变更分类、context chunking、60% 损耗点
  - 架构:双插件拆分点、能力面适配器、为何放弃 MCP(对照 A5 弯路)
  - 质量:SSOT 5 边界规则、证据链 8 类、negative_code_search、Readiness 五维+权重+85/60 阈值、Spec Review Gate、R01/R02 54→68
  - 端到端(prd2code-gen):6 阶段、Handlebars 0 token + LLM 兜底、4 类校验 + 3 重试、A→B→A 震荡检测、eval/auto-tune 五模块
  - 实现:Tool 识别率优化、幻觉四层、上下文三轮检索、归因三维度、Skill/Tools/Function Calling 边界
- 数字核对不到的明说"源码未硬编,面试说模糊数/不报"。
- 末尾写死:"只产出 `.prd-facts.md`;禁改三个源码项目(只读);禁碰 stealth.html/其他文件。"

- [ ] **Step 2: 人工核对关键数字**

确认:6 yaml/11 步/Readiness 85-60/证据链 8 类/R01-R02 54→68/4 类校验+3 重试 均有源码出处或标⚠️;无编造。

- [ ] **Step 3: Commit**

```bash
git -C /Users/didi/work/linze-journal add learning/interview-tools/.prd-facts.md
git -C /Users/didi/work/linze-journal commit -m "feat(stealth): PRD模块源码事实清单prd-facts.md(8模块✅⚠️❌)"
```

---

### Task 5–13: 9 个模块产出(可并行派 9 agent)

> **统一执行方式**:每 task = 派 1 个 general-purpose agent,prompt = `.prd-prompt-template.md` 填入「该模块映射表行」(下表)+ `--type` + title 建议 + 不重复边界 → 产指定 fragment 文件 → `python3 check_prd.py <frag> --type <t>` 校验过 → 人工抽看 → commit。**模块 ① 完整示范如下,②–⑧+入口同模板,只换映射表行。**

#### Task 5: 入口·总览重写(`.prd-entry.html`,`--type master`)

- **映射行**:入口·总览。**title 建议**:`这个项目是做什么的`(沿用原标题,assemble 按 title 抽取时会先删旧 533 再插新,故 title 保持一致便于 cross-ref;或新 title 如`这个 PRD 工作流项目到底是什么`)。**四要素/结构**:沿用现有 533 的 5 段(是什么/怎么运转/怎么保证可信/代码生成那段/现状),**吸收 2456**「AI工作流完整介绍」未覆盖的要点,**新增段末 cross-ref** 指向 8 模块主卡(reference/蒸馏/架构/对比/质量/端到端/实现/推广)。**不重复**:2696 王牌素材卡。**雷区**:端到端段必带"个人原型探索、非生产级闭环";团队"约 1–5 人";无 6 步闭环。
- 校验:`python3 check_prd.py .prd-entry.html --type master`。Commit:`feat(stealth): PRD入口总览主卡重写(吸收2456+8模块cross-ref)`。

#### Task 6: 模块① reference(3 frag)

- `.prd-m1-master.html --type master`:四要素见映射表①行。**title 建议**:`reference 是什么、为什么我自己造`。**不重复**:2467(6 文件深挖,数据结构层)、2583(知识库本质定位)、2277(知识过时);主卡讲决策层(为什么需要/为什么自研索引/冷启动+eval 债),数据结构细节留 2467。
- `.prd-m1-coldstart.html --type gap`:冷启动——新项目无 reference 数据怎么 bootstrap(先跑 /reference 扫代码+历史 PRD、需人工引导标注首批领域知识、之后新需求自动回流)。**诚实**:冷启动成本高、适合中大型稳定项目。
- `.prd-m1-followup.html --type followup`:从 `.prd-followup-sources.md` reference 节挑 ≥6 追问(怎么保鲜/多大仓库/和 RAG 区别/倒排索引怎么建/漂移怎么发现/冷启动多久),答案对照 `.prd-facts.md`。
- 每 frag 跑 check_prd.py 过 → commit `feat(stealth): PRD①reference模块(主卡+冷启动+追问库)`。

#### Task 7: 模块② PRD 蒸馏(2 frag)

- `.prd-m2-master.html --type master`:四要素见映射表②行。**title 建议**:`PRD 蒸馏这条 11 步流水线怎么跑`。**不重复**:2232(变更分类)、2293(context)、2309(60%损耗)、2444(摄入)、2480(Spec/Plan 产物)。
- `.prd-m2-followup.html --type followup`:≥6 追问(11 步哪步最难/Spec 长啥样/变更分类准确率/多 PRD 合并/硬停人工确认会不会拖慢/和直接喂 LLM 区别)。
- check + commit `feat(stealth): PRD②蒸馏模块(主卡+追问库)`。

#### Task 8: 模块③ 架构(2 frag)

- `.prd-m3-master.html --type master`:四要素见映射表③行。**title 建议**:`整体架构为什么拆成双插件、为什么放弃 MCP`。**不重复**:2408(双插件)、2386(能力面)、2622(传统工程映射);BMAD(2396)已归 ④。
- `.prd-m3-followup.html --type followup`:≥6 追问(双插件为何不合一/MCP 为何不行/能力面怎么抽象/可扩展性/上下文隔离怎么做/和 BMAD 区别)。
- check + commit `feat(stealth): PRD③架构模块(主卡+追问库)`。

#### Task 9: 模块④ 对比(2 frag)

- `.prd-m4-master.html --type master`:四要素见映射表④行。**title 建议**:`和 Cursor / Copilot / Devin 这些比,差异在哪`。**不重复**:2344(vs CC init)、2643(为何自定义 Agent)、2396(BMAD);3087 已归 ⑥。
- `.prd-m4-followup.html --type followup`:≥6 追问(和 Devin 区别/为何不做 IDE 插件/开源吗/护城河/Cursor 交互更强你怎么看/Copilot 会不会追上)。
- check + commit `feat(stealth): PRD④对比模块(主卡+追问库)`。

#### Task 10: 模块⑤ 质量(4 frag)

- `.prd-m5-master.html --type master`:四要素见映射表⑤行。**title 建议**:`质量怎么保证——SSOT、证据链、门禁怎么串成可信链`。**不重复**:2264(SSOT 五条)、2787(证据链详解)、2432(Readiness)、2534(Benchmark)。
- `.prd-m5-5h2h.html --type gap`:**合并 2326+3010**→「效果验证:5h→2h 怎么测的」(度量口径 L1/L2/L3 + 实验组对照组,**诚实说分母/样本局限、前后工时非严格 AB**)。
- `.prd-m5-gate.html --type master`:**重写 2420**「质量门禁体系」,吸收 2810「Skill 执行不稳定保质量」(三层门禁:步骤间前置检查 → 蒸馏门禁 → Readiness 五维评分)。
- `.prd-m5-followup.html --type followup`:≥6 追问(SSOT 怎么保证/证据链 8 类是哪 8 类/门禁阈值怎么定/eval 有没有 labeled set[诚实债]/R01 R02 怎么做/Readiness 不过怎么办)。
- check + commit `feat(stealth): PRD⑤质量模块(主卡+5h2h合并+门禁重写+追问库)`。

#### Task 11: 模块⑥ 端到端(1 frag;A10 由 assemble 搬入)

- `.prd-m6-followup.html --type followup`:≥6 追问(震荡检测怎么实现/4 类校验具体/为何不推广代码生成/模板覆盖多少/双路径怎么选/端到端和团队版关系)。A10(主卡)由 Task 14 assemble 搬入 + 加 data-g,**本 task 不产 A10**。
- check + commit `feat(stealth): PRD⑥端到端模块追问库(A10由assemble搬入)`。

#### Task 12: 模块⑦ 实现深坑(4 frag)

- `.prd-m7-master.html --type master`:四要素见映射表⑦行。**title 建议**:`实现过程踩的坑——MCP、识别率、幻觉、上下文漏文件`。**不重复**:2609(识别率)、2671(幻觉四层)、2775(上下文定位)、2852(归因)、2821(PRD 过时)。
- `.prd-m7-skilltools.html --type gap`:**合并 2550+2562+2595**→「Skill / Tools / Function Calling 边界」(三者粒度/状态/编排区别 + prd-tools 为什么用 Skill)。
- `.prd-m7-errorleak.html --type gap`:工错流出错——错误/编造怎么流到产物、怎么拦(四层防线在产物侧:证据链溯源拦无引用/negative_code_search 拦编造引用/Spec Review 硬停/Readiness 兜底;没拦住的靠人工 Review)。
- `.prd-m7-followup.html --type followup`:≥6 追问(识别率多少/幻觉率怎么测/上下文怎么不漏/skill 和 tool 边界/出错归因三维度/工错流拦不住咋办)。
- check + commit `feat(stealth): PRD⑦实现深坑模块(主卡+skilltools合并+工错流+追问库)`。

#### Task 13: 模块⑧ 推广(3 frag)

- `.prd-m8-master.html --type master`:四要素见映射表⑧行。**title 建议**:`怎么在团队推、遇到什么阻力、怎么解`。**不重复**:2899(ROI)、2715(质量卡口)、2799(团队落地)。
- `.prd-m8-resistance.html --type gap`:推广阻力清单(质量责任划分/各人工具偏好/信任/学习成本)+ 对应解法(停 PRD→Plan 低风险先推/人工确认才开发/王牌 case 示范/赋能不替代)。
- `.prd-m8-followup.html --type followup`:≥6 追问(多少人用/最大阻力是什么/怎么说服/ROI 怎么算/后续规划/失败过吗)。
- check + commit `feat(stealth): PRD⑧推广模块(主卡+阻力+追问库)`。

---

### Task 14: 组装 —— assemble_prd.py 删旧 + 重排 9 簇 + 搬 A10

**Files:**
- Create: `learning/interview-tools/assemble_prd.py`
- Modify: `learning/interview-tools/stealth.html`

**Interfaces:**
- Consumes: 22 个 `.prd-m*.html`/`.prd-entry.html`(Task 5-13)、`stealth-source-current.html`(Task 1)
- Produces: 改写后的 stealth.html(9 簇重排、A10 搬入、旧 8 张删、master 类加)

- [ ] **Step 1: 写 assemble_prd.py**

```python
#!/usr/bin/env python3
"""PRD 模块重构组装:删全部旧 PRD-g 卡 + A10 → 按 LAYOUT 重排 9 簇插入 AI 模块锚点前。原子写。
- 抽取: 扫每个 <div class="card",depth 数到闭合 </div>,data-g=PRD 工作流 或 title 含 A10 → 存 dict{title_sub:block}
- 删: 把这些 block 原样字符串 replace 成 ''
- A10: block 首标签加 data-g="PRD 工作流"(原在 proj 根无 data-g)
- LAYOUT: 9 簇,每簇 = [(kind,val)...]; kind='frag'→读 .prd-m*.html; kind='keep'→dict 取; 首卡加 master 类
- 插入锚点: '<!-- ==================== AI 模块' 前(proj 段尾)"""
import re, os, sys
ROOT = "/Users/didi/work/linze-journal/learning/interview-tools/"
HTML = ROOT + "stealth.html"
A10_SUB = "从 PRD 到上线的完整链路"
ANCHOR = "<!-- ==================== AI 模块"

# 9 簇布局:(簇名, [(kind,val), ...]); kind: frag=读文件 / keep=按 title 子串从 dict 取
LAYOUT = [
 ("入口·项目总览", [("frag",".prd-entry.html"), ("keep","prd-tools 4个王牌素材")]),
 ("① reference 深挖", [("frag",".prd-m1-master.html"),("keep","AI知识库的本质定位"),
     ("keep","/reference 蒸馏出来的 6 个文件"),("keep","reference 知识过时"),
     ("frag",".prd-m1-coldstart.html"),("frag",".prd-m1-followup.html")]),
 ("② PRD 蒸馏", [("frag",".prd-m2-master.html"),("keep","PRD 到代码最难的一步"),
     ("keep","2-3万字 PRD"),("keep","团队模式准确率 60"),("keep","PRD摄入：多格式"),
     ("keep","Spec和Plan长什么样"),("frag",".prd-m2-followup.html")]),
 ("③ 整体架构", [("frag",".prd-m3-master.html"),("keep","双插件体系"),
     ("keep","能力面适配器"),("keep","传统工程思维"),("frag",".prd-m3-followup.html")]),
 ("④ 对比市面工具", [("frag",".prd-m4-master.html"),("keep","和 Claude Code init"),
     ("keep","有Claude Code了"),("keep","BMAD架构"),("frag",".prd-m4-followup.html")]),
 ("⑤ SSOT/证据链/门禁/评估", [("frag",".prd-m5-master.html"),("keep","SSOT 五条边界规则"),
     ("keep","证据链机制详解"),("frag",".prd-m5-gate.html"),("keep","Readiness Score"),
     ("keep","AI工作流怎么优化"),("frag",".prd-m5-5h2h.html"),("frag",".prd-m5-followup.html")]),
 ("⑥ 端到端", [("keep","A10:"+A10_SUB),("keep","端到端原型：自验证"),
     ("keep","端到端原型：模板/LLM"),("keep","端到端原型 → 生产"),("keep","Harness 三种引擎"),
     ("keep","SDD 完整流程"),("frag",".prd-m6-followup.html")]),
 ("⑦ 实现深坑", [("frag",".prd-m7-master.html"),("keep","Tool多了识别率"),
     ("keep","幻觉怎么答"),("keep","代码上下文怎么定位"),("keep","AI工作流出错了怎么归因"),
     ("keep","PRD过时或临时改动"),("frag",".prd-m7-skilltools.html"),
     ("frag",".prd-m7-errorleak.html"),("frag",".prd-m7-followup.html")]),
 ("⑧ 推广落地", [("frag",".prd-m8-master.html"),("keep","AI工作流推广ROI"),
     ("keep","PRD质量卡口"),("keep","AI工作流在团队怎么落地"),("frag",".prd-m8-resistance.html"),
     ("frag",".prd-m8-followup.html")]),
]

def extract_cards(html):
    """返回 (dict{title_sub:block}, a10_block)。title_sub = card-title 全文。"""
    cards, a10 = {}, None
    i, n = 0, len(html)
    while i < n:
        o = html.find('<div class="card"', i)
        if o < 0: break
        # depth 到闭合
        depth, j, close = 0, o, None
        while j < n:
            if html[j:j+4] == '<div':
                depth += 1; j = html.find('>', j)+1
            elif html[j:j+6] == '</div>':
                depth -= 1; j += 6
                if depth == 0: close = j; break
            else: j += 1
        if close is None: break
        block = html[o:close]
        m = re.search(r'card-title">([^<]*)<', block)
        title = m.group(1) if m else ""
        is_prd = 'data-g="PRD 工作流"' in block[:200]
        is_a10 = A10_SUB in title
        if is_a10:
            a10 = block
        elif is_prd:
            cards[title] = block
        i = close
    return cards, a10

html = open(HTML, encoding="utf-8").read()
cards, a10 = extract_cards(html)
print(f"抽取: PRD-g {len(cards)} 张, A10 {'有' if a10 else '无'}")
if a10 is None:
    print("❌ 找不到 A10"); sys.exit(1)

# A10 加 data-g(原 proj 根无)
a10 = a10.replace('<div class="card" data-c="proj" data-kw=', '<div class="card master" data-c="proj" data-g="PRD 工作流" data-kw=', 1)
if 'data-g="PRD 工作流"' not in a10[:300]:
    # 兜底:在首个 > 前插
    a10 = re.sub(r'(<div class="card[^>]*?)>', r'\1 data-g="PRD 工作流">', a10, count=1)

# 删全部旧 PRD-g 卡 + A10
removed = 0
for t, b in cards.items():
    if b in html: html = html.replace(b, ""); removed += 1
    else: print(f"⚠️ 删除未命中(可能子串漂移): {t}")
if a10 and a10[200:] in html:  # a10 已被改写,用尾部匹配原文
    pass
# A10 原文删除:重新抽原文(未加 data-g 的)
_, a10_orig = extract_cards(open(HTML,encoding="utf-8").read())
if a10_orig and a10_orig in html: html = html.replace(a10_orig, ""); removed += 1
print(f"删除旧卡 {removed} 张(应 43)")

# 建 keep 索引(title 子串 → block; A10 特殊)
def get_block(kind, val):
    if kind == "frag":
        b = open(ROOT+val, encoding="utf-8").read().strip()
        if not b.startswith('<div class="card"'): raise Exception(f"{val} 非完整 card")
        if b.count('<div') != b.count('</div>'): raise Exception(f"{val} div 不平衡")
        return b
    if val.startswith("A10:"):
        return a10  # 已加 data-g+master
    hits = [t for t in cards if val in t]
    if len(hits) != 1: raise Exception(f"keep '{val}' 命中 {len(hits)} 张: {hits}")
    return cards[hits[0]]

def mark_master(block):
    return block.replace('<div class="card"', '<div class="card master"', 1)

# 拼 9 簇
new_block = ""
for name, slots in LAYOUT:
    new_block += f'\n<!-- ===== PRD 模块: {name} ===== -->\n'
    for idx, (kind, val) in enumerate(slots):
        b = get_block(kind, val)
        if idx == 0: b = mark_master(b)
        new_block += b + "\n"

# 插入锚点前
if html.count(ANCHOR) != 1:
    print(f"❌ 锚点 {ANCHOR!r} 命中 {html.count(ANCHOR)} 次,应 1"); sys.exit(1)
html = html.replace(ANCHOR, new_block + "\n" + ANCHOR, 1)

assert html.count('<div') == html.count('</div>'), f"全文 div 不平衡: {html.count('<div')}/{html.count('</div>')}"
assert '<script>' in html and '</script>' in html, "script 残缺"
tmp = HTML + ".tmp"
open(tmp, "w", encoding="utf-8").write(html)
os.replace(tmp, HTML)
print("✅ PRD 9 簇重排完成(删43+插55+A10搬入+master类)")
```

- [ ] **Step 2: 跑组装**

```bash
cd /Users/didi/work/linze-journal/learning/interview-tools
python3 assemble_prd.py
```
Expected: `抽取: PRD-g 42 张, A10 有` → `删除旧卡 43 张(应 43)` → `✅ PRD 9 簇重排完成`。若 keep 命中 ≠1 或锚点 ≠1,停下:对照 `.prd-anchors.txt` 改 LAYOUT 里的 title 子串(全角标点);`git checkout stealth.html` 回退。

- [ ] **Step 3: 验证组装结果**

```bash
cd /Users/didi/work/linze-journal/learning/interview-tools
echo "=== PRD-g 卡数(应 55) ==="; grep -oE 'data-g="PRD 工作流"' stealth.html | wc -l | tr -d ' '
echo "=== 9 簇注释各在 ==="; grep -c '<!-- ===== PRD 模块:' stealth.html
echo "=== A10 已加 data-g(应 1) ==="; grep -B2 '从 PRD 到上线的完整链路' stealth.html | grep -c 'data-g="PRD 工作流"'
echo "=== master 类卡数(应 9,每簇首卡) ==="; grep -oE 'class="card master"' stealth.html | wc -l | tr -d ' '
echo "=== 删除的旧卡应 0 ==="; for t in "AI工作流完整介绍（面试第一答）" "AI 怎么理解陌生项目？" "Skill解决什么问题" "Skill vs 写代码调AI的区别" "Tools vs Skill"; do printf '%s: ' "$t"; grep -c "card-title\">$t" stealth.html; done
echo "=== div 平衡 ==="; echo "<div: $(grep -oE '<div[^>]*>' stealth.html|wc -l|tr -d ' ')  </div>: $(grep -oE '</div>' stealth.html|wc -l|tr -d ' ')"
```
Expected: PRD-g=55;9 簇注释=9;A10 有 data-g=1;master=9;5 张删除旧卡各=0;div 开=闭。不符→`git checkout stealth.html` 回退查 LAYOUT。

- [ ] **Step 4: 浏览器肉眼验收**

`open stealth.html` → 项目 tab → PRD 工作流 → 9 簇顺序(入口→①→...→⑧)、每簇首卡有色条、A10 在⑥首、追问库挂簇尾、core 高亮、无破版。

- [ ] **Step 5: Commit**

```bash
git -C /Users/didi/work/linze-journal add learning/interview-tools/stealth.html learning/interview-tools/assemble_prd.py
git -C /Users/didi/work/linze-journal commit -m "feat(stealth): 组装PRD模块9簇重排(删43旧+插55新+A10搬入+master类,routing不动)"
```

---

### Task 15: CSS + 全局校验 + 雷区抽检 + bump sw + push + 清理

**Files:**
- Modify: `learning/interview-tools/stealth.html`(`<style>` 加 `.card.master`)
- Modify: `sw.js`

- [ ] **Step 1: 加 `.card.master` CSS**

在 stealth.html 的 `<style>` 内(找现有 `.card{` 规则附近)加:
```css
.card.master{border-left:4px solid var(--gold,#d4a017);background:linear-gradient(90deg,rgba(212,160,23,0.06),transparent 30%);}
.card.master .tag.proj{font-weight:700;}
```
(色值对齐页面粉金色;若变量名不同,改用现有 core 金色 hex。)

- [ ] **Step 2: 全局 grep 校验**

```bash
cd /Users/didi/work/linze-journal/learning/interview-tools
echo "=== div 平衡 + script ==="
echo "<div: $(grep -oE '<div[^>]*>' stealth.html|wc -l|tr -d ' ')  </div>: $(grep -oE '</div>' stealth.html|wc -l|tr -d ' ')"
echo "script:$(grep -c '<script' stealth.html)/$(grep -c '</script>' stealth.html)"
echo "=== 禁用项(应 0) ==="; grep -cE '说白了|得说句实话|我自己比较得意|\[loop' stealth.html
echo "=== 6 步闭环(应 0) ==="; grep -cE '6 步闭环|6步闭环' stealth.html
echo "=== quickbar 按钮数(应与改前同) ==="; grep -c 'data-g="PRD 工作流"' stealth.html
```
Expected: div 开=闭;script 开=闭;禁用项 0;6步闭环 0;PRD-g=55。

- [ ] **Step 3: 雷区语境抽检**

```bash
cd /Users/didi/work/linze-journal/learning/interview-tools
echo "=== SDD 平台/20+人/直接生成代码 命中行(人工确认在否定语境) ==="
grep -nE 'SDD ?平台|20\+ ?人|直接生成代码' stealth.html || echo "(无 ✓)"
```
Expected: 命中行均在"不用/拒绝/对比/软化"语境。

- [ ] **Step 4: bump sw.js(看 origin +1)**

```bash
cd /Users/didi/work/linze-journal
git fetch origin main 2>/dev/null
echo "=== origin CACHE_NAME(应 kb-v335) ==="; git show origin/main:sw.js | grep CACHE_NAME
echo "=== 本地 ==="; grep CACHE_NAME sw.js
```
确认 origin=`kb-v335`,把 `sw.js` 的 `'kb-v335'` 改成 `'kb-v336'`。若 origin 已 >kb-v335(被别处 bump),改成 origin+1。

- [ ] **Step 5: 确认个人账号 + Commit + push**

```bash
cd /Users/didi/work/linze-journal
git remote -v | head -1   # 必须指向 zachary-lz-glm 个人账号
git add learning/interview-tools/stealth.html sw.js
git commit -m "chore(stealth): bump CACHE_NAME kb-v335→kb-v336(PRD模块9簇重构55卡)"
git push origin main
```
若 remote 非个人账号,**停下**确认正确 remote 名再 `git push <个人remote> main`。绝不推公司账号。

- [ ] **Step 6: 硬刷新验证 + 清理临时产物**

```bash
open learning/interview-tools/stealth.html   # Cmd+Shift+R 硬刷新,确认 SW 接管、9 簇显示
cd /Users/didi/work/linze-journal/learning/interview-tools
rm -f .prd-m*.html .prd-entry.html .prd-anchors.txt .prd-prompt-template.md .prd-facts.md .prd-followup-sources.md stealth-source-current.html
git add -A && git commit -m "chore(stealth): 清理PRD模块重构临时产物" || echo "无变更"
git push origin main
```
**保留** `check_prd.py` 和 `assemble_prd.py`(后续可复用)。

---

## 自审(对照 spec)

- **Spec 覆盖**:spec §2 结构(单组+主题分区/master 类/routing 不动)→ Task 14 assemble(删旧重排+首卡 master)+ Task 15-1 CSS + Task 14-3 验证 routing/quickbar 不变;§3 模块映射(8 模块+入口)→ 映射总表 + Task 5-13;§4 卡数 55 → Task 1-3 基线/Task 14-3 验证 55;§5 源码核对 → Task 4 读源码产事实清单 + 每 task 引用 .prd-facts.md;§6 外部方法论 → Task 3 + 追问库 task;§7 雷区 → Task 2 check_prd.py 雷区 + Task 15-3 抽检;§8 卡型 → Task 2 模板 + check_prd.py 三 type;§9 执行流程 → Task 1-15;§10 验收 → Task 14-3/15-2。✅ 全覆盖。
- **Placeholder**:check_prd.py / assemble_prd.py 为完整可跑代码(好坏样例自检);映射总表每模块给了四要素要点 + title 建议 + 不重复边界 + frag 清单,非 TBD;LAYOUT 里 32 个 keep title 子串 + 22 frag 文件名全写实。✅
- **命名一致**:fragment 文件名(`.prd-m1-master.html` 等)在映射表、Task 5-13、assemble LAYOUT 一致;`--type master|followup|gap` 在 Task 2 定义、Task 5-13 调用一致;A10 子串 `从 PRD 到上线的完整链路` 在 Task 1/14 一致;kb-v335→kb-v336 在 Task 15 + Global Constraints 一致。✅
- **关键差异(vs D)已落实**:assemble 是**删旧+重排连续块**(非 D 的"插主卡后");**A10 搬入加 data-g**(非新增);**现有弹药 keep 原样抽取不重写**(防漂移,仅 entry/2420/合并卡重写);**追问库/补缺是新 type**(check_prd.py 三 type);**master 类由 assemble 加首卡**(agent 不操心)。✅
```
