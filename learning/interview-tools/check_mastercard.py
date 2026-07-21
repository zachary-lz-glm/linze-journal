#!/usr/bin/env python3
"""校验 P0 老前端主陈述卡 card-body 产物。用法: python3 check_mastercard.py <body.html>"""
import re, sys

f = sys.argv[1]
html = open(f, encoding="utf-8").read()
errs = []

# 1. 五段 <strong> 段首(至少 5 个)
strongs = re.findall(r"<strong>[^<]{2,}</strong>", html)
if len(strongs) < 5:
    errs.append(f"段首 <strong> 只有 {len(strongs)} 个,需 ≥5(五步骨架)")

# 2. 禁用口语碎嘴
banned = ["说白了", "得说句实话", "我自己比较得意", "这套东西", "你就懂了",
          "被问", "我答", "听着像"]
hit = [w for w in banned if w in html]
if hit:
    errs.append(f"命中口语碎嘴: {hit}")

# 3. ①②③④⑤ 堆叠(连续 4 个以上圈号)
if re.search(r"[①②③④⑤][①②③④⑤][①②③④⑤][①②③④⑤]", html):
    errs.append("①②③④⑤ 堆叠(≥4 连续),速查表腔")

# 4. loop 残留 / html 包裹
if "[loop" in html or "<html" in html.lower() or "<body" in html.lower():
    errs.append("含 loop 残留或 html/body 包裹")

# 5. div 平衡
if html.count("<div") != html.count("</div>"):
    errs.append(f"div 不平衡: <div {html.count('<div')} / </div> {html.count('</div>')}")

# 6. P0 老前端卡雷区:不该出现 PRD/agent 项目词(A5 拆分别串味)
poison = ["5h→2h", "prd-tools", "prd2code", "6 步闭环", "6步闭环", "Claude", "GPT-4", "GPT-5"]
phit = [w for w in poison if w in html]
if phit:
    errs.append(f"串入 PRD/agent 项目词(老前端卡不该有): {phit}")

# 7. 硬数字未软化(应已按 §4 软化)
hard = ["8个国", "8国", "月均20起", "95%场景", "18个月", "16个联动"]
hhit = [w for w in hard if w in html]
if hhit:
    errs.append(f"硬数字未软化(§4 要求软化): {hhit}")

if errs:
    print("❌ 校验失败:")
    for e in errs: print("  -", e)
    sys.exit(1)
print(f"✅ 校验通过({len(strongs)} 段 <strong>)")
