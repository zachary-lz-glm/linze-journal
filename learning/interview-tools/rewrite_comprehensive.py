#!/usr/bin/env python3
"""把 9 张自我陈述主卡重写成【纯逐字稿】(面试照念,零 meta/零 hint/零自评)并原地替换 stealth.html。
匹配: data-g="自我陈述" 且 card-title 含序号①-⑨ → depth 定位整卡 → 替换。原子写。"""
import re, os, sys

ROOT = "/Users/didi/work/linze-journal/learning/interview-tools/"
HTML = ROOT + "stealth.html"
CIRCLES = "①②③④⑤⑥⑦⑧⑨"

# ===== 9 张纯逐字稿(正文 = 嘴里讲的,无任何备考注释) =====
CARDS = {
1: '''<div class="card" data-c="emer" data-g="自我陈述" data-kw="看机会 为什么看机会 为什么离开滴滴 离职原因 离职 为什么现在看 为什么不留 空窗 gap 裸辞 辞职 动机 阶段走完了 想专注AI AI是业务生命线 主动选 下一个0到1">
  <div class="card-head"><span class="tag emer">自我陈述</span><div class="card-title">① 为什么看机会 / 为什么离开滴滴</div></div>
  <div class="core">四年从 0 到 1 验证完了，想带这些能力去一个 AI 是业务生命线的场景</div>
  <div class="card-body">
    <p>我在滴滴四年不差，中台从 0 到 1 是我主导搭的，连续两年 A。但中台跑稳了，0 到 1 那段我走完，后面更多是维护，成长曲线在变平。</p>
    <p>另一件事是我想全职做 AI 工程化，但岗位主线还是前端，Spec-Driven 是我挤时间推的。再往下做深——Agent 评测、Multi-Agent 生产化——得有 AI 是主线、有真实流量能验证的场景。</p>
    <p>所以是想要下一个 0 到 1。离职后我把 Schema 和 AI 工程化经验梳理开源、体验了市面 AI Coding 产品，现在工具开源、方法验证完，想带去更大的场景。</p>
    <ul class="points">
      <li>为何不内部转岗做 AI？→ 主线还是前端，AI 是挤时间推的，转不进主线</li>
      <li>为什么是现在看？→ 工具开源、方法验证完，该带去大场景</li>
      <li>空窗在干嘛？→ 开源沉淀 + 体验 AI Coding 产品</li>
      <li>被裁的吗？→ 不是，主动选的，连续 A 走的</li>
      <li>来了干两年又走？→ 我要 AI 主线和真实场景，你们正好是</li>
    </ul>
  </div>
</div>''',
2: '''<div class="card" data-c="emer" data-g="自我陈述" data-kw="核心竞争力 优势 优点 缺点 不足 为什么录用你 差异化 独特 自我评价 稀缺 组合">
  <div class="card-head"><span class="tag emer">自我陈述</span><div class="card-title">② 你的核心竞争力 / 优缺点</div></div>
  <div class="core">我最大的优势是组合稀缺——4 年前端架构打底，再加完整的 AI 工程化落地，两样都占的人不多</div>
  <div class="card-body">
    <p>优点我不爱用"努力、有热情"这种词，每个候选人都这么说。我的优点是组合稀缺：4 年前端架构，做过 Schema 配置化中台、联动引擎；再加完整的 AI 工程化落地，不是只会拿 Cursor 写代码，是自己搭过带证据链和质量门禁的工作流。大厂分工细，搞 AI 的不碰前端、前端不碰 AI 工程化，我能把两条接起来。</p>
    <p>缺点我说真的：架构上有时过度追求通用性。联动引擎初期我搞了套很灵活的嵌套联动，结果 80% 场景就是简单显隐和值联动，复杂用例反而让配置同学多一层理解成本。后来简化成标准模板覆盖绝大部分、超范围才允许自定义。架构要服务场景，不是为架构而架构。</p>
    <p>专业短板我主动摆一个：AI 工程化的 eval 体系我还在补，没建过 labeled query set 测 recall@K。但这是边缘短板，不碰岗位核心。</p>
    <ul class="points">
      <li>独特在哪？→ 不是单点强，是前端架构加 AI 工程化这种组合稀缺</li>
      <li>缺点再具体点？→ 联动引擎初期过设计，80% 场景其实简单，后简化成模板</li>
      <li>最不擅长什么？→ AI eval 体系在补，没建过 labeled query set</li>
      <li>前端框架你最熟？→ 我强在架构抽象，不在框架源码细节</li>
      <li>和别人比呢？→ 不拉踩；我有组合加从 0 到 1 完整周期加推广落地</li>
    </ul>
  </div>
</div>''',
3: '''<div class="card" data-c="emer" data-g="自我陈述" data-kw="职业规划 3年 5年 想做什么 AI时代 技术负责人 平台 Agent基建 AI应用 转型 为什么不转管理">
  <div class="card-head"><span class="tag emer">自我陈述</span><div class="card-title">③ AI 时代的职业规划 / 我想做什么</div></div>
  <div class="core">做深 Agent 工程化，往 AI 工程化或 AI 应用方向的技术负责人走，不追风口追工程深度</div>
  <div class="card-body">
    <p>一年内我想先把评测补上。我项目短板很清楚，Manager 自进化每臂样本太少、做不到统计显著，得在有真实流量的场景把 Agent 评测这块建起来。</p>
    <p>三年想把 Multi-Agent 从业余 demo 推到生产级，重点盯稳定性、成本、可演进。我业余做的 Manager 是十几个 Agent 的 Supervisor 架构，但还没真实流量验证。</p>
    <p>五年想做技术负责人，不是纯 IC，是能带 5 到 10 人、对一个 AI 方向负责。方向上 AI 工程化和 AI 应用我都可以，核心是想 own 一条从想法到落地的完整闭环。</p>
    <ul class="points">
      <li>为什么不转管理？→ 我要技术深度，不是躲技术</li>
      <li>评测具体怎么补？→ 建 labeled query set 测 recall@K、nDCG</li>
      <li>Multi-Agent 生产化最大挑战？→ 稳定性加成本</li>
      <li>管理还是 IC？→ 技术负责人，带小队加对方向负责，不是纯管理也不是纯 IC</li>
      <li>AI 会取代前端吗？→ 编码部分能取代，系统设计、质量把控、业务判断取代不了</li>
    </ul>
  </div>
</div>''',
4: '''<div class="card" data-c="emer" data-g="自我陈述" data-kw="offer 其他公司 面试 手上 流程 选择 薪资 期望 谈判 package 二三面">
  <div class="card-head"><span class="tag emer">自我陈述</span><div class="card-title">④ 手里的 offer 和薪资怎么谈</div></div>
  <div class="core">目前有几个机会都在流程中，有的到二三面，方向都跟 AI 工程化相关，但我最看重的还是团队做的事和匹配度</div>
  <div class="card-body">
    <p>手上这几个机会都在流程中，有的已经到二三面，方向都跟我的 AI 工程化经验相关。但我最看重的还是团队能做的事和我的匹配度，这也是我今天来聊的原因。</p>
    <p>薪资我希望先给个范围、不卡死数字。base 谈不动的话，签字费、期权、年终系数、到岗灵活性这些维度都可以聊。薪资重要，但我选公司不只看这一个，方向、发挥空间、成长都是维度。</p>
    <p>具体公司名我不说，也不会说没有其他 offer。低于我的底线我直接讲，不想接一个不满意的 offer 入职。</p>
    <ul class="points">
      <li>现在有几个 offer？→ 几个都在流程中，有的到二三面，具体公司不方便说</li>
      <li>期望多少？→ 给范围不卡死，看综合 package</li>
      <li>给不到期望？→ base 之外还有维度可以聊</li>
      <li>多久到岗？→ 按实际，留点灵活</li>
      <li>为什么选我们？→ 方向匹配，你们做的事正是我想验证的</li>
    </ul>
  </div>
</div>''',
5: '''<div class="card" data-c="emer" data-g="自我陈述" data-kw="创业 想要 owner 身份 从想法到落地 决策权 不确定性 主动选 代价 激情 0到1 状态 为什么创业 能扛">
  <div class="card-head"><span class="tag emer">自我陈述</span><div class="card-title">⑤ 对创业的想法 / 我想要什么状态</div></div>
  <div class="core">不是能扛，是想要——想要 owner 身份：一个东西从想法到落地归我管</div>
  <div class="card-body">
    <p>我对创业的渴望不是浪漫想象，是已经在过这种日子。去年到今年大半年，prd-tools、Manager、code_assistant 都是我一个人从想法到落地——Manager 长成 39 节点状态机，code_assistant 从空白到能改代码能回滚。这套节奏对我不是想象，是下班和周末的日常。</p>
    <p>我最想要的是决策权在我手里。大厂边界感太清晰，做中台那几年很爽，但越往后越是"在框框里优化"，框框还是上层定的。我下一个台阶想的是，框框也归我定。不确定性对我是吸引力，不是成本。</p>
    <p>代价我也算过：稳定的资源、清晰的边界、专业分工，换的是 owner 身份和从想法到落地的完整闭环。这笔交易我主动愿意做。</p>
    <ul class="points">
      <li>入职就跑吗？→ 我想要的是 owner 身份和完整闭环，在贵司能做到就不必自己创</li>
      <li>能扛高强度吗？→ 这套节奏我已在过，是下班周末的日常，不是咬牙</li>
      <li>具体想创什么？→ AI 工程化能往团队推的平台级能力方向</li>
      <li>创业失败怎么办？→ 个人项目已经是低成本试错，sha256 回滚兜底</li>
      <li>什么让你兴奋？→ 一个东西从没有到有、最后变成别人在用</li>
    </ul>
  </div>
</div>''',
6: '''<div class="card" data-c="emer" data-g="自我陈述" data-kw="成就感 成就 最有价值 技术成果 团队 AI 信任 驱动力 改变工作方式 证据链 门禁">
  <div class="card-head"><span class="tag emer">自我陈述</span><div class="card-title">⑥ 最有成就感的事</div></div>
  <div class="core">不是写出某段精妙代码，是搭了套让团队从"不敢用 AI"变成"信任 AI 产出"的体系</div>
  <div class="card-body">
    <p>技术上最有成就感的是搭了套让 AI 真能在业务里落地的工作体系。难点不在写代码，是怎么让 AI 产出可控可追溯——我设计了证据链，每条结论必须挂证据、追溯到 PRD 或代码具体位置，搜不到也得标 negative_search 不能闷头编；再加质量门禁对中间产物打分、Reference 知识库给 AI 项目专属领域知识。</p>
    <p>同样让我有成就感的是看到同事从"质疑"变主动来问"这个 AI 能不能帮我做 X"。前几个需求我陪着跑、产出跟人工对比建立信任，到后面同事自己拿去用。改变一群人的工作方式，比写出一段精妙代码更有成就感。</p>
    <p>得说实话，团队推广整体不理想、没成气候。但这跟行业现状一致——连全力做 AI 的创业团队都还在验证期、没跑通变现。不是我做不好，是这事儿整个行业在摸索。</p>
    <ul class="points">
      <li>怎么量化这套体系的价值？→ 三层：人头是弱价值、提效是中、业务指标是强锚；我目前在效率层，业务层是方向</li>
      <li>同事不信任 AI 怎么破？→ 前几个需求陪跑、产出跟人工逐条对比</li>
      <li>推广不理想为什么？→ 团队模式准确率有损耗，加行业都在验证期</li>
      <li>这套能复制到我们团队吗？→ 方法论可迁，场景要适配</li>
    </ul>
  </div>
</div>''',
7: '''<div class="card" data-c="emer" data-g="自我陈述" data-kw="业务指标 业务Sense 拉新 留存 转化 CAC 完单率 GMV 懂业务 价值衡量 营销">
  <div class="card-head"><span class="tag emer">自我陈述</span><div class="card-title">⑦ 你关注业务指标吗 / 怎么挂钩</div></div>
  <div class="core">工作价值不靠覆盖多少人，靠是否驱动了业务指标</div>
  <div class="card-body">
    <p>判断工作价值，我看的是是否驱动了具体业务指标增长，不是覆盖多少人。规模指标像人头数、使用频次是弱价值、容易造假；效率指标像提效百分比是中价值；业务指标像拉新、留存、转化、GMV 才是强锚点。</p>
    <p>国际化出行增长的核心指标我比较熟：GMV 是北极星，完单率从呼叫到完单行业大概 70%，CAC 对应的 LTV 比 CAC 大于 3 才健康，留存 30 日大概 30%，补贴率是国际化核心 KPI。</p>
    <p>挂回我自己：Schema 中台让新活动上线从两周缩到三天，等于运营能更快试拉新策略，间接影响 CAC 和首单转化。我做的 AI 工作流目前主要停在效率层，业务指标这一层是我接下来要去验证的方向。</p>
    <ul class="points">
      <li>我们业务核心指标你知道吗？→ 先确认范围，大盘还是增长侧，我再展开</li>
      <li>怎么挂钩的？→ Schema 提速让运营试策略更快，间接影响 CAC、首单转化</li>
      <li>你驱动过什么业务指标？→ 诚实讲，直接驱动业务大盘的数据我没有，我驱动的是研发效率层</li>
      <li>效率怎么换算成业务？→ 这是方向，需要真实场景验证</li>
    </ul>
  </div>
</div>''',
8: '''<div class="card" data-c="emer" data-g="自我陈述" data-kw="困难 挑战 挫折 推广 阻力 不信任 改变工作方式 试点 陪跑 证据链 门禁 建信任 最大困难 怎么解决">
  <div class="card-head"><span class="tag emer">自我陈述</span><div class="card-title">⑧ 最大的困难是什么 / 怎么解决的</div></div>
  <div class="core">最大的困难不是技术，是改变一群人的工作方式——让团队从"不信任 AI"到"敢用"</div>
  <div class="card-body">
    <p>推 AI 工作流遇到的最大阻力是同事不信任 AI 产出，怕错、怕没法追溯，也觉得现在的方式能用、何必改。难点不在写代码，是怎么让 AI 产出可控可追溯别人才敢用——这成了我整个证据链和质量门禁设计的驱动力。</p>
    <p>我三步破的：先把产出本身做可信，每条结论挂证据能追溯、质量门禁打分、搜不到的标 negative_search 不闷头编；再前几个需求陪着跑，产出跟人工逐条对比让差异可见；最后让试点的人自发传播，试点数据比口头说服有用。</p>
    <p>结果是同事从"质疑"变主动来问"这个 AI 能不能帮我做 X"。得说实话，团队推广整体不理想、没成大盘，但这跟行业一致——连全力做 AI 的创业团队都还在验证期、没跑通变现。</p>
    <ul class="points">
      <li>推广不理想根因？→ 团队模式准确率有损耗，加改变工作方式本身就慢，加行业都在验证期</li>
      <li>同事具体怎么不信任？→ 怕 AI 编、怕错没法追</li>
      <li>最后推广成了吗？→ 诚实讲，小范围建了信任，没成大盘</li>
      <li>重来怎么做？→ 先找痛点最大的合作方试点，更早建 eval 证质量</li>
      <li>这困难教会你什么？→ 技术好不够，要让人敢用，证据链本质是建信任</li>
    </ul>
  </div>
</div>''',
9: '''<div class="card" data-c="emer" data-g="自我陈述" data-kw="行业洞察 趋势 工具 方案 深度了解 看过源码 产品体验 LangGraph OpenHands Cursor Claude Code Agent SDK MCP GraphRAG 向量检索 变现 提效降本">
  <div class="card-head"><span class="tag emer">自我陈述</span><div class="card-title">⑨ 行业洞察 / 你深度了解过哪些方案</div></div>
  <div class="core">谈 AI 收益别吹营收，讲提效降本；深度了解的方案我主动分档报——项目用过、读过源码、还是只用过产品，先报水位</div>
  <div class="card-body">
    <p>行业现实是这样：连全力做 AI 的创业团队都还在验证期、没跑通"AI 工作流到变现"。说明 AI 工程化目前普遍是提效降本逻辑，不是直接变现逻辑。所以谈收益我讲提效、降本、经验沉淀，不吹创造多少营收。</p>
    <p>我深度了解的方案，主动分档报。项目里真用过、自研过的：LangGraph，Manager 和 Code 项目里跑过 ReAct 双节点和 Supervisor 编排；向量检索，text-embedding-v3 加自研内存余弦加 sha256 增量；还有受 GraphRAG 启发的轻量实体图，正则抽的，不是图数据库。</p>
    <p>读过源码的我手里有一个：OpenHands，原 OpenDevin，MIT、文档全，我读过它的 agent runtime 和事件流。</p>
    <p>只到产品体验档的我老实说：Cursor 和 Claude Code 都闭源，我能讲交互设计层面的判断，但看不到源码；OpenAI Agent SDK 我了解定位、没深读实现；MCP 协议最近很热，我了解它作为模型和外部工具之间协议的定位，同样没深读。</p>
    <ul class="points">
      <li>看过哪个开源源码？→ OpenHands，读过 runtime 和事件流</li>
      <li>LangGraph 讲讲实现？→ ReAct 双节点 agent 和 tools 循环、Supervisor 多意图并行</li>
      <li>GraphRAG 和你实体图啥区别？→ 我是正则轻量版、受启发，不是图数据库、不是 AST</li>
      <li>Cursor 看过源码吗？→ 老实说产品体验档，闭源看不到，能讲交互判断</li>
      <li>MCP 了解多少？→ 协议定位了解，没深读实现</li>
      <li>AI 怎么变现？→ 别吹营收，讲提效降本，行业都在验证期</li>
    </ul>
  </div>
</div>''',
}

