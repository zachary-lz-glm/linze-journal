# prd-tools 蒸馏准确率 — 定义、量化与三案例快照

> 配合 [技术实现精读](./2026-05-19-prd-tools-技术实现精读.md)、[源码深潜 quality-gate](./2026-05-19-prd-tools-源码深潜-context-pack与quality-gate.md)  
> 实施复盘模板：[`../templates/distill-post-implementation.yaml`](../templates/distill-post-implementation.yaml)

---

## 一、为什么不要只报一个「准确率」

蒸馏产出同时承担三种用途，对应三种「对」：

| 用途 | 问的问题 | 典型读者 |
|------|----------|----------|
| **决策** | 做不做、优先级、风险 | PM / 负责人 |
| **排期** | 谁先做、依赖链、人天 | TL |
| **施工** | 改哪个文件、怎么改 | 开发 |

一个总分会把「PRD 看得懂」和「跨仓契约已对齐」混在一起。分享时建议用 **五维 + 两层分数**（蒸馏时 / 实施后）。

---

## 二、五维定义（A–E）

| 维度 | 代号 | 含义 | 单仓主要 | 多仓主要 |
|------|------|------|----------|----------|
| PRD 保真度 | **A** | 需求有无漏、错、与 PRD 冲突未标出 | ●●● | ●●● |
| 范围边界准确度 | **B** | report §2 纳入/排除是否符合真实分工 | ●●● | ●● |
| 代码锚点准确度 | **C** | `file:line`、符号、switch 注册点是否真实 | ●●● | ●● |
| 方案可执行度 | **D** | 按 plan 实施是否需推翻架构或大块返工 | ●●● | ●● |
| 跨仓契约准确度 | **E** | producer/consumer/字段三仓是否一致 | — | ●●● |

### 建议权重（「可照 plan 施工、少返工」）

**单仓**

```text
综合 ≈ 0.25×A + 0.15×B + 0.25×C + 0.35×D
```

**团队（三仓）**

```text
综合 ≈ 0.20×A + 0.10×B + 0.15×C + 0.25×D + 0.30×E
```

> E 权重大：多仓 case 的瓶颈通常在 contract-delta，不在「读没读到 PRD」。

### 口语对照（分享用）

| 体感 | 单仓 | 多仓 | 含义 |
|------|------|------|------|
| **~80%** | ✓ 合理 | 仅指 A+B+C+D 加权 | 本仓 IMP 大多能照着写，阻塞 OQ 清掉即可开工 |
| **~60%** | 偏低 | ✓ 合理 | 含 E 后整体；PRD/排期仍可用，契约不能当 SSOT |

---

## 三、蒸馏时怎么量化（工具 + 产物）

### 3.1 机器分：`quality-gate.py`

```bash
# 蒸馏中途：文件齐不齐、PRD 块覆盖
python3 .prd-tools/scripts/quality-gate.py distill \
  --distill-dir _prd-tools/distill/<slug> \
  --repo-root . \
  --mode all

# 蒸馏结束：五项加权（不等于业务正确，但可对比 case）
python3 .prd-tools/scripts/quality-gate.py final \
  --distill-dir _prd-tools/distill/<slug> \
  --repo-root .
```

**`final` 五项权重（与源码一致）**

| 检查项 | 权重 |
|--------|------|
| required_files | 20% |
| context_pack_consumed | 15% |
| code_anchor_coverage | 25% |
| plan_actionability | 25% |
| blocker_quality | 15% |

注意：`final` 测的是 **产物形态质量**（有 plan、有锚点、阻塞项写清楚），不是联调后是否真的对。

### 3.2 Agent 自评：`readiness-report.yaml`

维度分直接用于分享对比，重点看：

- `contract_alignment` — 单仓新模式、多仓 needs_confirmation 比例
- `ready_to_implement` — 哪些 Phase 能开工
- `blocking_items` / `open_questions`

### 3.3 实施准确率（开发结束后，最可信）

```text
implementation_accuracy = 1 - (imp_discarded + imp_major_rewrite + 0.5 × imp_added_unplanned) / planned_imp_count
```

- `imp_discarded`：plan 里写了但最终不做  
- `imp_major_rewrite`：同一 IMP 方案级推翻（非改行号/改命名）  
- `imp_added_unplanned`：plan 未预见的新增任务（半个权重）

填写模板：[`templates/distill-post-implementation.yaml`](../templates/distill-post-implementation.yaml)

---

## 四、三案例蒸馏时快照（2026-05，开发前）

### 案例 1 · BFF 单仓 — 油站新司机完单得券

| 项 | 值 |
|----|-----|
| 路径 | `marketing-bff/_prd-tools/distill/gas-station-new-driver-coupon-l1/` |
| PRD | `prd-docs/DIVE 2.0-油站新司机完单领券-L1.docx` |
| readiness | **82**，`warning`，`needs_owner_confirmation` |
| 阻塞 | OQ-002 explain 页、OQ-003 双字段联动、OQ-004 后端接口 |
| 可开工 | Phase 1 ✅；Phase 2/3 ❌（等确认） |

