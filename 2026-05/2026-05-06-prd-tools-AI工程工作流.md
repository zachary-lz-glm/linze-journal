# 04 · prd-tools AI 工程工作流 — 2026-05-06

## 一、今日核心事件

**prd-tools 源码深度复盘**。读完 reference + prd-distill 双插件全部源码（SKILL.md / workflow.md / steps / references / templates / ADR），梳理出 7 个核心讲点，发现 3 个与之前认知的重大差异。

> **2026-05-15 更新**：prd-tools 已从 v2.6.0 迭代到 v2.19.9，新增 Evidence Index（build-index.py）、Context Pack（context-pack.py）、多层 Quality Gate（quality-gate.py 三个子命令）、Benchmark 回归系统、团队模式（team-reference / team-distill）、12 个 ADR。以下内容已同步更新。

**三个重大纠正**：
1. prd2code-gen 已更名为 **prd-tools**，从"代码生成工具"升级为**PRD 工程工作流**——核心不是"生成代码"，而是"把 PRD 转成有证据、可执行、可回流的结构化开发计划"
2. 之前题库说"7 维度 YAML 领域知识体系（01-entities ~ 06-glossary + 00-index）"——实际已进化到 **reference v4.0（6 文件 SSOT 架构）**，10 文件精简为 6 文件，每个事实只存在一处
3. 之前题库说"对照实验 +9 vs +35"——prd-tools 本身不包含实验数据，那部分是早期 prd2code-gen 的实验；prd-tools 的质量保证靠**证据链 + 代码锚定 + 多层质量门控 + 反馈回流闭环 + Benchmark 回归**

**三个新发现**：
1. **能力面适配器**——不绑定固定目录结构，前端/BFF/后端通过能力面（前端 9 个 / BFF 10 个 / 后端 10 个）统一描述，这是跨层可扩展的关键设计
2. **三层图谱融合架构**——Graphify（业务维度"为什么这样设计"）+ GitNexus（代码维度"代码怎么连接"）+ prd-tools（治理维度"怎么从 PRD 到代码"），图谱是原始发现层，reference 是精选后的企业知识库
3. **渐进式披露**——report.md 从 30 秒结论到完整细节，同文件内逐层展开，不是分多个报告

---

## 二、项目结构全景

```
prd-tools/  (v2.19.9)
├── README.md                    # 项目总览
├── CLAUDE.md                    # 项目约定（版本管理 / commit 规范 / 文件边界 / 反膨胀）
├── VERSION                      # 统一版本号 (2.19.9)
├── CHANGELOG.md                 # 项目级版本迭代总览
├── .claude-plugin/
│   └── marketplace.json         # 插件市场声明（2 插件）
├── install.sh                   # 安装脚本（复制 skills + scripts 到目标项目）
├── plugins/
│   ├── reference/               # 插件 1：项目知识库构建（原 build-reference）
│   │   ├── .claude-plugin/plugin.json
│   │   ├── CHANGELOG.md
│   │   └── skills/
│   │       ├── reference/       # 主 reference skill
│   │       │   ├── SKILL.md     # 入口：8 种模式（F/A/B/B2/C/E/T/T2）
│   │       │   ├── workflow.md  # 6 阶段工作流
│   │       │   ├── steps/       # 6 个执行步骤
│   │       │   ├── references/  # 参考资料（reference-v4/layer-adapters/output-contracts 等）
│   │       │   └── templates/   # Reference 模板（project-profile + 01-05 YAML）
│   │       └── team-reference/  # 团队级 reference 收集 skill
│   └── prd-distill/             # 插件 2：PRD 蒸馏
│       ├── .claude-plugin/plugin.json
│       ├── CHANGELOG.md
│       └── skills/
│           ├── prd-distill/     # 主蒸馏 skill（11 步工作流）
│           └── team-distill/    # 团队级蒸馏 skill
├── scripts/
│   ├── build-index.py           # Evidence Index 构建器（正则扫描 TS/JS/Go）
│   ├── context-pack.py          # Context Pack 生成器（合并蒸馏+索引）
│   ├── quality-gate.py          # 统一质量门控（distill/final/reference 三子命令）
│   ├── ingest-docx.py           # .docx 提取（Python zipfile，零依赖）
│   ├── release.sh               # 一键发版（semver bump + CHANGELOG）
│   ├── benchmark.sh             # Benchmark 运行器（oracle + snapshot 评分）
│   ├── validate-contracts.sh    # 契约漂移检查（跨插件一致性）
│   └── hooks/                   # Git hooks（版本一致性校验）
├── benchmarks/
│   ├── cases/                   # 测试用例
│   ├── baselines/               # 版本基准
│   └── results/                 # 评分结果
└── docs/
    └── adr/                     # 12 个架构决策记录
        ├── 0001~0006            # 基础架构决策
        ├── 0008-安装脚本职责拆分.md
        ├── 0009-PRD-Tools-3.0产品化落地计划.md
        ├── 0010-PRD-to-Code质量闭环实施计划.md
        ├── 0011-Agent工作流可靠性与保真度建设计划.md
        └── 0012-团队公共知识库聚合与继承.md
```

