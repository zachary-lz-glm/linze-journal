# 算法突击 30 题 + Node/BFF 底层补强

> 你 14+ 场面试的另一个致命短板：**算法 Easy 题崩 + BFF 底层被追问就崩**。
> 阿里二面 Move Zeroes 写 13 分钟还有 bug，快手二面 Node 内存泄漏"不太理解"。
> 这个文档是 7 天突击方案：30 题肌肉记忆 + 8 个 Node 底层概念。

---

## Part 1：算法 30 题（按 CodeTop 字节+阿里+快手前端高频）

### 使用方法

1. **每题限时**：Easy 5min、Medium 8min、Hard 15min
2. **写不出直接看答案**，但第二天必须重写一遍
3. **追求 Medium 能稳定 AC**，Hard 能讲清思路就行
4. **每题记录**：思路 + 代码 + 边界 case（空数组 / 单元素 / 全相同 / 负数）

### 算法模板（9 大套路）

#### 模板 1：双指针（最高频）

```javascript
// 适用：有序数组、两端夹、去重、原地修改
function twoPointer(nums) {
  let left = 0, right = nums.length - 1;
  while (left < right) {
    if (条件) left++;
    else right--;
  }
}

// 快慢指针（同向）
function fastSlow(nums) {
  let slow = 0;
  for (let fast = 0; fast < nums.length; fast++) {
    if (条件) nums[slow++] = nums[fast];
  }
}
```

#### 模板 2：滑动窗口

```javascript
// 适用：最长/最短子串、连续区间、不重复
function slidingWindow(s) {
  let left = 0, result = 0;
  const window = new Map();
  for (let right = 0; right < s.length; right++) {
    window.set(s[right], (window.get(s[right]) || 0) + 1);
    while (窗口需要收缩) {
      window.set(s[left], window.get(s[left]) - 1);
      left++;
    }
    result = Math.max(result, right - left + 1);
  }
  return result;
}
```

#### 模板 3：DFS 回溯

```javascript
// 适用：全排列、组合、所有方案
function backtrack(path, choices) {
  if (满足结束条件) {
    result.push([...path]);
    return;
  }
  for (const choice of choices) {
    path.push(choice);
    backtrack(path, 新choices);
    path.pop();
  }
}
```

#### 模板 4：BFS 队列

```javascript
// 适用：层序、最短路径、最少步数、岛屿
function bfs(root) {
  const queue = [root];
  let level = 0;
  while (queue.length) {
    const size = queue.length;
    for (let i = 0; i < size; i++) {
      const node = queue.shift();
      // 处理 node
      if (node.left) queue.push(node.left);
      if (node.right) queue.push(node.right);
    }
    level++;
  }
}
```

#### 模板 5：链表

```javascript
// 反转链表
function reverseList(head) {
  let prev = null, cur = head;
  while (cur) {
    const next = cur.next;
    cur.next = prev;
    prev = cur;
    cur = next;
  }
  return prev;
}

// 环检测（快慢指针）
function hasCycle(head) {
  let slow = head, fast = head;
  while (fast && fast.next) {
    slow = slow.next;
    fast = fast.next.next;
    if (slow === fast) return true;
  }
  return false;
}
```

#### 模板 6：二叉树 DFS

```javascript
function dfs(node) {
  if (!node) return;
  // 前序：node → 左 → 右
  dfs(node.left);
  // 中序：左 → node → 右
  dfs(node.right);
  // 后序：左 → 右 → node
}
```

#### 模板 7：二分查找

```javascript
function binarySearch(nums, target) {
  let left = 0, right = nums.length - 1;
  while (left <= right) {
    const mid = Math.floor((left + right) / 2);
    if (nums[mid] === target) return mid;
    else if (nums[mid] < target) left = mid + 1;
    else right = mid - 1;
  }
  return -1;
}
```

#### 模板 8：动态规划