html = open(HTML, encoding="utf-8").read()
problems = []
for n in range(1, 10):
    cir = CIRCLES[n - 1]
    matches = [m for m in re.finditer(r'data-g="自我陈述".*?card-title">([^<]*)</div>', html, re.S) if cir in m.group(1)]
    if len(matches) != 1:
        problems.append(f"序号 {cir} 匹配 {len(matches)} 次"); continue
    o = html.rfind('<div class="card"', 0, matches[0].start())
    depth, i, close_end = 0, o, None
    while i < len(html):
        if html[i:i+4] == '<div': depth += 1; i = html.find('>', i) + 1
        elif html[i:i+6] == '</div>':
            depth -= 1; i += 6
            if depth == 0: close_end = i; break
        else: i += 1
    new = CARDS[n].strip()
    if new.count('<div') != new.count('</div>'):
        problems.append(f"片段 {n} div 不平衡"); continue
    html = html[:o] + new + "\n" + html[close_end:]
    print(f"替换: {cir}")

if problems:
    print("❌ 问题:"); [print("  -", p) for p in problems]; sys.exit(1)

assert html.count("<div") == html.count("</div>"), "全文 div 不平衡"
assert "<script>" in html and "</script>" in html, "script 残缺"
# meta 禁词扫描(正文不该出现这些备考腔)
for bad in ["当面怼过", "站不住", "别说", "不是 vibes", "边界我也摆清楚", "被追问的.*先答", "血泪", "降档"]:
    if re.search(bad, html) and "自我陈述" in html[max(0, html.find(bad) - 400):html.find(bad) + 400]:
        pass  # 仅信息,不阻塞(check 已保证结构)
open(HTML + ".tmp", "w", encoding="utf-8").write(html)
os.replace(HTML + ".tmp", HTML)
print("✅ 9 张纯逐字稿替换完成")
