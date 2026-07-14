#!/usr/bin/env node
// 将手机速查页 stealth.html 导出为飞书友好的 Markdown 题库（面试速查题库.md）。
// 用法：node export-md.mjs   （stealth.html 更新后重跑即可刷新题库）
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const SRC = path.join(__dirname, 'stealth.html');
const OUT = path.join(__dirname, '面试速查题库.md');
const html = fs.readFileSync(SRC, 'utf8');
const BR = "\uE000"; // <br> 占位符（私有区字符，源码用转义保证可见且不为空）

function decodeEntities(s) {
  return s
    .replace(/&lt;/g, '<').replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"').replace(/&#39;/g, "'").replace(/&apos;/g, "'")
    .replace(/&nbsp;/g, ' ').replace(/&mdash;/g, '—').replace(/&hellip;/g, '…')
    .replace(/&amp;/g, '&'); // amp 最后
}

// 行内：strong/b → **, code → `, em → *, br → 软换行, 去残留标签
function inline(s) {
  let t = s.replace(/<br\s*\/?>/gi, BR);
  t = t.replace(/<strong(?:\s[^>]*)?>([\s\S]*?)<\/strong>/gi, '**$1**');
  t = t.replace(/<b>([\s\S]*?)<\/b>/gi, '**$1**');
  t = t.replace(/<code>([\s\S]*?)<\/code>/gi, '`$1`');
  t = t.replace(/<em>([\s\S]*?)<\/em>/gi, '*$1*');
  t = decodeEntities(t);
  t = t.replace(/<[a-zA-Z/!][^>]*>/g, ''); // 只删真实标签(<字母开头)，保护 < 比较运算
  t = t.replace(/\n/g, ' '); // 源码换行折叠为空格
  t = t.replace(new RegExp(BR, 'g'), '  \n'); // br → md 软换行
  t = t.replace(/\s{2,}/g, ' ');
  return t.trim();
}

function renderList(ulHtml) {
  const items = [];
  const liRe = /<li(?:\s[^>]*)?>([\s\S]*?)<\/li>/gi;
  let m;
  while ((m = liRe.exec(ulHtml)) !== null) items.push('- ' + inline(m[1]));
  return items.join('\n');
}

function renderTable(tableHtml) {
  const rows = [];
  const trRe = /<tr[^>]*>([\s\S]*?)<\/tr>/gi;
  let m;
  while ((m = trRe.exec(tableHtml)) !== null) {
    const cells = [];
    const cellRe = /<t[hd][^>]*>([\s\S]*?)<\/t[hd]>/gi;
    let c;
    while ((c = cellRe.exec(m[1])) !== null) cells.push(inline(c[1]).replace(/\|/g, '\\|'));
    if (cells.length) rows.push(cells);
  }
  if (!rows.length) return '';
  const col = Math.max(...rows.map(r => r.length));
  rows.forEach(r => { while (r.length < col) r.push(''); });
  let out = '| ' + rows[0].join(' | ') + ' |\n';
  out += '| ' + rows[0].map(() => '---').join(' | ') + ' |\n';
  for (const r of rows.slice(1)) out += '| ' + r.join(' | ') + ' |\n';
  return out;
}

function renderCode(codeHtml) {
  // 去格式标签(留文字)但保留 < > 运算符 —— 只剥 strong/b/code/em/span 成对标签
  let t = codeHtml.replace(/<\/?(strong|b|code|em|span|i)\b[^>]*>/gi, '');
  t = decodeEntities(t);
  return '```\n' + t.replace(/^\n+/, '').replace(/\n+$/, '') + '\n```';
}

// pre-body: 保留换行（white-space:pre-line），行内标签照转
function renderPre(preHtml) {
  let t = preHtml.replace(/<strong(?:\s[^>]*)?>([\s\S]*?)<\/strong>/gi, '**$1**');
  t = t.replace(/<code>([\s\S]*?)<\/code>/gi, '`$1`');
  t = t.replace(/<br\s*\/?>/gi, '\n');
  t = decodeEntities(t).replace(/<[a-zA-Z/!][^>]*>/g, '');
  return t.split('\n').map(l => l.trim()).filter(Boolean).join('  \n').trim();
}

