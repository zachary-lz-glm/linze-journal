# PRD2Code 项目日报

> BFF 代码生成器 & PRD 解析工具的每日进展记录

## 项目概述

**PRD2Code** 是一套 AI 驱动的 BFF（Backend for Frontend）代码生成工具链，核心能力是将 PRD 文档自动转化为 BFF 项目代码。

### 核心项目
- **mcp-bff-gen** — BFF 增量代码生成器（MCP 工具 / 即将升级为 CLI Agent）
- **mcp-营销平台** — PRD 解析工具（PRD → 结构化 AST → 代码建议）

### 关键技术
- LLM：Claude Sonnet 4.6（中转站）/ GLM-5.1（Coding Plan）/ MiniMax M2.7（已废弃）
- 流程管理：BMAD Method（41 Skills）
- 测试：自动化 Ground Truth 对比（git diff + 评分系统）

## 目录结构

```
├── 2026-04/          # 按月归档
│   ├── 2026-04-09.md
│   ├── 2026-04-10.md
│   └── ...
└── README.md         # 本文件
```

## 相关链接

- mcp-bff-gen（公司 GitLab）：`git@git.xiaojukeji.com:global-fe/Growth/MCPS/mcp-bff-gen.git`
- mcp-营销平台（公司 GitLab）：`git@git.xiaojukeji.com:global-fe/Growth/MCPS/mcp-营销平台.git`
- 个人 GitHub：[zachary-lz-glm](https://github.com/zachary-lz-glm)

---

*自动生成，由 bubu 🫧 维护*
