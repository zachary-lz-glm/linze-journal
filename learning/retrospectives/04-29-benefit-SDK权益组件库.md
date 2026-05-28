# 03 · benefit SDK 权益组件库 — 2026-04-29

## 一、今日核心事件

**benefit-sdk 权益组件库深度复盘**。从源码逐文件精读，梳理出 6 个核心讲点，纠正 1 个认知偏差，发现 1 个重大架构洞察。

**一个重大发现**：
1. **benefit-sdk 自己也是 Schema 渲染引擎的消费者** — `BenefitForm` 接收 `currentSchema`（form_data 数组），通过 `d_component` 映射 Register 注册的 24 个组件，用 `FieldWrapper` 迭代渲染。和 营销平台 完全同构！这意味着 Schema 驱动不是"前端项目的事"，而是横跨 营销平台 + 权益SDK 的统一架构模式。

**一个纠正**：
1. 复盘文档 A3 说"Register 注册模式，动态注册扩展点" — 实际是构造时静态注册 24 个组件 + `add()`/`addMultipleCmps()` 运行时扩展。不是纯动态注册，而是"内置基础 + 开放扩展"。

---

## 二、项目结构全景

```
benefit-sdk/
├── src/
│   ├── index.ts              # 入口：导出 App/ViewBenefit/CopyBenefit/EditBenefit/CreateBenefit/BenefitAdmin
│   ├── components/
│   │   ├── register.tsx      # Register 类：24 个内置组件 + add/addMultipleCmps 扩展
│   │   ├── Common/           # 通用组件（16 个）
│   │   │   ├── FieldWrapper      # Schema 渲染迭代器（和 营销平台 的 FieldWrapper 同构！）
│   │   │   ├── FormItem          # 表单项容器
│   │   │   ├── Input/Select/Radio/Checkbox/DatePicker  # 基础表单
│   │   │   ├── CommonRuleCmp     # 嵌套字段容器
│   │   │   ├── CommonCollapseCmp # 折叠面板（对应 Schema 的 d_component: "CommonCollapse"）
│   │   │   ├── InLineInput/ListRuleCard/ListInLineInput  # 行级/列表组件
│   │   │   ├── ContainerCmp      # 容器组件
│   │   │   ├── CityGroup         # 城市选择器
│   │   │   └── Explain           # 说明文本
│   │   ├── ForDLP/           # DLP 业务组件（3 个）
│   │   │   ├── BenefitImageCmp   # 权益图片上传
│   │   │   ├── DiscountInput     # 折扣输入
│   │   │   └── DiscountInfo      # 折扣信息展示
│   │   ├── ForUserCamp/      # 用户运营组件（1 个）
│   │   │   └── TimeRangeCmp      # 时间范围选择
│   │   └── ForWang/          # Wang 业务组件（5 个）
│   │       ├── RichTextCmp       # 富文本编辑器（wangeditor）
│   │       ├── PriceTable     # 价格表格（动态列配置）
│   │       ├── ValidPeriodCmp    # 有效期选择（days/hours）
│   │       ├── FileUpload         # 券码文件上传
│   │       └── CycleSelector      # 上架周期选择
│   ├── modules/
│   │   ├── App.tsx               # 组件模式入口（forwardRef）
│   │   ├── openBenefit.tsx       # 统一入口（推荐）
│   │   ├── BenefitViewByUser/    # 查看弹窗（Modal.info）
│   │   ├── BenefitCreateByUser/  # 创建弹窗
│   │   ├── BenefitEditByUser/    # 编辑弹窗
│   │   ├── BenefitCopyByUser/    # 复制弹窗
│   │   ├── BenefitDetailContent/ # 详情内容核心（CRUD 状态机 + Schema 获取）
│   │   ├── BenefitDetailModal/   # 详情弹窗（内部模式，组件内状态驱动）
│   │   ├── BenefitForm # 表单渲染核心（Schema → Form 渲染）
│   │   ├── BenefitList/          # 权益列表（无限滚动）
│   │   └── ConfirmModal/         # 二次确认弹窗
│   ├── api/                 # API 层
│   │   ├── create-api.ts     # 创建/提交/更新/下架
│   │   ├── list-api.ts       # 列表查询
│   │   ├── index.ts          # 统一导出
│   │   └── formatPrefix.ts  # API 前缀
│   ├── config/
│   │   └── schema.tsx       # Schema mock 数据（开发用）
│   ├── hooks/               # 自定义 hooks + listener
│   ├── locales/             # i18n 国际化
│   └── utils/               # 工具函数
├── rollup.config.js         # 3 输出：CJS + ESM + .d.ts
├── scripts/
│   └── publish.mjs          # zx 发版脚本（alpha/release）
└── package.json             # @company/benefit-sdk v1.2.2
```

