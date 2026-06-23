# 05 · prd-tools 技术实现精读 — 2026-05-19

> 配合 [2026-05-06-prd-tools-AI工程工作流.md](./2026-05-06-prd-tools-AI工程工作流.md)（7 个讲点 / 项目结构）使用。  
> 本文聚焦：**怎么实现的、关键技术节点**，供团队分享与技术复盘。  
> 准确率五维 + 三案例快照 + 实施后复盘模板：[蒸馏准确率定义与复盘](./2026-05-19-prd-tools-蒸馏准确率定义与复盘.md)

---

## 一、先建立总观：这不是传统应用

**prd-tools = Skill（Agent 规程）+ 脚本（确定性层）+ 文件系统约定（产物 SSOT）**

```
┌─────────────────────────────────────────────────────────────┐
│  Claude Code（Agent 运行时）                                  │
│    读 SKILL.md / workflow.md / steps/*.md → 按规程执行        │
│    用 rg / Read / Glob 扫源码 → 写 YAML / Markdown 产物       │
└───────────────────────────┬─────────────────────────────────┘
                            │ 调用
┌───────────────────────────▼─────────────────────────────────┐
│  确定性 Python 脚本（零/少依赖，装到目标项目 .prd-tools/scripts） │
│    build-index.py   → Evidence Index                        │
│    context-pack.py  → query-plan + context-pack               │
│    quality-gate.py  → 产出完整性 / 评分                        │
│    ingest-docx.py   → docx → md + 图片                         │
└───────────────────────────┬─────────────────────────────────┘
                            │ 读写
┌───────────────────────────▼─────────────────────────────────┐
│  文件系统约定（SSOT 知识库 + 蒸馏产物）                         │
│    _prd-tools/reference/     ← /reference 产出                │
│    _prd-tools/distill/<slug>/ ← /prd-distill 产出             │
└─────────────────────────────────────────────────────────────┘
```

**关键技术判断**：核心智能在 **Agent 工作流（Markdown 规程）**；工程可靠性靠 **脚本门禁 + 结构化中间产物（YAML）+ 硬停止闸门**。没有独立后端服务，没有数据库。

---

## 二、分发与运行时：install.sh

`install.sh` 只做三件事：

| 动作 | 目标路径 | 作用 |
|------|----------|------|
| 复制 Skill | `目标项目/.claude/skills/{reference,prd-distill}/` | Claude Code 识别 `/reference`、`/prd-distill` |
| 复制脚本 | `目标项目/.prd-tools/scripts/*.py` | 在业务仓本地执行索引/门禁 |
| 写版本标记 | `.prd-tools-version` | 追踪安装版本 |

Skill 源码在 `prd-tools/plugins/<plugin>/skills/<skill>/`，是 **prompt 工程 + 目录约定** 的插件，不是 npm 包。

---

## 三、Skill 内部结构：Agent 的「操作系统」

以 `prd-distill` 为例：

```
SKILL.md          ← 入口：触发条件、职责边界、输入输出契约
workflow.md       ← 11 步主流程（状态机）
steps/*.md        ← 分步细则（workflow_state 前置检查）
references/*.md   ← 能力面、输出格式、golden sample
```

`reference` 同理：`workflow.md` 定义 Phase 1～6（上下文收集 → 结构扫描 → 深度分析 → 质量门控 → Index → 回流）。

**技术点**：`workflow_state` XML 块约束 Agent「这一步能读什么、不能产出什么」，减少跳步和串味（见 `step-02-deep-analysis.md` 的 `must_not_produce`）。

---

## 四、链路一：`/reference` — 建「可验证的项目记忆」

### 4.1 六阶段流水线

| Phase | 输入 | 输出 | 谁执行 |
|-------|------|------|--------|
| 1 上下文收集 (F) | 历史 PRD、技术方案、diff | `build/context-enrichment.yaml` | Agent |
| 2 结构扫描 | 目录、rg | `build/modules-index.yaml` + `project-profile.yaml` | Agent |
| 3 深度分析 (A) | 源码 Read 确认 | `reference/01~05.yaml` | Agent |
| 4 质量门控 (C) | reference + 源码 | `build/quality-report.yaml` | Agent + `quality-gate.py reference` |
| 5 Evidence Index | 源码 | `reference/index/*` | **`build-index.py`** |
| 6 反馈回流 (E) | distill 建议 | `build/feedback-report.yaml` | Agent |

### 4.2 v4.0 SSOT：为什么 6 个文件

每个事实**只存一处**，别处用 ID 引用：

| 文件 | 唯一职责 |
|------|----------|
| `01-codebase` | 静态结构：模块、枚举、注册点、数据流 |
| `02-coding-rules` | 编码规范、踩坑（severity） |
| `03-contracts` | **字段级契约**（唯一权威） |
| `04-routing-playbooks` | PRD 关键词 → 能力面 → 打法 / golden sample |
| `05-domain` | 术语、隐式规则、决策日志 |
| `index/` | 机器检索层（非 SSOT，从源码扫出来） |

