---
title: 如何给github仓库重命名
url: github-rename
category:
- 后端学习
- 前端学习
tags:
- github
- git
---

## 重命名仓库
github主页 -> 仓库 -> Settings -> 重命名仓库

## 修改本地仓库的远程地址
```bash
git remote set-url origin <new-url>
```

值得注意的是，即使你不修改本地仓库的远程地址，git push暂时也能使用，但是时间久了会出现问题，所以建议修改。