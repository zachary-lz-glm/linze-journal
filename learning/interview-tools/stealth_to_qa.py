#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
把 stealth.html（面试手机速查页，唯一真相源）导出成 Excel/知识库可读的「问答表」CSV。

用法： python stealth_to_qa.py [stealth.html 路径] [输出 csv 路径]
默认： stealth.html 同目录 → ../interview-kb/stealth-面试问答库.csv

列： 问题 | 答案（答案 = 核心一句话 + 空行 + 详细回答）
编码： utf-8-sig（带 BOM，Excel 直接双击中文不乱码）

每张 <div class="card" data-c=.. data-g=.. data-kw=..> 一行；
问题=card-title，答案=core + card-body 文本（按 <p>/列表/代码块分行）。
"""
import os, re, sys, csv, html

SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "stealth.html")
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(SRC), "..", "interview-kb", "stealth-面试问答库.csv")

CAT_CN = {"open": "开场", "proj": "项目", "bagu": "基础", "code": "手撕", "ai": "AI", "emer": "综合"}

with open(SRC, "r", encoding="utf-8") as f:
    doc = f.read()

# 定位卡片容器范围（<div class="container" id="cards"> ... 后到 <script>），避免误吃 quickbar/script 里的 div
m_container = re.search(r'<div class="container"[^>]*id="cards"[^>]*>', doc)
m_script = re.search(r'<script>', doc)
start = m_container.end() if m_container else 0
end = m_script.start() if m_script and m_script.start() > start else len(doc)
scope = doc[start:end]

# 找每张卡的起始标签：<div class="card ..." ...>
card_re = re.compile(r'<div class="card(?:\s[^"]*)?"([^>]*)>')
cards = []
for mm in card_re.finditer(scope):
    attrs = mm.group(1)
    tag_open_end = mm.end()
    # 提取 data-c / data-g / data-kw
    dc = re.search(r'data-c="([^"]*)"', attrs)
    dg = re.search(r'data-g="([^"]*)"', attrs)
    dkw = re.search(r'data-kw="([^"]*)"', attrs)
    if not dc:
        continue
    # 从 tag_open_end 起，按 <div> 深度找到本卡闭合 </div>
    depth = 1
    i = tag_open_end
    pos = tag_open_end
    scan_re = re.compile(r'<div\b[^>]*>|</div\s*>')
    found_end = None
    for sm in scan_re.finditer(scope, pos):
        if sm.group(0).startswith("</div"):
            depth -= 1
        else:
            depth += 1
        if depth == 0:
            found_end = sm.start()
            break
    if found_end is None:
        continue
    block = scope[tag_open_end:found_end]
    cards.append({
        "c": dc.group(1) if dc else "",
        "g": dg.group(1) if dg else "",
        "kw": dkw.group(1) if dkw else "",
        "block": block,
    })

def text_of(block, cls):
    """取某 class 的 div 内部纯文本（取第一个匹配）。"""
    m = re.search(r'<div class="%s"[^>]*>(.*?)</div>' % re.escape(cls), block, re.S)
    if not m:
        return ""
    return m.group(1)

def strip_tags(s):
    s = re.sub(r'<br\s*/?>', '\n', s)
    s = re.sub(r'</p>', '\n', s)
    s = re.sub(r'<p[^>]*>', '', s)
    s = re.sub(r'</li>', '\n', s)
    s = re.sub(r'<li[^>]*>', '- ', s)
    s = re.sub(r'<strong[^>]*>', '【', s)
    s = re.sub(r'</strong>', '】', s)
    s = re.sub(r'<code[^>]*>|</code>', '`', s)
    s = re.sub(r'<[^>]+>', '', s)            # 去剩余标签
    s = html.unescape(s)
    s = re.sub(r'[ \t]+', ' ', s)
    s = re.sub(r'\n{3,}', '\n\n', s)
    return s.strip()

rows = []
idx = 0
for c in cards:
    title_m = re.search(r'<div class="card-title"[^>]*>(.*?)</div>', c["block"], re.S)
    core_m = re.search(r'<div class="core"[^>]*>(.*?)</div>', c["block"], re.S)
    body_html = text_of(c["block"], "card-body")
    title = html.unescape(re.sub(r'<[^>]+>', '', title_m.group(1))).strip() if title_m else ""
    core = html.unescape(re.sub(r'<[^>]+>', '', core_m.group(1))).strip() if core_m else ""
    body = strip_tags(body_html)
    idx += 1
    # 答案 = 核心一句话 + 空行 + 详细回答（两列版）
    if core and body:
        answer = core + "\n\n" + body
    elif core:
        answer = core
    else:
        answer = body
    rows.append([title, answer])

os.makedirs(os.path.dirname(os.path.abspath(OUT)), exist_ok=True)
with open(OUT, "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f)
    w.writerow(["问题", "答案"])
    w.writerows(rows)

# 统计
print("导出完成：%d 张卡（2 列：问题/答案） → %s" % (len(rows), OUT))
# 抽查 5 张高 ROI 新增卡
roi = ["大厂稳定", "日常用哪些 AI", "为创业团队设计", "Agent Safety", "向量召回 vs"]
print("\n=== 高 ROI 新增卡抽查 ===")
for r in rows:
    if any(k in r[0] for k in roi):
        print("  Q: %s\n     A: %s" % (r[0], (r[1][:50] + "…")))