### 4.3 `build-index.py`：确定性代码索引

- 用**正则**扫 TS/JS/Go（非 AST 全解析），产出：
  - `entities.json`：enum、class、function、registry 等
  - `edges.json`：import / 调用关系
  - `inverted-index.json`：词 → 实体
  - `manifest.yaml`：文件 hash（支持增量）

**意义**：把「Agent 每次从零 grep」变成「先查索引再精读」。

### 4.4 能力面适配器（`layer-adapters.md`）

不硬编码 `src/pages/**`，按 **surface** 描述能力：

- 前端：`form_or_schema`、`client_validation`、`state_flow`…
- BFF：`schema_or_template`、`transform_mapping`…
- 后端：`validation_policy`、`persistence_model`…

路径只是 **搜索候选**；写入 reference 前必须 **Read 源码** 或 `negative_code_search`。

---

## 五、链路二：`/prd-distill` — 11 步蒸馏流水线

```
PRD 原文
  ↓ Step 1  Ingestion          → _ingest/document.md + extraction-quality.yaml
  ↓ Step 2  Evidence Ledger    → context/evidence.yaml
  ↓ Step 3  Requirement IR     → context/requirement-ir.yaml  (ADD/MODIFY/DELETE/NO_CHANGE)
  ↓ Step 4  Code Search        → graph-context.md + layer-impact.yaml (+ query-plan/context-pack)
  ↓ Step 5  Contract Delta     → context/contract-delta.yaml
  ↓ Step 6  Report             → report.md
  ↓ Step 7  ★ Review Gate      → report-confirmation.yaml (必须 approved)
  ↓ Step 8  Plan               → plan.md
  ↓ Step 9  Readiness          → readiness-report.yaml
  ↓ Step 10 Backflow suggest   → reference-update-suggestions.yaml
  ↓ Step 11 Quality Gate       → final-quality-gate.yaml (quality-gate.py final)
```

### 5.1 Step 1：Ingestion

| 输入类型 | 实现 |
|----------|------|
| `.md` / `.txt` | 复制为 `document.md`，远程图片下载 + `media-analysis.yaml` |
| `.docx` | **`ingest-docx.py`**（zipfile 解 XML，零依赖） |
| 粘贴文本 | 手工建 manifest |

`extraction-quality.yaml`：`pass` / `warn` / `block` — **block 则硬停**。

**Step 1 末尾强制消费 reference**：读 `04` 路由、`01` 代码图、`03` 契约、`05` 术语。无 reference → 后续 confidence 强制 `low`。

### 5.2 Step 3：Requirement IR

- 结构化需求中间表示，**不写实现方案**
- **项目相关性过滤**：PRD 含多端描述但当前仓只是 BFF → 标 `NO_CHANGE`

### 5.3 Step 4：代码搜索（三层检索）

```
阶段 1  Reference 路由     04-playbooks + 01-codebase + query-plan
阶段 2  rg/glob 补充扫描    业务实体、动作词
阶段 3  Read 源码确认       callers/callees → graph-context.md
         ↓
      layer-impact.yaml（IMP + code_anchors）
```

**`context-pack.py`**：输入 `requirement-ir.yaml` + `index/` → 输出 `query-plan.yaml` + `context-pack.md`。

**Code Anchor 规则**：

- `MODIFY`/`DELETE` 的 IMP **必须有** `file/symbol/line`，否则写 fallback reason
- 来源：`graph` | `rg` | `reference` | `inferred`

### 5.4 Step 5：Contract Delta

多层、schema 字段变更、**奖励/券/预算/审计** 等必须生成。每条 contract 含 `producer`、`consumers[]`、`alignment_status`。

### 5.5 Step 6～7：Report + 硬闸门

Step 6 **HARD GATE**：`evidence.yaml`、`requirement-ir.yaml`、`graph-context.md`、`layer-impact.yaml`、`contract-delta.yaml` **全部就绪** 才能写 `report.md`（禁止边生成 context 边写 report — ADR-0011 教训）。

Step 7：生成 report 后 **必须暂停**，用户 `approved` 才写 plan。

### 5.6 Step 8：Plan

`plan.md` 12 章 + **§2.5 需求→文件映射**，任务粒度到 **文件:行号**、含 QA 矩阵。

### 5.7 Step 10～11：闭环与门禁

- distill **只建议** reference 更新，**不直接改** reference
- `quality-gate.py final` 五项加权评分

---

## 六、确定性 vs 非确定性分工

| 能力 | Agent | 脚本 |
|------|-------|------|
| 理解 PRD 语义 | ✅ | |
| 读源码、写 IMP | ✅ | |
| 写 report/plan | ✅ | |
| 扫全仓建索引 | | ✅ `build-index.py` |
| REQ→实体预匹配 | | ✅ `context-pack.py` |
| 产出文件是否齐全 | | ✅ `quality-gate.py` |
| docx 解压 | | ✅ `ingest-docx.py` |
| 用户是否 approved | | ✅ `report-confirmation.yaml` 检查 |