---

## 三、6 个核心讲点

### 讲点 1：Register 注册模式 — 内置 24 组件 + 运行时扩展

```
class Register {
  _components: { [key: string]: (props: any) => JSX.Element };

  constructor() {
    this._components = {
      // 通用基础组件（16 个）
      CommonRuleCmp, FormWrapper, FormItem, ItemWrap,
      Checkbox, Input, Radio, Select,
      CommonCollapse, InLineInput, ListRuleCard, ListInLineInput,
      ContainerCmp, CityGroup, DatePicker, Explain,
      // DLP 业务组件（3 个）
      BenefitImage, FormDiscountInput, DiscountInfo,
      // 用户运营组件（1 个）
      TimeRangeCmp,
      // Wang 业务组件（5 个）
      Editor, PriceTable, ValidityPeriod, CouponFileUpload, CycleSelector,
    };
  }

  add(cmpName: string, cmp: (props: any) => JSX.Element) { ... }
  addMultipleCmps(cmps: { cmpName: string; cmp: ... }[]) { ... }
}
```

**关键设计**：
- 构造时注册 24 个内置组件，按业务线分 3 个目录（Common/ForDLP/ForWang）
- `add()` 支持运行时扩展新组件，消费方可以注册自定义权益类型的组件
- 组件分类：通用 16 + DLP 3 + UserCamp 1 + Wang 5 = 25 个 key（CommonRuleCmp 和 FieldWrapper 是容器型组件）

### 讲点 2：Schema 驱动渲染 — 与 营销平台 完全同构

**这是最关键的发现**：benefit SDK 的 `BenefitForm` 用了和 营销平台 完全相同的 Schema 渲染模式：

```
// BenefitForm — 和 营销平台 的 StepForm 同构
const RegisteredComponents = new Register();
const registeredComponents = RegisteredComponents._components;

{currentSchema?.map((item, index) => {
  return (
    <FieldWrapper
      key={item.name}
      {...item}                        // Schema 节点展开
      form={createForm}
      registeredComponents={registeredComponents}  // 组件注册表
      operationFlag={operationFlag}    // 操作类型（查看/编辑/创建）
    />
  );
})}
```

**Schema 结构**（从 config/schema.tsx 和实际 API 返回）：

```
{
  name: "spu_type_info",        // 字段名
  visible: true,                // 显隐
  d_component: "CommonCollapse", // 组件映射名 → Register._components[key]
  label: { display: "权益类型管理", info: "..." },
  attrs: { anchorItem: { ... } },
  content_schema: [              // 嵌套子字段
    {
      name: "spu_type",
      d_component: "Select",
      options: [...],
      attrs: { required: true, style: {...} },
      errs: { required: "Required" },
      value: 1010,
    }
  ]
}
```

**Schema 渲染架构对比**：

| 维度 | 营销平台 (dive) | benefit-sdk |
|------|-------------|-------------------|
| Schema 来源 | marketing-bff 生成 | MIS 后端 API 返回 |
| 渲染入口 | StepForm | BenefitForm |
| 组件映射 | d_component → switch-case + RegisteredComponents | d_component → registeredComponents[key] |
| 字段容器 | FieldWrapper | FieldWrapper |
| 嵌套结构 | steps → cards → fields → rows | collapses → fields → children |
| 表单管理 | Form.useForm() + Redux | Form.useForm() |
| 联动机制 | d_actions + listener | 暂无（Schema 由后端按操作类型下发） |

