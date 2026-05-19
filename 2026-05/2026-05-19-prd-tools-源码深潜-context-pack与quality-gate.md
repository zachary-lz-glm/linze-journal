# 06 · prd-tools 源码深潜 — context-pack / quality-gate / 分享 Q&A — 2026-05-19

> 配套：[技术实现精读](./2026-05-19-prd-tools-技术实现精读.md) | [AI 工程工作流](./2026-05-06-prd-tools-AI工程工作流.md) | [蒸馏准确率与复盘](./2026-05-19-prd-tools-蒸馏准确率定义与复盘.md)

---

## 一、context-pack.py：IR 如何匹配 index

### 1.1 它在流水线中的位置

```
requirement-ir.yaml  ──┐
layer-impact.yaml    ──┼──► context-pack.py ──► query-plan.yaml
reference/index/*    ──┘                      └──► context-pack.md
     ▲                                              │
     │ build-index.py                               ▼
reference/05-domain.yaml                    Agent 读 pack 写 report/plan
reference/04-routing-playbooks.yaml
```

**角色**：在 Agent 做 Step 4 源码扫描之前/之中，用**确定性规则**把「需求词」映射到「代码实体 ID」，生成机器可读的查询计划和人类/模型可读的锚点摘要。

**注意**：`workflow.md` 要求 Agent 在 layer-impact 之后跑此脚本；脚本本身**不**调用 LLM。

### 1.2 输入与前置条件

| 输入 | 必须 | 用途 |
|------|------|------|
| `context/requirement-ir.yaml` | ✅ | 解析 REQ 列表 |
| `context/layer-impact.yaml` | 可选但推荐 | Phase 3 从 impact target 抽查询词 |
| `reference/index/entities.json` 等 | ✅（单仓） | 倒排检索 |
| `reference/05-domain.yaml` | 可选 | PRD 中文词 → 代码枚举/标识符 |
| `reference/04-routing-playbooks.yaml` | 可选 | seed 查询 + similar patterns |

团队模式：`--team-references` 合并多仓 `references/{repo}/index/`。

### 1.3 IR 怎么被读出来（`parse_requirement_ir`）

**不是完整 YAML 解析器**，而是用正则按块切 `requirement-ir.yaml`：

```python
# 每个 REQ 块：- id: REQ-001 开头，到下一个 - id: 或文件尾
pattern = r'^\s*-\s+id:\s+"?([A-Z]+-\d+)"?\s*$(.*?)(?=^\s*-\s+id:|\Z)'
```

从块内抽取：`title`、`intent`、`change_type`、`priority`、`confidence`、`rules[]`、`business_entities[]`、`open_questions[]`（列表也有上限，如 rules 最多 6 条，防爆炸）。

**局限（分享可能被问）**：

- 依赖 IR 格式稳定；Agent 若写出非标准 YAML，正则可能漏字段。
- 这是**刻意零依赖**（不用 PyYAML）的权衡。

### 1.4 index 怎么建、怎么查

#### build-index.py（建库，context-pack 消费其产物）

1. `discover(repo)` 遍历 TS/JS/Go，跳过 `node_modules`、`dist`、`.prd-tools` 等。
2. `extract_ts` / Go 提取器用正则抓：`enum`、`interface`、`class`、`function`、`registry`、`switch_case` 等。
3. 每个实体生成：
   - `id`: `enum:path:name:line`（确定性）
   - `terms[]`: `name_to_terms(name)` — CamelCase 拆分、下划线分段、小写变体
4. `inverted_index(entities)`：`term.lower() → [entity_id, ...]`

#### query_entities（查库，与 build-index 评分一致）

对查询串 `query_str`：

1. `q_terms = name_to_terms(query_str)` 拆词
2. 在 `inverted-index.json` 里对每个 term 取候选 entity id 并集
3. 对每个候选打分：
   - 名字完全匹配：+10
   - term 命中 entity.terms：每个 +3
   - term 命中路径段：每个 +2
   - 类型是 enum/template/registry/class：+1
4. 取 top N（默认 10，build_query_plan 里常用 5）

**这不是语义搜索**，是「标识符级倒排 + 启发式打分」，所以：

- 中文 PRD 词**不会**直接命中 index，要靠 **domain bridge** 或 reference seed。
- 泛词（`data`、`config`）在 `_GENERIC_NAMES` / `_TERM_STOPWORDS` 里会被滤掉。

