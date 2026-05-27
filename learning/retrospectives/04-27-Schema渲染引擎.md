# 01 · 营销平台 Schema 渲染引擎 — 2026-04-27

## 一、今日核心事件

**Genos Dive 前端 Schema 渲染引擎深度源码复盘**。从错误理解到纠正，完成核心架构的完整分析，并更新复盘文档。

1. **营销平台 前端 Schema 渲染引擎源码深潜**（formatName 拍平 + d_actions 联动 + listener 发布订阅）
2. **前端联动解析引擎分析**（eval 轻量执行 + 四套 parseVisible + 变量作用域）
3. **纠正技术题库 A2 答案**：从错误的"两级联动 HOC"改为正确的架构分析
4. **更新复盘规划文档**：30 秒开场白 + 项目描述 + W1 周一周二任务

---

## 二、Schema 渲染引擎核心架构

### 2.1 整体数据流

```
BFF 拼装 Schema JSON → 前端 StepForm 遍历渲染 → FieldWrapper 包裹每个字段 → 表单交互
```

BFF 负责拼装活动配置的 Schema JSON，前端拿到后通过 `StepForm` 组件遍历 `schemaList` 渲染表单。

### 2.2 五层核心机制

#### 第一层：Schema 遍历渲染

`StepForm` 中 `schemaList.map()` 遍历，每个字段由 `FieldWrapper` 包裹：

```tsx
schemaList.map((fieldSchema, index) => (
  <FieldWrapper key={index} fieldSchema={fieldSchema} ... />
))
```

#### 第二层：formatName 字段路径拍平

**这是核心中的核心**。表单有层级结构：`step → card → Form.List row → field`，但联动引擎需要精确定位到每个字段。`formatName` 将层级结构拍平为 dot-separated 路径：

```
"rules.reward.0.method"  →  规则 > 奖励 > 第 0 行 > 发放方式
"rules.condition.1.type" →  规则 > 条件 > 第 1 行 > 条件类型
```

这解决了**嵌套表单 + 联动定位**的核心矛盾。

#### 第三层：d_actions 联动配置

每个字段的 Schema 中可以携带 `d_actions`，描述当依赖字段变化时该做什么：

```json
{
  "d_component": "Select",
  "d_actions": [{
    "dependencies": ["rules.reward.0.method"],
    "callback": { "visible": true, "disabled": false }
  }]
}
```

- `dependencies`：监听哪些字段的路径
- `callback`：条件满足后做什么（visible / disabled / API 调用 / options 更新）

#### 第四层：Listener 发布订阅

`listener.js` 是一个简单的 EventEmitter（on/emit/once/off），负责字段间变更通知：

- **注册阶段**：`FieldWrapper` mount 时，读 `d_actions.dependencies`，对每个依赖路径执行 `listener.on(path, callback)`
- **触发阶段**：`onFormChange` 中，字段值变化时执行 `listener.emit(formatName, value)` 
- **执行阶段**：`parseCallback` 解析 d_actions，应用 visible/disabled/API/options 变更

```
字段 A 变化 → onFormChange → listener.emit("rules.reward.0.method", value)
                                    ↓
                            FieldWrapper B 的 listener.on callback 触发
                                    ↓
                            parseCallback → 更新 B 的 visible/disabled/...
```

#### 第五层：双轨组件映射

- **switch-case**：基础组件（Radio、Select、DatePicker、Input 等）— 简单直接
- **RegisteredComponents 注册表**：35+ 业务组件（奖励、条件、地域选择等）— 可扩展

`app.tsx` 启动时批量注册：`RegisteredComponents.set(cmpName, Component)`

### 2.3 三层状态管理

| 层 | 职责 | 存储 |
|---|---|---|
| Redux | 全局 flat-key 存储 | `saveFormData` → `dataSet` slice |
| Form 实例 | 字段级操作（校验、取值） | Ant Design Form |
| Listener | 变更通知 + 预览 | EventEmitter 实例 |

---

## 三、纠正过程

### 之前的错误理解

1. **过度关注 DynamicComponent HOC**：把 `ConditionMethodCmp.tsx` 中的 `DynamicComponent`/`DynamicComponentWithBFF` 当成核心联动引擎。实际上这只是 DxgyFormList（阶梯奖励列表）专用的组件，不是通用联动机制。
2. **"两级联动 HOC" 说法**：把 HOC 包裹理解为架构核心，实际核心是 formatName + d_actions + listener 这条链路。

### 纠正后的核心认知

**Schema 渲染引擎的核心含金量不在组件映射，而在字段路径拍平 + 联动解析引擎**：

- **formatName**：解决嵌套表单到扁平路径的映射，是联动引擎能工作的基础
- **d_actions + listener**：声明式联动配置 + 发布订阅执行，是引擎的核心链路
- **parseCallback**：解析 d_actions 并应用变更（visible/disabled/API/options）的执行器

