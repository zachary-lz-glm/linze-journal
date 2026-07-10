---
日期: 2026-07-09
主题方向: AI Agent 平台 / Coding Agent / Skill 生态 / 大厂内部 AI 实战
关键词: Claude Managed Agents, Coze 3.0, Cursor, Devin, Claude Skills, 大厂 AI 落地
信息来源: WebSearch 公开报道（部分内容含营销水分，已在文中标注）
---

# AI 最新情报 · 2026-07-09

> 主题：**好用的 Agent、Skill，以及互联网大厂中真正在产生价值的 AI 应用**
> 视角：从前端工程师 / 大厂面试准备的角度筛选信息。

---

## 一、模型 & Agent 平台：当前梯队在哪儿

### 1.1 头部模型分工（2026 年中观察）

来自多份评测对比，共识大致是：

| 维度 | 领跑者 | 备注 |
|------|--------|------|
| Coding 工程 | **Claude Opus 4.6+ / Grok 4** | Anthropic 官方称 Claude 已写其 80%+ 代码，工程师每日合并量是 2024 年的 8 倍 ⚠️营销水分较大 |
| 推理能力 | **Gemini 3.x Pro** | 长上下文 + 多模态强 |
| 自然语言写作 | **Claude** | 文笔最自然 |
| 通用 all-around | **GPT-5.x** | 综合最稳 |

> ⚠️ 关于"Claude Fable 5 / Mythos 5"、"Grok 4"等具体型号版本号，搜索引擎给出的部分内容可能是营销或推测，建议以官方发布为准。

### 1.2 Anthropic 2026 年动作（重磅）