---

## 三、7 个核心讲点

### 讲点 1：双插件四 Skill 体系 — 构建知识库 + 蒸馏 PRD + 团队协作

prd-tools 不是"一个工具"，而是**两个核心插件（reference + prd-distill）+ 两个团队模式 Skill（team-reference + team-distill）**：

```
reference（知识库构建）               prd-distill（PRD 蒸馏）
  构建长期记忆 _reference/              消费 _reference/ + PRD
  8 种模式：F/A/B/B2/C/E/T/T2          11 步工作流
       ↓                                    ↓
  _reference/ v4.0 (6 文件)              report + plan + questions + artifacts
  + Evidence Index (entities/edges/idx)  + Context Pack (query-plan + 锚点)
       ↑                                    ↓
       └──── reference-update-suggestions ←─┘
                    反馈回流闭环
```

**reference 8 种模式**：

| 模式 | 用途 |
|------|------|
| F 上下文收集 | 收集历史 PRD/技术方案/分支 diff |
| A 全量构建 | 首次构建 `_reference/` + Evidence Index |
| B 增量更新 | 根据代码变化更新部分 reference |
| B2 健康检查 | 判断 reference 是否过期/缺证据 |
| C 质量门控 | quality-gate.py reference 子命令检查 |
| E 反馈回流 | 从 prd-distill 输出回收新知识 |
| T 团队收集 | 将成员仓库 reference 聚合到团队仓库 |
| T2 团队继承 | 从团队仓库继承知识到成员仓库 |

**prd-distill 11 步工作流**：
1. PRD Ingestion（Python zipfile 提取 + 质量门禁）
2. 证据台账（evidence.yaml）
3. Requirement IR（变更分类 ADD/MODIFY/DELETE/NO_CHANGE）
4. 代码搜索（reference 路由 + index 扫描 + grep 补充）
5. Layer Impact（按能力面分层分析）
6. Contract Delta（跨层契约差异）
7. 报告（report.md 渐进式披露）
8. **Report Review Gate（硬停止，用户确认后才继续）**
9. 计划（plan.md 12 章 + questions.md）
10. Reference 回流建议
11. **Quality Gate（quality-gate.py final 5项加权评分）**

---

### 讲点 2：Reference v4.0 — 6 文件 SSOT + Evidence Index

从 v3.1 的 10 文件精简到 v4.0 的 6 文件，核心变化是**每个事实只存在一处（SSOT），其他文件通过 ID 引用**：

```
_reference/
├── 00-portal.md                # 人类导航 + 场景阅读指南
├── project-profile.yaml        # 项目画像（技术栈/入口/能力面）
├── 01-codebase.yaml            # 静态清单（目录/枚举/模块/注册点/数据流）
├── 02-coding-rules.yaml        # 编码规则（规范+约束，severity 区分软硬）
├── 03-contracts.yaml           # 跨层和外部契约（字段级信息的唯一权威来源）
├── 04-routing-playbooks.yaml   # PRD 路由信号 + 场景打法 + golden samples
├── 05-domain.yaml              # 业务领域知识（术语/隐式规则/决策日志）
└── index/                      # Evidence Index（build-index.py 产出）
    ├── entities.json           # 代码实体（enums/classes/interfaces/functions...）
    ├── edges.json              # 跨文件调用边（RESOLVED_IMPORT）
    ├── inverted-index.json     # BM25 倒排索引
    └── manifest.yaml           # 文件哈希（增量构建）
```

**跨文件引用规则（5 条铁律）**：