Agent 负责「理解与推理」，脚本负责「可重复验证」；用 **YAML 中间产物** 解耦。

---

## 七、五个关键技术节点（分享可重点讲）

### 节点 1：Evidence Chain（证据链）

所有结论挂 `evidence id`：`prd` | `code` | `negative_code_search` | `reference` | `api_doc`…  
**搜不到也是证据** → 避免 AI 补脑编路径。

### 节点 2：Reference-First + Index 加速

```
reference（人 curated）  →  路由到文件/符号
index（机扫）           →  倒排检索缩小范围
rg + Read（确认）       →  code_anchor
```

### 节点 3：Report Review Gate（状态机断点）

把长对话拆成 report / plan 两段，打断「错误理解从 report 传染到 plan」（ADR-0011）。

### 节点 4：能力面而非目录结构

同一套 workflow 服务 营销平台、marketing-bff、后端 —— **适配器模式**在文档层实现。

### 节点 5：飞轮（Reference 回流）

```
reference → distill → reference-update-suggestions → Mode E → reference
```

---

## 八、团队模式（了解即可）

`project-profile.yaml` 里 `layer: team-common` 时：

- 产出 `team-plan.md` + `plans/plan-{repo}.md`
- **禁止**在团队仓直接 `rg` 业务代码，从各成员仓 `references/{repo}/` 下钻
- `team-reference` / `team-distill` 为独立 Skill

---

## 九、和「直接问 Claude」的本质差异

| 维度 | 裸 Claude | prd-tools |
|------|-----------|-----------|
| 项目上下文 | 当次对话临时读 | 持久 `_prd-tools/reference/` |
| 过程产物 | 无 | IR / impact / contract / evidence 分层 |
| 人机节点 | 无 | `report-confirmation.yaml` |
| 可验证性 | 无 | `quality-gate.py` + code_anchor |
| 知识沉淀 | 无 | Mode E 回流 |

---

## 十、全链路图（可放 PPT）

```
flowchart TB
  subgraph install [安装层]
    IS[install.sh] --> SK[.claude/skills]
    IS --> PY[.prd-tools/scripts]
  end

  subgraph ref [reference 链路]
    F[Mode F 收材料] --> A[Mode A 深度分析]
    A --> R6[6 YAML SSOT]
    A --> BI[build-index.py]
    BI --> IDX[index/]
  end

  subgraph distill [prd-distill 链路]
    IN[Ingest + docx] --> EV[evidence.yaml]
    EV --> IR[requirement-ir.yaml]
    IR --> CP[context-pack.py]
    CP --> GC[graph-context + layer-impact]
    GC --> CD[contract-delta.yaml]
    CD --> REP[report.md]
    REP --> GATE{Review Gate}
    GATE -->|approved| PLN[plan.md]
    PLN --> QG[quality-gate.py final]
  end

  R6 --> IN
  IDX --> CP
  QG --> E[Mode E 回流]
  E --> R6
```

---

## 十一、学习路径（建议亲自走一遍）

1. **读** `prd-tools/README.md` + `plugins/prd-distill/workflow.md`（Step 1～8）
2. **看** 业务仓里一份真实 `_prd-tools/distill/*/context/` 目录
3. **跑** `python3 .prd-tools/scripts/quality-gate.py distill --distill-dir ...`
4. **扫** `build-index.py` 前 100 行 — 理解 index 不是魔法
5. **读** `docs/adr/0011` 前半 — Review Gate / HARD GATE 的由来

---

## 十二、相关文档索引

| 文档 | 路径 |
|------|------|
| **源码深潜（context-pack / quality-gate / Q&A）** | [2026-05-19-prd-tools-源码深潜-context-pack与quality-gate.md](./2026-05-19-prd-tools-源码深潜-context-pack与quality-gate.md) |
| 项目总览 | `prd-tools/README.md` |
| reference 工作流 | `prd-tools/plugins/reference/skills/reference/workflow.md` |
| prd-distill 工作流 | `prd-tools/plugins/prd-distill/skills/prd-distill/workflow.md` |
| 能力面适配器 | `prd-tools/plugins/reference/skills/reference/references/layer-adapters.md` |
| ADR-0011 可靠性 | `prd-tools/docs/adr/0011-Agent工作流可靠性与保真度建设计划.md` |
| 上次复盘（7 讲点） | [2026-05-06-prd-tools-AI工程工作流.md](./2026-05-06-prd-tools-AI工程工作流.md) |
| 准确率与复盘 | [2026-05-19-prd-tools-蒸馏准确率定义与复盘.md](./2026-05-19-prd-tools-蒸馏准确率定义与复盘.md) |

---

## 十三、分享备忘（30 min 技术段可摘）

- **一句话**：PRD 工程工作流，不是自动写代码机器人
- **三件套**：reference 记忆 + distill 蒸馏 + Review Gate 人审
- **五节点**：证据链 / Reference+Index / Review Gate / 能力面 / 回流飞轮
- **Demo 必指**：`report.md` 需求映射、`plan.md` §2.5、QA 矩阵、带行号的 code_anchor