```javascript
// 一维 DP
function dp(nums) {
  const dp = new Array(nums.length);
  dp[0] = nums[0];
  for (let i = 1; i < nums.length; i++) {
    dp[i] = Math.max(dp[i-1] + nums[i], nums[i]);
  }
  return Math.max(...dp);
}

// 二维 DP（背包问题）
function knapsack(weights, values, capacity) {
  const n = weights.length;
  const dp = Array.from({length: n + 1}, () => new Array(capacity + 1).fill(0));
  for (let i = 1; i <= n; i++) {
    for (let w = 1; w <= capacity; w++) {
      if (weights[i-1] <= w) {
        dp[i][w] = Math.max(dp[i-1][w], dp[i-1][w-weights[i-1]] + values[i-1]);
      } else {
        dp[i][w] = dp[i-1][w];
      }
    }
  }
  return dp[n][capacity];
}
```

#### 模板 9：堆（TopK 问题）

```javascript
// 第 K 大元素（小顶堆）
class MinHeap {
  constructor() { this.heap = []; }
  push(val) {
    this.heap.push(val);
    this._bubbleUp(this.heap.length - 1);
  }
  pop() {
    const top = this.heap[0];
    const last = this.heap.pop();
    if (this.heap.length) {
      this.heap[0] = last;
      this._bubbleDown(0);
    }
    return top;
  }
  _bubbleUp(i) {
    while (i > 0) {
      const parent = Math.floor((i - 1) / 2);
      if (this.heap[i] >= this.heap[parent]) break;
      [this.heap[i], this.heap[parent]] = [this.heap[parent], this.heap[i]];
      i = parent;
    }
  }
  _bubbleDown(i) {
    while (true) {
      const left = 2 * i + 1, right = 2 * i + 2;
      let smallest = i;
      if (left < this.heap.length && this.heap[left] < this.heap[smallest]) smallest = left;
      if (right < this.heap.length && this.heap[right] < this.heap[smallest]) smallest = right;
      if (smallest === i) break;
      [this.heap[i], this.heap[smallest]] = [this.heap[smallest], this.heap[i]];
      i = smallest;
    }
  }
}
```

---

### 30 题速记卡（按类型分组）

#### 双指针（7 题）

| # | 题目 | LC | 难度 | 核心思路 |
|---|------|----|----|------|
| 1 | 移动零 | 283 | Easy | 快慢指针，非零前移 |
| 2 | 三数之和 | 15 | Medium | 排序 + 双指针，固定一个数 |
| 3 | 颜色分类 | 75 | Medium | 三指针，0/1/2 分区 |
| 4 | 盛最多水的容器 | 11 | Medium | 左右指针，谁短谁移 |
| 5 | 删除有序数组中的重复项 | 26 | Easy | 快慢指针 |
| 6 | 两数之和（有序数组） | 167 | Medium | 左右指针 |
| 7 | 删除链表倒数第 N 个 | 19 | Medium | 快慢指针，快先走 N 步 |

#### 滑动窗口（3 题）

| # | 题目 | LC | 难度 | 核心思路 |
|---|------|----|----|------|
| 8 | 无重复字符的最长子串 | 3 | Medium | Map 记录字符位置，左指针跳 |
| 9 | 最小覆盖子串 | 76 | Hard | 滑动窗口 + 计数 |
| 10 | 找到字符串中所有字母异位词 | 438 | Medium | 固定窗口 + 计数对比 |

#### DFS 回溯（4 题）

| # | 题目 | LC | 难度 | 核心思路 |
|---|------|----|----|------|
| 11 | 全排列 | 46 | Medium | 回溯 + used 数组 |
| 12 | 组合总和 | 39 | Medium | 回溯 + 剪枝 |
| 13 | 子集 | 78 | Medium | 回溯 / 迭代 |
| 14 | 括号生成 | 22 | Medium | 回溯 + 剪枝（左<右） |

#### BFS（3 题）

| # | 题目 | LC | 难度 | 核心思路 |
|---|------|----|----|------|
| 15 | 二叉树层序遍历 | 102 | Medium | 队列 + 按层处理 |
| 16 | 岛屿数量 | 200 | Medium | DFS / BFS 标记访问 |
| 17 | 最短单词路径 | 127 | Hard | BFS 找最短 |

#### 链表（4 题）