### 1.5 build_query_plan 四阶段（核心）

```
Phase 1: 需求驱动（IR）
Phase 2: Reference seed（04-playbooks + 01-codebase enums）
Phase 3: Layer-impact 目标文件 stem
Phase 4: P0 需求标题里的 CamelCase 符号
```

#### Phase 1：从 IR 抽「像代码的词」

对每条 REQ 的 title / intent / business_entities / rules / open_questions 跑 `_codeish_terms`：

保留条件（满足其一）：

- 含 `_`
- 含 CamelCase（首字母大写后续小写）
- 全大写
- 在 `signal_terms` 里（来自 index 非泛名 + domain 术语）

过滤 `_TERM_STOPWORDS`（`add`、`config`、`bff`…）。

然后 **domain 扩展**（`_expand_with_domain`）：

- 读 `05-domain.yaml` 的 `term`、`prd_keywords`、`synonyms`、`related_enum`
- 若 PRD 词匹配 → 追加 `related_enum`、英文 `term` 等**代码向**标识符
- 支持中文：对 `combined_text` 做 `kw in combined_text` 子串匹配

对每个候选 term：

1. `query_entities(t, inv, by_id)`
2. **无命中则跳过**（不产生空 QP）
3. 有命中则写一条 `QP-xxx`：`query_terms`、`matched_entities[]`、`confidence`

上限：**最多 30 条** Phase 1 查询（防 context 爆炸）。

`confidence` 规则：

- 命中 enum/template/registry/class → 倾向 `high`
- 经 domain 桥接扩展的词 → 最高 `medium`（即使命中 enum 也 cap）

#### Phase 2：Reference seed

从 `04-routing-playbooks.yaml` 正则提取：

- `key_files: [...]` → 文件 stem
- `prd_keywords: [...]`
- `structural_signals: [...]`

从 `01-codebase.yaml` 的 `enums:` 段提取枚举名。

每个 seed 再 `query_entities`；**无命中则 confidence=low** 但仍可能入 plan（给 Agent 提示「搜了但没命中」）。

#### Phase 3：Layer-impact

`parse_layer_impact` 目前正则较窄（主要抓 BFF 层某格式）；`_extract_query_hints_from_impacts` 从 `target` 路径取 stem，从 `changes` 文本抓 `getXxxTemplate`、`XxxType` 等。

#### Phase 4：P0 专用

对 `priority == P0` 的 REQ，从 title/rules 再抽 CamelCase / `XxxType` 等，补漏。

### 1.6 context-pack.md 怎么生成

`generate_context_pack` 把 query_plan 里的 `matched_entities` 去重，按实体类型分桶：

- Type Registry / Template / Registry / Dispatcher / Similar Examples

**Tier（must / should / optional）**：

- query `confidence == high` 或 hint 关联 P0 REQ → `must`
- `medium` → `should`
- `low` → `optional`

Must-Reference 段明确要求：**report §5/§6 和 plan 必须引用这些锚点** — 这是给 Agent 的硬提示，脚本本身不 enforce（enforce 在 `quality-gate.py final`）。

### 1.7 端到端数据流（一张图）

```text
IR: "完单油站券" + business_entities: ["CompleteOrderGas"]
         │
         ▼
_codeish_terms → 可能为空（中文无 CamelCase）
         │
         ▼
05-domain: prd_keywords 含 "完单" → related_enum: CompleteOrderGas
         │
         ▼
query_entities("CompleteOrderGas")
         │
         ▼
inverted-index["completeordergas"] / ["complete"] / ["order"] / ...
         │
         ▼
matched_entities: [enum:...:CompleteOrderGas:42, ...]
         │
         ▼
query-plan.yaml QP-003 + context-pack.md Must-Reference 表
```

### 1.8 实现局限（诚实讲，防被质疑）

| 点 | 说明 |
|----|------|
| 非语义检索 | 中文 PRD 依赖 domain.yaml 质量；domain 没维护则 Phase 1 弱 |
| 正则读 YAML | IR/impact 格式漂移会解析失败 |
| layer-impact 解析偏 BFF 旧格式 | 其他 layer 格式可能抽不到 hint |
| 与 Agent 扫描重复 | index 是**加速器**，最终仍以 Agent Read 源码为准 |
| main() 完整性 | 设计上 main 应调用 `parse_requirement_ir` / `parse_layer_impact` 并设 `slug`；若本地脚本直接运行报错，以 workflow 中 Agent 调用链为准，或检查 prd-tools 版本 |

