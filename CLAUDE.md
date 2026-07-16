# CLAUDE.md

## Project Context

Personal knowledge base & interview prep site, deployed to GitHub Pages.

- **Tech Stack**: Self-contained HTML/CSS/JS (no build tools, no framework)
- **Key Files**: `index.html` (main page), `sw.js` (Service Worker offline cache), `_sidebar.md` (navigation)
- **Content**: `learning/` (interview, interview-tools), `reviews/` (面试实战记录: qa, transcripts), `archive/` (retrospectives 项目复盘 + interactive tools)
- **Deploy**: Push to `main` → GitHub Pages auto-deploys
- **Cache**: 每次部署后必须 bump `sw.js` 的 `CACHE_NAME`（kb-vN → kb-vN+1），否则 Service Worker 会给访客返回旧缓存
- **Git**: Use personal GitHub account, not company account

## 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

## 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

## 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

## 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:
```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

---

**These guidelines are working if:** fewer unnecessary changes in diffs, fewer rewrites due to overcomplication, and clarifying questions come before implementation rather than after mistakes.

---

## 5. stealth.html 卡片（面试手机速查页 · 核心资产）

`learning/interview-tools/stealth.html` 是面试中手机速查用的单页。**改它前必读 `learning/interview-tools/STEALTH-CARDS-GUIDE.md`**（完整方法论 + 卡片模板 + 踩坑记录）。铁律：

- **语气口语化**：第一人称、像真懂项目的人在聊天；禁速查表腔（"必背 / 杀手锏 / 被问 X 必答 / ①②③ / 金句钩子"），少滥用 `<strong>`。不用太工整。
- **标题不带英文项目名前缀**（"Manager_Agent xxx" 会让侧边栏索引没法看）。
- **数字必须核对源码**：Agent 项目查 `D:/work/agent-main/`，再对照 `learning/interview-kb/明日面试_预测题校准与匹配分析.md`。简历话术 / AI 生成的"预测答案"里的百分比、倍数、团队规模**大多编造**，不确定就软化（"小范围验证过"）或省略。
- **分组用 `data-g` 显式挂**（getGroup 开头 `if(c.dataset.g)return c.dataset.g`），别依赖 tag 的 textContent——曾因 `class="tag Manager"` 的 textContent 是 "M0" 导致 39 张卡全错位。
- 改完**必须 bump `sw.js` 的 `CACHE_NAME`**（kb-vN → kb-vN+1），否则 Service Worker 给访客旧缓存。
- 大改动走多 agent 流程（每子模块一个 agent 读源+校准+铁律产 HTML，主会话组装），见指南 §3。