---

## 四、复盘文档更新

### 技术题库详解.md — A2 答案重写

完全重写了 营销平台 项目亮点回答，结构改为：

1. **30 秒版本**：Schema 驱动 → formatName 拍平 → d_actions + listener 联动
2. **完整版本**：五层架构 + 三层状态管理 + 数据流图
3. **口语化表述**：按"用户操作视角"讲述，从表单渲染到联动触发

### 复盘规划.md 更新

- 30 秒开场白：强调 Schema 渲染引擎
- 营销平台 项目描述：新增"前端 Schema 渲染引擎"
- W1 周一任务：聚焦 Schema 渲染引擎各组件
- W1 周二任务：覆盖 BFF + 前端全链路

---

## 五、源码关键文件索引

| 文件 | 路径 | 核心内容 |
|------|------|----------|
| StepForm | `dive/src/pages/create/StepForm` | Schema 遍历渲染 + onFormChange |
| FieldWrapper | `user_camp/components/FormField/FieldWrapper/index.tsx` | d_actions 注册 + 联动执行 |
| listener.js | `dive/src/hooks/listener.js` | EventEmitter 发布订阅 |
| app.tsx | `dive/src/app.tsx` | RegisteredComponents 注册 35+ 组件 |
| types.ts | `dive/components/FormField/types.ts` | IFormFieldProps（d_component, d_actions） |
| dataSet.ts | `dive/src/store/reducers/dataSet.ts` | Redux saveFormData |

---

## 六、前端联动解析引擎深度分析

> 这部分是对「d_actions + listener 发布订阅」的补充——上一节讲了**联动的事件驱动机制**（emit/on），这节讲**联动表达式的实际解析执行**：字符串表达式怎么变成 JavaScript 判断结果的。

### 6.1 核心模式：eval 轻量执行

前端联动的 `visible`、`disabled`、`options` 本质是把**字符串表达式丢进 eval 执行**，但这个解析非常"轻量"——不是一个完整的 JS 运行环境：

```
Schema 声明 → 正则提取 {{...}} 内容 → 变量替换 → eval()
```

**三条铁律：**
1. 不能用自定义函数/变量（IIFE 里的 `unwrap`、`new Date()` 等都会失败）
2. 表达式执行失败 = 联动不生效 = 字段一直隐藏/一直禁用（条件恒 false）
3. 最稳写法：**纯布尔表达式 + 直接用 `${field_name}[0]` 取值**

### 6.2 四套解析函数

#### parseVisible — 行级联动（RuleCard）

```typescript
// RuleCard
const parseVisible = (str: string, stateName: string, rowKey: number) => {
    return String(str.match(/(?<={{).*?(?=}})/))
        .replaceAll(' ', '')
        .replaceAll('$', `${stateName}?.[${rowKey}]?.`)
}

// 用法：rowValue 是 Form.List 某一行的数据
visible = eval(parseVisible(itemSchema.visible, 'rowValue', rowKey))
```

**数据流：**
```
Schema: "{{$.driver_type === 'truck'}}"
  ↓ 正则提取
"$.driver_type === 'truck'"
  ↓ 替换 $ → rowValue?.[0]?.
"rowValue?.[0]?.driver_type === 'truck'"
  ↓ eval()
true / false
```

**eval 作用域变量：** `rowValue`（当前行数据），通过闭包可以访问组件 props

#### getExpression + parseVisible — 跨字段联动（RewardCondition）

```typescript
// joinCondition.tsx:288-290
const getExpression = (exprStr: string) => {
    return String(exprStr.match(/(?<={{).*?(?=}})/))
        .replace(/\$\[([^\]]+)\]/g, (_, varName) => varName)
}

// joinCondition.tsx:80-88
const parseVisible = (visibleValue: string | boolean) => {
    if (typeString(visibleValue) === DataType.STRING) {
        const v = getExpression(visibleValue as string)
        return eval(v)
    }
    return visibleValue
}
```

**数据流：**
```
Schema: "{{$['driver_type']}} === 'bus'"
  ↓ 正则提取
"$['driver_type'] === 'bus'"
  ↓ replace $['xxx'] → xxx
"driver_type === 'bus'"
  ↓ eval() — 闭包访问组件 props 中的 driverType
true / false
```

**eval 作用域变量：** 组件 props 中的 `arcr_calc_type`、`tripType`、`campaignType`、`timeRange` 等，通过闭包直接访问

#### parseVisible — 选项级禁用（FuelReward）

```typescript
// pushSendTime.tsx:104-109
const parseVisible = (str: string) => {
    return String(str.match(/(?<={{).*?(?=}})/))
        .replaceAll(' ', '')
        .replaceAll('$["', '')
        .replaceAll('"]', '')
}

// 用法：
disabled: eval(parseVisible(item.disabled))
// 注释："driverType不能删, eval有用" — 说明 eval 依赖闭包变量
```

