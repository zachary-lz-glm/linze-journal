# stealth PRD 工作流模块重构 · Design Spec

> 2026-07-24。把 `learning/interview-tools/stealth.html` 里散在一个 flat 列表的 PRD 卡(含 A10 这种最重要却不在 PRD 组的卡)重组成 **8 个主题模块**,每模块三层(深挖主卡 + 精修弹药 + 追问库),源码核对 + 对齐外部方法论,目标扛住 L7 二面三面深挖。
> 承接 [[stealth-full-refactor-roadmap]] 的「PRD 归位」子项目并扩成完整模块化。遵循 `learning/interview-tools/STEALTH-CARDS-GUIDE.md` 全部铁律。

## 1. 背景与目标

**现状(2026-07-24 勘察):**
- 42 张卡挂 `data-g="PRD 工作流"`(subOrder 1.7),但按**插入历史**排,不按主题。
- 最关键的「从 PRD 到上线的完整链路」(A10,line 579)和「最有技术挑战」(A5,line 546)**根本不在 PRD 组**,散在 proj 根 → 这是"零散"感的根因之一。
- 重复/重叠卡多:两张 5h→2h(2326/3010)、三张 Skill/Tools 区别(2550/2562/2595)、两张"工作流介绍"(533/2456)、两张"质量保证"(2420/2810)。
- 缺口:`reference 冷启动`、`工错流出错`(错误/编造流到产物)、`推广阻力与解法` 都没专门卡。

**目标:** PRD 工作流改成 8 主题模块,每模块 = 1 张 Form A 深挖主卡(源码核对)+ 精修弹药(去重)+ 1 张追问库卡(外部方法论预判追问)。让候选人被 L7 追到第 3-5 层 Why 不散。

**非目标(本轮不做):**
- 不动 proj 其它组(Manager/Code/前端项目/AI 总览等)。
- 不改 quickbar/routing/subOrder 机制(单组+主题分区,routing 零改动)。
- 不做跨场挖失分模式(roadmap 另列子项目)。

## 2. 结构机制(已与用户敲定)

- **单组 + 主题分区**:`PRD 工作流` 仍是一个 quickbar 按钮,subOrder 1.7 不动。
- 组内按 **入口总览 + 8 模块** 聚成 9 簇,DOM 顺序排列。
- **模块主卡当分隔 + 导览**:每簇第一张主卡加视觉区分 —— 新增 CSS `.card.master`(左侧色条 + 略大 tag),tag 文本写 `◆ 模块名`。CSS 增量极小(一条规则),写在现有 `<style>` 内。
- **tag 正式化成模块名**:reference / 蒸馏 / 架构 / 对比 / 质量 / 端到端 / 实现 / 推广。现场扫 tag 知归属。
- **追问库卡(用户拍板选项 c)**:8 张普通卡,不做特殊弱化,平铺在各模块簇尾。tag 用 `追问`。
- **组装**:Python 锚点脚本,按模块注释 `<!-- ===== PRD 模块 N: xxx ===== -->` 之间的整块替换/插入,复用 D 模块 `assemble_d.py` 的 title-锚点 + depth 计数插入法。`subOrder`、`getGroup` 不动(组内按 DOM 序展示)。
- routing 验收:改完后 `grep` 确认 `data-g="PRD 工作流"` 卡数、div 平衡、`<script>` 完整、quickbar 按钮数不变。

## 3. 模块 → 卡片映射(核心)

> 标注:【沿用】不动 /【精修】改 body /【合并】并入他卡后删 /【新主】Form A 深挖主卡 /【新弹】补缺弹药 /【追问库】新追问库卡。行号是 2026-07-24 勘察值,执行时以 title 锚点为准。

### 入口 · 项目总览(组首,非编号模块)
| 卡 | 处理 |
|---|---|
| 533 总览·这个项目是做什么的 | 【沿用·精修】组首 lead master(已 5 段源码核对),补 cross-ref 指向 8 模块主卡 |
| 2696 prd-tools 4个王牌素材 | 【沿用】顶部亮点弹药 |
| 2456 AI工作流完整介绍(面试第一答) | 【合并】并入 533(内容重叠),删 |

> A5(最有挑战,line 546)留在 proj 根,不搬,只在 533 加双向 cross-ref。

