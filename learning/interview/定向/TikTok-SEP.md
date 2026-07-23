# 字节 TikTok · Service Experience Platform · 中后台前端 · 定向准备

> 定向准备文档 · 2026-06-24 整理
> **机会含金量**：字节 3-2 朋友直推 TL，单独约面不走系统（字节最高质量内推）
> 部门：TikTok - Service Experience Platform（客服体验平台）
> 业务方向：中后台系统（客服工作台 / 工单 / 智能客服）
> 来源：字节亲历真题（reviews/transcripts/面经.md）+ 同梯队大厂面经 + 联网最新面经

---

## 〇、背景关键情报（先读）

### 这次机会的特殊性

| 信号 | 解读 | 你该怎么做 |
|------|------|----------|
| **3-2 朋友亲自推** | 字节 3-2 = 资深专家（年薪 350-500 万），用自己信誉背书 | 别让朋友丢脸，准备要扎实 |
| **直接找 TL（Hiring Manager）** | 绕过 HR 筛选，直达决策者 | 等于直接进二面/三面节奏 |
| **单独约面不走系统** | TL 先做技术对齐，**不是正式面试** | 这是"试面"，合适才补正式流程 |
| **TikTok SEP** | TikTok 客服体验平台，中后台 + AI 客服双线 | 业务对口度 9.5/10 |

### ⚠️ 立刻向朋友确认的 3 件事（直接问，3-2 不会介意）

1. **HC 级别**：L3（高级）/L4（资深）/L5（专家）？—— 直接决定级别和薪资
2. **这次约面的性质**：技术评估 / 走个过场就发 offer / 正式面试第一轮？
3. **后续流程**：如果通过，正式流程几轮？是 TikTok 标准的 3 技 + HR，还是有调整？

### TikTok SEP 业务画像（联网 + 推断）

| 模块 | 业务特征 | 你的对口度 |
|------|---------|----------|
| **客服工作台** | 多渠道接入（IM/邮件/电话）、工单流转、坐席管理 | ⭐⭐⭐⭐⭐ Schema 中台直接对口 |
| **智能客服/AI 客服** | 意图识别、自动回复、多大模型混合架构、10 万 QPS | ⭐⭐⭐⭐⭐ prd-tools + AI 工程化直接对口 |
| **工单系统** | 复杂状态机、SLA、分配引擎 | ⭐⭐⭐⭐ 营销联动 DSL 可迁移 |
| **数据看板/报表** | 多维度分析、实时大屏 | ⭐⭐⭐ 需补可视化深度 |
| **全球多区域** | 多语言/多时区/GDPR/CCPA/PIPL | ⭐⭐⭐⭐⭐ 滴滴国际化 10+ 国家直接对口 |

---

## 一、JD 分析与匹配度

> 暂无具体 JD，按字节招聘官网"资深前端研发工程师（客服平台方向）- TikTok Shop"画像 + TikTok SEP 业务特性反推。

### 1.1 推断的岗位要求

| 维度 | 推断要求 | 你的匹配 |
|------|---------|---------|
| React + TypeScript 深度 | React 原理（Fiber/并发模式/Hooks）、TS 高级类型 | ★★★★★ 4 年 React + TS |
| **中后台工程化** | Monorepo + 组件库 + 微前端 + CI/CD | ★★★★★ Lerna+Nx 15+ 模块 + 400+ 组件库 |
| **复杂表单/表格** | Schema 驱动、虚拟滚动、字段联动 | ★★★★★ Schema 中台 20+ 活动类型 |
| **性能优化** | LCP/FID/LCP 预算、长列表、内存泄漏排查 | ★★★★ B 端经验丰富，需补 C 端深度 |
| **Node.js BFF** | Serverless + 模板引擎 + 数据编排 | ★★★★★ 滴滴 BFF 模板引擎主导者 |
| **AI 工程化（强加分）** | Agent / RAG / Prompt / 多语言 NLP | ★★★★★ prd-tools 双 Skill 工作流 |
| **国际化** | i18n / RTL / 多时区 / 合规 | ★★★★★ 滴滴 10+ 国家实战 |
| **系统设计** | 中后台架构、工单状态机、实时消息 | ★★★★ 需补 WebSocket 深度 |
| **算法（字节必考）** | LeetCode 中等难度（链表/树/DP/二分） | ★★★ ⚠️ **必补强** |

### 1.2 三大最强匹配点（TL 约面的关键原因）

1. **Schema 驱动营销中台** ↔ TikTok 客服工作台配置（20+ 活动类型 → 工单类型/服务模板配置）
2. **AI 工程工作流 prd-tools** ↔ TikTok 智能客服方向（Agent + RAG + 业务知识库）
3. **滴滴国际化 10+ 国家** ↔ TikTok 全球化业务（多语言/多时区/多合规）

### 1.3 两个必须补强的薄弱点

#### 薄弱点 1：算法（字节必考，候选人在阿里系面试中没遇到，但字节必考）

**现状**：字节一面亲历真题考了"最大数组和算法"（maxSumAfterNegations，贪心）
**补强计划**：
- **本周**：刷完 LeetCode 字节高频 30 题（链表 5 + 树 5 + DP 5 + 二分 5 + 字符串 5 + 其他 5）
- **重点**：手撕时**先说思路再写代码**，写完主动跑测试用例

#### 薄弱点 2：系统设计（字节中后台必考，候选人之前答得偏散）

**现状**：拼多多一面 Q3"统一地址选择页"答得不够结构化
**补强计划**：用"需求拆解 → 架构分层 → 关键决策 → 扩展性"四段式练 3 个场景：
- TikTok 客服工作台设计
- 工单状态机设计
- 实时消息系统设计

### 1.4 面试风格特点