function parseCard(cardHtml) {
  const tagM = cardHtml.match(/<span class="tag[^"]*"[^>]*>([\s\S]*?)<\/span>/);
  const tag = tagM ? decodeEntities(tagM[1]).trim() : '';
  const titleM = cardHtml.match(/<div class="card-title">([\s\S]*?)<\/div>/);
  const title = titleM ? inline(titleM[1]) : '(无标题)';
  const blocks = [];
  const add = (re, kind) => {
    const r = new RegExp(re, 'g'); let m;
    while ((m = r.exec(cardHtml)) !== null) blocks.push({ idx: m.index, kind, text: m[1] });
  };
  add(/<div class="core">([\s\S]*?)<\/div>/, 'core');
  add(/<p(?:\s[^>]*)?>([\s\S]*?)<\/p>/, 'p');
  add(/<ul class="points">([\s\S]*?)<\/ul>/, 'ul');
  add(/<table>([\s\S]*?)<\/table>/, 'table');
  add(/<div class="pre-body">([\s\S]*?)<\/div>/, 'pre');
  add(/<div class="code-blk">([\s\S]*?)<\/div>/, 'code');
  blocks.sort((a, b) => a.idx - b.idx);
  return { tag, title, blocks };
}

function renderCard(card) {
  let out = '';
  const prefix = card.tag ? `**[${card.tag}]** ` : '';
  out += `### ${prefix}${card.title}\n\n`;
  for (const b of card.blocks) {
    if (b.kind === 'core') {
      const c = inline(b.text).replace(/  \n/g, '\n> ');
      out += `> ${c}\n\n`;
    } else if (b.kind === 'p') out += `${inline(b.text)}\n\n`;
    else if (b.kind === 'ul') out += `${renderList(b.text)}\n\n`;
    else if (b.kind === 'table') out += `${renderTable(b.text)}\n\n`;
    else if (b.kind === 'pre') out += `${renderPre(b.text)}\n\n`;
    else if (b.kind === 'code') out += `${renderCode(b.text)}\n\n`;
  }
  return out;
}

// —— 主流程：按 index 收集 章节注释 + 卡片 ——
const scriptIdx = html.indexOf('<script');
const upper = scriptIdx > 0 ? scriptIdx : html.length;

const events = [];
const secRe = /<!--\s*=+\s*(.+?)\s*=+\s*-->/g;
let m;
while ((m = secRe.exec(html)) !== null) {
  const title = m[1].replace(/=+$/g, '').replace(/^=+/, '').trim();
  // 跳过纯结束/完结标记（如"防御卡结束"），它们不是章节
  if (title && !/(结束|完结|END)$/.test(title)) events.push({ idx: m.index, type: 'sec', title });
}

const starts = [];
const cr = /<div class="card[\s"]/g;
while ((m = cr.exec(html)) !== null) starts.push(m.index);
for (let i = 0; i < starts.length; i++) {
  const s = starts[i];
  const e = i + 1 < starts.length ? Math.min(starts[i + 1], upper) : upper;
  events.push({ idx: s, type: 'card', card: parseCard(html.slice(s, e)) });
}
events.sort((a, b) => a.idx - b.idx);

let md = `# 面试速查题库\n\n`;
md += `> 来源：手机速查页 stealth.html · 共 ${starts.length} 张卡 · 按原页章节顺序整理\n\n`;
md += `---\n\n`;
let secCount = 0;
for (const ev of events) {
  if (ev.type === 'sec') { md += `## ${ev.title}\n\n`; secCount++; }
  else md += renderCard(ev.card);
}
md = md.replace(/\n{3,}/g, '\n\n');

fs.writeFileSync(OUT, md);
console.log(`✅ 导出完成`);
console.log(`   章节: ${secCount}  卡片: ${starts.length}`);
console.log(`   输出: ${OUT}`);
console.log(`   大小: ${(fs.statSync(OUT).size / 1024).toFixed(1)} KB`);