---

## 二、quality-gate.py：三个子命令检查什么

统一入口：`python3 .prd-tools/scripts/quality-gate.py <subcommand>`

退出码：**0 = pass 或 pass-with-warnings，2 = fail**。

### 2.1 `distill` — 流程完整性（偏「有没有跑完」）

```bash
python3 .prd-tools/scripts/quality-gate.py distill \
  --distill-dir _prd-tools/distill/<slug> \
  --repo-root . \
  --mode quality    # 或 coverage | all
```

#### mode=quality 检查项

| 检查 key | 逻辑 | fail 条件 |
|----------|------|-----------|
| **required_files** | critical + important 文件存在且非空 | 缺 critical → fail；缺 important → warning |
| **requirement_ir** | 文件非空且含 `requirements:` 和 `evidence:` | 否则 fail |
| **layer_impact** | 含 `code_anchors:` 或 `fallback` | 都没有 → warning |
| **index_bridge** | 若 `_prd-tools/reference/index` 存在，则必须有 `query-plan.yaml` + `context-pack.md` | index 存在但缺 bridge → **fail** |
| **final_quality_gate** | `final-quality-gate.yaml` 存在非空 | 缺 → fail |
| **report_quality** | report 含「质量摘要」类关键词 | 无 → warning |
| **report_confirmation** | `report-confirmation.yaml` 里 `status: approved` | 非 approved → **fail** |
| **plan_missing_confirmation** | plan 里含 `missing_confirmation` 但同行无「假设/待确认」等 → warning | |
| **team_sub_plans** | 团队模式：每个 member repo 有 `plans/plan-{repo}.md` | 缺 → warning |
| **prd_coverage** | 读 `coverage-report.yaml` 或提示需跑 coverage | |

**单仓 critical 文件**：

- `_ingest/document.md`、`report.md`、`plan.md`

**团队模式 critical**：

- `team-plan.md` + `plans/plan-*.md`

#### mode=coverage — PRD 保真度（偏「有没有漏读 PRD」）

| 检查 | 含义 | fail 条件 |
|------|------|-----------|
| **block_coverage** | `document-structure.json` 每个 block 在 `evidence-map.yaml` 有映射 | 有遗漏 block → **fail** |
| **media_coverage** | `media/` 下每张图在 `media-analysis.yaml` 有分析 | 有图无分析 → **fail** |
| **requirement_trace** | 每条 REQ 的 evidence 有 `source_blocks` | 缺 trace → **fail** |
| **detail_recall** | table/code_block 类型 block 是否 linked 到某 REQ | 未 link → warning |

Fatal 集合：`block_coverage`、`media_coverage`、`requirement_trace` — 任一项 fail 则 coverage 整体 fail。

**分享话术**：coverage 解决 ADR-0011 说的「AI-friendly 压缩导致信息蒸发」— 用结构化的 block→evidence 映射做**覆盖率审计**，不是理解深度审计。

### 2.2 `final` — 交付物质量（偏「能不能照着干」）

```bash
python3 .prd-tools/scripts/quality-gate.py final --distill-dir _prd-tools/distill/<slug>
```

产出：`context/final-quality-gate.yaml`，含 **0–100 分** 和分项。

#### 五项加权（CHECK_WEIGHTS）

| 权重 | 检查项 | 做什么 |
|------|--------|--------|
| 20% | **required_files** | report/plan + 关键 context 是否存在 |
| 15% | **context_pack_consumed** | context-pack 里的路径/符号是否在 report 或 plan 中出现 ≥30% |
| 25% | **code_anchor_coverage** | layer-impact/graph-context/pack 里的路径，plan 是否提到文件名；且 04-playbooks 的 key_files 是否覆盖 |
| 25% | **plan_actionability** | plan 里是否有 `- [ ]` checklist、≥3 个源文件路径、≥1 条验证命令（rg/test/curl…） |
| 15% | **blocker_quality** | 阻塞项是否含 owner/建议/风险等上下文 |