| 维度 | 字节特点 | vs 阿里系 |
|------|---------|----------|
| **项目 vs 八股** | 项目优先（TikTok 特别明显），八股为辅 | 八股 + 项目深挖并重 |
| **算法** | **必考**，LeetCode 中等难度 | 偶尔考，偏简单 |
| **系统设计** | 中后台岗位必考 | 二面+偶尔考 |
| **节奏** | **快**，每轮 40-60 分钟，间隔短 | 慢，每轮 60-90 分钟，间隔 1-2 周 |
| **追问深度** | 技术原理（why） | 业务效果（how much） |
| **文化** | Always Day 1 / 坦诚清晰 / 追求极致 | 拥抱变化 / 客户第一 |

### 1.5 面试流程（标准，TL 直推可能简化）

| 轮次 | 时长 | 内容 | 备注 |
|------|------|------|------|
| **TL 非正式约面**（本次） | 30-60min | 项目深挖 + 技术对齐 + 文化匹配 | 走过场也可能直接进正式流程 |
| 一面（基础面） | 30-40min | 自我介绍 + 项目 + 八股 + 算法 | 较年轻面试官 |
| 二面（深度面） | 50min | 技术深度 + 系统/架构设计 + 算法 | 同级或交叉面 |
| 三面（Leader 面） | 50min | 开放问题 + 系统设计 + 职业规划 | 偏抽象 |
| HR 面 | 10-20min | 价值观 + 薪资 + 选项 | 电话面 |

---

## 二、我的亲历真题命中 ⭐（来自 reviews/）

### 2.1 字节一面亲历真题（2026 年初，来自 reviews/transcripts/面经.md）— ✅ 最高价值

> 这是你之前面字节的真题，本次必考方向高度可参考。

| # | 真题 | 你的历史表现 | 本次重点 |
|---|------|-----------|---------|
| 1 | **权益 SDK 做了什么？解决了什么问题？** | ✅ 答得有结构（痛点+技术+效果） | 稳住，按四段式重讲 |
| 2 | **JSON Schema 包含哪些属性？** | ✅ 答出 properties/dependencies/x-display | 加上你项目里的 D2 联动语法 |
| 3 | **前端如何捕获错误？** | ✅ 三层兜底（window.onerror + Promise + Error Boundary） | 加上 Axios 拦截器 + Sentry |
| 4 | **回流与重绘的机制与区别** | ✅ 答出渲染管线 | 补 will-change/GPU 加速 |
| 5 | **React 的 Diff 机制** | ✅ 答出三种 Diff 策略 | 加 Key 作用原理 + Fiber 调度 |
| 6 | **JS 原型链机制** | ✅ 答出查找路径 | 补 Object.create/继承实现 |
| 7 | **实现请求终止方法**（手撕） | ✅ 用 AbortController | 加 RequestManager 单例模式 |
| 8 | **最大数组和算法**（手撕贪心） | 🟡 答出基本思路 | **本周必须练熟**，字节喜欢贪心+DP |

**关键洞察**：字节一面**全程问项目为主**，八股为辅，但**两道手撕（一道场景一道算法）是硬指标**。

### 2.2 同梯队大厂（阿里/腾讯/美团/拼多多）高频题 × 候选人薄弱点

| 高频题 | 出现公司 | 候选人表现 | 本次重点 |
|--------|--------|----------|---------|
| Formily 选型对比 | 阿里一面 | 🔴 被打穿 | 必背差异化（双端联动 + DSL） |
| Service Worker 缓存 | 千问/拼多多 | ✅ 稳 | 稳住 |
| React Fiber + Hooks 规则 | 千问/字节 | ✅ 稳 | 稳住 |
| SSR + Hydration | 千问 | ✅ 稳 | 稳住 |
| 防抖 vs 节流 | 千问 | 🔴 比喻说反 | **必背正确比喻** |
| 原型链 + 继承 | 字节/美团 | ✅ 稳 | 稳住 |
| 监控/异常捕获 | 字节/拼多多 | ✅ 稳 | 稳住 |
| Monorepo 拓扑排序 | 拼多多 | 🟡 答不全 | **补 NX 原理** |
| 系统设计（场景题） | 美团 | 🟡 答得散 | **四段式训练** |
| Harness Engineering | 小红书二面 | 🔴 答得浅 | **本周必学** |
| AI 工作流 vs Cursor/Codex | 千问/小红书 | 🟡 偏散 | 用"业务语义+证据链+质量门控"三段式 |

### 2.3 候选人系统性失分模式（跨 5+ 次面试验证）

#### 🔴 失分点 1：表达冗长无框架

**证据**：
- 千问一面 Q28 被面试官直接打断
- 小红书二面：口头禅"然后"30+ 次
- 阿里一面：口头禅"然后"50+ 次

**纠正方案**：
```
【角色】我在这个项目里是 XXX（主导/5-5 开）
【做事】具体做了三件事：①... ②... ③...
【难点】最大的难点是 XXX，解决思路是 XXX
【效果】量化结果 XXX（带口径，30 秒能说清）
```

#### 🔴 失分点 2：反问问宏大选偏

**证据**：千问一面 Q43 被面试官当面批评"问的问题跟你关系不大"

**纠正方案 —— TikTok 反问 3 件套**（已备好，见第八章）

#### 🔴 失分点 3：数据口径被追问时答得慌乱

**纠正方案 —— 口径必背清单**：
- **5h→2h**（PRD→Plan）：5 个中等复杂度需求对照
- **80% 文件覆盖**：实际开发分支改动文件 vs Plan 产出文件
- **85% 一致性**：同一 PRD 跑 10 次文件列表一致的占比
- **400+ 权益 SKU**：30-40 个底层组件，8 个业务项目
- **20+ 活动类型 / 2 周→3 天**：上线周期对比