**eval 作用域变量：** `driverType`（props 解构）、`currentValue`、`dataSet`（Redux）

#### schemaExpression — 通用表达式解析（tools.ts）

```typescript
// tools.ts:16-30
export const schemaExpression = (str: string) => {
    const reg = str.includes('deps') ? /(?<=\$).*?\]/g : /\[(.+?)\]/g
    const newStr = String(str.match(/(?<={{).*?(?=}})/))
        .replace(reg, (matchStr) => {
            if (str.includes('deps')) {
                return `dataSet[${matchStr}]`
            } else {
                return `dataSet['${matchStr.slice(1, -1)}']`
            }
        })
        .replaceAll('$', '')
    return newStr
}
```

**数据流：**
```
Schema: "{{$['driver_type']}}"
  ↓ 正则提取 + 替换
"dataSet['driver_type']"

Schema: "{{$['deps'].campaign_type}}"
  ↓ deps 模式
"dataSet[$['deps'].campaign_type]"
```

**eval 作用域变量：** `dataSet`（Redux 全局表单数据）

### 6.3 统一模式总结

所有解析函数遵循同一个三步模式：

```
┌──────────────────────────────────────────────────────────────────┐
│                     联动表达式解析流程                             │
│                                                                  │
│  Schema 声明          正则提取           变量替换         eval()  │
│  ───────────    →    ──────────    →    ──────────    →   ───── │
│  {{$.field}}          $.field         dataSet['field']    true   │
│  {{$.field===1}}      $.field===1     dataSet['field']===1 false  │
│  {{$["field"]}}       $["field"]      field（闭包变量）    true   │
└──────────────────────────────────────────────────────────────────┘
```

**公共工具：**
| 函数 | 位置 | 用途 |
|------|------|------|
| `typeString()` | tools.ts | `Object.prototype.toString.call()` 类型检查 |
| `DataType` | types.ts | 枚举 `[object String]`、`[object Array]` 等 |
| `schemaExpression()` | tools.ts | 通用 dataSet 路径替换 |

**eval 可访问的变量（按组件不同）：**

| 变量 | 来源 | 典型组件 |
|------|------|---------|
| `dataSet` | Redux 全局状态 | FieldWrapper (通用) |
| `rowValue` | Form.List 当前行 | RuleCard |
| `formInstance` | Ant Design Form | RewardCondition |
| `driverType` 等 | 组件 props 解构 | FuelReward |
| `windowRuleData` | window 全局 | 某些预览组件 |

### 6.4 设计缺陷与实际踩坑

**为什么复杂 JS 表达式会失败：**

1. **没有注入自定义函数/变量**：IIFE 里用的 `unwrap`、`new Date()` 等在 eval 作用域中不存在
2. **eval 失败 = 静默失败**：`eval()` 抛异常会被 try-catch 吞掉，联动不生效，字段一直隐藏
3. **作用域依赖组件闭包**：不同组件 eval 可访问的变量不同，同一表达式在不同组件可能表现不同

**最稳写法示例：**
```json
// ✅ 稳：纯布尔 + 直接字段引用
"visible": "{{$['need_receive']}} === true"

// ❌ 不稳：IIFE + 自定义函数
"visible": "{{(() => { const unwrap = v => v?.[0] ?? v; return unwrap($['date_period']) === 'DAILY'; })()}}"

// ✅ 稳：简单比较
"visible": "{{$['date_period']}[0] === 'DAILY'}"
```

### 6.5 与 d_actions + listener 的关系

上一节（第二节）讲的 d_actions + listener 是联动的**事件驱动层**（谁变了通知谁），这节讲的 eval 解析是联动的**表达式执行层**（条件怎么判断）：

```
字段 A 变值
    ↓ listener.emit(formatName, value)
FieldWrapper B 的 listener.on callback 触发
    ↓ parseCallback → 读取 d_actions.callback.state.visible
    ↓ 如果 visible 是字符串（不是布尔值）
    ↓ 进入 eval 解析流程：
    ↓   正则提取 {{...}} → 变量替换 → eval()
    ↓   eval 失败 → visible = false → 字段隐藏
    ↓   eval 成功 → visible = true/false → 字段显隐
```

**联动完整链路** = **d_actions 声明** + **listener 事件** + **eval 表达式解析** + **FieldWrapper 状态更新**

---

## 七、明日计划（W1 周二）

- [ ] BFF Schema 拼装逻辑复盘（marketing-bff 如何组装 Schema JSON）
- [ ] BFF + 前端全链路串联：从 PRD → BFF 拼装 → 前端渲染 → 联动
- [ ] A2 口语化表述练习（计时 2 分钟）
