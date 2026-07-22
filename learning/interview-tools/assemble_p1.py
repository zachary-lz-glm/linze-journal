#!/usr/bin/env python3
"""组装 P1 弹药卡:把 5 个产物文件的 69 张新 card-body,按 card-title 子串锚点
替换进 stealth.html(只换 card-body,不动 data-g/subOrder/title/core)。原子写。
产物用 <!-- P1CARD: {子串} --> ... <!-- /P1CARD --> 标记,内含完整新 card-body。
锚点:子串必须在某 card-title 内且唯一(避免短子串在 body 里误匹配)。
原文 card-body 用深度 div 匹配切分(避免嵌套 div 截断)。"""
import re, sys

HTML = "learning/interview-tools/stealth.html"
PROD = ["learning/interview-tools/.p1-mgr.html",
        "learning/interview-tools/.p1-code.html",
        "learning/interview-tools/.p1-prd-up.html",
        "learning/interview-tools/.p1-prd-down.html",
        "learning/interview-tools/.p1-tech.html"]

# 1. 解析产物: 子串 -> 新 card-body(P1CARD 标记间内容,含完整 <div class="card-body">...</div>)
new_bodies = {}
for f in PROD:
    txt = open(f, encoding="utf-8").read()
    for m in re.finditer(r"<!-- P1CARD: (.+?) -->(.*?)<!-- /P1CARD -->", txt, re.S):
        sub = m.group(1).strip()
        new_bodies[sub] = m.group(2).strip()

html = open(HTML, encoding="utf-8").read()
replaced = 0
missing = []

for sub, new_body in new_bodies.items():
    # 锚点:子串必须在某 card-title 内且唯一
    matches = list(re.finditer(r'card-title">[^<]*' + re.escape(sub), html))
    if len(matches) != 1:
        missing.append((sub, f"title匹配{len(matches)}次,应1")); continue
    ti = matches[0].start()
    bi = html.find('<div class="card-body">', ti)
    if bi < 0:
        missing.append((sub, "无card-body")); continue
    # 深度匹配切原文 card-body(处理嵌套 div)
    i = bi; depth = 0; be = None
    while i < len(html):
        if html[i:i+4] == '<div':
            depth += 1; i = html.find('>', i) + 1
        elif html[i:i+6] == '</div>':
            depth -= 1; i += 6
            if depth == 0:
                be = i; break
        else:
            i += 1
    if be is None:
        missing.append((sub, "body未闭合")); continue
    old = html[bi:be]
    if old.strip() == new_body.strip():
        continue  # 无变化
    html = html[:bi] + new_body + html[be:]
    replaced += 1

if missing:
    print("❌ 锚点问题,未写文件:")
    for m in missing:
        print("  -", m)
    sys.exit(1)

# div 平衡 + script 完整快检
assert html.count("<div") == html.count("</div>"), f"div不平衡: {html.count('<div')}/{html.count('</div>')}"
assert "<script>" in html and "</script>" in html, "script残缺"

open(HTML, "w", encoding="utf-8").write(html)
print(f"✅ 组装完成:替换 {replaced} 张 card-body(共 {len(new_bodies)} 锚点,产物文件 {len(PROD)})")
