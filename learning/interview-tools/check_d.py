#!/usr/bin/env python3
"""校验 D 深挖卡产物(Form A 四要素)。用法:
python3 check_d.py <new_card.html> --project front|mgr|code|prd
四要素: 数据结构词 + 算法词 + 拒绝alternative词 + 诚实边界词(各至少1,语义靠人工抽检只 warn)
结构: <strong>领起标签。</strong> 段 ≥ 4
硬约束: 禁口语碎嘴 / 无①②③④⑤堆叠 / div 平衡 / 无'6步闭环'(err)
雷区: per-project warn(Chroma/git钩子/Claude/GPT/20+人 等出现在'拒绝/对比'语境属正常,人工确认)"""
import re, sys, argparse

p = argparse.ArgumentParser()
p.add_argument("new")
p.add_argument("--project", required=True, choices=["front", "mgr", "code", "prd"])
a = p.parse_args()

html = open(a.new, encoding="utf-8").read()
errs, warns = [], []

# 1. 四要素词(各至少命中一个 → warn 不命中,语义靠人工)
DATA = ["数据结构", "结构", "字段", "JSON", "schema", "文件", "节点", "边", "拓扑", "语法", "存的是", "长这样", "协议"]
ALGO = ["算法", "流程", "余弦", "top-k", "topK", "召回", "求值", "蒸馏", "扫描", "匹配", "计算", "检索", "调度", "流转"]
REJECT = ["自研", "拒绝", "本可以", "没选", "而不是", "instead", "不用", "不选", "放弃了", "权衡", "排除了"]
HONESTY = ["没接", "研究型", "诚实", "局限", "上限", "框架先行", "规模", "边界", "代价", "不适用", "原型"]
if not any(w in html for w in DATA): warns.append("未见数据结构词")
if not any(w in html for w in ALGO): warns.append("未见算法/流程词")
if not any(w in html for w in REJECT): warns.append("未见'自研/拒绝alternative'词")
if not any(w in html for w in HONESTY): warns.append("未见诚实边界词(四要素第④项不可省)")

# 2. <strong> 段首 ≥ 4
strongs = re.findall(r"<strong>[^<]{2,}</strong>", html)
if len(strongs) < 4:
    errs.append(f"段首 <strong> 只有 {len(strongs)} 个,需 ≥4(Form A 四要素)")

# 3. 禁口语碎嘴
banned = ["说白了", "得说句实话", "我自己比较得意", "这套东西", "你就懂了", "听着像"]
hit = [w for w in banned if w in html]
if hit: errs.append(f"命中口语碎嘴: {hit}")

# 4. ①②③④⑤ 堆叠
if re.search(r"[①②③④⑤][①②③④⑤][①②③④⑤][①②③④⑤]", html):
    errs.append("①②③④⑤ 堆叠(≥4 连续),速查表腔")

# 5. div 平衡
if html.count("<div") != html.count("</div>"):
    errs.append(f"div 不平衡: <div {html.count('<div')} / </div> {html.count('</div>')}")

# 6. 完整 card 片段校验
if not html.lstrip().startswith("<div class=\"card\""):
    errs.append("片段非完整 card(应以 <div class=\"card\" 开头)")

# 7. 硬雷区 err:'6 步闭环'(全项目)
if "6 步闭环" in html or "6步闭环" in html:
    errs.append("含'6 步闭环'(此说法不存在,§4.2 雷区)")

# 8. per-project 雷区 warn(naive 子串在'拒绝/对比'语境会误报,人工确认)
if a.project == "mgr":
    for w in ["Claude", "GPT-4", "GPT-5", "Anthropic"]:
        if w in html: warns.append(f"Manager 卡出现 {w}(应为 qwen-flash;确认是对比非自述)")
if a.project == "code":
    if "Chroma" in html: warns.append("Code 卡出现 Chroma(自研非Chroma;确认是'不用Chroma'语境)")
    if "git 钩子" in html or "git钩子" in html: warns.append("Code 卡出现 git 钩子(增量靠sha256;确认是'不用git钩子'语境)")
if a.project == "prd":
    if "SDD 平台" in html or "SDD平台" in html: warns.append("PRD 卡出现 SDD 平台(prd-tools是Claude Code插件非SDD)")
    if "20+人" in html or "20+ 人" in html: warns.append("PRD 卡出现 20+人(应软化,ADR-0005写1-5人)")
    if "直接生成代码" in html: warns.append("PRD 卡出现'直接生成代码'(插件不直接生成代码)")

if warns:
    print(f"⚠️ 提示(--project {a.project},语义/语境在即可,不阻塞):")
    for w in warns: print("  -", w)
if errs:
    print(f"❌ 校验失败(--project {a.project}):")
    for e in errs: print("  -", e)
    sys.exit(1)
print(f"✅ 校验通过(--project {a.project},{len(strongs)} 段 <strong>,{len(warns)}条提示)")
