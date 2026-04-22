# PRD2Code — BFF 代码生成工具

> 基于 AI 的 BFF（Backend for Frontend）代码生成工具链，将运营 PRD 自动转化为可部署的 BFF 配置代码。

## 核心理念

**确定性优先**：有模板走模板（零 Token），无模板才走 AI 兜底。

```
工具效果 = 30% prompt 工程 + 40% 程序化校验 + 20% 流程编排 + 10% 数据管线
```

## 6 步工作流

```
PRD 文档 (.docx/.md)
    │
    ▼
┌──────────────────────────────────┐
│ Step 1: PRD 蒸馏 (3K-8K tokens) │  LLM 解析 → 结构化 JSON
│ → distilled.json                │  字段定义、校验规则、联动关系
└──────────────┬───────────────────┘
               ▼
┌──────────────────────────────────┐
│ Step 2: 项目分析 (0 tokens)      │  AST 扫描已有代码
│ → analysis.json                 │  已有字段、枚举、i18n keys
└──────────────┬───────────────────┘
               ▼
┌──────────────────────────────────┐
│ Step 3: 变更计划 (1K-3K tokens)  │  对比蒸馏 vs 现状
│ → plan.json                     │  决定模板路径 or LLM 路径
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
│                                  │  自动修正，最多 3 轮重试
└──────────────┬───────────────────┘
               ▼
┌──────────────────────────────────┐
│ Step 6: 输出报告                 │  变更报告 + Token 统计
│ → report.json + session.json    │
└──────────────────────────────────┘
```

## 架构概览