---

## 三、基础高频题（按字节风格排序）

### 3.1 JavaScript 核心（字节一面权重 ≈ 25%）

| # | 题目 | 回答要点 | 频率 |
|---|------|---------|------|
| 1 | **原型链 + 继承实现** | `__proto__` 链查找；Object.create 实现继承；ES6 class 本质是语法糖 | ⭐⭐⭐ 字节+美团 |
| 2 | **闭包应用与内存泄漏** | 函数嵌套+内层访问外层变量；引用未释放导致泄漏；WeakMap 解决 | ⭐⭐ |
| 3 | **事件循环（宏/微任务）** | 调用栈 → 微任务（Promise.then）→ 宏任务（setTimeout）→ 渲染 | ⭐⭐⭐ 阿里 3 次 |
| 4 | **Promise 原理 + 手写** | 状态机 + then 链 + catch + all/race | ⭐⭐⭐ |
| 5 | **async/await 原理** | Generator + 自动执行器的语法糖 | ⭐⭐ |
| 6 | **ES6+ 新特性** | let/const/箭头函数/解构/模板字符串/Symbol/Set/Map | ⭐⭐ |
| 7 | **深拷贝（处理循环引用）** | WeakMap 记录已拷贝对象，递归 | ⭐⭐ 字节常考 |

### 3.2 CSS 与布局

| # | 题目 | 回答要点 |
|---|------|---------|
| 1 | **回流（reflow）vs 重绘（repaint）** | 字节真题；回流=几何变化触发重新布局；重绘=样式变化；优化：transform/opacity 触发 composite 跳过 layout |
| 2 | **BFC 触发与应用** | float/position/overflow/display；清除浮动+防 margin 重叠 |
| 3 | **CSS 选择器优先级** | !important > 内联(1000) > ID(100) > 类(10) > 标签(1) |
| 4 | **三栏布局** | flex/grid/float+负边距/absolute/table |
| 5 | **水平垂直居中** | flex/absolute+transform/grid/table-cell |
| 6 | **响应式适配** | 媒体查询 + rem/vw + 固定栅格（TikTok 必考） |

### 3.3 React·Vue（字节重点）

| # | 题目 | 回答要点 |
|---|------|---------|
| 1 | **React Diff 机制** | 字节真题；三种策略（Tree/Component/Element）+ Key 作用原理 |
| 2 | **React Fiber 架构** | 链表式子任务+优先级+时间分片；可中断/恢复 |
| 3 | **Hooks 规则 + 为什么** | 必须顶层调用；React 用链表+调用顺序索引 Hook |
| 4 | **useState vs useReducer** | useState 适合独立状态；useReducer 适合关联状态 |
| 5 | **useEffect 依赖数组** | 空数组=挂载时；无数组=每次；具体值=该值变化时 |
| 6 | **React.memo / useMemo / useCallback** | memo 包组件、useMemo 缓存值、useCallback 缓存函数 |
| 7 | **虚拟列表实现** | 可视区域+绝对定位+scroll 计算 startIndex/endIndex |
| 8 | **React 18 并发模式** | startTransition / useDeferredValue / Suspense / Selective Hydration |
| 9 | **SSR + Hydration** | 服务端 renderToString → 浏览器绘制 → JS 执行后构建 virtual DOM 对比 |

### 3.4 浏览器与网络

| # | 题目 | 回答要点 |
|---|------|---------|
| 1 | **URL 输入到响应全过程** | DNS→TCP→TLS→HTTP→服务器→浏览器渲染管线 |
| 2 | **HTTP 缓存** | 强制缓存（Cache-Control）+ 协商缓存（ETag/If-None-Match） |
| 3 | **HTTP/2 vs HTTP/1.1** | 二进制分帧+多路复用+头部压缩+服务端推送 |
| 4 | **TCP 三次握手 + 四次挥手** | SYN→SYN+ACK→ACK；FIN→ACK→FIN→ACK |
| 5 | **HTTPS 加密过程** | TLS 握手 5 步：ClientHello/ServerHello/Certificate/Key Exchange/Finished |
| 6 | **跨域解决方案** | CORS / JSONP / 代理 / postMessage |
| 7 | **XSS / CSRF 防御** | XSS：转义+CSP；CSRF：Token+SameSite Cookie |
| 8 | **Service Worker 缓存** | 字节/千问真题；fetch 拦截+Cache API+fallback 网络 |

### 3.5 TypeScript

| # | 题目 | 回答要点 |
|---|------|---------|
| 1 | **Pick / Omit 实现** | 拼多多真题；`Pick<T,K> = {[P in K]: T[P]}` |
| 2 | **Partial / Required 实现** | `-?` 和 `?` 映射 |
| 3 | **infer 关键字** | 类型推断，提取函数返回值等 |
| 4 | **泛型约束** | `T extends XXX` |

---

## 四、手撕代码（字节必考，分梯队）

### 第一梯队（字节亲历真题 + 高频，必会）

#### 题 1：最大数组和（贪心，字节一面真题）

```javascript
// LeetCode 1005：K 次取反后最大化的数组和
function maxSumAfterNegations(arr, k) {
  arr.sort((a, b) => a - b);
  // 步骤1：优先取反负数
  for (let i = 0; i < arr.length && k > 0 && arr[i] < 0; i++, k--) {
    arr[i] = -arr[i];
  }
  // 步骤2：剩余奇数次取反，翻转最小值
  if (k % 2 === 1) {
    const minIdx = arr.indexOf(Math.min(...arr));
    arr[minIdx] = -arr[minIdx];
  }
  return arr.reduce((a, b) => a + b, 0);
}
```

