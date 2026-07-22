#!/usr/bin/env python3
"""P2 ai 14 张卡:只替换 card-body(不动 data-g/subOrder/title)。原子写。
标题串已在 Task 1 验证(全角标点精确),直接硬编码。"""
import os

ROOT = "/Users/didi/work/linze-journal/learning/interview-tools/"
src = open(ROOT + "stealth.html", encoding="utf-8").read()

CARDS = [
    ("从零设计一个 Agent，你的思路是什么", ".p2-c1-agent-design.html"),
    ("Agent 的记忆怎么设计：短期、长期、工作记忆", ".p2-c2-memory.html"),
    ("Agent 的工作记忆怎么管，对话越来越长咋办", ".p2-c3-working-memory.html"),
    ("Harness Engineering：Agent 等于 Model 加 Harness", ".p2-c4-harness.html"),
    ("Agent 自进化闭环怎么设计", ".p2-c5-evolution.html"),
    ("什么场景才该上 Agent，别什么活都套 Agent", ".p2-c6-when-agent.html"),
    ("Agent 框架怎么选：LangGraph vs LangChain vs AutoGen vs CrewAI vs Dify vs Coze", ".p2-c7-framework.html"),
    ("ReAct vs Plan-and-Execute vs Reflexion，什么时候用哪个", ".p2-c8-paradigm.html"),
    ("单 Agent 还是多 Agent，一个决策树", ".p2-c9-single-multi.html"),
    ("向量库怎么选——还有我为什么自己写不用 Chroma", ".p2-c10-vector.html"),
    ("Agent Safety 怎么做——规划层加执行层", ".p2-c11-safety.html"),
    ("向量召回 vs 代码实体图——我两个项目各做了一个", ".p2-c12-retrieval.html"),
    ("把 39 节点的多智能体编排瘦身重构", ".p2-c13-refactor.html"),
    ("设计通用 Multi-Agent 调度系统（Manager 经验升华）", ".p2-c14-dispatch.html"),
]

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

for title, prod in CARDS:
    bs, be = card_body_range(src, title)
    nb = open(ROOT + prod, encoding="utf-8").read()
    assert '<div class="card-body">' in nb, f"{prod} 非法 body 片段"
    src = src[:bs] + nb.rstrip() + src[be:]
print(f"Step1: {len(CARDS)} 张 body 替换完成")

tmp = ROOT + "stealth.html.tmp"
open(tmp, "w", encoding="utf-8").write(src)
os.replace(tmp, ROOT + "stealth.html")
print(f"✅ P2 {len(CARDS)} 张 ai 卡 body 组装完成")