| 信息类型 | 权威文件 | 其他文件引用方式 |
|---------|---------|---------------|
| 字段 type/required | 03-contracts | `contract_ref` |
| 编码规则 | 02-coding-rules | `ref_rule` |
| 开发步骤 | 04-routing-playbooks | `playbook_ref` |
| 外部系统 endpoint | 03-contracts | `contract_ref` |
| 业务术语 | 05-domain | 枚举 label 在 01-codebase |

**证据要求**：每个非显然事实必须有 evidence（kind: code/prd/tech_doc/git_diff/negative_code_search/human/api_doc），confidence 标 high/medium/low。

---

### 讲点 3：能力面适配器 — 跨层统一描述

不绑定固定目录结构，通过能力面（Capability Surface）统一描述前端/BFF/后端各自承担的能力：

**前端能力面**：
| surface | 关注内容 |
|---------|---------|
| ui_route | 页面路由、菜单、权限入口 |
| view_component | 可见组件、弹窗、表格、详情 |
| form_or_schema | 表单字段、动态 schema |
| state_flow | store、hook、跨组件数据流 |
| client_contract | 前端请求、响应、错误处理 |
| client_validation | disabled、互斥、上限、格式校验 |

**BFF 能力面**：edge_api / schema_or_template / orchestration / transform_mapping / linkage_options / upstream_contract / frontend_contract

**后端能力面**：api_surface / application_service / domain_model / validation_policy / persistence_model / async_event / external_integration

**关键设计**：路径只是搜索候选，最终结论必须来自源码、配置、类型定义、注册点、调用链、测试或负向搜索证据。

---

### 讲点 4：三层图谱融合架构

```
Graphify (业务维度)          GitNexus (代码维度)          prd-tools (治理维度)
"为什么这样设计"              "代码怎么连接"               "怎么从 PRD 到代码"
PRD/技术方案/截图/历史文档     代码仓库                     编排 + 证据治理 + 质量门控
        │                          │                           │
        └──────────────────────────┼───────────────────────────┘
                                   ▼
                         _reference/ 企业级可治理知识库
```

**核心原则：图谱是原始发现层，reference 是精选后的企业知识库。Raw Graph ≠ Reference。**

图谱 Provider 对应关系：
| Provider | 维度 | 适用的 reference 文件 |
|----------|------|---------------------|
| GitNexus | code（模块/调用链/字段/契约/影响面） | 01-codebase、03-contracts |
| Graphify | business（概念/规则/因果/历史决策/设计原理） | 02-coding-rules、04-routing-playbooks、05-domain |

**两套独立证据追踪**：
- `evidence: ["EV-xxx"]` — 可审计证据（源码/文档/人工确认），不能被图谱替代
- `graph_evidence_refs: ["GEV-xxx"]` — 图谱溯源（结构化发现），不能替代 EV

**图谱不可用时完全回退到 rg/glob + Read 流程**，不影响核心工作流。

---

### 讲点 5：证据链 + 代码锚定 + 多层质量门控 + Benchmark 回归

prd-tools 的质量保证不是靠 LLM 生成质量，而是靠**证据链 + 代码锚定 + 多层门控 + 回归**：

**证据类型**：prd / tech_doc / code / git_diff / negative_code_search / human / api_doc / reference

**Evidence Index（build-index.py）**：
- 正则扫描 TypeScript/JavaScript/Go，提取 enums/classes/interfaces/functions/constants/imports/switch-cases
- 构建跨文件 RESOLVED_IMPORT 调用边
- BM25 倒排索引做精确检索
- 文件哈希增量构建

**Context Pack（context-pack.py）**：
- 合并蒸馏产物（requirement-ir, layer-impact）和 Evidence Index
- 输出 query-plan.yaml（需求→匹配实体+置信度）
- 输出 context-pack.md（6 段：PRD Signals / Query Plan / Code Anchors / Similar Examples / Required Plan Tasks / Missing Items）
- 代码锚点按 must-reference / should-reference / optional 分层

**质量门控（quality-gate.py）三个子命令**：
- **distill**：检查产物完整性、Requirement IR、Layer Impact、索引桥接、报告确认
- **final**：5 项加权评分——required_files 20% + context_pack_consumed 15% + code_anchor_coverage 25% + plan_actionability 25% + blocker_quality 15%
- **reference**：6 文件完整性、索引、YAML 可读性、证据声明、schema_version

**Benchmark 回归（benchmark.sh）**：
- Oracle 评分：需求召回 35分 + 代码锚点准确率 30分 + 阻塞项质量 20分 + 计划可执行性 15分 + 误报扣分 -10分
- Snapshot 回归：对比历史基准发现退步

