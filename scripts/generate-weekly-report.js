#!/usr/bin/env node
'use strict';

const fs = require('fs');
const path = require('path');

const DEEPSEEK_API_KEY = process.env.DEEPSEEK_API_KEY;
if (!DEEPSEEK_API_KEY) {
  console.error('❌ 缺少 DEEPSEEK_API_KEY 环境变量');
  process.exit(1);
}

const API_URL = 'https://api.deepseek.com/chat/completions';
const AI_DIR = path.resolve(__dirname, '..', 'AI情报');

// ─── 工具函数 ───

function getISOWeek(date) {
  const d = new Date(Date.UTC(date.getFullYear(), date.getMonth(), date.getDate()));
  const dayNum = d.getUTCDay() || 7;
  d.setUTCDate(d.getUTCDate() + 4 - dayNum);
  const yearStart = new Date(Date.UTC(d.getUTCFullYear(), 0, 1));
  const weekNo = Math.ceil(((d - yearStart) / 86400000 + 1) / 7);
  return { year: d.getUTCFullYear(), week: weekNo };
}

function weekDirName(date) {
  const { year, week } = getISOWeek(date);
  return `${year}-W${String(week).padStart(2, '0')}`;
}

async function fetchJSON(url, timeout = 15000) {
  const res = await fetch(url, { signal: AbortSignal.timeout(timeout) });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}

async function fetchText(url, timeout = 15000) {
  const res = await fetch(url, { signal: AbortSignal.timeout(timeout) });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.text();
}

// ─── 数据源 ───

async function collectHackerNews(limit = 20) {
  const ids = await fetchJSON('https://hacker-news.firebaseio.com/v0/topstories.json');
  const items = await Promise.all(
    ids.slice(0, limit).map(id =>
      fetchJSON(`https://hacker-news.firebaseio.com/v0/item/${id}.json`).catch(() => null)
    )
  );
  return items.filter(Boolean).map(i => ({
    title: i.title,
    url: i.url || `https://news.ycombinator.com/item?id=${i.id}`,
    score: i.score,
    comments: i.descendants || 0,
  }));
}

async function collectGitHubTrending() {
  const since = new Date(Date.now() - 7 * 86400000).toISOString().split('T')[0];
  const data = await fetchJSON(
    `https://api.github.com/search/repositories?q=created:>${since}&sort=stars&order=desc&per_page=20`,
    20000
  );
  return (data.items || []).map(r => ({
    name: r.full_name,
    desc: r.description || '',
    stars: r.stargazers_count,
    lang: r.language || '',
    url: r.html_url,
  }));
}

function parseRSS(xml) {
  const items = [];
  for (const block of (xml.match(/<item[\s>][\s\S]*?<\/item>/gi) || []).slice(0, 15)) {
    const tag = t => {
      const m = block.match(new RegExp(`<${t}[^>]*>([\\s\\S]*?)<\\/${t}>`, 'i'));
      return m ? m[1].replace(/<!\[CDATA\[([\s\S]*?)\]\]>/, '$1').replace(/<[^>]+>/g, '').trim() : '';
    };
    const title = tag('title');
    if (title) items.push({ title, link: tag('link'), desc: tag('description').slice(0, 200) });
  }
  return items;
}

async function collectRSS(feeds) {
  const results = [];
  for (const { name, url } of feeds) {
    try {
      const items = parseRSS(await fetchText(url));
      results.push(...items.map(i => ({ ...i, source: name })));
    } catch { /* skip */ }
  }
  return results;
}

async function collectAllData() {
  console.log('📡 收集 Hacker News...');
  const hn = await collectHackerNews().catch(e => (console.log(`  ⚠️ ${e.message}`), []));
  console.log(`  ✅ ${hn.length} 条`);

  console.log('📡 收集 GitHub Trending（近 7 天）...');
  const gh = await collectGitHubTrending().catch(e => (console.log(`  ⚠️ ${e.message}`), []));
  console.log(`  ✅ ${gh.length} 条`);

  console.log('📡 收集 RSS...');
  const rss = await collectRSS([
    { name: '机器之心', url: 'https://www.jiqizhixin.com/rss' },
    { name: 'HNRSS', url: 'https://hnrss.org/frontpage?count=15' },
    { name: 'dev.to', url: 'https://dev.to/feed' },
  ]);
  console.log(`  ✅ ${rss.length} 条`);

  return { hn, gh, rss };
}

