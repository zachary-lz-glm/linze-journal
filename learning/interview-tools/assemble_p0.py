#!/usr/bin/env python3
"""P0 老前端 5 张卡:替换 body + 卡1改标题/data-kw + 5张加 data-g + subOrder补值。原子写。
顺序:先替换 body(用原 title 定位)→ 加 data-g → subOrder → 最后改卡1 title(改完不再用 title 定位)。"""
import re, os

ROOT = "/Users/didi/work/linze-journal/learning/interview-tools/"
src = open(ROOT + "stealth.html", encoding="utf-8").read()

TITLES = [
    "最有价值项目（STAR逐字稿）",
    "架构决策故事：为什么选Schema？",
    "跨团队推广故事：组件库如何从1到8？",
    "怎么证明前端扎实？",
    "线上事故反思 + 基础设施架构判断",
]
BODIES = [
    ".p0-card1-star.html",
    ".p0-card2-decision.html",
    ".p0-card3-promote.html",
    ".p0-card4-frontend.html",
    ".p0-card5-accident.html",
]
CARD1_OLD_TITLE = TITLES[0]
CARD1_NEW_TITLE = "最有价值的项目：Schema 营销中台"
CARD1_NEW_KW = "最有价值的项目 最得意的项目 介绍下你的项目 Schema 营销中台 最有成就感 STAR 项目陈述 前端负责人"
DATA_G = "前端项目"

def card_body_range(html, title):
    tidx = html.find(f'card-title">{title}')
    assert tidx > 0, f"找不到 title: {title}"
    bs = html.find('<div class="card-body">', tidx)
    assert bs > 0, f"找不到 card-body: {title}"
    depth, i = 0, bs
    while i < len(html):
        if html[i:i+4] == "<div": depth += 1
        elif html[i:i+6] == "</div>":
            depth -= 1
            if depth == 0: return bs, i + 6
        i += 1
    assert False, f"card-body 不闭合: {title}"

def card_open_tag_range(html, title):
    tidx = html.find(f'card-title">{title}')
    assert tidx > 0
    o = html.rfind('<div class="card"', 0, tidx)
    assert o >= 0, f"找不到 card 开标签: {title}"
    e = html.find('>', o)
    assert e > 0
    return o, e + 1

# Step 1: 替换 5 张 body(title 未改,定位安全)
for title, prod in zip(TITLES, BODIES):
    bs, be = card_body_range(src, title)
    nb = open(ROOT + prod, encoding="utf-8").read()
    assert '<div class="card-body">' in nb, f"{prod} 非法 body 片段"
    src = src[:bs] + nb.rstrip() + src[be:]
print("Step1: 5 张 body 替换完成")

# Step 2: 5 张加 data-g="前端项目"(若没有)
for title in TITLES:
    o, e = card_open_tag_range(src, title)
    tag = src[o:e]
    if "data-g=" not in tag:
        newtag = tag.replace('data-c="proj"', f'data-c="proj" data-g="{DATA_G}"', 1)
        assert newtag != tag, f"{title} 加 data-g 失败(找不到 data-c=\"proj\")"
        src = src[:o] + newtag + src[e:]
print("Step2: 5 张加 data-g=前端项目")

# Step 3: subOrder 加 '前端项目':1.4
assert "'前端项目':" not in src, "subOrder 已含 前端项目,检查是否重复运行"
new_src = src.replace("'Schema 项目':8", "'前端项目':1.4,'Schema 项目':8", 1)
assert new_src != src, "找不到 subOrder 'Schema 项目':8 锚点"
src = new_src
print("Step3: subOrder 加 前端项目:1.4")

# Step 4: 卡1 改 title + data-kw(最后做,之后不再用 title 定位)
o, e = card_open_tag_range(src, CARD1_OLD_TITLE)
tag = src[o:e]
newtag = re.sub(r'data-kw="[^"]*"', f'data-kw="{CARD1_NEW_KW}"', tag, 1)
assert newtag != tag, "卡1 data-kw 替换失败"
src = src[:o] + newtag + src[e:]
old_t = f'card-title">{CARD1_OLD_TITLE}</div>'
assert old_t in src, "卡1 旧标题找不到"
src = src.replace(old_t, f'card-title">{CARD1_NEW_TITLE}</div>', 1)
print("Step4: 卡1 改标题+data-kw")

tmp = ROOT + "stealth.html.tmp"
open(tmp, "w", encoding="utf-8").write(src)
os.replace(tmp, ROOT + "stealth.html")
print("✅ P0 5 张老前端卡组装完成")