另有 **section_structure**（report/plan 章节标题顺序），参与输出但**不在** CHECK_WEIGHTS 加权里（用于 fail 章节错位）。

#### 硬 fail 规则（`fq_compute_overall`）

- `required_files` 缺 critical → overall **fail**
- `plan_actionability` **无任何文件路径** → overall **fail**
- 无 checklist → overall 最高 **warning**（分数 cap 84）
- context_pack 消费率 <10% → warning
- 总分 ≥85 pass，≥60 warning，否则 fail

**关键细节**：

- `code_anchor_coverage` 用**文件名/ stem 子串**匹配 plan，不是 AST 级验证「改对了」。
- `context_pack_consumed` 阈值 30%：pack 里锚点术语在 report/plan 出现比例，低于 10% 严重 warning。

### 2.3 `reference` — 知识库最低标准

```bash
python3 .prd-tools/scripts/quality-gate.py reference --root .
```

| 检查 | 内容 |
|------|------|
| required_files | 6 个 YAML + project-profile 存在非空 |
| index_files | entities/edges/inverted-index/manifest 四文件 |
| yaml_readable | 无空文件、无 `\x00` |
| schema_version | 每个 yaml 有 `schema_version:` |
| evidence_claims | `owner`/`confidence: high` 附近 8 行内应有 evidence — 否则 warning |

**不检查** reference 内容是否正确，只检查**结构和证据气味**。

---

## 三、三层门禁的关系（分享一张表就够）

| 层级 | 工具 | 回答的问题 |
|------|------|------------|
| Agent 规程 | workflow HARD GATE、Review Gate | 步骤顺序对不对、人审了没有 |
| distill quality | `quality-gate.py distill` | 文件齐不齐、index bridge 有没有、approved 没有 |
| distill coverage | `quality-gate.py distill --mode coverage` | PRD 每个 block 有没有进 evidence |
| final score | `quality-gate.py final` | plan 能不能执行、锚点有没有用上 |

**重要**：门禁通过 ≠ 方案正确；**不通过** ≈ 流程/格式/保真/可执行性有硬伤。

---

## 四、分享时高频质疑 & 建议答法

### Q1：「这不就是 Claude 读 PRD + grep 吗？为什么要一套工具？」

**答**：

1. **持久知识库**（reference）跨需求复用，不是每次从零 grep。
2. **结构化中间产物**（IR / impact / contract）可 diff、可评审、可门禁。
3. **人审闸门**（report approved 才 plan）防错误级联。
4. **脚本门禁**把「有没有漏读 PRD」「plan 有没有路径」变成可自动化检查。
5. **证据链**要求负向搜索、低置信标阻塞 — 裸对话很难稳定做到。

### Q2：「准确率多少？能保证不发错券/不改错文件吗？」

**答**：

- **不能保证**业务 100% 正确；门禁保证的是**流程完整性和可执行性下限**。
- `code_anchor` 是「在源码里找到相关符号」，不是「改动正确」。
- 业务正确性靠：人审 report、研发按 plan 改完再 CR、测试走 QA 矩阵。
- reference 越厚、PRD 越清晰、domain 术语维护越好 → **人工修正量**越少。

### Q3：「build-index 正则扫代码，会不会漏/误报？」

**答**：

- 会。它是 **MVP 索引**，不是 IDE/Language Server。
- 设计是 **reference 路由 + index 缩小范围 + Agent Read 确认** 三层；index 错杀/漏杀由上层纠正。
- 动态 import、字符串拼接路径、宏生成代码 — 索引弱项，靠 `rg` 补充和 `negative_code_search` 标注。

### Q4：「中文 PRD context-pack 有用吗？」

**答**：

- 纯倒排对中文无效；靠 **`05-domain.yaml` 的 prd_keywords → related_enum** 桥接。
- 若团队没维护 domain，Phase 1 弱，主要靠 Phase 2 seed（playbooks 里配置的 key_files/enums）和 Agent 自己 rg。
- **推广建议**：首次 `/reference` 时把业务术语表写进 `05-domain`。

### Q5：「quality-gate 过了就能上线吗？」

**答**：

- **不能**。final 分高只说明 plan 像样（有路径、有 checklist、引用了 pack）。
- `report_confirmation: approved` 才是「人认为 AI 读懂了」。
- coverage fail 说明 PRD 块没映射全，要回去补 IR/evidence。