#### 题 2：请求终止方法（字节真题）

```javascript
class RequestManager {
  constructor() {
    this.controllers = new Map();
  }
  request(url, options = {}) {
    this.cancel(url); // 取消重复请求
    const controller = new AbortController();
    this.controllers.set(url, controller);
    return fetch(url, { ...options, signal: controller.signal })
      .then(res => res.json())
      .finally(() => this.controllers.delete(url));
  }
  cancel(url) {
    this.controllers.get(url)?.abort();
    this.controllers.delete(url);
  }
  cancelAll() {
    this.controllers.forEach(c => c.abort());
    this.controllers.clear();
  }
}
```

#### 题 3：扁平数组转树（拼多多真题，字节高频）

```javascript
// O(n) 解法
function buildTree(list) {
  const map = {};
  const roots = [];
  list.forEach(item => { map[item.id] = { ...item, children: [] }; });
  list.forEach(item => {
    if (item.parentId === null) roots.push(map[item.id]);
    else map[item.parentId]?.children.push(map[item.id]);
  });
  return roots;
}
```

#### 题 4：防抖 + 节流（千问翻车点，必背正确比喻）

```javascript
// 防抖 = 玩英雄联盟回城：每次按都重新读条，只有最后那次能完成
function debounce(fn, delay) {
  let timer;
  return (...args) => {
    clearTimeout(timer);
    timer = setTimeout(() => fn(...args), delay);
  };
}

// 节流 = 技能冷却：用完后固定 CD 内不能再放，CD 到了就一定能放
function throttle(fn, limit) {
  let inThrottle = false;
  return (...args) => {
    if (!inThrottle) {
      fn(...args);
      inThrottle = true;
      setTimeout(() => (inThrottle = false), limit);
    }
  };
}
```

#### 题 5：Promise.all + Promise.race

```javascript
// Promise.all：全部 fulfilled 才 resolve，任一 rejected 立即 reject
function all(promises) {
  return new Promise((resolve, reject) => {
    const results = [];
    let count = 0;
    promises.forEach((p, i) => {
      Promise.resolve(p).then(val => {
        results[i] = val;
        if (++count === promises.length) resolve(results);
      }, reject);
    });
  });
}

// Promise.race：第一个完成的决定结果
function race(promises) {
  return new Promise((resolve, reject) => {
    promises.forEach(p => Promise.resolve(p).then(resolve, reject));
  });
}
```

### 第二梯队（字节高频考点）

| 题目 | 核心思路 | 难度 |
|------|---------|------|
| 深拷贝（循环引用） | WeakMap + 递归 | 中 |
| LRU 缓存 | Map 保持插入顺序，get/put 时 delete+重新 set | 中 |
| 发布订阅模式 | eventMap + on/emit/off | 易 |
| 函数柯里化 | 递归 + length 判断 | 中 |
| Promise 串行（最大并发数） | 队列 + 计数器递归调度 | 中 |
| 实现 call/apply/bind | this 绑定 + 参数展开 | 中 |
| new 的实现 | 创建对象 + 链原型 + 执行 + 返回 | 易 |
| instanceof | 沿原型链查找 | 易 |

### 第三梯队（TikTok 业务场景手撕）

#### 题：简化版 Schema 渲染引擎（字节可能考）

```javascript
function render(schema) {
  if (typeof schema === 'string') return schema;
  if (Array.isArray(schema)) return schema.map(render);
  
  const { component: Component, props = {}, children = [] } = schema;
  const childElements = children.map(render);
  return { Component, props, children: childElements };
}

// 用法：render({ component: 'Form', props: {layout: 'vertical'}, children: [...] })
```

#### 题：工单状态机（业务场景）

```javascript
class TicketStateMachine {
  constructor() {
    this.state = 'created';
    this.transitions = {
      created: ['assigned'],
      assigned: ['in_progress', 'closed'],
      in_progress: ['resolved', 'closed'],
      resolved: ['closed', 'reopened'],
      reopened: ['in_progress', 'closed'],
      closed: []
    };
  }
  canTransition(to) {
    return this.transitions[this.state]?.includes(to) ?? false;
  }
  transition(to) {
    if (!this.canTransition(to)) throw new Error(`非法状态转换: ${this.state} → ${to}`);
    this.state = to;
  }
}
```

### 练习优先级

| 优先级 | 内容 | 时间 |
|--------|------|------|
| **P0 今天** | 最大数组和 + 请求终止 + 扁平转树 + 防抖节流 | 2h |
| **P0 明天** | Promise.all/race + 深拷贝 + LRU + 发布订阅 | 2h |
| **P1 后天** | Schema 渲染 + 状态机 + 函数柯里化 | 1.5h |
| **P1 6/27** | LeetCode 字节高频 30 题（链表/树/DP/二分） | 4h |

---

## 五、算法题（字节必考，LeetCode 中等为主）

### 5.1 字节高频方向（基于 LeetCode 字节题库统计）

| 方向 | 高频题目 | 难度 |
|------|---------|------|
| **链表** | 反转链表 / 环形链表 / 合并 K 个有序链表 / 删除倒数第 N 个 | 中 |
| **树** | 二叉树层序遍历 / 最近公共祖先 / 验证 BST / 翻转二叉树 | 中 |
| **动态规划** | 最长递增子序列 / 最长公共子序列 / 编辑距离 / 打家劫舍 | 中-难 |
| **二分查找** | 搜索旋转排序数组 / 寻找峰值 / 在排序数组中查找元素第一个和最后一个位置 | 中 |
| **字符串** | 无重复字符的最长子串 / 字符串相乘 / 最长回文子串 | 中 |
| **栈/队列** | 有效括号 / 最小栈 / 滑动窗口最大值 | 中 |
| **贪心** | 跳跃游戏 / 分发糖果 / 最大数组和（字节真题） | 中 |

