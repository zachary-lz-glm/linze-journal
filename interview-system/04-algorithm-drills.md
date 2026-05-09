# 算法最小训练集

> 目标：不题海。每题能口述思路、写出核心代码、讲复杂度和边界。

## 训练节奏

每题 25 分钟：

```text
1. 2分钟复述题意
2. 5分钟讲暴力和优化方向
3. 12分钟写代码
4. 3分钟跑样例和边界
5. 3分钟总结复杂度和坑
```

面试口头模板：

```text
我先确认下题意。暴力做法是...复杂度是...
这里可以优化，因为...
我准备用...维护...
边界情况有空数组、重复值、长度为1...
```

## 12 题必练清单

| 状态 | 类型 | 题目 | 核心套路 | 复杂度目标 |
|---|---|---|---|---|
| todo | 哈希 | 两数之和 | Map 存 target - x | O(n) |
| todo | 哈希 | 字母异位词分组 | 排序 key / 计数 key | O(nklogk) |
| todo | 双指针 | 三数之和 | 排序 + 左右夹 + 去重 | O(n^2) |
| todo | 滑窗 | 无重复最长子串 | Map 记录字符最新位置 | O(n) |
| todo | 链表 | 反转链表 II | dummy + 头插法 | O(n) |
| todo | 栈 | 有效括号 | 栈匹配右括号 | O(n) |
| todo | 栈 | 最小栈 | 双栈维护 min | O(1) |
| todo | 树 | 二叉树层序遍历 | BFS queue | O(n) |
| todo | 树 | 最近公共祖先 | 递归返回命中节点 | O(n) |
| todo | DFS/BFS | 岛屿数量 | 遇 1 染色 | O(mn) |
| todo | 回溯 | 全排列 | path + used | O(n*n!) |
| todo | DP | 最长递增子序列 | dp 或 patience | O(n^2) / O(nlogn) |

## 模板 1：Map

适用：配对、重复、计数、索引。

```ts
function twoSum(nums: number[], target: number): number[] {
  const seen = new Map<number, number>();
  for (let i = 0; i < nums.length; i++) {
    const need = target - nums[i];
    if (seen.has(need)) return [seen.get(need)!, i];
    seen.set(nums[i], i);
  }
  return [];
}
```

口述：

```text
我用 Map 记录已经遍历过的数和下标。遍历当前数时先查 target - 当前数是否出现过，出现就返回；否则把当前数存进去。这样每个数只遍历一次。
```

## 模板 2：滑动窗口

适用：最长/最短子串、连续子数组。

```ts
function lengthOfLongestSubstring(s: string): number {
  const last = new Map<string, number>();
  let left = 0;
  let ans = 0;

  for (let right = 0; right < s.length; right++) {
    const ch = s[right];
    if (last.has(ch) && last.get(ch)! >= left) {
      left = last.get(ch)! + 1;
    }
    last.set(ch, right);
    ans = Math.max(ans, right - left + 1);
  }

  return ans;
}
```

口述：

```text
右指针一直扩，Map 记录字符最近位置。如果当前字符在窗口里出现过，就把 left 跳到上一次位置的后一位，避免重复。
```

## 模板 3：BFS

适用：层序遍历、最短路径、逐层扩散。

```ts
type TreeNode = {
  val: number;
  left: TreeNode | null;
  right: TreeNode | null;
};

function levelOrder(root: TreeNode | null): number[][] {
  if (!root) return [];
  const ans: number[][] = [];
  const queue: TreeNode[] = [root];

  while (queue.length) {
    const size = queue.length;
    const level: number[] = [];
    for (let i = 0; i < size; i++) {
      const node = queue.shift()!;
      level.push(node.val);
      if (node.left) queue.push(node.left);
      if (node.right) queue.push(node.right);
    }
    ans.push(level);
  }

  return ans;
}
```

口述：

```text
队列里放当前层节点，每轮先记录 size，只处理这一层的 size 个节点，处理过程中把下一层节点入队。
```

## 模板 4：DFS 染色

适用：岛屿、连通块、矩阵搜索。

```ts
function numIslands(grid: string[][]): number {
  const m = grid.length;
  if (m === 0) return 0;
  const n = grid[0].length;
  let ans = 0;

  const dfs = (i: number, j: number) => {
    if (i < 0 || i >= m || j < 0 || j >= n || grid[i][j] !== "1") return;
    grid[i][j] = "0";
    dfs(i + 1, j);
    dfs(i - 1, j);
    dfs(i, j + 1);
    dfs(i, j - 1);
  };

  for (let i = 0; i < m; i++) {
    for (let j = 0; j < n; j++) {
      if (grid[i][j] === "1") {
        ans++;
        dfs(i, j);
      }
    }
  }

  return ans;
}
```

口述：

```text
遍历矩阵，遇到一个 1 就说明发现一个新岛屿，答案加一，然后 DFS 把和它连通的 1 全部染成 0，避免重复统计。
```

## 模板 5：回溯

适用：排列、组合、子集。

```ts
function permute(nums: number[]): number[][] {
  const ans: number[][] = [];
  const used = new Array(nums.length).fill(false);
  const path: number[] = [];

  const dfs = () => {
    if (path.length === nums.length) {
      ans.push([...path]);
      return;
    }

    for (let i = 0; i < nums.length; i++) {
      if (used[i]) continue;
      used[i] = true;
      path.push(nums[i]);
      dfs();
      path.pop();
      used[i] = false;
    }
  };

  dfs();
  return ans;
}
```

口述：

```text
回溯就是选择、递归、撤销选择。used 保证每个数字在当前路径里只用一次，path 满了就复制进结果。
```

## 今日刷题记录

```text
日期：
题目：
是否独立写出：
卡住点：
边界遗漏：
下次复习时间：
```