| # | 题目 | LC | 难度 | 核心思路 |
|---|------|----|----|------|
| 18 | 反转链表 | 206 | Easy | 三指针 prev/cur/next |
| 19 | 环形链表 | 141 | Easy | 快慢指针 |
| 20 | 合并两个有序链表 | 21 | Easy | dummy 头 + 比较 |
| 21 | 两数相加（链表） | 2 | Medium | 进位 + dummy 头 |

#### 二叉树（3 题）

| # | 题目 | LC | 难度 | 核心思路 |
|---|------|----|----|------|
| 22 | 二叉树的最大深度 | 104 | Easy | DFS 递归 |
| 23 | 对称二叉树 | 101 | Easy | 双 DFS 比较 |
| 24 | 二叉树的中序遍历 | 94 | Easy | 迭代用栈 |

#### 动态规划（3 题）

| # | 题目 | LC | 难度 | 核心思路 |
|---|------|----|----|------|
| 25 | 最大子序和 | 53 | Easy | dp[i] = max(dp[i-1]+nums[i], nums[i]) |
| 26 | 爬楼梯 | 70 | Easy | 斐波那契 dp[i] = dp[i-1] + dp[i-2] |
| 27 | 买卖股票的最佳时机 | 121 | Easy | 维护最小值 + 最大差 |

#### 字符串 + 其他（3 题）

| # | 题目 | LC | 难度 | 核心思路 |
|---|------|----|----|------|
| 28 | 字符串相加 | 415 | Easy | 双指针从末尾 + 进位 |
| 29 | 有效的括号 | 20 | Easy | 栈匹配 |
| 30 | 第 K 大元素 | 215 | Medium | 小顶堆 / 快排分区 |

---

### 边界 case 检查清单

每题写完都要跑这 5 个 case：

```
1. 空输入：[] / "" / null
2. 单元素：[1] / "a"
3. 全相同：[1,1,1] / "aaa"
4. 负数 / 0：[-1,0,1]
5. 极端：超长数组 / 超大数
```

---

### 真题踩坑记录（你的血泪）

#### Move Zeroes（LC283）—— 阿里二面崩

**错误写法**（双指针 off-by-one）：
```javascript
function moveZeroes(nums) {
  let k = 0;
  for (let i = 0; i < nums.length; i++) {  // ❌ i+1 越界
    if (nums[i] !== 0) {
      [nums[k], nums[i+1]] = [nums[i+1], nums[k]];  // ❌ i+1 错
      k++;
    }
  }
}
```

**正确写法**：
```javascript
function moveZeroes(nums) {
  let k = 0;
  for (let i = 0; i < nums.length; i++) {
    if (nums[i] !== 0) {
      [nums[k], nums[i]] = [nums[i], nums[k]];
      k++;
    }
  }
}
```

**关键**：k 和 i 都从 0 开始，i 是当前遍历位置，k 是非零元素应该放的位置。

#### Promise 的 then 和 catch（高德一面卡）

```javascript
// 链式调用，第二个 catch 不执行
var p1 = new Promise((resolve, reject) => {
  reject(new Error('The Fails!'))
})
.catch(error => console.log(error.message))   // 执行
.catch(error => console.log(error.message));  // 不执行（前一个 catch 已经"处理"了）

// 分别调用，都执行
var p2 = new Promise((resolve, reject) => {
  reject(new Error('The Fails!'))
});
p2.catch(error => console.log(error.message));  // 执行
p2.catch(error => console.log(error.message));  // 执行（同一个 rejection 可以被多次捕获）
```

---

## Part 2：Node.js / BFF 底层补强（8 大概念）

### 1. Node.js 事件循环（必背）

#### 6 个阶段

```
   ┌───────────────────────────┐
┌─>│        timers             │  ← setTimeout / setInterval
│  └─────────────┬─────────────┘
│  ┌─────────────┴─────────────┐
│  │     pending callbacks     │  ← 系统级回调（TCP 错误）
│  └─────────────┬─────────────┘
│  ┌─────────────┴─────────────┐
│  │       idle, prepare       │  ← 内部使用
│  └─────────────┬─────────────┘
│  ┌─────────────┴─────────────┐
│  │           poll             │  ← I/O 事件（fs / net）
│  └─────────────┬─────────────┘
│  ┌─────────────┴─────────────┐
│  │           check            │  ← setImmediate
│  └─────────────┬─────────────┘
│  ┌─────────────┴─────────────┐
└──│      close callbacks       │  ← close 事件
   └───────────────────────────┘
```