### 5.2 本周必练 10 题（覆盖字节 80% 高频）

| # | 题目 | 难度 | 核心思路 |
|---|------|------|---------|
| 1 | 反转链表 | 易 | 迭代：pre/cur/next 三指针 |
| 2 | 环形链表 II | 中 | 快慢指针+找入口 |
| 3 | 二叉树层序遍历 | 中 | BFS + 队列 |
| 4 | 最近公共祖先 | 中 | 递归后序遍历 |
| 5 | 最长递增子序列 | 中 | DP O(n²) 或 二分 O(nlogn) |
| 6 | 打家劫舍 | 中 | DP：dp[i] = max(dp[i-1], dp[i-2]+nums[i]) |
| 7 | 无重复字符的最长子串 | 中 | 滑动窗口 |
| 8 | 搜索旋转排序数组 | 中 | 二分变种 |
| 9 | 有效括号 | 易 | 栈 |
| 10 | 滑动窗口最大值 | 难 | 单调队列 |

### 5.3 字节算法面试的硬规则

1. **先说思路再写代码**：90 秒讲清时间复杂度+空间复杂度+边界
2. **写完主动跑测试用例**：不要等面试官催
3. **不会就老实说**：别硬编，承认后给思路方向
4. **优化要主动**：写完暴力解主动说优化方案

---

## 六、项目深挖 + 场景设计

### 6.1 字节追问模式（基于字节亲历一面 + 同梯队大厂）

**Schema 中台项目 N 层递进**（字节特别爱追技术原理）：

| 层 | 追问 | 你的回答 |
|----|------|---------|
| L1 | 你做了什么？ | Schema 驱动营销中台三层架构（前端渲染引擎+BFF 模板引擎+联动 DSL） |
| L2 | 为什么不用 Formily？ | Formily 是纯前端方案，覆盖不了 BFF 端联动（切换城市→BFF 重新剪裁 Schema） |
| L3 | 联动 DSL 怎么实现？ | dependence 数组 + 三元表达式模板；前端发布订阅监听 |
| L4 | 性能瓶颈在哪？ | 联动接口响应慢，用 Service Worker 缓存（按入参 hash） |
| L5 | 大表单性能？ | 200+ 字段重渲染用 React.memo + 虚拟滚动 + hover 渲染 |
| L6 | 数据口径？ | 老代码月均 10+ 事故 → 新代码 2 年 2-3 bug；2 周→3 天 |

**AI 工作流 N 层递进**（TikTok SEP 重点）：

| 层 | 追问 | 你的回答 |
|----|------|---------|
| L1 | 是什么？ | PRD→Spec→Plan 自动蒸馏，Claude Code 双 Skill |
| L2 | 和 Cursor/Codex 区别？ | ①业务语义（PRD 关键词→代码字段映射）②证据链 ③质量门控 |
| L3 | 知识过时怎么办？ | 三层防护：冷启动用最新 PRD；蒸馏后自动回流；产物前人工 review |
| L4 | PRD 2 万字怎么办？ | 分段摘要提取需求骨架（<2000 字）+ 按需检索 |
| L5 | Token 优化？ | 上下文预算 + 渐进式披露 + condense 打包 + 中间文件传递 |
| L6 | 数据口径？ | 5h→2h（5 需求对照）；80% 文件覆盖；85% 一致性 |
| L7 | **如何应用到 TikTok 客服场景？** | **重点准备**：客服知识库构建 + 工单意图蒸馏 + 自动回复生成 |

### 6.2 项目话术锚点（对准 TikTok SEP 业务）

| TikTok 业务关键词 | 你的话术锚点 |
|---------------|-----------|
| **客服工作台** | "我做的 Schema 驱动营销中台覆盖 20+ 活动类型，新增活动前端零代码——这套思路可以直接迁移到 TikTok 客服工作台的工单类型/服务模板配置，让运营自助配置不用开发介入" |
| **工单系统** | "营销联动 DSL 本质是状态机——声明式描述谁依赖谁、条件是什么。工单状态流转（created→assigned→in_progress→resolved→closed）用同样的声明式 DSL 描述，避免 if-else 硬编码" |
| **智能客服/AI** | "我的 prd-tools 工作流是 SDD 雏形——PRD→Spec→Plan 自动蒸馏，本质和智能客服的'意图识别→回复生成'是同一个模式：都是让 AI 基于业务知识库产出可信结论。差别是客服场景的多语言、实时性要求更高" |
| **全球多区域** | "滴滴国际化覆盖 10+ 国家，我处理过拉美西语/葡语、中东 RTL 布局、跨时区活动配置。TikTok 的全球化挑战更复杂——支付方式、文化禁忌、GDPR/CCPA 合规。这块我能直接上手" |
| **高并发** | "营销联动接口我用 Service Worker 缓存——按入参 hash 做缓存键。TikTok 客服 10 万 QPS 场景，前端可以做 WebSocket 长连复用 + 消息合并 + 降级兜底" |

### 6.3 场景设计题（TikTok 业务场景）

#### 场景 1：设计 TikTok 客服工作台（必考）

**四段式回答框架**：

```
【需求拆解】客服工作台核心三件事：工单管理 + 实时消息 + 坐席效率
【架构分层】
  - 接入层：多渠道（IM/邮件/电话）统一接入，WebSocket 长连
  - 业务层：工单状态机 + 分配引擎 + 权限系统（RBAC）
  - 数据层：工单存储（MySQL）+ 搜索（ES）+ 实时数据（Redis）
  - AI 层：意图识别 + 自动回复 + 知识库检索
【关键决策】
  - WebSocket 而非轮询：实时性 + 节省带宽
  - 工单状态机用 XStat/Redux 描述：可视化 + 可追溯
  - 大列表用虚拟滚动：工单池可能 1万+
  - 权限 RBAC + 字段级：不同区域看不同字段
【扩展性】
  - 插件化：新渠道接入走适配器模式
  - 多区域：按 region 分部署，数据合规隔离
  - 监控：全链路 TraceID + Sentry
```

