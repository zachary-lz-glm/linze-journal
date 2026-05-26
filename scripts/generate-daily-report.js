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
const MODEL = 'deepseek-v4-pro';
const ROOT = path.resolve(__dirname, '..');

// ─── 工具函数 ───

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

// ─── 调用 DeepSeek 生成报告 ───

async function generateReport(hn, gh, rss, dateStr) {
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

  const res = await fetch(API_URL, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${DEEPSEEK_API_KEY}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      model: MODEL,
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
    throw new Error(`DeepSeek API ${res.status}: ${err}`);
  }

  const data = await res.json();
  const content = data.choices?.[0]?.message?.content;
  if (!content) throw new Error('DeepSeek 返回内容为空');

  // 去掉可能的 markdown 代码块包裹
  return content.replace(/^```(?:markdown)?\n?/i, '').replace(/\n?```\s*$/i, '');
}

// ─── 更新侧边栏 ───

function updateSidebar(filename, title) {
  const p = path.join(ROOT, '_sidebar.md');
  const lines = fs.readFileSync(p, 'utf-8').split('\n');
  const entry = `  - [${title}](AI情报/${filename})`;

  // 避免重复
  if (lines.some(l => l.includes(filename))) return;

  // 在 "AI 日报 prompt" 行之前插入
  const idx = lines.findIndex(l => l.includes('AI 日报 prompt'));
  if (idx > 0) {
    lines.splice(idx, 0, entry);
    fs.writeFileSync(p, lines.join('\n'));
  }
}

// ─── 主流程 ───

async function main() {
  const now = new Date();
  const pad = n => String(n).padStart(2, '0');
  const dateStr = `${now.getFullYear()}-${pad(now.getMonth() + 1)}-${pad(now.getDate())}`;
  const filename = `${dateStr}-日报.md`;
  const filepath = path.join(ROOT, 'AI情报', filename);

  // 跳过已存在的日报
  if (fs.existsSync(filepath)) {
    console.log(`⏭️  ${dateStr} 日报已存在，跳过`);
    return;
  }

  console.log(`📅 生成 ${dateStr} AI 情报日报...\n`);

  // 1. 收集数据
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

  // 2. 生成报告
  console.log('\n🤖 调用 DeepSeek V4-Pro 生成日报...');
  const report = await generateReport(hn, gh, rss, dateStr);

  // 3. 保存文件
  fs.writeFileSync(filepath, report);
  console.log(`💾 已保存: AI情报/${filename}`);

  // 4. 更新侧边栏
  updateSidebar(filename, `日报 ${dateStr}`);
  console.log('✅ 侧边栏已更新');

  console.log(`\n🎉 ${dateStr} AI 情报日报生成完成！`);
}

main().catch(e => {
  console.error('❌ 生成失败:', e);
  process.exit(1);
});
