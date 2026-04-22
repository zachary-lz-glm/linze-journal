# PRD2Code — BFF 代码生成工具

> 基于 AI 的 BFF（Backend for Frontend）代码生成工具链，将运营 PRD 自动转化为可部署的 BFF 配置代码。

## 一、工具定位

**解决什么问题**：运营 PRD → BFF 配置代码的手工转换存在重复劳动、易出错、不可追溯、知识分散四大痛点。

**不是什么**：
- **不是全自动 AI 写代码** — 核心是"确定性优先"：有模板走模板（零 AI），无模板才走 AI 兜底
- **不是银弹** — 效果依赖预置的领域知识文件（reference/），新项目需要人工编写这些知识

**核心公式**：
```
bff-gen 效果 = 30% prompt 工程 + 40% 程序化校验 + 20% 流程编排 + 10% 数据管线
```

## 二、6 步工作流

```
PRD 文档 (.docx/.md)
    │
    ▼
┌──────────────────────────────────┐
│ Step 1: PRD 蒸馏 (3K-8K tokens) │  LLM 解析 → 结构化 JSON
│ → distilled.json                │  字段定义、校验规则、联动关系、奖励条件
└──────────────┬───────────────────┘
               ▼
┌──────────────────────────────────┐
│ Step 2: 项目分析 (0 tokens)      │  AST 扫描已有代码
│ → analysis.json                 │  已有字段、枚举、i18n keys、字段分布追踪
└──────────────┬───────────────────┘
               ▼
┌──────────────────────────────────┐
│ Step 3: 变更计划 (1K-3K tokens)  │  对比蒸馏 vs 现状
│ → plan.json                     │  决定模板路径 or LLM 路径
│                                  │  含 module_coverage 防遗漏检查
│                                  │  含 field_trace 相似字段分布分析
└──────────────┬───────────────────┘
               ▼
┌──────────────────────────────────┐
│ Step 4: 代码生成                 │  模板命中 → Handlebars (0 tokens)
│ → 直接修改 BFF 源文件           │  无模板 → LLM 生成 (5K-15K)
└──────────────┬───────────────────┘
               ▼
┌──────────────────────────────────┐
│ Step 5: 验证修正 (0-6K tokens)   │  4 类验证器
│ → validation.json               │  编译/字段/规则/集成
│                                  │  自动修正（最多 3 轮）
│                                  │  修正策略：diff_fix / section_rewrite / full_rewrite
└──────────────┬───────────────────┘
               ▼
┌──────────────────────────────────┐
│ Step 6: 输出报告                 │  变更报告 + 用户评分反馈
│ → report.json + session.json    │  含 Token 统计
└──────────────────────────────────┘
```

### 中间产物（每步可断点续传）

| 步骤 | 产物 | 关键设计 |
|------|------|---------|
| Step 1 | `distilled.json` | 每个字段带 confidence（high/medium/low）+ source_ref（PRD 原文追溯） |
| Step 2 | `analysis.json` | 纯 AST 操作，零 Token；含 field_trace 字段分布追踪 |
| Step 3 | `plan.json` | generation_strategy 决定走模板还是 LLM；module_coverage 防遗漏 |
| Step 4 | 直接改文件 | 模板路径 0 Token |
| Step 5 | `validation.json` | errors(warning)/errors(fatal)/info 三级；history 记录修正历史 |
| Step 6 | `report.json` + `session.json` | field_coverage 覆盖率统计 |

## 三、架构概览