**关键规则**：
1. 源码和技术文档是最终证据，reference 是加速器
2. 搜不到也是证据（negative_code_search）
3. 不确定就标 low confidence，不要补脑
4. 业务关键规则不能只靠前端守
5. 每个输出都要能回溯 evidence

---

### 讲点 6：PRD Ingestion — 从原始文档到结构化输入

prd-distill 不是把 .docx 直接丢给 LLM 猜，而是先做一层**PRD Ingestion**：

```
原始 PRD (.docx/.md/.txt/.pdf/.pptx/.xlsx/.html)
        ↓
MarkItDown 转换 + 图片提取 + 表格提取
        ↓
prd-ingest/ 目录（9 个文件）
├── source-manifest.yaml      # 原始文件元信息
├── document.md               # 转换后的可读 markdown
├── document-structure.json   # 段落/表格/图片结构块
├── evidence-map.yaml         # PRD 块级证据 id
├── media/                    # 抽出的图片原文件
├── media-analysis.yaml       # 图片分析状态
├── tables/                   # 抽出的表格 markdown
├── extraction-quality.yaml   # 质量门禁（pass/warn/block）
└── conversion-warnings.md    # 转换风险
```

**质量门禁三级**：
- `pass`：可进入后续蒸馏
- `warn`：可继续，但必须暴露风险
- `block`：暂停，要求用户补充

**图片分析**：设置 `OPENAI_API_KEY` 后自动启用 LLM Vision；未确认图片不能作为高置信度结论。

---

### 讲点 7：反馈回流闭环 — 越用越准

```
build-reference 构建 _reference/
        ↓
prd-distill 消费 reference + PRD → 产出 report/plan/questions/artifacts
        ↓
artifacts/reference-update-suggestions.yaml（回流建议）
        ↓
build-reference 反馈回流模式 → 人工确认 → 更新 reference
        ↓
下次蒸馏更准
```

**回流建议类型**：
- new_term：PRD 出现 reference 没有的术语
- new_route：新的 PRD 路由信号
- new_contract：新的跨层契约
- new_playbook：新的场景打法
- contradiction：reference 和源码矛盾
- golden_sample_candidate：本次需求可作为高价值样例

**关键约束**：不自动修改 reference，只生成建议；用户逐条确认后才应用。

---

## 四、全链路 STAR 讲稿

**S**：B 端业务开发中，PRD 到代码的难点不在"写几行代码"，而在：PRD 业务词和代码字段不一致、前后端对同一字段的 owner 和 required 认知不一致、同类需求反复返工但历史经验没有沉淀、测试计划和开发计划脱节。

**T**：设计一套 AI 工程工作流，把 PRD 从"自然语言需求"转成"有证据、可执行、可测试、可回流"的结构化开发计划。

**A**：
1. **双插件四 Skill 体系**：reference 构建项目长期知识库（reference v4.0，6 文件 SSOT + Evidence Index），prd-distill 消费 reference + PRD 蒸馏出 report/plan/questions/artifacts（11 步工作流），team-reference / team-distill 支持跨仓库协作
2. **能力面适配器**：不绑定固定目录结构，前端 9 个 / BFF 10 个 / 后端 10 个能力面统一描述，路径只是搜索候选
3. **证据链 + 代码锚定**：每个非显然事实必须有证据（8 种类型），`build-index.py` 做静态分析构建代码实体索引，`context-pack.py` 把需求精准匹配到代码位置（must/should/optional 分层）
4. **三层图谱融合**：Graphify（业务维度）+ GitNexus（代码维度）+ prd-tools（治理维度），图谱是原始发现层，reference 是精选后的企业知识库
5. **多层质量门控**：`quality-gate.py` 三个子命令，final 做 5 项加权评分（代码锚点覆盖率 25% + 计划可执行性 25% + 必需文件 20% + context pack 消耗 15% + 阻塞项质量 15%）
6. **反馈回流闭环**：prd-distill 产出回流建议 → reference 人工确认后更新 reference → 下次蒸馏更准
7. **Benchmark 回归**：oracle 评分（需求召回 35分 + 代码锚点准确率 30分 + 阻塞项质量 20分 + 计划可执行性 15分）防止质量退步

