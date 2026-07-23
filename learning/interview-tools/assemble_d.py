#!/usr/bin/env python3
"""D 深挖卡:把 4 张新深挖卡(完整 card)插到各自主陈述卡正后方。原子写。
锚点:主卡 card-title 子串(唯一)→ 定位主卡开标签 → depth 数到主卡闭合 </div> → 在其后插入新卡。"""
import re, os, sys

ROOT = "/Users/didi/work/linze-journal/learning/interview-tools/"
HTML = ROOT + "stealth.html"

# (主卡 card-title 子串, 新卡 fragment 文件)
INSERTS = [
    ("最有价值的项目：Schema 营销中台", ".d-front.html"),   # 前端项目
    ("这个项目 30 秒怎么说", ".d-mgr.html"),                # Manager 智能体
    ("这个 Code Agent 到底是什么", ".d-code.html"),         # Code 智能体 (修正:brief 原文漏 "这个 " 前缀,据 .d-anchors.txt L14 + brief Step3 verify grep 校正)
    ("AI工作流完整介绍", ".d-prd.html"),                    # PRD 工作流
]

html = open(HTML, encoding="utf-8").read()
problems = []

for title_sub, frag in INSERTS:
    pat = 'card-title">' + title_sub
    idxs = [m.start() for m in re.finditer(re.escape(pat), html)]
    if len(idxs) != 1:
        problems.append((frag, f"主卡锚点匹配{len(idxs)}次,应1: {title_sub!r}")); continue
    tidx = idxs[0]
    o = html.rfind('<div class="card"', 0, tidx)
    if o < 0:
        problems.append((frag, "找不到主卡开标签")); continue
    # depth 数到主卡闭合
    depth, i, close_end = 0, o, None
    while i < len(html):
        if html[i:i+4] == '<div':
            depth += 1; i = html.find('>', i) + 1
        elif html[i:i+6] == '</div>':
            depth -= 1; i += 6
            if depth == 0:
                close_end = i; break
        else:
            i += 1
    if close_end is None:
        problems.append((frag, "主卡未闭合")); continue
    new_card = open(ROOT + frag, encoding="utf-8").read().strip()
    if not new_card.startswith('<div class="card"'):
        problems.append((frag, "片段非完整 card")); continue
    if new_card.count('<div') != new_card.count('</div>'):
        problems.append((frag, "片段 div 不平衡")); continue
    html = html[:close_end] + "\n" + new_card + "\n" + html[close_end:]
    print(f"插入: {frag} → 主卡「{title_sub}」后")

if problems:
    print("❌ 锚点/片段问题,未写文件:")
    for f, p in problems: print(f"  - {f}: {p}")
    sys.exit(1)

assert html.count('<div') == html.count('</div>'), f"全文 div 不平衡: {html.count('<div')}/{html.count('</div>')}"
assert '<script>' in html and '</script>' in html, "script 残缺"
tmp = HTML + ".tmp"
open(tmp, "w", encoding="utf-8").write(html)
os.replace(tmp, HTML)
print("✅ D 4 张深挖卡插入完成")
