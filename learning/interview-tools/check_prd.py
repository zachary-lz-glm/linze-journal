#!/usr/bin/env python3
"""校验 PRD 模块重构产物。用法:
python3 check_prd.py <frag.html> --type master|followup|gap
  master  = 模块主卡/重写卡(Form A 四要素 + <strong>段 ≥4)
  followup= 追问库卡(<ul class="points"> + <li> ≥6)
  gap     = 补缺弹药卡(基础结构)
公共硬约束: 禁口语碎嘴 / 无①②③④⑤堆叠 / div 平衡 / 完整card / 无'6步闭环'(err)
PRD 雷区 warn: SDD平台 / 20+人 / 直接生成代码(否定语境 OK,人工确认)"""
import re, sys, argparse

p = argparse.ArgumentParser()
p.add_argument("new")
p.add_argument("--type", required=True, choices=["master", "followup", "gap"])
a = p.parse_args()
html = open(a.new, encoding="utf-8").read()
errs, warns = [], []

# 公共: 完整 card
if not html.lstrip().startswith('<div class="card"'):
    errs.append("片段非完整 card(应以 <div class=\"card\" 开头)")
# 公共: div 平衡
if html.count("<div") != html.count("</div>"):
    errs.append(f"div 不平衡: <div {html.count('<div')} / </div> {html.count('</div>')}")
# 公共: 禁口语碎嘴
banned = ["说白了", "得说句实话", "我自己比较得意", "这套东西", "你就懂了", "听着像"]
hit = [w for w in banned if w in html]
if hit: errs.append(f"命中口语碎嘴: {hit}")
# 公共: ①②③④⑤ 堆叠
if re.search(r"[①②③④⑤][①②③④⑤][①②③④⑤][①②③④⑤]", html):
    errs.append("①②③④⑤ 堆叠(≥4 连续),速查表腔")
# 公共: 硬雷区 '6 步闭环'
if "6 步闭环" in html or "6步闭环" in html:
    errs.append("含'6 步闭环'(不存在,雷区)")
# 公共: data-g 必须是 PRD 工作流
if 'data-g="PRD 工作流"' not in html:
    errs.append("缺 data-g=\"PRD 工作流\"")

# type 专属
strongs = re.findall(r"<strong>[^<]{2,}</strong>", html)
if a.type == "master":
    DATA = ["数据结构","结构","字段","JSON","schema","文件","节点","边","拓扑","语法","存的是","长这样","协议","流水线","步骤"]
    ALGO = ["算法","流程","余弦","top-k","召回","求值","蒸馏","扫描","匹配","计算","检索","调度","流转","路由"]
    REJECT = ["自研","拒绝","本可以","没选","而不是","不用","不选","放弃了","权衡","排除了","放弃"]
    HONESTY = ["没接","研究型","诚实","局限","上限","框架先行","规模","边界","代价","不适用","原型","债","小范围"]
    if not any(w in html for w in DATA): warns.append("未见数据结构词")
    if not any(w in html for w in ALGO): warns.append("未见算法/流程词")
    if not any(w in html for w in REJECT): warns.append("未见'自研/拒绝alternative'词")
    if not any(w in html for w in HONESTY): warns.append("未见诚实边界词(四要素第④项不可省)")
    if len(strongs) < 4:
        errs.append(f"master 段首 <strong> 只有 {len(strongs)} 个,需 ≥4(Form A)")
elif a.type == "followup":
    if '<ul class="points">' not in html and '<ul class="points' not in html:
        errs.append("追问库卡缺 <ul class=\"points\">")
    nli = len(re.findall(r"<li>", html))
    if nli < 6:
        errs.append(f"追问库卡 <li> 只有 {nli} 条,需 ≥6")
elif a.type == "gap":
    if len(strongs) < 2:
        warns.append("gap 卡 <strong> 段偏少(建议 ≥2,非硬)")

# PRD 雷区 warn(全 type)
for w in ["SDD 平台", "SDD平台"]:
    if w in html: warns.append(f"出现 {w}(prd-tools 是 CC 插件非 SDD 平台;确认是对比/否定语境)")
if "20+人" in html or "20+ 人" in html: warns.append("出现 20+人(应软化 ADR-0005 1-5 人)")
if "直接生成代码" in html: warns.append("出现'直接生成代码'(插件不直接生成代码;确认语境)")

if warns:
    print(f"⚠️ 提示(--type {a.type},语义/语境在即可,不阻塞):")
    for w in warns: print("  -", w)
if errs:
    print(f"❌ 校验失败(--type {a.type}):")
    for e in errs: print("  -", e)
    sys.exit(1)
extra = f",{len(strongs)} 段 <strong>" if a.type!="followup" else f",{len(re.findall(r'<li>',html))} 条追问"
print(f"✅ 校验通过(--type {a.type}{extra},{len(warns)}条提示)")
