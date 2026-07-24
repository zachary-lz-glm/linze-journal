#!/usr/bin/env python3
"""综合重构组装:插 9 张主卡 + 删 15 张旧卡 + 改 3 张 residue 的 data-g + 改 subOrder + 修悬空引用。原子写。
锚点(card-title 文本"包含"子串,稳: handles 带前缀标题如'被问"业务方关心什么"'):
  删除: card-title 含子串 → rfind <div class="card" → depth 数到闭合 </div> → 切除整块
  data-g 改:入职规划 软技能→HR·行为面;上级冲突/加班 HR面→HR·行为面
  插入: <!-- 综合模块 v2 --> 标记后(emer 顶部,主卡置首)
  subOrder:加'自我陈述':0.5,删'软技能',改'HR面'→'HR·行为面'
  悬空引用:open职业规划 hint 指向已删创业卡 → 指向新主卡⑤"""
import re, os, sys

ROOT = "/Users/didi/work/linze-journal/learning/interview-tools/"
HTML = ROOT + "stealth.html"

# 待删 15 张旧卡:card-title 文本包含该子串(精确)。若 stealth.html 被改过,先重新核对!
DELETE_TITLES = [
    "优点和缺点", "为什么录用你", "最有成就感的事", "AI 会取代前端吗",
    "方案推不动", "价值靠什么衡量", "为什么我想要创业状态",
    "从 0 到 1 让我兴奋在哪", "我为什么主动选创业节奏",
    "空窗期怎么解释", "最大的失败", "薪资低于预期怎么谈",
    "手上有其他 offer 吗", "业务方关心什么", "了解 X 吗",
]


def find_card_block(h, title_sub):
    """返回 (start, end) 卡片 <div...>...</div> 闭区间;card-title 文本含 title_sub 且唯一。
    返回 (None, err) 失败。"""
    matches = [m for m in re.finditer(r'card-title">([^<]*)</div>', h) if title_sub in m.group(1)]
    if len(matches) != 1:
        return None, f"锚点'{title_sub}'在 card-title 中匹配{len(matches)}次,应1"
    m = matches[0]
    o = h.rfind('<div class="card"', 0, m.start())
    if o < 0:
        return None, f"找不到'{title_sub}'的 card 开标签"
    depth, i, close_end = 0, o, None
    while i < len(h):
        if h[i:i+4] == '<div':
            depth += 1; i = h.find('>', i) + 1
        elif h[i:i+6] == '</div>':
            depth -= 1; i += 6
            if depth == 0:
                close_end = i; break
        else:
            i += 1
    if close_end is None:
        return None, f"'{title_sub}' 未闭合"
    return (o, close_end), None


html = open(HTML, encoding="utf-8").read()
problems = []

# --- A. 删 15 张旧卡 ---
for t in DELETE_TITLES:
    blk, err = find_card_block(html, t)
    if err:
        problems.append("删:" + err); continue
    html = html[:blk[0]] + html[blk[1]:]
    print(f"删除: {t}")

if problems:
    print("❌ 删除锚点问题,未写文件:"); [print("  -", p) for p in problems]; sys.exit(1)

# --- B. 改 3 张 residue 的 data-g ---
for t, old_g, new_g in [
    ("入职前 3 个月怎么规划", "软技能", "HR·行为面"),
    ("和上级意见冲突", "HR面", "HR·行为面"),
    ("怎么看待加班", "HR面", "HR·行为面"),
]:
    blk, err = find_card_block(html, t)
    if err:
        problems.append(f"data-g改:{err}"); continue
    block = html[blk[0]:blk[1]]
    if f'data-g="{old_g}"' not in block:
        problems.append(f"data-g改:'{t}' 当前非 data-g=\"{old_g}\"(可能已改/PRD动过)"); continue
    block = block.replace(f'data-g="{old_g}"', f'data-g="{new_g}"', 1)
    html = html[:blk[0]] + block + html[blk[1]:]
    print(f"改 data-g: {t}  {old_g}→{new_g}")

if problems:
    print("❌ data-g 改问题,未写文件:"); [print("  -", p) for p in problems]; sys.exit(1)

# --- C. 插 9 张主卡(emer 顶部,综合模块 v2 标记后) ---
marker = "<!-- ==================== 综合模块 v2 ==================== -->"
if html.count(marker) != 1:
    problems.append(f"插入标记匹配{html.count(marker)}次,应1")
else:
    frag_all = "\n".join(
        open(f"/tmp/comp-card-{n}.html", encoding="utf-8").read().strip()
        for n in range(1, 10)
    )
    mi = html.index(marker) + len(marker)
    html = html[:mi] + "\n" + frag_all + "\n" + html[mi:]
    print("插入: 9 张自我陈述主卡 → 综合模块 v2 顶部")

# --- D. 改 subOrder ---
old_sub = "'项目数据':1,'软技能':2,'HR面':3,'反问':4,'话术急救':5"
new_sub = "'自我陈述':0.5,'项目数据':1,'HR·行为面':3,'反问':4,'话术急救':5"
if old_sub not in html:
    problems.append(f"subOrder 原串未找到(可能 PRD 改过):\n  {old_sub}")
else:
    html = html.replace(old_sub, new_sub, 1)
    print("改 subOrder: +自我陈述, -软技能, HR面→HR·行为面")

# --- E. 修悬空引用:open职业规划 hint 指向已删创业卡 → 新主卡⑤ ---
old_ref = "详见软技能组「为什么我想要创业状态」补卡"
new_ref = "详见综合·自我陈述⑤「对创业的想法」"
if old_ref in html:
    html = html.replace(old_ref, new_ref, 1)
    print("修悬空引用: open职业规划 → 自我陈述⑤")
else:
    problems.append("悬空引用原串未找到(open职业规划 hint 可能已被改)")

if problems:
    print("❌ 组装问题,未写文件:"); [print("  -", p) for p in problems]; sys.exit(1)

# --- F. 完整性断言 + 原子写 ---
assert html.count("<div") == html.count("</div>"), f"全文 div 不平衡: {html.count('<div')}/{html.count('</div>')}"
assert "<script>" in html and "</script>" in html, "script 残缺"
tmp = HTML + ".tmp"
open(tmp, "w", encoding="utf-8").write(html)
os.replace(tmp, HTML)
print("✅ 综合重构组装完成")