function formatDataBlock(hn, gh, rss) {
  return [
    `## Hacker News Top ${hn.length}`,
    ...hn.map((i, n) => `${n + 1}. [${i.score}↑ ${i.comments}评] ${i.title}\n   ${i.url}`),
    '',
    `## GitHub 热门新项目 (近 7 天)`,
    ...gh.map((i, n) => `${n + 1}. ⭐${i.stars} [${i.lang}] ${i.name}: ${i.desc}\n   ${i.url}`),
    '',
    `## RSS 订阅`,
    ...rss.map((i, n) => `${n + 1}. [${i.source}] ${i.title}\n   ${i.desc}`),
  ].join('\n');
}

// ─── 调用 DeepSeek ───

async function callDeepSeek(system, user) {
  const models = ['deepseek-v4-pro', 'deepseek-v4-flash'];
  let lastErr;
  for (const model of models) {
    console.log(`  🤖 调用 ${model}...`);
    try {
      const res = await fetch(API_URL, {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${DEEPSEEK_API_KEY}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          model,
          messages: [
            { role: 'system', content: system },
            { role: 'user', content: user },
          ],
          temperature: 0.7,
          max_tokens: 8192,
        }),
        signal: AbortSignal.timeout(300000),
      });

      if (!res.ok) {
        const err = await res.text();
        throw new Error(`API ${res.status}: ${err}`);
      }

      const data = await res.json();
      const choice = data.choices?.[0];
      const content = choice?.message?.content;

      if (!content) {
        const reason = choice?.finish_reason || 'unknown';
        const refusal = choice?.message?.refusal;
        console.error('⚠️ 原始响应:', JSON.stringify(data, null, 2).slice(0, 2000));
        throw new Error(`返回内容为空 (finish_reason=${reason}, refusal=${refusal || 'none'})`);
      }

      console.log(`  ✅ ${model} 生成成功`);
      return content.replace(/^```(?:markdown)?\n?/i, '').replace(/\n?```\s*$/i, '');
    } catch (e) {
      console.error(`  ❌ ${model} 失败: ${e.message}`);
      lastErr = e;
    }
  }
  throw lastErr;
}

// ─── 生成周报（全景趋势扫描） ───

async function generateWeeklyReport(hn, gh, rss, weekLabel) {
  const dataBlock = formatDataBlock(hn, gh, rss);

  const system = `你是一位企业级 AI 工程化领域的资深研究分析师。你的任务是帮我生成一份「AI 工程化周度深度研报」。

### 我是谁

- 一名前端工程师，研究方向是企业级 AI 工程化
- 日常工作涉及 AI Coding 工具链（Claude Code / MCP / Skills）、Agent 编排、RAG 系统、PRD 自动化
- 关注前沿的目的是：学习新技术、工作中直接复用成熟方案、面试中展示信息差优势
- 周报的目的和日报不同——日报看"发生了什么"，周报看"趋势往哪走"

### 信息源要求

1. 基于提供的数据和你的知识进行分析
2. 对关键数据点（百分比、star 数、融资金额等）标注数据来源可信度

### 筛选标准

❌ 跳过：纯观点/评论，没有事实支撑的
❌ 跳过：与"企业级AI工程化"无关的消费级/娱乐级 AI 动态

✅ 重点筛选：
- 本周出现的新趋势/新模式（日报可能只看到单个事件，周报要识别模式）
- 多个独立事件指向同一个方向时（= 强信号）
- 有具体技术细节的架构设计/方案实现
- 有量化数据支撑的结论
- 面试中可以作为系统性回答输出的知识点（标注 ⭐）`;

  const user = `以下是本周（${weekLabel}）收集到的行业数据：

${dataBlock}

请结合以上数据和你的专业知识，生成周报。严格按以下格式输出（不要包裹在代码块中），总字数 2000-3000 字（中文），术语保留英文原文：

# AI 工程化周报 | ${weekLabel}

> **本周定调**：一句话概括本周 AI 工程化领域最重要的变化方向

---

## 一、趋势研判（2-4 条）

这是周报的核心。每条趋势不是单个事件的搬运，而是从多个事件中提炼出的方向性判断。

每条趋势包含：

**趋势名称**
- 本周信号：哪 2-3 个独立事件指向这个方向（各附链接）
- 为什么重要：对企业级 AI 工程化的影响
- 成熟度评估：🔬 研究阶段 / 🏗️ 早期实践 / ✅ 可生产使用 / 📦 已有成熟方案
- 行动建议：我接下来应该做什么（具体动作，不要写"持续关注"）
- 面试话术：如何在面试中 30 秒讲清楚这个趋势 ⭐

---

## 二、本周最值得关注的项目/工具（1-3 个）

不是简单列 star 数，而是回答"我什么场景下会用它"：

| 维度 | 内容 |
|------|------|
| 名称 + 链接 | |
| 一句话定位 | 不是"XX是一个YY框架"，而是"解决XX痛点的YY方案" |
| 核心创新点 | 与现有方案的差异，不是功能列表 |
| 适用场景 | 我在什么具体场景下会选择它而不是现有工具 |
| 上手成本 | 预估学习曲线 |

---

## 三、架构/方案速写（0-1 个）

如果本周出现了一个值得学习的架构设计或技术方案，用通俗语言讲清楚：

**方案名称**
- 解决什么问题
- 核心设计思路（用图/伪代码/类比说明，不要贴大段源码）
- 关键 trade-off（它牺牲了什么换来了什么）
- 与我当前技术栈的结合点

如果没有特别值得展开的方案，这一节直接省略。

---

## 四、面试弹药库（1-3 个）⭐

本周积累的、可以在面试中直接使用的技术知识点或行业洞察：

每个知识点：
- **问题形式**：面试官可能会怎么问
- **30秒回答**：核心观点 + 一个数据/案例支撑
- **深入追问准备**：如果面试官追问细节，我能展开讲什么

---

## 五、数据看板

本周出现的关键数据，按主题分组：

\`\`\`
模型/基础设施
  指标 — 数值 — 来源

工具链/生态
  指标 — 数值 — 来源

企业采用/市场
  指标 — 数值 — 来源
\`\`\`

---

## 六、下周值得关注

1-3 个预告性事件或下周预期会出结果的动态：
- 事件 + 预计时间 + 关注理由

### 自检清单
1. ✅ 趋势研判是否有多事件交叉支撑？
2. ✅ 「行动建议」是否具体到"下周可以做 X"？
3. ✅ 面试话术是否真的能在 30 秒内讲完？
4. ✅ 数据点是否标注了来源？
5. ✅ 总字数在 2000-3000 字之间？`;

  return callDeepSeek(system, user);
}