```
┌─────────────────────────────────────────────────────────┐
│                     bff-gen 架构                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  输入层                                                  │
│  ├── PRD 文档 (.docx / .md / 纯文本)                    │
│  ├── 目标 BFF 项目路径                                   │
│  ├── reference/ 领域知识（核心变量！）                    │
│  │   ├── field-mapping.md        字段归属决策树          │
│  │   ├── naming.md               命名规范                │
│  │   ├── validation.md           校验规则库              │
│  │   ├── anti-patterns.md        反模式清单（AP-1~4）    │
│  │   └── bff-hooks.md            BFF 框架机制            │
│  ├── templates/ Handlebars 模板（按活动类型分目录）       │
│  └── architecture.yaml          项目文件路径映射          │
│                                                         │
│  处理层                                                  │
│  ├── distiller/     PRD 蒸馏（LLM → 结构化 JSON）        │
│  ├── planner/       变更计划（对比现状 vs 蒸馏结果）     │
│  ├── generator/     代码生成（模板 or LLM）               │
│  └── validators/    验证修正（4 类独立验证器）           │
│                                                         │
│  输出层                                                  │
│  ├── BFF 源代码（直接修改目标项目文件）                  │
│  ├── report.json（变更报告 + 覆盖率）                    │
│  └── session.json（会话记录 + Token 统计）               │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### reference/ 是核心变量

> **有了 reference/ 不能保证 100% 精准映射，但能从 ~30% 提升到 ~70%**

它不是"精确映射表"，而是"决策规则"。LLM 需要：理解规则 → 理解 PRD → 应用规则，每一步都可能出错。

| 有/无 reference/ | 字段归属准确率 | i18n 格式 | 反模式避免 |
|-----------------|--------------|----------|----------|
| 无 | ~30%（随机猜测） | 风格漂移 | 可能生成隐性错误 |
| 有 | ~70%（按规则判断） | 统一格式 | 自动检测规避 |

## 四、核心机制

### 4.1 确定性优先

| 场景 | 生成方式 | Token | 占比 |
|------|---------|-------|------|
| 新增同类型活动（结构相同） | Handlebars 模板 | **0** | ~30% |
| 新增字段到已有活动 | 模板 + LLM 补充 | 2K-5K | ~50% |
| 修改已有字段 / 新活动类型首次 | LLM 生成 | 5K-15K | ~20% |
| 新活动类型（二次） | 保存的模板 | **0** | — |

### 4.2 可审计性

每个生成字段可追溯到 PRD 原文：
```json
{
  "prd_name": "达标班次量",
  "bff_name": "qualified_shift_count",
  "confidence": "high",
  "source_ref": "PRD 第 6 段: '司机需完成X个班次'"
}
```

### 4.3 4 类验证器

| 验证器 | 检查内容 | 失败处理 |
|--------|---------|---------|
| `check-syntax` | TypeScript 语法正确性 | 自动修正 |
| `check-fields` | 字段集合 = 蒸馏字段集合 | 报错提示 |
| `check-rules` | i18n 格式 / enum 白名单 / Context Function 白名单 | 自动修正 |
| `check-integration` | import 路径可解析 / 类型兼容 | 报错提示 |

### 4.4 防遗漏机制

- **module_coverage**：检查蒸馏结果的每个模块（fields/reward_conditions/validations）都有对应变更
- **field_trace**：参考相似已有字段的文件分布，发现新字段可能漏了某些目标文件

## 五、Token 成本

| 场景 | 总 Token | 费用 (Sonnet) |
|------|---------|--------------|
| 最优路径（模板命中） | 4K-11K | ~$0.02 |
| 常见路径（+1 次修正） | 6K-17K | ~$0.05 |
| 最差路径（无模板 + 3 次修正） | 15K-35K | ~$0.10 |
| 重复 PRD（缓存命中） | 1K-3K | ~$0.005 |

**省钱机制**：蒸馏缓存 / 模板匹配 / 差异修正（只修报错行）

## 六、vs 直接 AI 对比

| 维度 | 直接 PRD + 代码丢 AI | bff-gen |
|------|---------------------|---------|
| 可审计性 | 黑盒 | 每个字段追溯 PRD 原文 |
| 确定性 | 多次跑结果可能不同 | 模板路径 100% 确定 |
| 错误发现 | AI 检查自己 | 4 类独立验证 |
| 遗漏检测 | 依赖 AI 记得 | 强制 module_coverage 检查 |
| 断点续传 | 中断只能重来 | 可从任意步骤恢复 |
| 知识积累 | 每次一次性 | 好结果保存为模板复用 |

## 七、源码结构

```
mcp-bff-gen/
├── src/
│   ├── distiller/          # Step 1: PRD 蒸馏
│   │   ├── distill.ts           # 蒸馏入口
│   │   ├── llm-distiller.ts     # LLM 蒸馏逻辑
│   │   ├── prompt-builder.ts    # 蒸馏 prompt 组装
│   │   ├── input-processor.ts   # 输入预处理（docx/md/text）
│   │   ├── output-processor.ts  # 输出后处理
│   │   ├── cache.ts / cache-manager.ts / cache-types.ts  # 蒸馏缓存
│   │   ├── batch-parser.ts      # 批量解析
│   │   ├── session.ts           # 会话管理
│   │   └── types.ts
│   ├── planner/            # Step 3: 变更计划
│   │   └── change-plan.ts       # 变更清单 + 模块覆盖率 + 字段追踪
│   ├── confirm/            # 用户确认交互
│   │   ├── interactor.ts        # 交互逻辑
│   │   ├── analyzer.ts          # 变更影响分析
│   │   └── persist.ts           # 确认结果持久化
│   ├── reporter/           # Step 6: 报告输出
│   │   ├── report.ts            # 变更报告
│   │   ├── analyzer.ts          # 统计分析
│   │   └── session.ts           # 会话汇总 + Token 统计
│   ├── shared/             # 共享模块
│   │   ├── ast-parser.ts        # TypeScript AST 解析
│   │   ├── validate.ts          # 通用验证
│   │   ├── bridge.ts            # 旧架构桥接
│   │   ├── constants.ts / types.ts
│   ├── prd-reader.ts       # PRD 文件读取
│   └── llm-client.ts       # LLM 调用客户端
├── reference/               # 领域知识文件（marketing-bff 预置）
├── docs/
│   └── architecture-overview.md  # 完整架构文档（含中间产物 JSON 示例）
├── scripts/                 # 测试 & 工具脚本
│   ├── test-all.mjs
│   └── test-compare.mjs          # Ground Truth 对比评分
└── _bmad-output/            # BMAD 工作流产出
```

## 八、新项目接入

### 接入决策（三个 YES 才接）

1. 项目类型"规则化强 + 场景同质化"？→ BFF、后台管理、CMS、低代码
2. 每年 ≥ 20 个同质化需求？→ 约 8 个需求回本
3. 有老工程师兼职维护规则（~2h/周）？

### 准备度 × 准确率

| 准备度 | 一次编译通过 | 等同于 |
|--------|------------|--------|
| 0% 裸跑 | < 5% | 纯 vibe coding |
| 50% 有字段映射+命名 | ~40% | 能用但不稳 |
| 75% 5 份规则齐全 | ~80% | 能推广 |
| 100% 规则+模板+EvalSet | > 95% | 工业级 |

### 准备清单（~1 人周）

| # | 准备项 | 产出物 | 工作量 |
|---|--------|--------|--------|
| 1 | 字段映射规则 | `reference/field-mapping.md` | 2-3 天 |
| 2 | 校验规则库 | `reference/validation.md` | 1 天 |
| 3 | 反模式清单 | `reference/anti-patterns.md` | 1 天 |
| 4 | 命名规范 | `reference/naming.md` | 半天 |
| 5 | 项目架构描述 | `architecture.yaml` | 10 分钟 |

## 九、通用化路线图

> 当前：marketing-bff 专用（投入 ~11 人日预置知识）
> 目标：新项目接入成本从 11 人日 → 1-2 人日

| Phase | 目标 | 工作量 | 优先级 |
|-------|------|--------|--------|
| Phase 1 | 修复当前问题（空骨架/架构自动生成/验证器完善） | 5 人日 | P0 |
| Phase 2 | 规则自动学习（从 git diff 提取 field-mapping/naming/anti-patterns） | 16 人日 | P0 |
| Phase 3 | 模板自动生成（从已有代码抽象 Handlebars 模板） | 10 人日 | P0 |
| Phase 4 | 接入流程标准化（Schema 校验/回测验证/交互式向导/置信度标注） | 11 人日 | P0 |
| Phase 5 | 扩展能力（项目结构自动识别/验证规则生成） | 12 人日 | P1 |
| Phase 6 | 生态完善（接入向导 CLI/多语言/IDE 集成） | 24-31 人日 | P2 |
| **总计** | | **78-85 人日** | |

### 核心风险与对策

| 风险 | 对策 |
|------|------|
| 知识文件质量不稳定 | 自动学习 + Schema 校验 + 回测验证 |
| 新项目接入成本高 | 从历史 diff 自动提取规则 |
| PRD 格式多样 | PRD 质量预检 + 标准化建议 |
| LLM 输出不确定 | 置信度标注 + 多次验证 |

## 十、投入产出

- 当前 marketing-bff 预置投入：~11 人日（已完成）
- 通用化改造：78-85 人日
- 每需求节省：~5 小时手工编码
- 回本周期：每年 ≥ 20 个同质化需求 → 约 8 个需求回本

## 十一、技术栈

- **语言**: TypeScript
- **LLM**: Claude Sonnet 4.6（中转站 dk.claudecode.love）/ GLM-5.1（Coding Plan）
- **模板引擎**: Handlebars
- **AST 解析**: TypeScript Compiler API
- **流程管理**: BMAD Method (41 Skills)
- **测试**: Ground Truth 对比（git diff + 自动评分）
- **验证**: 4 类独立验证器（编译/字段/规则/集成）

## 相关项目

- **mcp-营销平台** — PRD 解析工具（PRD → 结构化 AST → 代码建议）
- **marketing-bff** — BFF 项目参考实现（测试 Ground Truth）

## 链接

- 公司 GitLab: `git@git.xiaojukeji.com:global-fe/Growth/MCPS/mcp-bff-gen.git`
- 完整架构文档: `docs/architecture-overview.md`（含中间产物 JSON 示例 + 接入流程标准化 + 通用化技术细节）

---

*维护者: 林泽 (zachary-lz-glm) · AI 助手: bubu 🫧*