#### 场景 2：设计实时消息系统（客服核心）

**关键点**：
- WebSocket 连接管理（心跳+断线重连）
- 消息可靠性（ACK 机制 + 消息去重 + 离线消息）
- 性能（消息合并 + 节流渲染 + 虚拟滚动）
- 降级（WebSocket 不可用时降级轮询）

#### 场景 3：设计客服 AI 辅助回复系统

**核心架构**：
```
用户消息 → 意图识别（LLM）→ 知识库检索（RAG）→ 生成候选回复（LLM）→ 人工审核 → 发送
```

**关键挑战**：
- **多语言**：跨语言意图理解，TikTok 全球化核心
- **幻觉控制**：必须有证据链 + 兜底（重要场景人工介入）
- **成本**：多大模型混合（强模型做意图，小模型做生成）
- **实时性**：用户等不及，流式输出 + 缓存高频问题

### 6.4 AI 工程深挖题（TikTok SEP 强相关）

#### Q1：Harness Engineering 是什么？（小红书二面考过，本次必会）

**核心回答**：
> Agent = Model + Harness。Harness 是为模型搭建约束、反馈、记忆、技能进化的全套控制架构。三类引擎：合并引擎（整合多 Agent 输出）、通信引擎（Agent 间状态传递）、反思引擎（从失败中提炼规则）。KSG（Knowledge-Skill-Growth）是核心：短期记忆→长期记忆→知识库→技能手册的抽象提取链路。

#### Q2：MCP vs Function Calling？

**核心回答**：
- Function Calling：模型内置、绑定具体厂商、单次调用
- MCP：Anthropic 开放协议、跨模型复用、标准化工具发现机制
- 配合使用：MCP 负责工具标准化暴露，Function Calling 负责模型的工具选择决策

#### Q3：多语言意图识别怎么做？

**核心回答**：
- 路线 A：先翻译成英文统一处理（成本低，但翻译误差传递）
- 路线 B：用多语言模型直接处理（Doubao/多语言 LLM）
- 路线 C：混合——先检测语言，小语种翻译成主语言，再用主模型处理

#### Q4：智能客服的幻觉怎么控制？

**核心回答**：
- 证据链机制：每条 AI 回复必须标注知识库来源
- 兜底机制：低置信度自动转人工
- 离线评测：用 golden sample 回归测试
- 人工 review：重要场景必须人工介入

---

## 七、方向专项题（中后台 + AI 工程化）

### 7.1 中后台工程化（字节重点）

| 题 | 回答要点 |
|----|---------|
| **Monorepo 拓扑排序** | NX 原理：读 package.json 建 DAG → 拓扑排序 → 并行构建 → hash 缓存 |
| **组件库打包** | Rollup 双模（ESM+CJS+类型）+ peerDependencies 隔离 react |
| **版本管理** | Changesets 语义化 + 自动 CHANGELOG |
| **接入形态** | 组件模式 + 函数调用 + 微前端（你的三态） |
| **微前端** | qiankun 原理（single-spa + HTML Entry + Proxy 沙箱 + 样式隔离） |
| **为什么不用 iframe** | 通信困难 + 性能差 + 布局割裂 |

### 7.2 性能优化（字节中后台必考）

| 维度 | 优化点 |
|------|--------|
| **首屏** | 路由分割 + 懒加载 + critical CSS + 预连接 |
| **大列表** | 虚拟滚动（react-window）+ 分页加载 |
| **大表单** | React.memo + 字段级订阅 + hover 渲染 |
| **接口** | Service Worker 缓存 + 请求合并 + 并发控制 |
| **资源** | Tree Shaking + 代码分割 + 图片 WebP/AVIF |
| **运行时** | 长任务拆分（requestIdleCallback）+ Web Worker |

### 7.3 BFF（你的强项）

| 题 | 回答要点 |
|----|---------|
| **BFF 模板引擎** | 模板驱动 Schema 生成，按活动类型分文件管理 |
| **双重求值联动** | BFF safeEval 求初始状态（SSR 正确）+ 序列化 d_actions 给前端 |
| **Node.js 中间件** |洋葱模型 + 错误统一处理 + TraceID |
| **Serverless** | 冷启动优化 + 函数粒度拆分 + 监控告警 |

### 7.4 监控与异常

| 题 | 回答要点 |
|----|---------|
| **JS 异常捕获** | window.onerror + unhandledrejection + Error Boundary |
| **资源错误** | addEventListener('error', fn, true) 捕获阶段 |
| **接口错误** | Axios 拦截器 + reason tag 分类 |
| **白屏检测** | MutationObserver + 骨架屏超时 |
| **性能监控** | LCP/FID/CLS + Performance Observer |
| **全链路追踪** | TraceID 串联前端→BFF→后端 |

---

## 八、软素质 + HR 面

### 8.1 为什么跳槽（高频必准备）

**核心句**：成长空间到顶 + 想深入 AI 工程化 + TikTok 业务高度对口

**展开（四段式）**：
- **感恩过去**：滴滴国际化 4 年，从 0 到 1 做了 Schema 架构 + 权益组件库 + AI 工作流，连续 2 年 A 绩效
- **明确诉求**：今年想完成 AI 应用方向的深度转化。滴滴 AI 落地节奏偏慢，希望去走得更快的环境
- **匹配 TikTok**：TikTok SEP 的客服场景是中后台 + AI 工程化的完美结合，跟我 prd-tools + Schema 中台的经验高度对口
- **个人定位**：希望在中后台 + AI 复合方向深入，对标字节内部的工程化标杆