**R**：PRD 蒸馏输出有完整的证据链，每个结论可追溯到 PRD 块/源码/技术文档。代码锚定让每个需求都匹配到具体代码位置。多层质量门控保证 reference 和产出可用。反馈回流让知识库越用越准。Benchmark 回归防止质量退步。

---

## 五、与之前认知的差异（需要更新题库详解.md）

| 位置 | 原说法 | 修正为 |
|------|--------|--------|
| 项目名 | prd2code-gen | **prd-tools**（v2.19.9） |
| 项目定位 | "AI 代码生成工具" | "PRD 工程工作流"——不是生成代码，是把 PRD 转成有证据的结构化开发计划 |
| 领域知识结构 | "7 维度 YAML（01-entities ~ 06-glossary）" | **reference v4.0（6 文件 SSOT）+ Evidence Index**（entities/edges/inverted-index） |
| 核心机制 | "3-Skill 体系（build-reference / prd-distill / bff-gen）" | **双插件四 Skill（reference / prd-distill / team-reference / team-distill）** |
| 质量保证 | "4 层 Eval + Auto-Tune + 对照实验" | **证据链 + 代码锚定 + 多层质量门控 + 反馈回流 + Benchmark 回归** |
| 工作流步骤 | "prd-distill 8 步" | **prd-distill 11 步**（含 Report Review Gate 硬停止 + Quality Gate） |
| 运行模式 | "build-reference 6 种模式" | **reference 8 种模式**（新增 T 团队收集 + T2 团队继承） |
| PRD 解析 | "MarkItDown 转换" | **Python zipfile 提取**（ingest-docx.py，零第三方依赖） |
| 质量门控 | "致命项/警告项" | **quality-gate.py 三子命令**（distill/final/reference），final 5项加权评分 |
| 代码检索 | 未提及 | **build-index.py 静态分析 + context-pack.py 精准锚定**（must/should/optional） |
| 回归测试 | 未提及 | **benchmark.sh oracle + snapshot 评分** |
| ADR 数量 | 6 个 | **12 个**（新增 0008~0012） |
| 实验数据 | "油站实验 +9 vs +35" | 早期 prd2code-gen 的实验，prd-tools 本身没有对照实验数据 |
| 30 秒开场白 | "prd2code-gen" | 改为 "prd-tools" |
| 能力面数量 | "20+ 能力面" | **前端 9 + BFF 10 + 后端 10 = 29 个能力面** |

---

## 六、项目架构设计亮点总结

| # | 设计亮点 | 为什么这样设计 |
|---|---------|-------------|
| 1 | 6 文件 SSOT + Evidence Index | 消除跨文件重复和矛盾，代码实体索引支持精准检索 |
| 2 | 能力面适配器（29 个） | 不绑定目录结构，跨项目可扩展（前端 9 + BFF 10 + 后端 10） |
| 3 | 8 种证据类型 | 保证结论可追溯，搜不到也是证据 |
| 4 | 图谱是发现层不是知识库 | 图谱发现需要精选才能进入 reference |
| 5 | PRD Ingestion 零依赖 | Python zipfile 提取 .docx，不依赖第三方库 |
| 6 | 反馈回流闭环 | 越用越准，不靠一次性构建 |
| 7 | 渐进式披露报告 | 30 秒到完整细节，按角色阅读 |
| 8 | 图谱不可用时完全回退 | 不依赖外部工具，核心流程鲁棒 |
| 9 | 跨文件边界 5 条铁律 | 避免 knowledge 污染（字段信息在 03、规则在 02、步骤在 04） |
| 10 | Provider 可替换 | 不绑定 GitNexus/Graphify，未来可换 Neo4j/Sourcegraph/CodeQL |
| 11 | build-index.py 增量构建 | 文件哈希对比，只重建变化部分，大仓库也能快速更新 |
| 12 | context-pack.py 分层锚点 | must/should/optional 三层，AI 消费时按优先级取 |
| 13 | quality-gate.py 加权评分 | 5 维度量化质量，不是简单的通过/不通过 |
| 14 | Benchmark 回归 | oracle + snapshot 评分防止质量退步 |
| 15 | 团队模式（T/T2） | 跨仓库公共知识只维护一份，成员仓库继承团队知识 |
| 16 | Lockstep 版本管理 | VERSION + 2x plugin.json + 2x marketplace.json 5 处一致性 |
| 17 | Anti-bloat 原则 | 3 问测试 + 文件数硬限制（20 .py / 10 ref .md / 6 step .md） |