#### 微任务 vs 宏任务

- **微任务**（每个阶段之间执行）：`Promise.then`、`process.nextTick`、`queueMicrotask`
- **宏任务**（阶段内的任务）：`setTimeout`、`setInterval`、`setImmediate`、I/O

#### 执行顺序

```
同步代码 → 微任务清空 → 宏任务一个阶段 → 微任务清空 → 下个阶段 → ...
```

#### nextTick vs setImmediate

```javascript
// nextTick 优先级最高，在所有微任务之前
setImmediate(() => console.log('immediate'));
process.nextTick(() => console.log('nextTick'));
// 输出：nextTick → immediate

// 在 I/O 中：setImmediate 先于 setTimeout(0)
fs.readFile('file', () => {
  setTimeout(() => console.log('timeout'), 0);
  setImmediate(() => console.log('immediate'));
});
// 输出顺序不确定，但通常 immediate 先（在 check 阶段）
```

---

### 2. 内存泄漏排查（快手二面问过）

#### 排查步骤

```bash
# 1. 启动时开启 inspect
node --inspect server.js

# 2. Chrome 打开 chrome://inspect，连接到 Node 进程

# 3. 在 Memory 面板拍快照
#    - Heap snapshot：堆快照
#    - Allocation timeline：分配时间线
#    - Allocation sampling：分配采样

# 4. 对比两个快照，找"只增不减"的对象
```

#### 内存监控

```javascript
// 实时监控内存
const used = process.memoryUsage();
console.log({
  rss: `${Math.round(used.rss / 1024 / 1024)}MB`,        // 常驻内存
  heapTotal: `${Math.round(used.heapTotal / 1024 / 1024)}MB`,  // 堆总量
  heapUsed: `${Math.round(used.heapUsed / 1024 / 1024)}MB`,    // 堆已用
  external: `${Math.round(used.external / 1024 / 1024)}MB`     // C++ 对象
});

// 内存告警
setInterval(() => {
  const used = process.memoryUsage();
  if (used.heapUsed > 500 * 1024 * 1024) {
    console.warn('内存超过 500MB，可能泄漏');
  }
}, 10000);
```

#### 常见泄漏原因

1. **全局变量未释放**：缓存无限增长
2. **闭包持有大对象**：闭包引用未释放
3. **事件监听器未移除**：EventEmitter.on 但没 off
4. **定时器未清理**：setInterval 没 clearInterval
5. **数据库连接未关闭**：连接池泄漏

#### 工具

- **clinic.js**：Node 性能分析（CPU / 内存 / 事件循环延迟）
- **heapdump**：生成堆快照文件
- **v8-profiler-next**：CPU profile

---

### 3. Stream 流（BFF 文件处理必备）

#### 4 种 Stream

- **Readable**：可读流（fs.createReadStream）
- **Writable**：可写流（fs.createWriteStream）
- **Duplex**：双工流（TCP socket）
- **Transform**：转换流（zlib.createGzip）

#### 背压（Backpressure）机制

```javascript
// ❌ 错误：pipe 没处理错误
readable.pipe(writable);

// ✅ 正确：pipeline 处理错误 + 背压
const { pipeline } = require('stream/promises');
await pipeline(
  fs.createReadStream('input.txt'),
  zlib.createGzip(),
  fs.createWriteStream('output.txt.gz')
);
```

**背压原理**：
- 写入速度 < 读取速度时，数据会堆积在内存
- highWaterMark 触发后，stream 暂停读取
- 写入端 drain 后恢复读取

---

### 4. Cluster / PM2 多进程

#### 为什么需要多进程

Node.js 是单线程，**单个进程无法利用多核 CPU**。Cluster 利用多核：

```javascript
const cluster = require('cluster');
const os = require('os');

if (cluster.isPrimary) {
  for (let i = 0; i < os.cpus().length; i++) {
    cluster.fork();
  }
} else {
  // worker 进程，启动 HTTP server
  require('./server');
}
```

