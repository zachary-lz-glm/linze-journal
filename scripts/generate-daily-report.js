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

// ─── 数据源：Hacker News ───

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

// ─── 数据源：GitHub 热门新项目 ───

async function collectGitHubTrending() {
  const since = new Date(Date.now() - 86400000).toISOString().split('T')[0];
  const data = await fetchJSON(
    `https://api.github.com/search/repositories?q=created:>${since}&sort=stars&order=desc&per_page=15`,
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

// ─── 数据源：RSS ───

function parseRSS(xml) {
  const items = [];
  for (const block of (xml.match(/<item[\s>][\s\S]*?<\/item>/gi) || []).slice(0, 10)) {
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
    } catch { /* 跳过不可用的源 */ }
  }
  return results;
}

// ─── 调用 DeepSeek ───

async function callDeepSeek(system, user, model = 'deepseek-v4-pro') {
  const models = [model, 'deepseek-v4-flash'];
  let lastErr;
  for (const m of models) {
    console.log(`  🤖 调用 ${m}...`);
    try {
      const res = await fetch(API_URL, {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${DEEPSEEK_API_KEY}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          model: m,
          messages: [
            { role: 'system', content: system },
            { role: 'user', content: user },
          ],
          temperature: 0.7,
          max_tokens: 4096,
        }),
        signal: AbortSignal.timeout(180000),
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

      console.log(`  ✅ ${m} 生成成功`);
      return content.replace(/^```(?:markdown)?\n?/i, '').replace(/\n?```\s*$/i, '');
    } catch (e) {
      console.error(`  ❌ ${m} 失败: ${e.message}`);
      lastErr = e;
    }
  }
  throw lastErr;
}

// ─── 生成日报 ───

async function generateDailyReport(hn, gh, rss, dateStr) {
  const system = `你是一位专注于 AI 工程化与前端技术的资深分析师。根据提供的实时数据和你的专业知识，生成一份高质量中文日报。

读者画像：前端工程师，关注 AI 工程化方向，正在准备面试，需要知道行业最新动态和技术趋势。

输出要求：
1. 总字数 1200-1800 字，术语保留英文
2. 分三个核心板块：AI 行业动态、前端技术趋势、招聘与职场
3. 每个板块 2-4 条，每条包含标题、摘要、影响分析
4. 额外板块：开源项目推荐（2-3 个）、今日信号（一句话）
5. 数据源中已有的信息优先使用，不足部分用你的知识补充
6. 不要入门科普，面向有经验的工程师`;

  const dataBlock = [
    `## Hacker News Top ${hn.length}`,
    ...hn.map((i, n) => `${n + 1}. [${i.score}↑ ${i.comments}评] ${i.title}\n   ${i.url}`),
    '',
    `## GitHub 热门新项目 (近 24h)`,
    ...gh.map((i, n) => `${n + 1}. ⭐${i.stars} [${i.lang}] ${i.name}: ${i.desc}\n   ${i.url}`),
    '',
    `## RSS 订阅`,
    ...rss.map((i, n) => `${n + 1}. [${i.source}] ${i.title}\n   ${i.desc}`),
  ].join('\n');

  const user = `今天是 ${dateStr}。以下是收集到的实时数据：

${dataBlock}

请生成日报，严格按以下格式输出（不要包裹在代码块中）：

# AI 情报日报 | ${dateStr}

> **今日概要**：一句话总结今天最值得关注的事情。

---

## 一、AI 行业动态

（2-4 条重要动态，每条格式：）
### N. 标题
- **摘要**：发生了什么
- **影响**：为什么值得关注
- **链接**：原文地址

---

## 二、前端技术趋势

（2-3 条前端相关动态，格式同上）

---

## 三、招聘与职场

（2-3 条前端/AI 相关的招聘趋势、面试变化、薪资动态。基于你的知识补充近期中国互联网大厂招聘动态。）

---

## 四、开源项目推荐

（从 GitHub 数据中选 2-3 个最值得关注的项目，简要说明价值和应用场景）

---

## 五、今日信号

> 用 1-2 句话总结今天最值得关注的行业信号。`;

  return callDeepSeek(system, user);
}

// ─── 生成周报 ───

async function generateWeeklyReport(weekPath, weekLabel) {
  // 收集本周所有日报内容
  const files = fs.readdirSync(weekPath).filter(f => f.startsWith('日报-') && f.endsWith('.md'));
  if (files.length === 0) {
    console.log('⏭️  本周无日报，跳过周报生成');
    return null;
  }

  const dailyContents = files.map(f => {
    const content = fs.readFileSync(path.join(weekPath, f), 'utf-8');
    return `=== ${f} ===\n${content}`;
  }).join('\n\n');

  const system = `你是一位专注于 AI 工程化与前端技术的资深分析师。根据本周的日报内容，提炼生成一份高质量中文周报。

读者画像：前端工程师，关注 AI 工程化方向，正在准备面试。

输出要求：
1. 总字数 1500-2500 字，术语保留英文
2. 从本周日报中提炼最重要的趋势和信号，去除重复信息
3. 分板块：本周核心事件回顾、技术趋势总结、招聘市场观察、下周关注点
4. 每个板块要有深度分析，不只是罗列
5. 面向有经验的工程师，不要入门科普`;

  const user = `以下是本周（${weekLabel}）的所有日报内容：

${dailyContents}

请生成周报，严格按以下格式输出（不要包裹在代码块中）：

# AI 情报周报 | ${weekLabel}

> **本周概要**：2-3 句话总结本周最重要的趋势。

---

## 一、本周核心事件

（3-5 条本周最重要的行业事件，每条包含标题、详细分析和影响评估）

---

## 二、技术趋势总结

（归纳本周出现的技术方向，分析趋势走向）

---

## 三、招聘市场观察

（总结本周招聘动态、薪资趋势、技能需求变化）

---

## 四、下周关注点

（预测下周可能的热点事件、产品发布、技术趋势）`;

  return callDeepSeek(system, user);
}

// ─── 更新侧边栏 ───

function updateSidebar() {
  const sidebarPath = path.join(path.dirname(AI_DIR), '_sidebar.md');
  const lines = fs.readFileSync(sidebarPath, 'utf-8').split('\n');

  // 找到 AI 情报板块的起止位置
  const aiStart = lines.findIndex(l => l.includes('AI 情报') || l.includes('AI情报'));
  if (aiStart < 0) return;

  // 找 AI 情报板块结束位置（下一个二级标题或同级别项）
  let aiEnd = lines.length;
  for (let i = aiStart + 1; i < lines.length; i++) {
    if (lines[i].match(/^  - \[/) && !lines[i].includes('AI情报') && !lines[i].includes('W20') && !lines[i].includes('W21') && !lines[i].includes('W22') && !lines[i].includes('周') && !lines[i].includes('日报') && !lines[i].includes('prompt') && !lines[i].includes('Prompt')) {
      // Check if this is already past the AI section
      // We look for items that are NOT weekly entries
    }
    if (lines[i].match(/^- \[/) && i > aiStart + 1) {
      aiEnd = i;
      break;
    }
  }

  // 扫描 AI情报 目录生成新的导航
  const weekDirs = fs.readdirSync(AI_DIR)
    .filter(d => d.match(/^\d{4}-W\d{2}$/) && fs.statSync(path.join(AI_DIR, d)).isDirectory())
    .sort()
    .reverse(); // 最新的在前面

  const newEntries = [];
  for (const week of weekDirs) {
    const weekPath = path.join(AI_DIR, week);
    newEntries.push(`  - **${week}**`);
    const files = fs.readdirSync(weekPath).filter(f => f.endsWith('.md')).sort().reverse();
    for (const f of files) {
      const label = f.startsWith('周报') ? `📰 周报` : `📄 ${f.replace('日报-', '').replace('.md', '')}`;
      newEntries.push(`    - [${label}](AI情报/${week}/${encodeURIComponent(f)})`);
    }
  }

  // 保留非 AI 情报相关的行，替换 AI 情报子项
  const before = lines.slice(0, aiStart + 1);
  const after = lines.slice(aiEnd);
  // 也保留 AI 情报标题后面到子项之前的内容
  fs.writeFileSync(sidebarPath, [...before, ...newEntries, ...after].join('\n'));
}

// ─── 主流程 ───

async function main() {
  const now = new Date();
  const pad = n => String(n).padStart(2, '0');
  const dateStr = `${now.getFullYear()}-${pad(now.getMonth() + 1)}-${pad(now.getDate())}`;
  const dayOfWeek = now.getDay(); // 0=Sun, 5=Fri
  const weekName = weekDirName(now);
  const weekPath = path.join(AI_DIR, weekName);

  // 确保周目录存在
  fs.mkdirSync(weekPath, { recursive: true });

  // ── 生成日报 ──
  const dailyFile = `日报-${dateStr.slice(5)}.md`; // e.g. 日报-05-27.md
  const dailyPath = path.join(weekPath, dailyFile);

  if (fs.existsSync(dailyPath)) {
    console.log(`⏭️  ${dateStr} 日报已存在，跳过`);
  } else {
    console.log(`📅 生成 ${dateStr} AI 情报日报 (目录: ${weekName})...\n`);

    console.log('📡 收集 Hacker News...');
    const hn = await collectHackerNews().catch(e => (console.log(`  ⚠️ ${e.message}`), []));
    console.log(`  ✅ ${hn.length} 条`);

    console.log('📡 收集 GitHub Trending...');
    const gh = await collectGitHubTrending().catch(e => (console.log(`  ⚠️ ${e.message}`), []));
    console.log(`  ✅ ${gh.length} 条`);

    console.log('📡 收集 RSS...');
    const rss = await collectRSS([
      { name: '机器之心', url: 'https://www.jiqizhixin.com/rss' },
      { name: 'HNRSS', url: 'https://hnrss.org/frontpage?count=15' },
      { name: 'dev.to', url: 'https://dev.to/feed' },
    ]);
    console.log(`  ✅ ${rss.length} 条`);

    const report = await generateDailyReport(hn, gh, rss, dateStr);
    fs.writeFileSync(dailyPath, report);
    console.log(`💾 已保存: AI情报/${weekName}/${dailyFile}`);
  }

  // ── 周五或周日自动生成周报 ──
  const weeklyFile = '周报.md';
  const weeklyPath = path.join(weekPath, weeklyFile);

  if (!fs.existsSync(weeklyPath)) {
    // 周五(5)、周六(6)、周日(0) 尝试生成周报
    if (dayOfWeek === 5 || dayOfWeek === 6 || dayOfWeek === 0) {
      console.log(`\n📊 今天是${['日','一','二','三','四','五','六'][dayOfWeek]}，尝试生成周报...`);
      const weeklyReport = await generateWeeklyReport(weekPath, weekName);
      if (weeklyReport) {
        fs.writeFileSync(weeklyPath, weeklyReport);
        console.log(`💾 已保存: AI情报/${weekName}/${weeklyFile}`);
      }
    }
  }

  // ── 更新侧边栏 ──
  updateSidebar();
  console.log('✅ 侧边栏已更新');

  console.log(`\n🎉 完成！`);
}

main().catch(e => {
  console.error('❌ 生成失败:', e);
  process.exit(1);
});