**结论**：Schema 驱动不是"前端项目的事"，而是横跨 营销平台 + 权益SDK 的统一架构。两个消费者，一套模式。

### 讲点 3：双入口设计 — 组件模式 vs 函数调用模式

**组件模式**（`<App>`）— 内嵌在页面中使用：

```
// App.tsx — forwardRef 组件，内部管理 list+detail 状态
const BenefitComponent = forwardRef((props, ref) => {
  // 创建按钮 → 打开 detail 弹窗（CREATE 模式）
  // 列表按钮 → 打开 list 抽屉 → 选择权益 → 打开 detail 弹窗（VIEW 模式）
  return (
    <ConfigProvider>
      <Button onClick={showDetailDrawer}>创建</Button>
      <Button onClick={showListDrawer}>列表</Button>
      {listOpen && <BenefitListModal ... />}
      {detailOpen && <BenefitDetailModal ... />}
    </ConfigProvider>
  );
});
```

**函数调用模式**（View/Edit/Copy/Create）— 命令式调用，通过 `Modal.info` 打开弹窗：

```
// BenefitViewByUser/index.tsx — 通过 Modal.info 弹窗
export const viewBenefitByUser = (params) => {
  const modal = Modal.info({});
  modal.update({
    width: "906px",
    content: (
      <ConfigProvider>
        <BenefitDetailContent
          operationFlag={OperationType.USER_VIEW}
          commonParams={commonParams}
          ...
        />
      </ConfigProvider>
    ),
  });
};
```

**统一入口**（`BenefitAdmin`）— 推荐，按操作类型分发：

```
// openBenefit.tsx — 类型安全的统一入口
type ParamsMap = {
  view: Parameters<typeof viewBenefitByUser>[number];
  edit: Parameters<typeof editBenefitByUser>[number];
  copy: Parameters<typeof copyBenefitByUser>[number];
  create: Parameters<typeof createBenefitByUser>[number];
};

export default <T extends keyof ParamsMap>(type: T, params: ParamsMap[T]) => {
  switch (type) {
    case 'view': viewBenefitByUser(params); break;
    case 'copy': copyBenefitByUser(params); break;
    case 'edit': editBenefitByUser(params); break;
    case 'create': createBenefitByUser(params); break;
  }
};
```

**API 迁移策略**：旧 API（ViewBenefit/EditBenefit/...）标记 `@deprecated`，新 API 统一走 BenefitAdmin。但旧 API 保持兼容不删除。

### 讲点 4：CRUD 生命周期 — 每个操作独立 Schema

```
┌──────────────────────────────────────────────────────────────────────┐
│                     Benefit CRUD Lifecycle                            │
│                                                                      │
│  CREATE  getBenefitType → 选择权益类型                                │
│          ↓                                                            │
│          getBenefitSchema(spu_type) → 获取创建 Schema                 │
│          ↓                                                            │
│          用户填写表单 → getCreateSubmit(values)                        │
│                                                                      │
│  VIEW    getBenefitDetailSchema(spu_id) → 获取查看 Schema（只读）      │
│          ↓                                                            │
│          展示详情 + 操作按钮（编辑/复制/下架）                          │
│                                                                      │
│  EDIT    getBenefitEditSchema(spu_id) → 获取编辑 Schema               │
│          ↓                                                            │
│          用户修改 → getConfirmUpdate → 二次确认 → getCreateUpdate     │
│                                                                      │
│  COPY    getBenefitCopySchema(spu_id) → 获取复制 Schema（预填数据）    │
│          ↓                                                            │
│          用户修改 → getCreateSubmit(values)                           │
└──────────────────────────────────────────────────────────────────────┘
```

