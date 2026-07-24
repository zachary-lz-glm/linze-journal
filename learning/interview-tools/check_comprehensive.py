#!/usr/bin/env python3
"""校验综合主卡片段(口语逐字稿版 CLEAR/L)。用法:
python3 check_comprehensive.py <card.html> --n 1..9
检查: data-g=自我陈述 / 标题带①-⑨序号 / CLEAR四要素词(背景·Leadership·执行·结果各≥1,warn) /
证据锚点词 / 诚实边界词 / 预判追问<ul>≥4条<li> / div平衡 / 完整card /
速查表腔(err) / Q9雷区(Cursor等只在'产品体验'语境,warn)
注:综合主卡是口语逐字稿,不禁'说白了'等口语连接词(那是§6 declarative卡的规矩)。"""
import re, sys, argparse

p = argparse.ArgumentParser()
p.add_argument("new")
p.add_argument("--n", type=int, required=True, choices=range(1, 10))
a = p.parse_args()

html = open(a.new, encoding="utf-8").read()
errs, warns = [], []

# 1. data-g=自我陈述
if 'data-g="自我陈述"' not in html:
    errs.append('缺 data-g="自我陈述"')

# 2. 标题带对应序号
circles = "①②③④⑤⑥⑦⑧⑨"
if circles[a.n - 1] not in html:
    errs.append(f"标题缺序号 {circles[a.n-1]}(第{a.n}张)")

# 3. CLEAR 四要素词(warn,口语逐字稿语义靠人工)
CONTEXT = ["背景", "之前", "那时", "起因", "遇到", "情境", "场景"]
LEADERSHIP = ["我主动", "我选", "我决定", "我想要", "为什么是我", "我牵头", "我主导", "主动选", "我算过", "我的判断"]
EXEC = ["做了", "设计了", "搭了", "三步", "两步", "策略", "具体", "陪跑", "试点", "门禁", "证据链"]
RESULT = ["结果", "变成", "从", "同事", "证据", "数据", "缩短", "验证"]
if not any(w in html for w in CONTEXT): warns.append("未见 Context 词")
if not any(w in html for w in LEADERSHIP): warns.append("未见 Leadership 词(为什么是你)")
if not any(w in html for w in EXEC): warns.append("未见 Execution 词")
if not any(w in html for w in RESULT): warns.append("未见 Results/证据词")

# 4. 诚实边界词(warn,Reflection 段不可省)
HONESTY = ["得说实话", "诚实", "没成", "不理想", "边界", "局限", "原型", "预研", "没接", "在补", "验证期", "小范围", "不是已", "坦白"]
if not any(w in html for w in HONESTY): warns.append("未见诚实边界词(Reflection 段不可省)")

# 5. 预判追问 ≥4 条 <li>
lis = re.findall(r"<li>[^<]", html)
if len(lis) < 4:
    errs.append(f"预判追问 <li> 只有 {len(lis)} 条,需 ≥4")

# 6. 速查表腔(err)
banned = ["必背", "杀手锏", "必答", "金句钩子"]
hit = [w for w in banned if w in html]
if hit: errs.append(f"命中速查表腔: {hit}")

# 7. div 平衡
if html.count("<div") != html.count("</div>"):
    errs.append(f"div 不平衡: <div {html.count('<div')} / </div> {html.count('</div>')}")

# 8. 完整 card 片段
if not html.lstrip().startswith('<div class="card"'):
    errs.append("片段非完整 card(应以 <div class=\"card\" 开头)")

# 9. 硬雷区 err:6 步闭环
if "6 步闭环" in html or "6步闭环" in html:
    errs.append("含'6 步闭环'(不存在,§4 雷区)")

# 10. Q9(n=9)产品体验档雷区 warn
if a.n == 9:
    for w in ["Cursor", "Claude Code", "Agent SDK", "MCP"]:
        if w in html and "产品体验" not in html and "只用过" not in html and "体验级" not in html:
            warns.append(f"Q9 出现 {w} 但未标'产品体验'(必须分档,防装读过源码)")

if warns:
    print(f"⚠️ 提示(--n {a.n},语义/语境在即可,不阻塞):")
    for w in warns: print("  -", w)
if errs:
    print(f"❌ 校验失败(--n {a.n}):")
    for e in errs: print("  -", e)
    sys.exit(1)
print(f"✅ 校验通过(--n {a.n},{len(lis)} 条追问,{len(warns)}条提示)")
