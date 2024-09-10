---
title: zola如何采用主题
url: zola-theme
category:
- 前端学习
tags:
- zola
- blog
- 博客
- ssg
---

## 安装主题
```bash
cd themes
git clone <theme repository URL>
```

可以参考官方教程：
https://www.getzola.org/documentation/themes/installing-and-using-themes/

## 使用主题
在config.toml中添加theme字段<br>
注意：要放在最上方。不要在[extra]下面。
```toml
theme = "Seje2"
```

## 使用主题会遇到的问题
1. content通常要复制点东西.
   比如从themes文件夹复制一些.html文件到content文件夹。
   需要参考主题本身的教程。
2. 通常要修改config.toml。
   自定义变量要放在[extra]下面：
    ```toml
    [extra]
    seje2_menu_links = [
    {url = "$BASE_URL", name = "Home"},
    {url = "$BASE_URL/categories", name = "Categories"},
    {url = "$BASE_URL/tags", name = "Tags"},
    {url = "https://google.com", name = "Google"},
    ]
    ```

## 下载主题
https://www.getzola.org/themes/

官方主题库，里面有主题和安装方法。