**关键设计**：
- 每个 CRUD 操作有独立的 Schema 获取 API，不是共享同一个 Schema
- EDIT 有二次确认机制：先 `getConfirmUpdate` 获取确认文案，用户确认后再 `getCreateUpdate`
- COPY 预填原权益数据，用户修改后走创建流程
- 操作类型通过 `OperationType` 枚举控制（VIEW/EDIT/COPY/CREATE + USER_* 变体）

### 讲点 5：Rollup 双模打包 + 三输出

```
// rollup.config.js — 3 个输出配置
export default [
  // CJS
  { input: "src/index.ts", output: { file: "dist/index.js", format: "cjs" } },
  // ESM
  { input: "src/index.ts", output: { file: "es/index.js", format: "esm" } },
  // 类型声明
  { input: "src/index.ts", output: { file: "es/index.d.ts", format: "es" },
    plugins: [dts()] },
];
```

**package.json 分发配置**：

```
{
  "main": "dist/index.js",           // CJS 入口
  "module": "es/index.js",           // ESM 入口
  "types": "es/index.d.ts",          // 类型声明
  "type": "module",                  // 项目用 ES Module
  "exports": {
    ".": {
      "import": "./es/index.js",     // import → ESM
      "require": "./dist/index.js"   // require → CJS
    }
  },
  "peerDependencies": {
    "react": ">=16.9.0",
    "react-dom": ">=16.9.0",
    "@company/design-system": ">=2.0.4"
  }
}
```

**构建工具链**：
- `@rollup/plugin-babel` — TypeScript + JSX 编译
- `rollup-plugin-postcss` + `postcss-url({ url: "inline" })` — CSS 内联（url 转 base64）
- `rollup-plugin-dts` — 从源码生成 .d.ts 类型声明
- `rollup-plugin-visualizer` — 包体积分析
- `@rollup/plugin-image` — 图片处理
- external: react, react-dom, pebble, wangeditor 不打包

### 讲点 6：发版流水线 — Changesets + zx 自动化

```
alpha 发版（scripts/publish.mjs）:
  changeset pre enter alpha
  → npm i
  → rollup -c (build)
  → changeset (选择变更)
  → changeset version (bump + CHANGELOG)
  → changeset pre exit
  → changeset publish
  → git commit + push + tags

正式发版:
  npm i → build → changeset → version → publish → commit + push + tags
```

**安全策略**：
- 禁止在 master 分支发布
- alpha 用 `changeset pre enter alpha` 进入预发布模式
- 本地联调：`build+yalc` → `yalc push` 到目标项目

---

## 四、Schema 驱动架构 — 从 营销平台 到 benefit SDK 的统一

这是今天最重要的发现。Schema 驱动不是某个项目的设计选择，而是**整个营销中台的统一架构模式**：

```
                    Schema 驱动 — 统一架构
                    ┌──────────────────┐
                    │   Schema 标准     │
                    │  d_component     │
                    │  name/value      │
                    │  visible/disabled│
                    │  attrs/options   │
                    │  content_schema  │
                    └────────┬─────────┘
                             │
              ┌──────────────┼──────────────┐
              ↓              ↓              ↓
        营销平台    benefit SDK    MIS 后端
        ┌─────────┐   ┌──────────┐   ┌────────┐
        │marketing-bff │   │MIS BFF   │   │API     │
        │生成     │   │生成      │   │返回    │
        └────┬────┘   └────┬─────┘   └───┬────┘
             ↓              ↓             ↓
        ┌─────────┐   ┌──────────┐
        │StepForm │   │DetailForm│
        │+ Field  │   │+ Field   │
        │ Wrapper │   │ Wrapper  │
        └─────────┘   └──────────┘
        35+ 组件       24 组件
```

**两个消费者共享同一套模式**：
- 营销平台：marketing-bff 生成 Schema → StepForm + FieldWrapper 渲染 → 35+ 组件
- benefit SDK：MIS 后端返回 Schema → BenefitDetailForm + FieldWrapper 渲染 → 24 组件

