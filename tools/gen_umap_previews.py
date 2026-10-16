#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
为「细胞类型分类」板块的每组配色合成一张 UMAP 风格示意图。

用法：
    python tools/gen_umap_previews.py

- 从 ../index.html 的 palettes 数组读取所有 cell 类型配色
- 簇数 = 颜色数，按该色板上色；以配色名称为种子保证结果可复现
- 输出到 ../assets/umap_01.png ... (序号与 cell 板块展示顺序一致)
重新跑即可随配色更新而重生成，纯本地、无外部依赖图片。
"""
import os, re, json, hashlib
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HTML = os.path.join(ROOT, "index.html")
OUT  = os.path.join(ROOT, "assets")


def extract_cell_palettes(path):
    """读取 index.html，解析 palettes 数组，返回所有 type=='cell' 的配色列表。"""
    txt = open(path, encoding="utf-8").read()
    m = re.search(r"const palettes = \[([\s\S]*?)\n\];", txt)
    if not m:
        raise RuntimeError("未找到 palettes 数组")
    inner = m.group(1)
    inner = re.sub(r"//[^\n]*", "", inner)       # 去掉 // 行内注释
    inner = re.sub(r"([{,]\s*)(\w+)\s*:", r'\1"\2":', inner)  # 给键加引号
    inner = inner.replace("'", '"')              # 单引号 -> 双引号
    inner = inner.strip()
    if inner.endswith(","):                      # 去掉数组尾随逗号（JS 允许、JSON 不允许）
        inner = inner[:-1]
    palettes = json.loads("[" + inner + "]")
    return [p for p in palettes if p.get("type") == "cell"]


def seed_from(s):
    return int(hashlib.md5(s.encode("utf-8")).hexdigest(), 16) % (2**31)


def gen_umap(colors, seed):
    """生成一组看起来像 UMAP 输出的聚类散点（不依赖真实数据）。"""
    rng = np.random.default_rng(seed)
    n = len(colors)
    # 簇中心：黄金角螺旋 + 抖动，模拟 UMAP 的不规则排布
    angles = np.linspace(0, 2 * np.pi * (1.6 * n), n)
    radii = np.sqrt(np.arange(1, n + 1)) * 1.15
    centers = np.column_stack([radii * np.cos(angles), radii * np.sin(angles)])
    centers += rng.normal(0, 0.7, centers.shape)
    pts, col = [], []
    for i in range(n):
        size = int(rng.integers(35, 175))          # 不同簇大小不一，更像真实细胞比例
        theta = rng.uniform(0, 2 * np.pi)
        scale = rng.uniform(0.5, 1.7)
        R = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
        cov = R @ np.diag([scale, rng.uniform(0.4, 1.0) * scale]) @ R.T
        X = rng.multivariate_normal(centers[i], cov, size=size)
        pts.append(X)
        col.extend([colors[i]] * size)
    pts = np.vstack(pts)
    col = np.array(col)
    fig, ax = plt.subplots(figsize=(3.4, 2.55), dpi=120)
    ax.set_axis_off()
    ax.scatter(pts[:, 0], pts[:, 1], s=9, c=col, alpha=0.85,
               edgecolors="none", linewidths=0)
    pad = 2.0
    ax.set_xlim(pts[:, 0].min() - pad, pts[:, 0].max() + pad)
    ax.set_ylim(pts[:, 1].min() - pad, pts[:, 1].max() + pad)
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    return fig


def main():
    cell = extract_cell_palettes(HTML)
    os.makedirs(OUT, exist_ok=True)
    for i, p in enumerate(cell, 1):
        fig = gen_umap(p["colors"], seed_from(p["name"]))
        fn = os.path.join(OUT, f"umap_{i:02d}.png")
        fig.savefig(fn, dpi=120, facecolor="white")
        plt.close(fig)
        print(f"  assets/umap_{i:02d}.png  ({len(p['colors'])} 色 · {p['name']})")
    print(f"\n完成：共生成 {len(cell)} 张 UMAP 示意图 -> {OUT}")


if __name__ == "__main__":
    main()
