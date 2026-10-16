# UMAP 科研配色卡

> 单细胞分析中，画**细胞类型**用离散多色（一色一类细胞），画**基因表达 / score** 用连续渐变色——两套色板不要混用。

👉 **在线访问：<https://zzzelyn.github.io/umap-color-palettes/>**

## 功能

- 共 4 大类、30+ 套配色：
  - **单色渐变**（基因表达 / feature plot）
  - **冷暖双色发散**（cell cycle / senescence score、Spatial Log2FC 等含正负方向的数据）
  - **彩虹渐变**（拟时序 / CytoTRACE）
  - **细胞类型分类**（13 组离散调色板：41 色通用板 + 按组织场景精配的 8–12 色板）
- 细胞类型板块每组配色附 **UMAP 效果示意图**（合成示例，簇数 = 颜色数），直观对比各色板的上图效果；
- 渐变类配色附由本组颜色生成的 **渐变预览条**，点击可复制 CSS 渐变代码；
- 点击任意色块或 HEX 标签即可复制单色；
- 点「复制 R 向量 / 复制 Python 向量」可整组复制，直接粘进 Seurat / Scanpy 使用。

## 使用

- **在线使用**：点击顶部「在线访问」链接即可；
- **本地使用**：无需任何依赖、无需联网，下载仓库后用浏览器打开 `index.html` 即可。

## 部署（GitHub Pages）

仓库根目录即 `index.html`。在仓库 `Settings → Pages` 选择 `main` 分支、根目录（`/`）发布即可生成在线访问地址。

## 如何新增配色 / 板块（开发者）

所有数据都在 `index.html` 底部：

- `palettes` 数组：新增一套配色 = 加一个对象 `{type, name, use, colors}`；
- `groups` 对象：新增一个板块（如「细胞类型分类」）= 加一行 `{title, tag, sub}`，并把配色对象的 `type` 设成同一个值即可，板块顺序按 `groups` 排列。

## 重新生成 UMAP 示意图（开发者）

细胞类型板块的示意图由脚本合成，新增 / 修改 cell 配色后重新跑一次即可同步更新：

```bash
pip install numpy matplotlib   # 仅需这两个依赖
python tools/gen_umap_previews.py
```

脚本会读取 `index.html` 里的 cell 配色，按「簇数 = 颜色数」生成 `assets/umap_01.png ...`，与页面展示顺序一一对应；以配色名称为随机种子，重复运行结果一致。图片缺失时页面会自动隐藏示意图，不会报错。


