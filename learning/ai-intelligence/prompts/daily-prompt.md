# 每日 AI 工程化深度日报

> 每天一个方向，丢给 AI 一句话即可。周报用全景扫描，日报用单点深挖。

---

## 固定数据源（每次必查）

| 数据源 | 用途 | 访问方式 |
|--------|------|----------|
| **OSSInsight Trending AI** | GitHub AI 项目热度排名（28天涨幅） | 搜索 "OSSInsight trending AI" 获取当前 Top 50 及 28 天增长数据 |
| **HuggingFace Daily Papers** | 学术前沿每日精选论文 | 搜索 "HuggingFace daily papers" 获取当日热门论文 |

> 每次生成日报时，先从这两个数据源提取与当天主题相关的项目/论文，再结合全网搜索补充。

---

## 周一 · MCP

> 先查一下 OSSInsight Trending AI 里 MCP Servers 类别的项目排名和 28 天涨幅，再查 HuggingFace 近期有没有 MCP 相关论文。然后全网搜 MCP 协议最近的进展，包括官方动态、GitHub 热门 MCP Server、企业落地案例，整理一份深度分析，重点看对前端工程师有什么可以直接用的

## 周二 · Agent 编排

> 先查一下 OSSInsight Trending AI 里 AI Agents 和 Coding Agents 类别的项目排名和 28 天涨幅，再查 HuggingFace 近期有没有 Multi-Agent 相关论文。然后全网搜 Multi-Agent 编排架构的最新实践，包括 LangGraph/AutoGen/CrewAI 对比、GitHub 热门项目、企业级 Agent 系统设计模式，整理一份深度分析给我

## 周三 · AI 前端应用

> 先查一下 OSSInsight Trending AI 里 LLM Tools 和 Vibe Coding 类别的项目排名和 28 天涨幅，再查 HuggingFace 近期有没有 AI 交互/前端相关论文。然后全网搜 AI 前端应用的最新实践，包括流式渲染、SSE/WebSocket 实时交互、AI 对话 UI 组件、语音/视频 AI 交互、AI 产品的前端架构设计，整理一份深度分析给我

## 周四 · RAG 与企业知识

> 先查一下 OSSInsight Trending AI 里 RAG 和 Vector DB 类别的项目排名和 28 天涨幅，再查 HuggingFace 近期有没有 RAG/检索增强相关论文。然后全网搜 RAG 最新进展，包括 GraphRAG、Agentic RAG、向量数据库选型、企业知识库方案，重点看前端工程师在 RAG 系统中负责什么、怎么做好交互层

## 周五 · AI 评估与治理

> 先查一下 OSSInsight Trending AI 里 Inference 类别的项目排名和 28 天涨幅（推理优化与评估相关），再查 HuggingFace 近期有没有 LLM 评估/安全相关论文。然后全网搜 AI 系统评估与治理的最新实践，包括 Evals 框架、生产监控、幻觉检测、安全合规、企业级 AI 质量保障体系，整理一份对面试有直接帮助的深度分析

---

## 说明

- 每句话直接丢给 AI 即可，不需要额外补充
- 方向轮换：MCP → Agent → AI前端 → RAG → 评估，每周一轮
- 如果某个方向本周特别热（周报里提到了），可以替换当天的方向
- 每次必查 OSSInsight（工程热榜）和 HuggingFace（学术前沿），确保不漏关键动态
- 产出自动保存到 `learning/ai-intelligence/{年}-W{周}/日报-{MM}-{DD}-{主题关键词}.md`
- 主题关键词从内容中提取 2-6 个字的概括（如"AI前端应用生态深度分析"、"MCP协议与企业落地"）
- 周报保存到 `learning/ai-intelligence/{年}-W{周}/周报-{主题关键词}.md`
- 保存后同步更新 `_sidebar.md` 导航
