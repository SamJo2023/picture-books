# 绘本图书馆

为女儿收藏的 3D 卡通儿童绘本，配童声朗读翻页效果。

## 结构

```
.
├── index.html              ← 绘本图书馆首页
├── xiaoma/                 ← 《小马过河》8 页 + 童声朗读
│   ├── index.html
│   ├── images/             ← 8 张 3D 卡通插图
│   └── audio/              ← 8 段 mmx speech 合成旁白
└── <book-name>/            ← 未来的绘本
```

## 增加新绘本

1. 在根目录新建子文件夹，例如 `caihong-mao/`
2. 复制 `xiaoma/index.html` 改写内容和图、音频
3. 把封面图（首页会展示）放在 `caihong-mao/images/cover.png`
4. 在 `index.html` 的 `<main class="grid">` 里加一个 `<a class="book-card">` 卡片
5. `git add . && git commit -m "添加《彩虹猫》" && git push`
6. Vercel 自动部署，几秒后 `yourdomain.com/caihong-mao/` 上线

## 本地预览

直接双击 `index.html` 即可在浏览器中查看（音频需在线）。