Anthropic 在 1-7 月连续放了几大招（来源：[Linas Substack 完整指南](https://linas.substack.com/p/anthropic-claude-2026-every-launch-guide)、[MindStudio](https://www.mindstudio.ai/blog/code-with-claude-2026-new-agent-features)、[Aragon Research](https://aragonresearch.com/anthropic-claude-cowork/)）：

| 产品 | 价值 |
|------|------|
| **Claude Cowork**（2026-01-12 研究预览） | "Computer Agent"，桌面自动化，对标 Computer Use 但更面向日常办公场景 |
| **Managed Agents** | 全托管 Agent 服务，底层基于 Agent SDK，提供 **scheduler（调度）+ dreaming pass（后台规划）+ rubric-based outcome grading（基于评分表的成果评定）** |
| **Dreaming** | 后台"做梦"式长程规划能力，让 agent 在空闲时为下一步做规划 |
| **Multi-agent orchestration** | 多 Agent 协同，可让多个 Claude 分工并行 |
| **/goal + Outcomes** | 目标驱动 + 基于评分表自动评估完成质量 |
| **Claude Finance** | 金融垂类 Agent |
| **Add-ins** | 类似 Office 插件的扩展机制 |

> 🔥 对工程师的意义：**dreaming + outcome grading** 是 Agent 从"听话的工具"走向"自主完成任务并自评"的关键能力，面试可作答素材。

---

## 二、国内大厂 AI Agent 战况

### 2.1 四大厂战略分化（来源：[36氪](https://m.36kr.com/p/3697425974013571)、华尔街见闻）

| 厂商 | 战略定位 | 旗舰产品 |
|------|---------|---------|
| **字节** | 娱乐 + 互动 | **豆包 + 抖音 + Coze（扣子）** |
| **阿里** | AI + 消费 | **通义千问 Qwen3 + 淘系 + 高德** |
| **腾讯** | 社交 + 裂变 | **微信 + 元宝 + WorkBuddy** |
| **百度** | 搜索 + AI 融合 | **文心 4.5 + 千帆 + 红手指 Operator** |

### 2.2 字节扣子 Coze 3.0 — 国内 Agent 平台标杆（[coze.cn](https://www.coze.cn/)）

3.0 版本（2025 年 6 月上线）核心新功能：

- **多人多 Agent 协作**：复杂任务拆解、并行处理
- **多行业技能包**：金融、自媒体、医疗、法律、科研 —— 内置专业能力
- **一键加载技能包** + **多端同步**
- **多模型接入**：豆包 / Claude / Codex CLI / OpenClaw 一键接入

底层模型：**豆包 1.8 深度思考模型** —— 多模态深度思考，agentic 能力（工具调用、指令遵循、视觉理解）显著增强，专为企业级 Agent 任务设计。

> 💼 落地：太平洋证券等机构已发布 Coze 投研应用研究报告。

### 2.3 国内企业级 Agent 平台对比

| 平台 | 厂商 | 特点 |
|------|------|------|
| [Coze 扣子](https://www.coze.cn/) | 字节 | 零代码 + 多 Agent 协作 + 行业技能包 |
| 百度千帆 | 百度 | 文心 + 搜索融合 |
| 腾讯元器 | 腾讯 | 微信生态接入 |
| [火山引擎扣子企业版](https://www.volcengine.com/product/coze-pro) | 字节 To-B | 企业级部署、合规、私有化 |

---

## 三、海外大厂内部 AI 应用：现实与隐忧

### 3.1 推 AI 用 AI 的副作用（[Fortune](https://fortune.com/2026/05/22/microsoft-ai-cost-problem-tokens-agents/)、[LeadDev](https://leaddev.com/ai/are-amazon-microsoft-and-meta-bankrolling-ai-with-layoffs)）

| 厂商 | 内部 AI 动作 | 2026 影响 |
|------|--------------|----------|
| **Microsoft** | [Work Trend Index 2026](https://www.microsoft.com/en-us/worklab/work-trend-index/agents-human-agency-and-the-opportunity-for-every-organization) 调研 2 万 AI 用户、追踪万亿级 M365 信号 | 大规模裁员 + AI capex 暴增；内部报告揭示 **token 成本正在失控** |
| **Amazon** | 内部 AI 使用排行榜 → **后被废除**（员工刷榜推高算力成本） | 2026-01 裁员 ~1.6 万 |
| **Meta** | **AI-driven impact 2026 起作为员工核心考核指标** | 裁员 1.04 万 - 2 万，资金转向 AI |

> ⚠️ 关键洞察：**"让员工尽可能多用 AI"** 的策略正在反噬 —— token 成本飙升、员工刷榜、ROI 难以衡量。面试谈"AI 落地难点"时可作反例素材。

---

## 四、Coding Agent 排名：2026 年工程师范儿

来源：[Coursiv](https://coursiv.io/blog/best-ai-agents-for-coding-2026)、[Vellum](https://www.vellum.ai/blog/best-ai-coding-agents)、[MightyBot](https://mightybot.ai/blog/coding-ai-agents-for-accelerating-engineering-workflows/)、[Medium - State of AI Coding Agents](https://medium.com/@dave-patten/the-state-of-ai-coding-agents-2026-from-pair-programming-to-autonomous-ai-teams-b11f2b39232a)

| 工具 | 强项 | 适用场景 |
|------|------|---------|
| **Cursor** | 最佳混合（本地 IDE + 云端持久 Agent） | 日常开发主力 |
| **Claude Code** | Claude 原生终端 Agent，最自然 | 复杂任务、命令行重度 |
| **Devin (Cognition)** | 最强专用自主 SWE | 端到端独立任务 |
| **GitHub Copilot** | 企业/IDE 集成最广 | 大企业合规场景 |
| **Codex (OpenAI)** | GPT 系编码能力 | OpenAI 生态用户 |
| **Aider / Cline / OpenCode (SST) / Windsurf** | 各有特色的垂类工具 | 个人偏好 |

> 趋势：**从"自动补全" → "自主 Agent 团队"**。Cursor 的"本地 + 云端持久 Agent"被多份评测认为是 **2026 最完整的混合 Agent 平台**。

---

## 五、Claude Skill 生态精选（工程师向，可直接用）

### 5.1 入口资源

| 仓库/站点 | 特点 |
|----------|------|
| [anthropics/skills](https://github.com/anthropics/skills) | 官方技能大全 |
| [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills) | 精选列表，含预构建工作流 |
| [VoltAgent/awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills) | **1000+ skill，跨 Claude Code / Codex / Gemini CLI / Cursor** |
| [awesomeclaudeskills.info](https://awesomeclaude.ai/awesome-claude-skills) | 169+ skill，13 类分类 |
| [SkillsMP](https://skillsmp.com/) | 2M+ skill 搜索目录（开放 SKILL.md 标准） |
| [AgentSkill Club](https://www.agentskill.club/) | 4045+ 开源 skill |

### 5.2 多份榜单共同推荐的"实用派"

| Skill | 解决问题 |
|-------|---------|
| **skill-creator** | 零代码创建自定义 Skill（教写 frontmatter + description，让 Claude 精准触发） |
| **find-skills** | 技能发现器，帮你找到现成 Skill |
| **planning-with-files** | 复杂项目规划神器 |
| **brainstorming** | 需求预判与分析 |
| **TDD Skill** | 测试驱动开发，自动生成测试 |
| **代码格式化 / Linting Skill** | 自动执行格式化与规范检查 |
| **5-Agent 并行代码审查** | 多 Agent 协同 CR |
| **obsidian-skills** | Obsidian 知识库管理 |
| **superpowers / claude-hud** | 综合增强（YouTube 博主推荐） |

> 💡 国内社区（[博客园](https://www.cnblogs.com/itech/p/19832124)、[腾讯云](https://cloud.tencent.com/developer/article/2657596)、[七牛云指南](https://news.qiniu.com/archives/1773714153285)）的建议：
> - **按场景筛选**，不要盲目装 30+ skill
> - **控制调用权限**，避免误触发
> - SKILL.md 已成为 **跨 Claude Code / Codex / Cursor 的开放标准**

---

## 六、企业级 Agent 落地：哪些场景真在产生价值

来源：[Rasa](https://rasa.com/blog/best-ai-agents-for-enterprise)、[Sema4.ai](https://sema4.ai/blog/ai-agent-use-cases/)、[Kore.ai](https://www.kore.ai/blog/top-ai-agents-for-customer-service-tested-reviewed)

### 6.1 成熟度排序（从最成熟开始）

1. **客服/客户支持**（Tier-1 厂商：Sierra、Decagon、Salesforce Agentforce、Cognigy、Kore.ai、Zendesk）
2. **销售辅助**（Salesforce Agentforce 排名 #1）
3. **Coding 工程**（Cursor / Claude Code / Devin）
4. **数据分析 / BI**（自然语言查询 + 报表生成）
5. **HR / 流程自动化**（Sema4.ai 等）
6. **金融 / 供应链**（垂类落地，但 ROI 评估严格）

### 6.2 价值验证的关键信号

- 2026 年买家更关注 **"what works vs what's overhyped"**
- **build vs buy** 决策更谨慎
- 客服场景 ROI 最明确，coding 次之，其他垂类仍在验证

---

## 七、给我的 Takeaways（结合个人情况）

### 面试可用的弹药

1. **大模型分工**：Claude 强在 coding/prose，Gemini 强在 reasoning，GPT 综合 —— 谈模型选型有数据
2. **Anthropic Managed Agents 三件套**：scheduler + dreaming + outcome grading —— 谈 Agent 工程化趋势
3. **大厂内部 AI 反例**：Amazon 排行榜被刷爆、Microsoft token 成本失控 —— 谈"AI 落地难点"
4. **国内大厂分化**：字节娱乐互动 / 阿里消费 / 腾讯社交 / 百度搜索 —— 谈各家战略差异

### 工程师工作可立刻用的

1. **Skill 安装顺序**：skill-creator → planning-with-files → 代码格式化 → TDD skill
2. **Coding Agent 配置**：Cursor（混合 IDE）+ Claude Code（终端）双开
3. **SKILL.md 是开放标准**：一份 skill 可跨工具复用

### 待深挖的方向

- [ ] Anthropic **Dreaming pass** 的实现原理 —— 是否类似 ReAct + 反思？
- [ ] Coze 3.0 **多 Agent 协作**的具体编排方式 —— 是否可对标 LangGraph？
- [ ] **outcome grading** 的评分表设计 —— 如何避免 Goodhart 定律？

---

## 八、参考链接汇总

### 模型 / 平台
- [Introducing Gemini Enterprise Agent Platform (Google Cloud)](https://cloud.google.com/blog/products/ai-machine-learning/introducing-gemini-enterprise-agent-platform)
- [Anthropic 2026 全发布指南 (Linas Substack)](https://linas.substack.com/p/anthropic-claude-2026-every-launch-guide)
- [Code with Claude 2026: 5 New Agent Features (MindStudio)](https://www.mindstudio.ai/blog/code-with-claude-2026-new-agent-features)
- [Claude Platform Release Notes](https://platform.claude.com/docs/en/release-notes/overview)

### Coding Agent
- [Best AI Coding Agents 2026 (Coursiv)](https://coursiv.io/blog/best-ai-agents-for-coding-2026)
- [10 Best AI Coding Agents (Vellum)](https://www.vellum.ai/blog/best-ai-coding-agents)
- [State of AI Coding Agents 2026 (Medium)](https://medium.com/@dave-patten/the-state-of-ai-coding-agents-2026-from-pair-programming-to-autonomous-ai-teams-b11f2b39232a)

### 国内大厂
- [AI 入口之战：字节阿里赢了，百度腾讯输了？(36氪)](https://m.36kr.com/p/3697425974013571)
- [扣子 Coze 官网](https://www.coze.cn/)
- [火山引擎扣子企业版](https://www.volcengine.com/product/coze-pro)
- [企业 AI 用扣子](https://www.volcengine.com/product/coze-pro)

### 海外大厂内部
- [Microsoft Work Trend Index 2026](https://www.microsoft.com/en-us/worklab/work-trend-index/agents-human-agency-and-the-opportunity-for-every-organization)
- [Microsoft AI Token 成本问题 (Fortune)](https://fortune.com/2026/05/22/microsoft-ai-cost-problem-tokens-agents/)
- [Are Amazon, Microsoft, Meta Bankrolling AI with Layoffs? (LeadDev)](https://leaddev.com/ai/are-amazon-microsoft-and-meta-bankrolling-ai-with-layoffs)

### Claude Skills
- [anthropics/skills (GitHub)](https://github.com/anthropics/skills)
- [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills)
- [VoltAgent/awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills)
- [SkillsMP](https://skillsmp.com/)
- [10 个必装 Claude Code Skills 完全指南 (七牛云)](https://news.qiniu.com/archives/1773714153285)
- [研发场景十大热门 Skill 推荐 (TRAE)](https://docs.trae.cn/ide_top-10-recommended-skills-for-development-scenarios)

### 企业级 Agent
- [15 Best AI Agents for Enterprise 2026 (Rasa)](https://rasa.com/blog/best-ai-agents-for-enterprise)
- [10 AI Agent Use Cases (Sema4.ai)](https://sema4.ai/blog/ai-agent-use-cases/)
- [8 Best AI Agents for Customer Service 2026 (Kore.ai)](https://www.kore.ai/blog/top-ai-agents-for-customer-service-tested-reviewed)