#### PM2（生产推荐）

```bash
# 启动 4 个进程
pm2 start server.js -i 4

# 自动按 CPU 数启动
pm2 start server.js -i max

# 零停机重启
pm2 reload server.js
```

#### 进程间通信（IPC）

- **Cluster 内置 IPC**：worker.send() / process.on('message')
- **独立进程**：Redis pub/sub / RabbitMQ / 共享内存

---

### 5. Serverless 冷启动

#### 冷启动原因

1. **容器调度**：K8s 分配 Pod + 拉镜像
2. **代码加载**：Node 启动 + require 整个依赖树
3. **V8 优化**：JIT 编译预热

#### 优化方案

| 方案 | 效果 | 成本 |
|------|------|------|
| **预置并发（Provisioned Concurrency）** | 几乎无冷启动 | 贵（按时间付费） |
| **瘦身依赖** | 加快代码加载 | 中 |
| **延迟加载（lazy require）** | 首次请求才加载 | 低 |
| **代码分割** | 只加载用到的 | 中 |

#### 实战经验

- Node Serverless 冷启动：500ms - 3s
- 优化后：100ms - 500ms
- 关键：**减少顶层 require**，用 lazy load

---

### 6. BFF 错误降级四件套

#### Circuit Breaker（熔断）

```javascript
// 半开 / 关闭 / 打开 三态
class CircuitBreaker {
  constructor(opts) {
    this.failureCount = 0;
    this.threshold = opts.threshold || 5;
    this.resetTimeout = opts.resetTimeout || 60000;
    this.state = 'CLOSED';  // CLOSED / OPEN / HALF_OPEN
  }
  
  async call(fn) {
    if (this.state === 'OPEN') {
      if (Date.now() > this.nextAttempt) {
        this.state = 'HALF_OPEN';
      } else {
        throw new Error('Circuit open');
      }
    }
    try {
      const result = await fn();
      this.failureCount = 0;
      this.state = 'CLOSED';
      return result;
    } catch (err) {
      this.failureCount++;
      if (this.failureCount >= this.threshold) {
        this.state = 'OPEN';
        this.nextAttempt = Date.now() + this.resetTimeout;
      }
      throw err;
    }
  }
}
```

#### Bulkhead（舱壁隔离）

- 不同下游服务用**独立线程池 / 连接池**
- 防止某个下游拖垮整体

#### Timeout（超时）

- **快速失败**：超时直接返回兜底数据
- **多级超时**：连接超时 < 读取超时 < 总超时

#### Retry（重试）

- **指数退避**：1s → 2s → 4s
- **最大重试次数**：通常 3 次
- **幂等性检查**：非幂等接口不能重试

---

### 7. 全链路追踪（TraceID）

#### 注入 TraceID

```javascript
// 中间件：注入 TraceID
app.use((req, res, next) => {
  req.traceId = req.headers['x-trace-id'] || uuid.v4();
  res.setHeader('x-trace-id', req.traceId);
  next();
});

// 调用下游时传递
axios.get(url, {
  headers: { 'x-trace-id': req.traceId }
});
```

#### OpenTelemetry（业界标准）

```javascript
const { trace } = require('@opentelemetry/api');

const span = tracer.startSpan('bff.getData');
try {
  // 业务逻辑
  span.setAttribute('user.id', userId);
} finally {
  span.end();
}
```

#### 串联查询

- 前端日志 → TraceID
- BFF 日志 → 同一个 TraceID
- 后端日志 → 同一个 TraceID
- 通过 LogInsight / ELK / Jaeger 串联全链路

---

### 8. 性能瓶颈定位

#### CPU profile

```bash
# clinic.js
clinic doctor -- node server.js
# 然后压测：ab -n 1000 -c 100 http://localhost:3000/

# 生成 CPU 火焰图
clinic flame -- node server.js
```

#### 关键指标

- **QPS**：每秒请求数
- **P50 / P95 / P99**：响应时间分位数
- **错误率**：5xx 比例
- **事件循环延迟**：<100ms 健康

#### 常见瓶颈

