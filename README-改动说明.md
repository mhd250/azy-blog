# 本次改动文件包

## 包含的文件(按目录)

```
_config.yml                         ← 修改:加 skip_render
_config.anzhiyu.yml                 ← 修改:inject 加 glass.css + pjax exclude
source/css/glass.css                ← 新建:整合后的毛玻璃 CSS
source/music/index.html             ← 修改:路径修正
source/music/manifest.json          ← 修改:PWA scope
source/music/config.js              ← 新建:HeoMusic 歌单配置(关键!)
```

## 每个文件改了什么(一句话版)

| 文件 | 改动 |
|------|------|
| `_config.yml` | 加 `skip_render: ['music/**']`,防止 hexo 处理 music 目录 |
| `_config.anzhiyu.yml` | (1) inject.head 加 `<link glass.css>` (2) pjax.exclude 加 `/music/` |
| `source/css/glass.css` | **新文件**,整合你原来两份 CSS,优化性能+深色适配 |
| `source/music/index.html` | 把绝对路径改成相对路径,加注释说明 |
| `source/music/manifest.json` | `"scope": "/"` → `"scope": "./"`,适配子目录 |
| `source/music/config.js` | **新文件**,你之前缺的!HeoMusic 一直加载不出来的根因 |

## 怎么用

把这些文件**覆盖**到你本地 `azy-blog/` 仓库的对应位置,然后:

```bash
git add -A
git commit -m "fix: music 页加载 + CSS 整合"
git push
```

## 删除的文件(不在包里)

- `source/css/apple-glass.css`(被 glass.css 取代)
- `source/css/apple-glassmorphism.css`(被 glass.css 取代)
- `source/music/meting-api/` 整目录(PHP 后端,GH Pages 跑不了,35 个文件)
