# React 原理

> 从 JSX 到 Fiber 到 Concurrent，系统理解 React 运行机制。

---

## 核心知识点

| 主题 | 关键概念 | 速查板 |
|------|---------|--------|
| Fiber 架构 | child/sibling/return 链表，可中断渲染 | 📗 React 18 并发 + Fiber |
| Scheduler 调度 | MessageChannel 优先级，非 setTimeout | 📗 React 18 并发 + Fiber |
| Concurrent Mode | useTransition, useDeferredValue, Automatic Batching | 📗 React 18 并发 + Fiber |
| useEffect vs useLayoutEffect | 同步 vs 异步，绘制前后 | 📗 useEffect vs useLayoutEffect |
| Hooks 调用规则 | 调用顺序匹配 state，不能条件调用 | 📗 Hooks 为什么不能条件调用 |
| React 19 新特性 | RSC, React Compiler, Form Actions | 📗 React 19 新特性 |
| 虚拟 DOM Diff | 同级比较 + key 优化 + 三策略 | 📗 虚拟 DOM Diff 算法 |

---

## 深入学习

- [题库详解 - C16 React 18 并发 + Fiber](learning/interview/题库/题库详解.md)
- [题库详解 - C17 useEffect vs useLayoutEffect](learning/interview/题库/题库详解.md)
- [急救包 - 八股口语化速记](learning/interview/题库/急救包.md)

---

## 学习路径

1. **先理解问题**：为什么 React 需要 Fiber？→ 递归 diff 不可中断
2. **理解数据结构**：Fiber 节点的链表结构（child/sibling/return）
3. **理解调度**：Scheduler 用 MessageChannel 做优先级调度
4. **理解并发**：React 18 的三个新能力（useTransition、useDeferredValue、Automatic Batching）
5. **理解 diff**：同级比较三策略 + key 的作用
6. **理解 Hooks**：调用顺序匹配 state 的底层原理