### Q6：「和 Graphify / GitNexus 重复吗？」

**答**：

- Graphify/GitNexus：**发现层**（业务图、调用图）。
- prd-tools reference：**治理层精选**（SSOT、契约、打法、可门禁的 yaml）。
- prd-tools distill：**单次需求的工程交付**（report/plan）。
- 可互补：图谱产出可 feed Mode F 上下文，再沉淀进 reference。

### Q7：「要多少成本？首次 reference 很久吧？」

**答**：

- 首次 Mode F+A：约 20–40 分钟（视仓大小），**一次性**。
- 日常：新 PRD 跑 distill，增量 Mode B 按需。
- 运行在 Claude Code，无单独服务器；脚本是本地 Python3 标准库为主。

### Q8：「团队多仓 营销平台 + marketing-bff 怎么用？」

**答**：

- 各仓本地 reference + index。
- team-reference 聚合到团队仓；team-distill 出 `team-plan.md` + `plans/plan-营销平台.md` 等。
- 团队模式 distill quality 检查 `plans/plan-*.md` 是否齐。

### Q9：「AI 会不会幻觉编造 file:line？」

**答**：

- 规程要求 code_anchor 必须 graph/rg 确认或标 `inferred` + 低置信。
- final 的 `code_anchor_coverage` 只检查 plan **是否提到**这些路径，不验证行号对错。
- **行号对错**靠研发打开文件确认 — 工具降低「找文件」成本，不替代 CR。

### Q10：「为什么 report 和 plan 分开？太慢了？」

**答**：

- ADR-0011：连续生成 report+plan 时，**错误理解会放大**到实现方案。
- 分开 = 用一次人审买后续少返工；可把它类比「需求评审通过再出详细设计」。

### Q11：「不用 prd-tools，直接 @codebase 分析 PRD 不行吗？」

**答**：

- 行，小需求可以。
- prd-tools 价值在**重复需求**、**跨层契约**、**团队统一产出格式**、**知识沉淀**。
- 适合：活动配置类、BFF schema 类、字段多的 PRD；不适合：一次性脚本、无 PRD 脑暴。

### Q12：「脚本/check 能集成 CI 吗？」

**答**：

- 可以。`quality-gate.py` 退出码 2 = fail，适合 CI step。
- 典型：PR 里提交 `_prd-tools/distill/<slug>/` 产物后跑 `distill` + `final`。
- reference 也可在 CI 跑 `reference` 检查知识库未腐烂。

---

## 五、Demo 时可展示的「硬核细节」（增加可信度）

1. 打开 `context/query-plan.yaml`，指一条 `domain-bridge: CompleteOrderGas` → `matched_entities`。
2. 打开 `context/context-pack.md` 的 **Must-Reference Anchors** 表。
3. 终端跑：`quality-gate.py final --distill-dir ...`，展示 5 项分数。
4. 故意展示 `report-confirmation.yaml` 非 approved 时 `distill` gate fail — 证明闸门是真 enforced。
5. 对比 `document-structure.json` block 数 vs `evidence-map.yaml` — 解释 coverage 在防什么。

---

## 六、命令速查

```bash
# 建 index（reference Mode A 之后）
python3 .prd-tools/scripts/build-index.py --repo . --out _prd-tools/reference/index

# IR → query-plan + context-pack
python3 .prd-tools/scripts/context-pack.py \
  --distill _prd-tools/distill/<slug> \
  --index _prd-tools/reference/index \
  --out _prd-tools/distill/<slug>/context/context-pack.md

# 门禁
python3 .prd-tools/scripts/quality-gate.py distill --distill-dir _prd-tools/distill/<slug> --repo-root . --mode all
python3 .prd-tools/scripts/quality-gate.py final --distill-dir _prd-tools/distill/<slug>
python3 .prd-tools/scripts/quality-gate.py reference --root .
```

---

## 七、与上篇文档的分工

| 文档 | 适合 |
|------|------|
| [2026-05-06 AI工程工作流](./2026-05-06-prd-tools-AI工程工作流.md) | 7 讲点、产品叙事、结构全景 |
| [2026-05-19 技术实现精读](./2026-05-19-prd-tools-技术实现精读.md) | 架构、11 步、五节点 |
| **本文** | 两个脚本源码级 + 分享 Q&A 弹药库 |