### ① reference 深挖(知识库 + 边界)
| 卡 | 处理 |
|---|---|
| (新)reference 模块主卡 | 【新主】Form A:数据结构(6 yaml + 自研倒排索引 schema)→ 算法(6 Phase 顺序产出 + 后生成查先生成去重)→ 为何自研(拒绝全量塞 context / 拒绝纯向量做精确路由)→ 踩坑/诚实(eval 债) |
| 2223 AI 怎么理解陌生项目 | 【合并】并入主卡 |
| 2583 知识库本质定位(阿里纠正) | 【沿用】约束层定位,重要反驳点 |
| 2467 /reference 6 文件深挖(D 卡) | 【沿用】数据结构深挖弹药,挂在主卡后 |
| 2277 reference 知识过时(G1) | 【沿用】边界:知识保鲜 |
| (新)reference 冷启动 | 【新弹】新项目无历史数据怎么 bootstrap reference |
| (新)reference 追问库 | 【追问库】 |

### ② PRD 蒸馏深挖(11 步 + 边界 + 产物)
| 卡 | 处理 |
|---|---|
| (新)PRD 蒸馏模块主卡 | 【新主】Form A:11 步流水线怎么跑、每步产出、为何硬停一步等人确认 |
| 2232 PRD 到代码最难的一步(变更分类) | 【沿用】 |
| 2293 2-3万字 PRD 打爆 Context(G2) | 【沿用】边界 |
| 2309 团队模式准确率 60% 损耗(G3) | 【沿用】边界 |
| 2444 PRD 摄入:多格式输入与图片并行 | 【沿用】 |
| 2480 Spec 和 Plan 长什么样 | 【沿用】产物 |
| (新)PRD 蒸馏追问库 | 【追问库】 |

### ③ 整体架构设计
| 卡 | 处理 |
|---|---|
| (新)架构主卡 | 【新主】Form A:双插件为何拆(上下文隔离)+ 能力面适配器 + 为何放弃 MCP(A5 弯路源真值) |
| 2408 双插件体系 | 【沿用】 |
| 2386 能力面适配器怎么设计 | 【沿用】 |
| 2622 传统工程思维在 AI 系统的映射 | 【沿用】 |
| (新)架构追问库 | 【追问库】 |
> 2396 BMAD → 移到 ④(对比)。

### ④ 对比市面工具优劣
| 卡 | 处理 |
|---|---|
| (新)对比主卡 | 【新主】系统对比 Cursor / Copilot / Windsurf / Devin / BMAD / Claude Code init,讲差异化(已有项目 vs 从 0 到 1、证据层、可追溯) |
| 2344 和 Claude Code init / Cursor 区别(G5) | 【沿用】 |
| 2643 有 Claude Code 了为何自定义 Agent | 【沿用】 |
| 2396 BMAD 架构(多 Skill 拆分) | 【沿用·从③移入】作为对比项 |
| (新)对比追问库 | 【追问库】 |

### ⑤ SSOT / 证据链 / 评估门禁 / 效果验证
| 卡 | 处理 |
|---|---|
| (新)质量可信链主卡 | 【新主】Form A:SSOT + 证据链 + 门禁 + eval 怎么串成可信链 |
| 2264 SSOT 五条边界规则 | 【沿用】 |
| 2787 证据链机制详解 | 【沿用】 |
| 2420 质量门控:门禁体系 | 【沿用·吸收 2810】(2810 的"执行不稳定保质量"内容并入此卡) |
| 2432 Readiness Score 评分 | 【沿用】 |
| 2534 AI 工作流优化迭代(Benchmark) | 【沿用】 |
| 2326 + 3010 两张 5h→2h | 【合并】→ 1 张「效果验证:5h→2h 怎么测的」(度量口径 + 实验组对照组,诚实说分母/样本局限) |
| 2810 Skill 执行不稳定保质量 | 【合并】并入 2420 |
| (新)质量追问库 | 【追问库】 |

### ⑥ 端到端
| 卡 | 处理 |
|---|---|
| A10(line 579)从 PRD 到上线的完整链路 | 【搬入·沿用】模块主卡(双轨 + 6 阶段,已是好主卡),从 proj 根移入 PRD 组,挂 `data-g="PRD 工作流"` |
| 2491 端到端:自验证 + 自修复循环 | 【沿用】 |
| 2504 端到端:模板/LLM 双路径 + verified_by | 【沿用】 |
| 2518 端到端 → 生产三步过渡 | 【沿用】 |
| 3101 Harness 三种引擎 | 【沿用】 |
| 3087 SDD 完整流程 | 【沿用·从④移入,用户拍板】 |
| (新)端到端追问库 | 【追问库】 |

