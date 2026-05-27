# CSS 布局

> BFC、Flexbox、Grid 三大布局体系。

---

## 核心知识点

| 主题 | 关键概念 | 速查板 |
|------|---------|--------|
| BFC | 块级格式化上下文，独立渲染区域 | 📗 CSS BFC + Flexbox + Grid 布局 |
| Flexbox | 一维布局，主轴+交叉轴，flex-grow/shrink/basis | 📗 CSS BFC + Flexbox + Grid 布局 |
| Grid | 二维布局，grid-template-rows/columns | 📗 CSS BFC + Flexbox + Grid 布局 |
| 渲染管线 | Reflow / Repaint / Composite 触发条件 | 📗 浏览器渲染管线 |

---

## BFC 速查

**触发条件**：
- `overflow: hidden` / `auto` / `scroll`（不为 visible）
- `float: left` / `right`（不为 none）
- `position: absolute` / `fixed`
- `display: inline-block` / `flex` / `grid`

**用途**：
- 清除浮动（父元素 `overflow: hidden`）
- 防止 margin 塌陷
- 阻止元素被浮动元素覆盖

---

## Flexbox 速查

```css
.container {
  display: flex;
  justify-content: center;    /* 主轴对齐 */
  align-items: center;        /* 交叉轴对齐 */
  gap: 16px;                  /* 间距 */
}
.item {
  flex: 1;                    /* flex-grow: 1, flex-shrink: 1, flex-basis: 0% */
}
```

---

## Grid 速查

```css
.container {
  display: grid;
  grid-template-columns: repeat(3, 1fr);  /* 三等分 */
  grid-template-rows: auto 1fr auto;       /* 三行 */
  gap: 16px;
}
.item {
  grid-area: 1 / 1 / 3 / 3;  /* row-start / col-start / row-end / col-end */
}
```

---

## 选择原则

- **单行或单列** → Flexbox
- **行列交叉、需要精确定位** → Grid
- **兼容性要求高** → Flexbox（Grid 需 IE 不支持）