// ─── 更新侧边栏 ───

function updateSidebar() {
  const sidebarPath = path.join(path.dirname(AI_DIR), '_sidebar.md');
  const lines = fs.readFileSync(sidebarPath, 'utf-8').split('\n');

  const aiStart = lines.findIndex(l => l.includes('AI 情报') || l.includes('AI情报'));
  if (aiStart < 0) return;

  let aiEnd = lines.length;
  for (let i = aiStart + 1; i < lines.length; i++) {
    if (lines[i].match(/^- \*\*/) && i > aiStart + 1) {
      aiEnd = i;
      break;
    }
  }

  const weekDirs = fs.readdirSync(AI_DIR)
    .filter(d => d.match(/^\d{4}-W\d{2}$/) && fs.statSync(path.join(AI_DIR, d)).isDirectory())
    .sort()
    .reverse();

  const newEntries = [];
  for (const week of weekDirs) {
    const weekPath = path.join(AI_DIR, week);
    newEntries.push(`  - **${week}**`);
    const files = fs.readdirSync(weekPath).filter(f => f.endsWith('.md')).sort().reverse();
    for (const f of files) {
      const label = f.startsWith('周报') ? '📰 周报' : `📄 ${f.replace('日报-', '').replace('.md', '')}`;
      newEntries.push(`    - [${label}](AI情报/${week}/${encodeURIComponent(f)})`);
    }
  }

  const before = lines.slice(0, aiStart + 1);
  const after = lines.slice(aiEnd);
  fs.writeFileSync(sidebarPath, [...before, ...newEntries, ...after].join('\n'));
}

// ─── 主流程 ───

async function main() {
  const now = new Date();
  const weekName = weekDirName(now);
  const weekPath = path.join(AI_DIR, weekName);

  fs.mkdirSync(weekPath, { recursive: true });

  const weeklyPath = path.join(weekPath, '周报.md');

  if (fs.existsSync(weeklyPath)) {
    console.log(`⏭️  ${weekName} 周报已存在，跳过`);
  } else {
    console.log(`📊 生成 ${weekName} 周报（全景趋势扫描）...\n`);

    const { hn, gh, rss } = await collectAllData();
    const report = await generateWeeklyReport(hn, gh, rss, weekName);

    fs.writeFileSync(weeklyPath, report);
    console.log(`💾 已保存: AI情报/${weekName}/周报.md`);
  }

  updateSidebar();
  console.log('✅ 侧边栏已更新');
  console.log('\n🎉 完成！');
}

main().catch(e => {
  console.error('❌ 生成失败:', e);
  process.exit(1);
});
