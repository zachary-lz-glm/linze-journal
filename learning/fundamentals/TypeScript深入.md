# TypeScript 深入

> 类型体操核心：infer + 条件类型 + 映射类型。

---

## 核心知识点

| 主题 | 关键概念 | 速查板 |
|------|---------|--------|
| infer 推断 | 在条件类型里推断子类型 | 📗 TypeScript 高级类型 |
| 条件类型 | T extends X ? A : B，类型层面的三元 | 📗 TypeScript 高级类型 |
| 映射类型 | 遍历联合类型生成新类型 | 📗 TypeScript 高级类型 |
| 内置工具类型 | Pick / Omit / Partial / Required / Record | 📗 TypeScript 高级类型 |

---

## 常用工具类型实现原理

```typescript
// Partial：把所有属性变成可选
type Partial<T> = { [P in keyof T]?: T[P] };

// Required：把所有属性变成必选
type Required<T> = { [P in keyof T]-?: T[P] };

// Pick：从 T 中选一部分属性
type Pick<T, K extends keyof T> = { [P in K]: T[P] };

// Omit：从 T 中排除一部分属性
type Omit<T, K extends keyof T> = Pick<T, Exclude<keyof T, K>>;

// infer 示例：提取函数返回值类型
type ReturnType<T> = T extends (...args: any[]) => infer R ? R : never;
```

---

## 深入学习

- [题库详解 - C20 TypeScript 高级类型](learning/interview/题库/题库详解.md)
- [2026 新增考点](learning/interview/题库/2026新增考点.md)