### ⑦ 实现深坑(tools/skill·识别率·幻觉·上下文定位·PRD变更·工错流·归因)
| 卡 | 处理 |
|---|---|
| (新)实现深坑主卡 | 【新主】Form A:踩过的工程坑 + 怎么解(MCP 不行 / 识别率 / 幻觉 / 上下文漏) |
| 2609 Tool 识别率下降 | 【沿用】 |
| 2671 幻觉四层防线(聚合卡) | 【沿用】 |
| 2775 上下文怎么定位不超 context 不漏文件 | 【沿用】 |
| 2852 AI 工作流出错归因修复 | 【沿用】 |
| 2821 PRD 过时或临时改动怎么同步 | 【沿用】 |
| 2550 + 2562 + 2595 三张 Skill/Tools 区别 | 【合并】→ 1 张「Skill/Tools/Function Calling 边界」 |
| (新)工错流出错 | 【新弹】错误/编造怎么流到产物、怎么拦(四层防线在产物侧的落地) |
| (新)实现追问库 | 【追问库】 |

### ⑧ 推广落地(落地·阻力·解决)
| 卡 | 处理 |
|---|---|
| (新)推广主卡 | 【新主】Form A:怎么在团队推 + 遇到什么阻力(质量责任划分 / 各人工具偏好 / 信任) + 怎么解(小范围试点 / ROI 量化 / 赋能不替代) |
| 2899 AI 工作流推广 ROI | 【沿用】 |
| 2715 PRD 质量卡口:赋能产品 | 【沿用】 |
| 2799 AI 工作流在团队怎么落地 | 【沿用】 |
| (新)推广阻力与解法 | 【新弹】L7 必问,单独弹药卡(阻力清单 + 对应解法) |
| (新)推广追问库 | 【追问库】 |

## 4. 卡片数变化

- 工作集:组内 42 + A10 搬入 = 43
- 合并删除:2456、2223、2326+3010→1、2810、2550+2562+2595→1 = **−6**
- 新主卡:①②③④⑤⑦⑧ = **+7**(⑥ 沿用 A10)
- 追问库:**+8**
- 补缺弹药:冷启动、工错流、推广阻力 = **+3**
- **净 ≈ 43 − 6 + 7 + 8 + 3 = 55 张**(用户已确认多几张无所谓)

## 5. 源码核对策略(GUIDE #1 铁律)

- 每个新主卡 / 补缺卡 / 追问库:派 agent 读 `/Users/didi/work/prd-to-code` + `/Users/didi/work/prd2code-gen` + `/Users/didi/work/prd-tools` 真源码,产「事实清单 + ✅⚠️❌ 可说清单」再写卡。
- 已知有源码支撑可写实数:reference 6 yaml、11 步蒸馏、Readiness 五维加权(85/60 降级)、证据链 8 类、negative_code_search、prd2code-gen 双路径(Handlebars 0 token + LLM 兜底)、4 类校验 + 3 次重试 + A→B→A 震荡检测、eval/auto-tune 五模块、R01/R02 对照(54→68)。
- 源码没硬编的不报(如向量维度):明说"模型决定、不报数字"。
- 文档 vs 代码不一致:以代码为准,面试说模糊数。

## 6. 外部方法论 → 追问库(5 源)