### 8.2 职业规划

- **1 年内**：快速上手业务，在 TikTok 客服工作台某个核心模块做出可量化交付
- **2-3 年**：成为团队 AI 工程化方向的骨干，推动 Agent/RAG 工作流在客服场景深度落地
- **长期**：做 AI+前端的中后台架构师方向，对标字节 4-1/4-2 级别

### 8.3 字节文化关键词（HR 面必考）

字节跳动核心价值观（背熟，每个准备一个事例）：

| 价值观 | 你的事例 |
|--------|---------|
| **Always Day 1（始终创业）** | prd-tools 是我自发做的，没有任务安排，主动发现问题+推动解决 |
| **坦诚清晰** | 主导《中台开发规范》《BFF 接口规范》落地，把隐性知识显性化 |
| **开放谦逊** | 主动向阿里淘天学习工业级 AI 研发体系，对标自己的工作流 |
| **追求极致** | 400+ 权益组件库 18 个月零 breaking change，2 年仅 2-3 bug |
| **多元兼容** | 滴滴国际化 10+ 国家，处理过文化/语言/合规的复杂适配 |

### 8.4 TikTok 特有问题

**Q：为什么选 TikTok 不选抖音？**
- **业务规模**：TikTok 是全球业务，挑战更复杂
- **技术深度**：全球化的多语言/多时区/多合规，对工程能力要求更高
- **职业天花板**：海外业务增长曲线优于国内存量

**Q：为什么从滴滴出来？**
（按 8.1 答案）

**Q：期望薪资？**
- 提前想好（建议按当前 + 30-50% 报，字节给得起）
- L3：年包 60-100 万；L4：年包 100-180 万；L5：年包 180-350 万+
- 不要主动报数，让 HR 先说范围

### 8.5 反问环节（3 个，避免千问翻车）

**第 1 问（个人强相关 - 必问）**：
> "TikTok SEP 这个岗位具体在哪个团队？客服平台下面有工作台/工单/智能客服几条线，前端在不同团队的分工边界是怎样的？进来后预期重点参与哪个方向？"

**第 2 问（技术深度 - 二选一）**：

问 AI 方向：
> "我看到 TikTok 客服平台在做 AI 智能客服，团队目前在 Agent / RAG / 多语言这块的现状和规划是怎样的？前端在 AI 工程化里能发挥多大作用？"

问业务/技术深度：
> "TikTok 全球化业务的高并发场景（10 万 QPS+），前端在实时消息/工单这块主要做了哪些架构优化？"

**第 3 问（团队情况 - 看气氛问）**：
> "团队目前前端同学大概多少位？大家的协作模式和技术分享机制是怎样的？"

**❌ 避免问**（千问翻车点）：
- TikTok 整体战略、字节集团规划
- 加班/福利（HR 面再问）
- "我有什么需要改进的"

---

## 九、备战优先级

| 优先级 | 内容 | 时间 | 状态 |
|--------|------|------|------|
| **P0** | 向朋友确认 HC 级别 / 约面性质 / 后续流程 | 今天（6/24） | ⏳ |
| **P0** | 4 段式表达训练 + 三个项目 30 秒版本 | 今天 | ⏳ |
| **P0** | 字节亲历真题 8 题逐题过一遍 | 明天（6/25） | ⏳ |
| **P0** | 手撕第一梯队 5 题（贪心 + AbortController + 扁平转树 + 防抖节流 + Promise.all） | 明天 | ⏳ |
| **P0** | 数据口径背诵 | 明天 | ⏳ |
| **P1** | 大麦面试正常走（6/29）当 TikTok 热身 | 6/29 | ⏳ |
| **P1** | LeetCode 字节高频 10 题（链表/树/DP/二分） | 6/26-6/27 | ⏳ |
| **P1** | Harness Engineering + AI 工程化深度 | 6/27 | ⏳ |
| **P1** | 场景题：客服工作台设计 + 实时消息 + AI 辅助回复 | 6/28 | ⏳ |
| **P2** | 英文自我介绍（TikTok 可能有英文面） | 6/28 | ⏳ |
| **P2** | 反问 3 件套定稿 + 模拟面试 | 面试前一天 | ⏳ |

---

## 十、30 秒自我介绍（TikTok SEP 定制版）

**核心句（15 秒）**：
> 面试官好，我叫邓泽霖，滴滴国际化高级前端 4 年，连续 2 年 A 绩效。我在滴滴做了三件事：**Schema 驱动营销中台 + 400+ 权益组件库 + AI 工程工作流**，这三块和 TikTok 客服平台的中后台 + AI 方向高度对口。

**展开（按 TikTok 业务锚点 - 30 秒）**：
> 1. **Schema 驱动营销中台**——覆盖 20+ 活动类型，新增活动前端零代码，上线周期 2 周→3 天。这套配置化思路直接迁移到客服工作台的工单模板/服务配置。
> 2. **400+ 权益 React 组件库**——Register 注册 + Schema 渲染 + Rollup 双模打包，覆盖 8 个业务，18 个月零事故。可以迁移到 TikTok 多业务线组件抽象。
> 3. **AI 工程工作流 prd-tools**——独立设计的 Claude Code 双 Skill 工作流，PRD→Spec→Plan 自动蒸馏，效率 5h→2h/需求。跟 TikTok 智能客服的"意图识别→回复生成"是同一个 AI 工程化模式。
> 4. **滴滴国际化 10+ 国家**——多语言、RTL、时区、合规都有实战，TikTok 全球化挑战直接上手。

