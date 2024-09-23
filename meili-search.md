---
title: meili search的安装方法？最好的站内搜索工具
url: docker-desktop
category:
- 后端学习
tags:
- docker
- docker desktop
---

# 服务器端安装meili-search
## 本地作为服务器
### 安装meili-search
```bash
brew install meilisearch
```
其他安装方法见[官网](https://www.meilisearch.com/docs/learn/self_hosted/install_meilisearch_locally)

### 运行meili-search
```bash
meilisearch --master-key <your-key>
```
你应该有个master-key，如果没有，直接运行`meilisearch`，会生成一个。

项目会运行在`http://localhost:7700`

# 扫描网站，生成index
接下来，我们需要扫描网站，生成index。这里用到一个工具是meilisearch的[docs-scraper](https://github.com/meilisearch/docs-scraper/).

## 编写供扫描的配置文件
以下是简单的示例。值得注意的是，我把`zola`放在本地的1111端口里面，希望它扫描blog页面的文档，所以需要指向本地端口。

因为后面要用到docker，docker里面的本地表示不一样，所以需要用`host.docker.internal`来代替`localhost`。
```json
{
    "index_uid": "docs",
    "start_urls": ["http://host.docker.internal:1111/blog/"],
    "sitemap_urls": ["http://host.docker.internal:1111/sitemap.xml"],
    "stop_urls": [],
    "selectors": {
      "lvl0": "h1",
      "lvl1": "h2",
      "lvl2": "h3",
      "text": "p, li"
    }
  }
```

## 运行Scrapper
这里要用到docker，所以需要先安装docker desktop。
```bash
docker run -t --rm \
  -e MEILISEARCH_HOST_URL="http://host.docker.internal:7700" \
  -e MEILISEARCH_API_KEY="yourkey" \
  -v /Users/lxz/Desktop/zola-basic/meili.json:/docs-scraper/config.json \
  --network host \
  getmeili/docs-scraper:latest pipenv run ./docs_scraper config.json
```
由于是在本地运行，所以需要加上--network host，这样docker才能访问到本地的端口。

另外，我用docker pull的image是getmeili/docs-scraper:latest，我实践过程，指定版本不行，会显示禁止POST访问，但是官网推荐生产环境要用指定版本。

出现以下信息，表示成功：
```bash
> Docs-Scraper: http://host.docker.internal:1111/blog/ 27 records)

Nb hits: 27
```
上面信息表示，扫描了27个文档。

# 前端安装js和css
## 安装docs-searchbar.js
接下来，我们正式在前端要搜索了，需要安装一个搜索工具，这里用到的是meilisearch的[docs-searchbar.js](https://github.com/meilisearch/docs-searchbar.js?tab=readme-ov-file)

### 安装库
```bash
yarn add docs-searchbar.js
```

### 在html里面引入
```html
<script src="https://cdn.jsdelivr.net/npm/docs-searchbar.js@latest/dist/cdn/docs-searchbar.min.js"></script>
```
如果直接在html里面引入，可以不安装库。与前面步骤是二选一的关系。

## html页面添加元素
### 添加搜索框：
```html
<input type="search" id="search-bar-input" />
```

### 添加js代码：
```html
  <script>
    docsSearchBar({
      hostUrl: 'http://127.0.0.1:7700',
      apiKey: 'your-key',
      indexUid: 'docs',
      inputSelector: '#search-bar-input',
      debug: false, // Set debug to true if you want to inspect the dropdown
    })
  </script>
```

### 添加css样式
```html
<link
  rel="stylesheet"
  href="https://cdn.jsdelivr.net/npm/docs-searchbar.js@latest/dist/cdn/docs-searchbar.min.css"
/>
```

好了，可以测试一下了。



# 云主机作为服务器
### 安装meili-search
```bash
# Install Meilisearch
curl -L https://install.meilisearch.com | sh

# Launch Meilisearch
./meilisearch
```

待更新。

# 参考
1. 为什么我知道meili-search?-[owen的博客](https://www.owenyoung.com/blog/add-search/#overview)