| 瓶颈 | 现象 | 解决 |
|------|------|------|
| 同步阻塞 | 事件循环延迟飙升 | 改异步 / 用 worker_threads |
| CPU 密集 | CPU 100% | worker_threads / 拆服务 |
| 内存泄漏 | heapUsed 持续增长 | 见上文 |
| I/O 慢 | P99 高 | 缓存 / 并发 / 流式 |
| 数据库慢 | 慢查询 | 索引 / 拆分 / 缓存 |

---

## Part 3：7 天突击计划

### Day 1-2：算法模板 + 双指针

- [ ] 9 个模板各手写 1 遍
- [ ] 双指针 7 题刷完（限时 5min/题）
- [ ] Move Zeroes 重写 5 遍（肌肉记忆）

### Day 3：滑动窗口 + DFS 回溯

- [ ] 滑动窗口 3 题
- [ ] DFS 回溯 4 题
- [ ] 全排列 + 组合总和解法背熟

### Day 4：BFS + 链表 + 二叉树

- [ ] BFS 3 题
- [ ] 链表 4 题
- [ ] 二叉树 3 题
- [ ] 反转链表 + 环检测背熟

### Day 5：DP + 字符串 + 其他

- [ ] DP 3 题
- [ ] 字符串 + 其他 3 题
- [ ] 最大子序和 + 爬楼梯 + 股票背熟

### Day 6：Node 底层

- [ ] 事件循环（6 阶段 + 微任务/宏任务）口述 3 遍
- [ ] 内存泄漏排查（clinic.js + heap snapshot）实操 1 次
- [ ] Stream 背压 + Cluster 多进程概念背熟
- [ ] BFF 错误降级四件套代码写一遍

### Day 7：综合模拟

- [ ] 找 3 道Medium 题，限时 8min/题，模拟面试
- [ ] Node 底层找 5 个问题口述回答
- [ ] 录音回听，标卡壳点

---

## Part 4：高频追问应对

### 算法类

**Q：时间复杂度 / 空间复杂度多少？**
A：先说当前解法，再说能不能优化。

**Q：有没有更好的解法？**
A：永远说"有"——双指针优化 O(n²) → O(n)、空间换时间、Hash 优化查找。

**Q：边界 case 考虑了吗？**
A：主动说空数组 / 单元素 / 全相同 / 负数 / 超长输入。

**Q：在真实项目中用过这个算法吗？**
A：双指针（数据去重）、滑动窗口（限流）、DFS（树形数据）、BFS（最短路径）都有真实场景。

### Node 类

**Q：Node 为什么是单线程？**
A：单线程 + 事件循环 + 异步 I/O，避免线程切换开销。CPU 密集用 worker_threads。

**Q：BFF 挂了怎么感知？**
A：主动监控（平台捕获 JS 运行时错误）+ 被动探测（K8s /health 探针）+ 全链路告警（TraceID 关联）。

**Q：Node 执行失败会让整个失败还是部分失败？**
A：分场景——全局性错误（数据库连接）整个失败，局部错误（非核心接口超时）降级返回部分数据。

**Q：Node 层内存泄漏怎么排查？**
A：--inspect → Chrome DevTools 堆快照 → 对比 retained size → 找只增不减的对象 → 定位闭包 / 全局变量 / 监听器泄漏。

---

## 总结：你的算法 + BFF 补强目标

| 维度 | 当前 | 目标（7 天后） |
|------|------|------|
| 算法 Easy | 写 13min 还有 bug | 5min 稳定 AC |
| 算法 Medium | 没系统刷 | Top 30 能稳定 AC |
| 算法 Hard | 完全不会 | 能讲清思路 |
| Node 事件循环 | 模糊 | 6 阶段 + 微/宏任务能脱口而出 |
| 内存排查 | "不太理解" | Chrome DevTools 实操过 |
| Stream | 听过 | 背压 + pipeline 能讲清 |
| Cluster | 知道概念 | 能写代码 + IPC 能讲 |
| Serverless 冷启动 | 没概念 | 知道原因 + 优化方案 |
| 错误降级 | 没体系 | 四件套能脱口而出 |
| 全链路追踪 | 知道 TraceID | OpenTelemetry 概念 + 注入代码 |