---

## 五、全链路 STAR 讲稿

**S**: 400+ 权益散落在各业务线（DLP、Wang、UserCamp），每个业务线独立管理权益，没有统一的创建/编辑/查看体验，新增权益类型需要各业务线重复开发。

**T**: 设计统一的权益组件库 SDK，覆盖权益全生命周期 CRUD，支持跨业务线复用。

**A**:
1. **Register 注册模式**：构造时注册 24 个内置组件（通用 16 + DLP 3 + UserCamp 1 + Wang 5），`add()` 支持运行时扩展新业务组件
2. **Schema 驱动渲染**：SDK 也是 Schema 渲染引擎的消费者——后端返回 `form_data`（含 `d_component` + `content_schema`），前端通过 FieldWrapper 迭代渲染，和 营销平台 完全同构
3. **双入口设计**：组件模式（`<App>` 内嵌）+ 函数调用模式（`Modal.info` 命令式），统一用 BenefitAdmin 分发
4. **CRUD 独立 Schema**：每个操作（创建/查看/编辑/复制）从不同 API 获取专用 Schema，编辑有二次确认机制
5. **Rollup 双模打包**：ESM + CJS + .d.ts 三输出，`exports` 字段条件导出，peerDependencies 避免重复打包
6. **Changesets + zx 发版**：alpha/release 双环境，本地 yalc 联调

**R**: 400+ 权益统一管理，新增权益类型只需后端配 Schema，SDK 零代码。双模打包覆盖现代/老项目，发版自动化。

---

## 六、复盘文档修正

| 位置 | 原说法 | 修正为 |
|------|--------|--------|
| A3 题 | "Register 注册模式，动态注册扩展点" | 构造时静态注册 24 个内置组件 + add()/addMultipleCmps() 运行时扩展 |
| A3 题 | 未提 benefit SDK 也是 Schema 消费者 | 补充：SDK 和 营销平台 用完全相同的 Schema 渲染模式（d_component + FieldWrapper） |
| A3 题 | "400+ 权益组件" | 注册了 24 种组件类型，覆盖 400+ 权益的 CRUD（不是 400 个组件） |
| 规划.md | "400+ 权益组件 / 双模打包 ESM+CJS / Rollup 构建 / Pebble 设计系统集成 / 权益生命周期 CRUD" | 需要升级：补充 Schema 驱动渲染同构 + Register 内置+扩展双模式 |

---

## 七、加分视角 — 和 营销平台 的对比

追问时可能会问到："benefit SDK 和 营销平台 的组件库有什么不同？"

| 维度 | 营销平台 (dive) | benefit-sdk |
|------|-------------|-------------------|
| **定位** | 营销活动表单 | 权益 CRUD |
| **Schema 来源** | marketing-bff 模板引擎生成 | MIS 后端 API 返回 |
| **组件数量** | 35+ | 24 |
| **联动机制** | d_actions + listener 发布订阅 | 暂无（Schema 按操作类型静态下发） |
| **状态管理** | Redux + Form + Listener 三层 | Form 单层（useState 管组件内状态） |
| **调用方式** | 页面内渲染 | 组件内嵌 / 命令式弹窗 |
| **打包** | Webpack（Monorepo 内） | Rollup（独立 npm 包） |
| **设计系统** | pebble-design-react | pebble-design-react（共享） |

**核心叙事**：同一个 Schema 驱动架构，两个消费者。营销平台 处理"活动怎么配"，benefit SDK 处理"权益怎么管"。

---

## 八、明日计划（W1 周四）

- [ ] prd2code-gen 复盘：3-Skill AI 工具链的 5 个核心讲点
- [ ] 写 prd2code-gen 的 STAR 讲稿
- [ ] 过一遍 experiments/results/ 对比数据
- [ ] 睡前背第 4 题「AI 生成代码怎么保证可靠性？」