每模块追问库卡由这 5 个源蒸馏该模块的预判追问 + 一句话答案:
- MyEngineeringPath 11 段模板 + 105 追问(https://myengineeringpath.dev/interview-guide/)
- alexeygrigorev 项目深挖题集(https://github.com/alexeygrigorev/ai-engineering-field-guide/blob/main/interview/questions/03-project-deep-dive.md)
- zsc 5-Why 深度追问(https://github.com/zsc/interview_tutorial)
- 掘金"证据链"总纲(https://juejin.cn/post/7644082483090587658)— 可追问/可验证/可复盘
- CLEAR 框架(https://www.pivotjourneys.com/blog/star-format-interview-prep-clear-is-better)— Context/Leadership/Execution/Accomplishment-Results

执行时用 WebFetch 拉取(公开内容),按模块归类,答案对照源码核对避免编造。

## 7. 诚实边界 / 避雷清单(check 脚本 per-project warn)

- 雷区词只能在"不用/拒绝/对比"否定语境出现,不能当自述:Chroma、git 钩子、Claude/GPT(模型是 qwen)、SDD 平台(真身是 Claude Code 插件)、6 步闭环(原型不存在生产级)。
- 软化:团队规模用 ADR-0005 "约 1–5 人"口径;"端到端"必带"个人原型探索、非生产级闭环";推广说"小范围在用"。
- eval 债主动认:没建 labeled query set 测 recall@K / nDCG 是已知评测债。
- 复用 `check_d.py` 的 per-project 雷区 warn(非 naive err,靠人工确认语境)+ "6 步闭环"硬 err。

## 8. 卡型风格(对标 GUIDE §6 参考卡 + §7 Form A)

- 主卡:Form A 四要素(数据结构 → 算法 → 为何自研拒绝 X → 踩坑/诚实边界),≥4 段 `<strong>领起。</strong>`,declarative 不碎嘴(禁"说白了/得说句实话")。对标「从 PRD 到上线的完整链路」(A10)。
- 弹药卡:精修 body,杀重叠,保留各自的 ✅⚠️❌ 校准。
- 追问库卡:`<ul class="points">` 列预判追问 + 一句话答案,挂簇尾。
- 所有新卡:`data-g="PRD 工作流"` + 充实 `data-kw`(各种问法)+ 标题不带英文项目名前缀。

## 9. 执行流程(同 A/C/B/D)

1. writing-plans 产出实施计划(分模块 task)。
2. 多 agent 执行:每模块一个 general-purpose agent,prompt 写死"只动指定卡/只产独立 HTML 片段,禁碰其它"(【agent-scope-constraint】),读源码 + 校准清单 + GUIDE §1/§6/§7 铁律。
3. `check_prd.py`(改造自 `check_d.py`):四要素词命中 + strong≥4 + 禁碎嘴 + ①②③④⑤不堆叠 + div 平衡 + 完整 card 片段 + "6 步闭环"硬 err + per-project 雷区 warn。
4. `assemble_prd.py`(改造自 `assemble_d.py`):按模块注释锚点 + title 深度计数,搬入 A10、插入新卡、重排成 9 簇。脚本最后才写文件(原子)。
5. bump `sw.js` `CACHE_NAME`:执行时先 `git show origin/main:sw.js | grep CACHE_NAME` 看已部署版本 +1(当前 origin = kb-v335 → 预计 kb-v336,以执行时为准)。硬刷新一次。
6. 提交前 `git status` 确认工作区干净,防串 commit(GUIDE §4.6)。

## 10. 验收标准

- [ ] `data-g="PRD 工作流"` 卡数 ≈ 55,9 簇按 入口+①~⑧ 顺序。
- [ ] A10 已移入 PRD 组、挂 `data-g`;A5 留 proj 根但有 cross-ref。
- [ ] 8 张模块主卡均为 Form A 四要素、源码核对、无雷区自述。
- [ ] 8 张追问库卡覆盖 5 个外部方法论的预判追问。
- [ ] 合并完成:2456/2223/2326+3010/2810/2550+2562+2595 不再独立存在(并入目标)。
- [ ] 补缺卡存在:冷启动、工错流、推广阻力。
- [ ] `.card.master` CSS 生效;tag 正式化为模块名。
- [ ] div 平衡、`<script>` 完整、quickbar 按钮数不变、subOrder 不动。
- [ ] `sw.js` CACHE_NAME bump(看 origin +1)。

## 11. 风险与开放问题

- **卡片总数涨到 ~55**:用户已确认接受。若后续觉得手机滚动累,可给追问库卡加 `data-g2` 做二级折叠(本轮不做)。
- **源码与现有卡口径冲突**:以源码为准,改卡时同步更新该模块其它卡的数字。
- **A10 搬入的 routing 风险**:A10 当前在 proj 根无 data-g,搬入只需加 `data-g="PRD 工作流"` + 物理移动 DOM;搬后 grep 确认 proj 根不再有游离 A10。
- **追问库答案准确性**:WebFetch 拉的外部方法论是"提问角度",答案必须对照本项目源码核对,不能照搬通用答案。

## 12. 复用资产

- `check_d.py` → `check_prd.py`(per-project 雷区 warn + 四要素)
- `assemble_d.py` → `assemble_prd.py`(title 锚点 + depth 插入)
- `learning/interview-tools/STEALTH-CARDS-GUIDE.md` §1/§6/§7 铁律
- 现有 ✅⚠️❌ 校准清单(`learning/interview-kb/明日面试_预测题校准与匹配分析.md` + 源码重读)
