---
title: Hello World
cover: /cover/hello-world.png
date: 2023/7/13 20:46:25
comments: True
abstracts: "分享我的经验和曾经遇到的问题" # 120个字好像是极限了，应该更少，推荐50字左右
categories: Test
tags:
- Hello World
- Beginner
---
# Hello
Welcome to [Hexo](https://hexo.io/)! This is your very first post. Check [documentation](https://hexo.io/docs/) for more info. If you get any problems when using Hexo, you can find the answer in<a name="inParagraph"></a> [troubleshooting](https://hexo.io/docs/troubleshooting.html) or you can ask me on [GitHub](https://github.com/hexojs/hexo/issues).

## Quick-Start 

### Create a new post

``` bash
$ hexo new "My New Post"
```

More info: [Writing](https://hexo.io/docs/writing.html)

### Run server

``` bash
$ hexo server
```

More info: [Server](https://hexo.io/docs/server.html)

### Generate static files

``` bash
$ hexo generate
```

More info: [Generating](https://hexo.io/docs/generating.html)

### Deploy to remote sites

``` bash
$ hexo deploy
```

More info: [Deployment](https://hexo.io/docs/one-command-deployment.html)

## 用户自定义front

由于每个md文档需要在首部生成一个特定格式的front，以供框架识别文章的元信息，包括标题、关键字、摘要、更新时间等等。
如果用户仅仅是想要快速迁移博客，不想要自定义front，可以由auto.py脚本自动生成；

同时如果用户想要自定义front，本框架依然允许，需要用户按照指定格式提前写入文件内，最好直接写在文件头，后面框架的处理会参考用户自定的front

## 这是一个页面内跳转的示例

markdown能够自动跳转各级标题，跳转方式为：[跳转链接的文字](#标题)，注意待跳转的标题不能存在空格，否则无法识别为跳转链接，跳转链接的文字可以存在空格

[跳 转 到he llo](#Hello)

还可以通过灵活设置锚点指示跳转的位置\<a name="锚点名"\>\<\/a\>，对于本博客，建议将锚点设置的比内容要“高一点”，锚点名同样不能有空格，跳转链接的文字同上

[跳到段落之间](#inParagraph)来跳转到第一个标题所在的位置。