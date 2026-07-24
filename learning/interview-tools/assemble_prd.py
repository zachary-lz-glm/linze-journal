#!/usr/bin/env python3
"""PRD 模块重构组装:删全部旧 PRD-g 卡 + A10 → 按 LAYOUT 重排 9 簇插入 AI 模块锚点前。原子写。
- 抽取: 扫每个 <div class="card",depth 数到闭合 </div>;data-g=PRD 工作流→dict{title:block}; title 含 A10→a10
- a10_orig 用于删除,a10_mod(加 data-g+master)用于插入
- LAYOUT: 9 簇 [(kind,val)...]; frag=读文件 / keep=按 title 子串取 / A10:xxx=a10_mod; 每簇首卡加 master 类
- 锚点: '<!-- ==================== AI 模块' 前"""
import re, os, sys
ROOT = "/Users/didi/work/linze-journal/learning/interview-tools/"
HTML = ROOT + "stealth.html"
A10_SUB = "从 PRD 到上线的完整链路"
ANCHOR = "<!-- ==================== AI 模块"

LAYOUT = [
 ("入口·项目总览", [("frag",".prd-entry.html"), ("keep","prd-tools 4个王牌素材")]),
 ("① reference 深挖", [("frag",".prd-m1-master.html"),("keep","AI知识库的本质定位"),
     ("keep","/reference 蒸馏出来的 6 个文件"),("keep","reference 知识过时"),
     ("frag",".prd-m1-coldstart.html"),("frag",".prd-m1-followup.html")]),
 ("② PRD 蒸馏", [("frag",".prd-m2-master.html"),("keep","PRD 到代码最难的一步"),
     ("frag",".prd-m2-context.html"),("frag",".prd-m2-loss.html"),("keep","PRD摄入：多格式"),
     ("keep","Spec和Plan长什么样"),("frag",".prd-m2-followup.html")]),
 ("③ 整体架构", [("frag",".prd-m3-master.html"),("keep","双插件体系"),
     ("keep","能力面适配器"),("keep","传统工程思维"),("frag",".prd-m3-followup.html")]),
 ("④ 对比市面工具", [("frag",".prd-m4-master.html"),("keep","和 Claude Code init"),
     ("keep","有Claude Code了"),("keep","BMAD架构"),("frag",".prd-m4-followup.html")]),
 ("⑤ SSOT/证据链/门禁/评估", [("frag",".prd-m5-master.html"),("keep","SSOT 五条边界规则"),
     ("keep","证据链机制详解"),("frag",".prd-m5-gate.html"),("keep","Readiness Score"),
     ("frag",".prd-m5-eval.html"),("frag",".prd-m5-5h2h.html"),("frag",".prd-m5-followup.html")]),
 ("⑥ 端到端", [("keep","A10:"+A10_SUB),("keep","端到端原型：自验证"),
     ("keep","端到端原型：模板/LLM"),("keep","端到端原型 → 生产"),("keep","Harness 三种引擎"),
     ("keep","SDD 完整流程"),("frag",".prd-m6-followup.html")]),
 ("⑦ 实现深坑", [("frag",".prd-m7-master.html"),("frag",".prd-m7-stability.html"),
     ("keep","幻觉怎么答"),("keep","代码上下文怎么定位"),("keep","AI工作流出错了怎么归因"),
     ("keep","PRD过时或临时改动"),("frag",".prd-m7-skilltools.html"),
     ("frag",".prd-m7-errorleak.html"),("frag",".prd-m7-followup.html")]),
 ("⑧ 推广落地", [("frag",".prd-m8-master.html"),("keep","AI工作流推广ROI"),
     ("keep","PRD质量卡口"),("keep","AI工作流在团队怎么落地"),("frag",".prd-m8-resistance.html"),
     ("frag",".prd-m8-followup.html")]),
]

def extract_cards(html):
    cards, a10 = {}, None
    i, n = 0, len(html)
    while True:
        o = html.find('<div class="card"', i)
        if o < 0: break
        depth, j, close = 0, o, None
        while j < n:
            if html[j:j+4] == '<div':
                depth += 1; j = html.find('>', j) + 1
            elif html[j:j+6] == '</div>':
                depth -= 1; j += 6
                if depth == 0: close = j; break
            else: j += 1
        if close is None: break
        block = html[o:close]
        m = re.search(r'card-title">([^<]*)<', block)
        title = m.group(1) if m else ""
        if A10_SUB in title: a10 = block
        elif 'data-g="PRD 工作流"' in block[:300]: cards[title] = block
        i = close
    return cards, a10

def prep_a10(block):
    b = re.sub(r'(<div class="card)"', r'\1 master"', block, count=1)  # 加 master
    if 'data-g="PRD 工作流"' not in b[:400]:
        b = re.sub(r'(<div class="card master"\s+data-c="proj")', r'\1 data-g="PRD 工作流"', b, count=1)
    return b

def mark_master(block):
    if 'class="card master"' in block[:200]: return block  # 已是(A10)
    return re.sub(r'(<div class="card)"', r'\1 master"', block, count=1)

html = open(HTML, encoding="utf-8").read()
cards, a10 = extract_cards(html)
print(f"抽取: PRD-g {len(cards)} 张, A10 {'有' if a10 else '无'}")
if a10 is None: sys.exit("❌ 找不到 A10")
a10_orig, a10_mod = a10, prep_a10(a10)
assert 'data-g="PRD 工作流"' in a10_mod[:400], "A10 data-g 注入失败"

removed = 0
for t, b in cards.items():
    if b in html: html = html.replace(b, ""); removed += 1
    else: print(f"⚠️ 删除未命中(子串漂移): {t}")
if a10_orig in html: html = html.replace(a10_orig, ""); removed += 1
else: print("⚠️ A10 原文删除未命中")
print(f"删除旧卡 {removed} 张(应 43)")

def get_block(kind, val):
    if kind == "frag":
        b = open(ROOT + val, encoding="utf-8").read().strip()
        if not b.startswith('<div class="card"'): raise Exception(f"{val} 非完整 card")
        if b.count('<div') != b.count('</div>'): raise Exception(f"{val} div 不平衡")
        return b
    if val.startswith("A10:"): return a10_mod
    hits = [t for t in cards if val in t]
    if len(hits) != 1: raise Exception(f"keep '{val}' 命中 {len(hits)} 张: {hits}")
    return cards[hits[0]]

new_block = ""
for name, slots in LAYOUT:
    new_block += f'\n<!-- ===== PRD 模块: {name} ===== -->\n'
    for idx, (kind, val) in enumerate(slots):
        b = get_block(kind, val)
        if idx == 0: b = mark_master(b)
        new_block += b + "\n"

if html.count(ANCHOR) != 1: sys.exit(f"❌ 锚点命中 {html.count(ANCHOR)} 次,应 1")
html = html.replace(ANCHOR, new_block + "\n" + ANCHOR, 1)

assert html.count('<div') == html.count('</div>'), f"全文 div 不平衡: {html.count('<div')}/{html.count('</div>')}"
assert '<script>' in html and '</script>' in html, "script 残缺"
open(HTML + ".tmp", "w", encoding="utf-8").write(html)
os.replace(HTML + ".tmp", HTML)
print("✅ PRD 9 簇重排完成(删43+插55+A10搬入+master类)")