```
┌─────────────────────────────────────────────────────────┐
│                     bff-gen 架构                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  输入层                                                  │
│  ├── PRD 文档 (.docx / .md / 纯文本)                    │
│  ├── 目标 BFF 项目路径                                   │
│  ├── reference/ 领域知识（字段映射、命名规范、反模式）     │
│  └── templates/ Handlebars 模板（按活动类型分目录）       │
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

## 源码结构

```
mcp-bff-gen/
├── src/
│   ├── distiller/          # Step 1: PRD 蒸馏
│   │   ├── distill.ts           # 蒸馏入口
│   │   ├── llm-distiller.ts     # LLM 蒸馏逻辑
│   │   ├── prompt-builder.ts    # 蒸馏 prompt 组装
│   │   ├── input-processor.ts   # 输入预处理（docx/md/text）
│   │   ├── output-processor.ts  # 输出后处理
│   │   ├── cache.ts             # 蒸馏结果缓存
│   │   ├── session.ts           # 会话管理
│   │   └── types.ts             # 类型定义
│   ├── planner/            # Step 3: 变更计划
│   │   └── change-plan.ts       # 变更清单生成
│   ├── confirm/            # 用户确认交互
│   │   ├── interactor.ts        # 交互逻辑
│   │   ├── analyzer.ts          # 分析变更影响
│   │   └── persist.ts           # 持久化确认结果
│   ├── reporter/           # Step 6: 报告输出
│   │   ├── report.ts            # 报告生成
│   │   ├── analyzer.ts          # 统计分析
│   │   └── session.ts           # 会话汇总
│   ├── shared/             # 共享模块
│   │   ├── ast-parser.ts        # TypeScript AST 解析
│   │   ├── validate.ts          # 通用验证工具
│   │   ├── types.ts             # 共享类型
│   │   ├── constants.ts         # 常量定义
│   │   └── bridge.ts            # 旧架构桥接（兼容）
│   ├── prd-reader.ts       # PRD 文件读取（docx/md/text）
│   └── llm-client.ts       # LLM 调用客户端
├── prompts/                 # LLM Prompt 模板（11 个）
├── scripts/                 # 测试 & 工具脚本
│   ├── test-all.mjs              # 全量测试
│   └── test-compare.mjs          # Ground Truth 对比评分
├── reference/               # 领域知识文件（marketing-bff 预置）
│   ├── field-mapping.md          # 字段归属决策树
│   ├── naming.md                 # 命名规范
│   ├── validation.md             # 校验规则库
│   ├── anti-patterns.md          # 反模式清单
│   └── bff-hooks.md             # BFF 框架机制说明
├── docs/
│   └── architecture-overview.md  # 完整架构文档（向领导汇报用）
├── _bmad-output/            # BMAD 工作流产出
│   ├── planning-artifacts/       # 调研 & 规划文档
│   └── implementation-artifacts/  # Story 文件 & Sprint 状态
└── _claude/skills/bff-gen/  # Claude Code Skill 定义
```

## 关键设计决策

### 确定性优先

| 场景 | 生成方式 | Token 消耗 |
|------|---------|-----------|
| 新增同类型活动（结构相同） | Handlebars 模板 | **0** |
| 新增字段到已有活动 | 模板 + LLM 补充 | 2K-5K |
| 修改已有字段 | LLM 生成 | 5K-15K |
| 重复 PRD（缓存命中） | 蒸馏缓存 | ~0 |

### 4 类验证器

| 验证器 | 检查内容 | 失败处理 |
|--------|---------|---------|
| check-syntax | TypeScript 语法 | 自动修正 |
| check-fields | 字段完整性 = 蒸馏结果 | 报错提示 |
| check-rules | i18n 格式 / enum 白名单 / 命名 | 自动修正 |
| check-integration | import 路径 / 类型兼容 | 报错提示 |

### 置信度机制

每个字段标注 `confidence`：high / medium / low，低置信度需人工确认。

### 可审计性

每个生成字段可追溯到 PRD 原文（`source_ref`），不是"AI 不知道为什么这么写"。

## Token 成本

| 场景 | 总 Token | 折合费用 (Sonnet) |
|------|---------|------------------|
| 最优路径（模板命中） | 4K-11K | ~$0.02 |
| 常见路径（+1 次修正） | 6K-17K | ~$0.05 |
| 最差路径（无模板 + 3 次修正） | 15K-35K | ~$0.10 |

## 效果公式

```
bff-gen 效果 = reference/ 质量 × PRD 质量 × LLM 能力
```

| 准备度 | 一次编译通过率 | 等同于 |
|--------|--------------|--------|
| 0% 裸跑 | < 5% | 纯 vibe coding |
| 50% 有字段映射+命名 | ~40% | 能用但不稳 |
| 75% 5 份规则齐全 | ~80% | 能推广 |
| 100% 规则+模板+EvalSet | > 95% | 工业级 |

## 通用化路线图

| 阶段 | 目标 | 工作量 |
|------|------|--------|
| Phase 1 | 修复当前问题 | 5 人日 |
| Phase 2 | 规则自动学习（从 git diff） | 16 人日 |
| Phase 3 | 模板自动生成（从已有代码抽象） | 10 人日 |
| Phase 4 | 接入流程标准化 | 11 人日 |
| Phase 5-6 | 扩展能力 + 生态完善 | 36-43 人日 |

## 技术栈

- **语言**: TypeScript
- **LLM**: Claude Sonnet 4.6（中转站）/ GLM-5.1（Coding Plan）
- **模板引擎**: Handlebars
- **AST 解析**: TypeScript Compiler API
- **流程管理**: BMAD Method (41 Skills)
- **测试**: Ground Truth 对比（git diff + 自动评分）

## 相关项目

- **mcp-营销平台** — PRD 解析工具（PRD → 结构化 AST → 代码建议）
- **marketing-bff** — BFF 项目参考实现（测试 Ground Truth）

## 相关链接

- 公司 GitLab: `git@git.xiaojukeji.com:global-fe/Growth/MCPS/mcp-bff-gen.git`
- 架构文档: `docs/architecture-overview.md`（完整版，含中间产物 JSON 示例和通用化路线图）

---

*维护者: 林泽 (zachary-lz-glm) · AI 助手: bubu 🫧*