**收尾**：
> 我的核心优势是从业务中抽取共性，做全流程质量把控，特别想在 TikTok 这种中后台 + AI 双线深度的场景深入。

---

## 十一、面试当天一页纸

```
【主线锚点】
- Schema 中台 → 客服工作台配置化
- 权益组件库 → 多业务线组件抽象
- prd-tools → 智能客服 AI 工程化
- 滴滴国际化 → TikTok 全球化

【八股核心 5-8 关键词】
- 原型链 + 闭包
- React Diff + Fiber + Hooks 规则
- 事件循环（宏/微任务）
- HTTP 缓存 + HTTP/2 + TLS 握手
- Service Worker 缓存
- 回流 vs 重绘
- Monorepo 拓扑排序

【手撕必会（字节必考）】
- 最大数组和：贪心 + 奇偶判断
- AbortController：RequestManager 单例
- 扁平转树：Map O(n)
- 防抖节流：正确比喻（回城 vs 技能 CD）
- Promise.all：计数器 + 索引保留

【项目追问 N 层防御】
- Schema 中台：三层架构 → Formily 差异 → DSL 联动 → SW 缓存 → 大表单性能 → 数据口径
- AI 工作流：双 Skill → vs Cursor → 知识保鲜 → PRD 爆 context → Token 优化 → 数据口径 → TikTok 应用
- 组件库：Register → Schema 渲染 → Rollup 双模 → 三种接入 → 18 个月 0 事故

【场景设计四段式】
需求拆解 → 架构分层 → 关键决策 → 扩展性

【兜底句 3 句】
- TikTok 高并发：没直接做过，但营销联动 SW 缓存 + WebSocket 长连复用可迁移
- 字节算法：不会就说"这块我没练过，思路是 XXX"
- 知识盲区：诚实说"了解不深，我的思路是 XXX"，不硬编

【反问 3 件套】
1. 岗位具体团队 + 前端分工 + 重点方向
2. AI 研发现状 + 高并发前端架构
3. 团队规模 + 协作模式

【字节文化关键词】
- Always Day 1（prd-tools 自发做）
- 坦诚清晰（规范落地）
- 追求极致（18 个月 0 事故）
- 多元兼容（10+ 国家国际化）
```

---

## 十二、面试记录 & 投递追踪

### 投递状态

| 日期 | 渠道 | 阶段 | 状态 |
|------|------|------|------|
| 2026-06-24 | 字节 3-2 朋友直推 TL | TL 非正式约面待定 | 📝 已生成定向文档 |

### 面试轮次

| 轮次 | 日期 | 面试官 | 时长 | 结果 | 备注 |
|------|------|--------|------|------|------|
| TL 非正式约面 | 待定（朋友协调） | TikTok SEP TL | - | ⏳ 待约 | 不走系统 |
| 正式流程 | 待定 | - | - | ⏳ 待定 | 等 TL 反馈 |

---

## 十三、来源索引

### 本地引用（reviews/）
- `reviews/transcripts/面经.md` 第 307 行起 — **字节一面亲历真题 8 题**（权益 SDK / JSON Schema / 错误捕获 / 回流重绘 / React Diff / 原型链 / 请求终止 / 最大数组和）
- `reviews/qa/2026-06-04_阿里一面.md` — Formily 选型被打穿 + 知识保鲜挑战
- `reviews/qa/2026-06-12_千问一面.md` — 表达冗长被批评 + 反问宏大翻车
- `reviews/qa/2026-06-05_小红书.md` — Skill/Agent/Tool 概念深挖
- `reviews/qa/2026-06-12_小红书二面.md` — Harness Engineering 答得浅
- `reviews/qa/2026-06-02_拼多多.md` — Schema 配置沙箱预渲染 + Monorepo 拓扑排序
- `learning/interview/resume/v3.md` — 候选人最新简历
- `archive/retrospectives/04-27-Schema渲染引擎.md` — Schema 渲染引擎细节
- `archive/retrospectives/04-28-BFF-Schema生成与联动链路.md` — BFF 联动链路
- `archive/retrospectives/04-29-benefit-SDK权益组件库.md` — 权益组件库
- `archive/retrospectives/05-26-prd-tools-技术分享讲稿.md` — prd-tools 深度

### 联网来源
- [字节 TikTok 前端一面 2026-04-17 深度解析 - CSDN](https://blog.csdn.net/weixin_50077637/article/details/160285571)
- [前端三年经验中大厂面经（字节 TikTok）- 掘金](https://juejin.cn/post/7537329716007616527)
- [字节跳动前端实习面经 - 牛客网](https://www.nowcoder.com/creation/subject/9c0c0bacf74b487eaf12a5cd96393a41)
- [2025 字节跳动前端面试趋势 - CSDN](https://blog.csdn.net/W1391517383/article/details/147143649)
- [React 高频面试题 100 - 知乎](https://zhuanlan.zhihu.com/p/1929224975224641430)
- [TikTok SDE NG 2026 面试全流程](https://oavoservice.com/articles/tiktok-sde-ng-2026-interview-experience-full)
- [大模型智能客服架构 - 瓴羊](https://www.lydaas.com/resourcedetail?id=1726214502)
- [从 0 到 10W QPS 智能客服平台架构演进 - 博客园](https://www.cnblogs.com/crazymakercircle/p/18170648)
- [字节跳动面试全流程 - 牛客网](https://www.nowcoder.com/discuss/353147958520651776)

### 待补充
- [ ] 朋友确认 HC 级别后更新匹配度分析
- [ ] 朋友确认约面性质后调整准备重点（技术评估 vs 正式一面）
- [ ] 拿到具体 JD 后补充 JD 原文要点