**维度粗估（蒸馏时）**

| A | B | C | D | E | 综合（单仓公式） |
|---|---|---|---|---|------------------|
| ~90 | ~90 | ~90 | ~75 | — | **~82–85** |

**拉低 D 的点**：`IMP-009` 双字段联动无先例（readiness `confidence: medium`）。

---

### 案例 2 · 前端单仓 — 世界杯点球大赛

| 项 | 值 |
|----|-----|
| 路径 | `app/soda_coupon/_prd-tools/distill/world-cup-penalty/` |
| PRD | `docs/世界杯点球大赛玩法_PRD_v2.0.md` |
| readiness | **83**，`ready_for_dev`，`approved_with_conditions` |
| final-quality-gate | **PASS 83** |
| 阻塞 | 无硬阻塞；4 个 OQ 为 P2/P3 |

**维度粗估**

| A | B | C | D | E | 综合 |
|---|---|---|---|---|------|
| ~90 | ~95 | ~95 | ~80 | ~70* | **~82–85** |

\* 4 个 cross_repo_handoff `needs_confirmation`，本仓 plan 仍可推进。

**亮点**：plan §0 三条架构决策（入口复用 / Schema 驱动 / API 路径）降低 D 风险。

---

### 案例 3 · 团队三仓 — 同 PRD 跨 dive-editor-g / marketing-bff / 营销平台-dive

| 项 | 值 |
|----|-----|
| 路径 | `dive-drv-reference/_prd-tools/distill/oil-station-new-driver-coupon/` |
| readiness | **62**，`conditional_go` |
| final-quality-gate | **warning 75** |
| 契约 | `contract_alignment: 45`；12 delta 中 11× needs_confirmation，1× blocked（OS2） |

**readiness 分项**

| 维度 | 分 |
|------|-----|
| prd_clarity | 85 |
| reference_coverage | 80 |
| impact_analysis | 75 |
| **contract_alignment** | **45** |
| plan_completeness | 70 |
| evidence_quality | 80 |

**维度粗估**

| A | B | C | D | E | 综合（团队公式） |
|---|---|---|---|---|------------------|
| ~85 | ~80 | ~75 | ~65 | **~45** | **~60–65** |

**怎么用**：`plan.md` + `plans/plan-*.md` 做排期与分仓认领；`contract-delta.yaml` 必须人工/会议对齐后再开发。

---

## 五、三案例对比一览（分享一页表）

| 度量 | BFF 单仓 | 前端单仓 | 团队三仓 |
|------|----------|----------|----------|
| readiness | 82 | 83 | **62** |
| final gate | — | 83 PASS | 75 WARN |
| 硬阻塞 OQ | 3 | 0 | OS2 + type 值 + 契约 |
| 适合怎么用 | 直接写 Phase 1 | 按 §0 决策写 | 排期 + 分仓，契约开会定 |
| 建议体感（综合） | **~80%** | **~82%** | **~60%**（E **~45%**） |

---

## 六、团队习惯（最小闭环）

```text
蒸馏结束
  → quality-gate distill + final（记下五项子分）
  → readiness 阻塞项必须有人名
开发中
  → 只信 ready_to_implement: true 的 Phase
上线后（1 天内）
  → 填写 context/post-implementation.yaml
季度
  → 汇总 implementation_accuracy、OQ 命中率
```

### OQ 命中率（蒸馏价值证明）

```text
OQ 命中率 = 开发中确实成为问题的 OQ 数 / 蒸馏列出 OQ 总数
```

高命中率说明蒸馏**提前标对了风险**；低命中率说明 OQ 过多误报，应收紧触发条件。

---

## 七、PPT / 口述金句

1. **工具分 ≠ 业务对**：readiness 82 表示「产物够厚」，不表示联调一次过。  
2. **单仓看 D，多仓看 E**：BFF 卡在 IMP-009；团队卡在 11 条契约待确认。  
3. **80 / 60 要讲清分层**：多仓 PRD 理解仍可 ~85，跨仓契约 ~45，加权才 ~60。  
4. **真准确率靠实施后复盘**：模板一行不落，季度才有曲线。

---

## 八、相关路径

| 资源 | 路径 |
|------|------|
| 复盘模板 | `prd2code-journal/templates/distill-post-implementation.yaml` |
| BFF distill | `marketing-bff/_prd-tools/distill/gas-station-new-driver-coupon-l1/` |
| 前端 distill | `app/soda_coupon/_prd-tools/distill/world-cup-penalty/` |
| 团队 distill | `dive-drv-reference/_prd-tools/distill/oil-station-new-driver-coupon/` |
| quality-gate 源码 | `prd-tools/scripts/quality-gate.py` |
