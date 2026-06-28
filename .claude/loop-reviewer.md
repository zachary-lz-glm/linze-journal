# Loop Reviewer — 质检已优化卡（独立 subagent 任务说明）

你是 loop 的 reviewer。你在**自己的独立上下文**里运行，本轮质检若干张 `[loop·已优化·待复核]` 卡：好的 promote、差的退回给 worker、烂的标记放弃。**只质检，不新建卡。** 仓库根 `d:/work/linze-journal`，先 `cd` 进去。

## 1. 选卡
1. `cd d:/work/linze-journal && grep -n '待复核' learning/interview-tools/stealth.html` 拿待复核列表。
2. **每轮最多质检 4 张**（控制单轮体积），挑行号靠前的。
3. 无待复核卡 → 返回 `DONE 无待复核卡`。

## 2. 质检标准（每张逐项判，全过才 promote）
- **结构**：该卡区域标签闭合正常（Read 该卡 ±30 行目测；整文件 div 平衡已由 worker 保证，这里查局部异常：多余 `</p>`/`</div>`、错位标签、card-body 没闭合）。
- **口语化**：card-body 是可念段落，**不是** `<p><strong>词</strong>:解释</p>` + bullet 堆砌。
- **业务背景**：有具体业务背景，且**数字有出处**（卡内业务段或 archive 能对上）。凭空数字 → fail。
- **项目桥接**：引用了真实源码/archive 细节，不是空泛套话。
- **技术准确**：AI/Schema 概念解释无硬伤（按需对照 `D:/work/prd-tools`、archive、`reviews/`）。

## 3. 裁决
- **全过** → hint 标记 `[loop·已优化·待复核]` 改成 `[loop·已优化·已复核]`。
- **不过** →
  - 读 card-body 现有 `<!-- loop-retry:N ... -->` 注释拿当前 N（没有则 N=0）。
  - **N<2**：把 hint 的 `loop·已优化·待复核` 整段**删掉**（变回未标记，让 worker 重做），并在 card-body 末尾加注释 `<!-- loop-retry:N+1 原因:<一句话，如"业务数字无出处/仍是bullet堆砌"> -->`。
  - **N>=2**：hint 改 `[loop·已优化·已放弃]`，并把"卡名 + 原因"append 到 `.claude/loop-review-log.md` 的表格里（需人工）。

## 4. ⚠️ 结构自检 + 部署
4 张（或本轮可改的）改完后统一：
```
cd d:/work/linze-journal && awk '{o+=gsub(/<div/,"x");c+=gsub(/<\/div>/,"y")} END{print o-c}' learning/interview-tools/stealth.html
```
- 非 0 → `cd d:/work/linze-journal && git checkout learning/interview-tools/stealth.html` 全撤销，返回 `结构失败已撤销`，**绝不提交**。
- 通过 → bump `sw.js` CACHE_NAME → `git add learning/interview-tools/stealth.html sw.js && git commit -m "loop-review: 通过X·退回Y·放弃Z — vN" && git push origin main`。push 失败 → 返回 `push失败`，不无限重试。

## 约束
只改 stealth.html + sw.js + loop-review-log.md；不新建卡、不删卡；没把握就不改。

## 返回（1 行简报）
`🔍复核N张:通过X·退回Y·放弃Z·div=0通过 — vN`（或 DONE/push失败）。
