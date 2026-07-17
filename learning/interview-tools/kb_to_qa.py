#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
把 01-面试题库.md（主源、同步后的最新版）导出成两列问答 CSV（供云端知识库导入）。

用法： python kb_to_qa.py [题库.md 路径] [输出 csv 路径]
默认： ../interview-kb/01-面试题库.md → ../interview-kb/面试问答库.csv

列： 问题 | 答案
- 问题 = 每个 `### **[标签]** 标题` 去掉标签后的纯标题
- 答案 = 该标题到下一个标题(#/##/###)之间的全部正文（含 > 核心一句话 + 详细回答）
编码： utf-8-sig（带 BOM，Excel 直接双击中文不乱码）

设计：题库.md 是唯一主源，stealth.html 改动先同步进 md，再跑本脚本刷新 CSV。
"""
import os, re, sys, csv

SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "interview-kb", "01-面试题库.md")
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "interview-kb", "面试问答库.csv")

with open(SRC, "r", encoding="utf-8") as f:
    lines = f.read().split("\n")

def clean_title(raw):
    # raw 形如 "**[A1]** Monorepo 怎么管理 15+ 模块？" 或 "**[速查]** 题目关键词 → 搜什么"
    s = raw.strip()
    s = re.sub(r'^\*\*\[[^\]]*\]\*\*\s*', '', s)   # 去掉开头的 **[标签]**
    s = s.replace('**', '')                          # 去掉标题里残留的 ** 加粗
    return s.strip()

rows = []
cur_q = None
cur_a = []

def flush():
    if cur_q:
        ans = "\n".join(cur_a).strip()
        # 去掉答案末尾多余空行
        ans = re.sub(r'\n{3,}', '\n\n', ans)
        rows.append([cur_q, ans])

for line in lines:
    if line.startswith('### '):
        flush()
        cur_q = clean_title(line[4:])
        cur_a = []
    elif line.startswith('# '):   # h1 文档标题，非问答
        flush()
        cur_q = None
        cur_a = []
    elif line.startswith('## '):  # h2 分区标题，非问答；其下到首个 ### 间的引言不收
        flush()
        cur_q = None
        cur_a = []
    else:
        if cur_q is not None:
            cur_a.append(line)
flush()

os.makedirs(os.path.dirname(os.path.abspath(OUT)), exist_ok=True)
with open(OUT, "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f)
    w.writerow(["问题", "答案"])
    w.writerows(rows)

print("导出完成：%d 条问答（2 列：问题/答案） → %s" % (len(rows), OUT))
print("前 5 条问题：")
for r in rows[:5]:
    print("  -", r[0])
print("后 3 条问题（含新增高 ROI 卡）：")
for r in rows[-3:]:
    print("  -", r[0])
