#!/usr/bin/env python3
"""校验 P1 弹药卡"加段补维度"产物。用法:
python3 check_p1.py <new_body.html> --orig <orig_body.html> --tier A|B
A 档(极薄/纯机制): 命中 ownership 词 + alternative 词
B 档(半截STAR/亮点成熟): 命中 eval 词 或 方法论句词
所有档: 改后长度 ≥ 原文*0.85(只增不删) + 禁碎嘴 + 无①②③④⑤堆叠 + div 平衡 + 无'6步闭环'
注:§4.1 其余雷区(Manager≠Claude/GPT、向量≠Chroma 等)因弹药卡会合法"提到被拒绝的选项",
naive 子串检查会误报,不在本脚本自动检查,改由 Task 9 人工 grep 抽检。"""
import re, sys, argparse

p = argparse.ArgumentParser()
p.add_argument("new")
p.add_argument("--orig", required=True)
p.add_argument("--tier", required=True, choices=["A", "B"])
a = p.parse_args()

new = open(a.new, encoding="utf-8").read()
orig = open(a.orig, encoding="utf-8").read()
errs = []
warns = []  # 维度词未命中只提示不禁(语义维度词表无法穷尽,靠人工抽检)

# 1. 只增不删(加段不应使 body 大幅变短)
if len(new) < len(orig) * 0.85:
    errs.append(f"只增不删失败: 新 {len(new)} < 原文 {len(orig)} * 0.85 (疑似删了原文段)")

# 2. 分档维度词
OWNERSHIP = ["我定的是", "我定的", "我在", "我负责", "我设计", "我做的是", "我 drive", "我主导", "我牵头",
             "我守的", "我拍板", "是我定的", "是我做", "我来定", "我挑的", "我选的", "是我拍板", "是我守", "我决定"]
ALTERNATIVE = ["拒绝", "本可以", "没选", "而不是", "instead", "不选", "放弃了", "权衡过", "排除了"]
EVAL = ["验证", "度量", "怎么知道", "效果", "若要度量", "指标", "测过", "看 ", "回放", "对照"]
METHOD = ["本质是", "本质在于", "下次", "可迁移", "可复用", "方法论", "规律", "套路", "抽象成"]
if a.tier == "A":
    if not any(w in new for w in OWNERSHIP):
        warns.append("A 档未见 ownership 词(语义在即可,人工确认)")
    if not any(w in new for w in ALTERNATIVE):
        warns.append("A 档未见 alternative 词(语义在即可,人工确认)")
else:  # B
    if not (any(w in new for w in EVAL) or any(w in new for w in METHOD)):
        warns.append("B 档未见 eval/方法论词(语义在即可,人工确认)")

# 3. 禁用口语碎嘴
banned = ["说白了", "得说句实话", "我自己比较得意", "这套东西", "你就懂了", "听着像"]
hit = [w for w in banned if w in new]
if hit:
    errs.append(f"命中口语碎嘴: {hit}")

# 4. ①②③④⑤ 堆叠(连续 4 个以上圈号)
if re.search(r"[①②③④⑤][①②③④⑤][①②③④⑤][①②③④⑤]", new):
    errs.append("①②③④⑤ 堆叠(≥4 连续),速查表腔")

# 5. div 平衡
if new.count("<div") != new.count("</div>"):
    errs.append(f"div 不平衡: <div {new.count('<div')} / </div> {new.count('</div>')}")

# 6. 唯一自动雷区:'6 步闭环'
if "6 步闭环" in new or "6步闭环" in new:
    errs.append("含'6 步闭环'(此说法不存在,§4.1 雷区)")

if warns:
    print(f"⚠️ 维度提示(--tier {a.tier},语义在即可,不阻塞):")
    for w in warns: print("  -", w)
if errs:
    print(f"❌ 校验失败(--tier {a.tier}):")
    for e in errs: print("  -", e)
    sys.exit(1)
extra = f", {len(warns)}条维度提示" if warns else ""
print(f"✅ 校验通过(--tier {a.tier},新 {len(new)} / 原 {len(orig)}{extra})")
