#!/usr/bin/env python3
"""校验 P2 ai 卡 card-body 产物。用法: python3 check_p2.py <body.html> [--light]
全改卡 ≥5 段 <strong>;轻过卡(--light) ≥4 段。
注:§4.2 雷区(Manager≠Claude/GPT、向量≠Chroma 等)因 ai 卡会"提到被拒绝的选项"(如 C10 合法说"不用 Chroma"),
naive 子串检查会误报,故不在本脚本自动检查,改由 Task 7 人工 grep 抽检(读上下文判断误用 vs 合法提及)。"""
import re, sys

light = "--light" in sys.argv
f = sys.argv[1]
html = open(f, encoding="utf-8").read()
errs = []
min_strong = 4 if light else 5

# 1. 段首 <strong>(全改≥5 / 轻过≥4)
strongs = re.findall(r"<strong>[^<]{2,}</strong>", html)
if len(strongs) < min_strong:
    errs.append(f"段首 <strong> 只有 {len(strongs)} 个,需 ≥{min_strong}({'轻过' if light else '全改'})")

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

# 6. 唯一自动雷区:'6 步闭环'(此短语不存在,任何出现都是错;其余 §4.2 雷区人工抽检)
if "6 步闭环" in html or "6步闭环" in html:
    errs.append("含'6 步闭环'(此说法不存在,§4.2 雷区)")

if errs:
    print("❌ 校验失败:")
    for e in errs: print("  -", e)
    sys.exit(1)
mode = "轻过" if light else "全改"
print(f"✅ 校验通过({len(strongs)} 段 <strong>,{mode})")
