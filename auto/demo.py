import re

# 定义md文件头的字符串
md_string = """
---
title: 正向代理
cover: /cover/正向代理.png
date: 2023-11-25 19:13:30.102475
comments: True
abstracts: 以校园网访问谷歌为由，介绍如何配置正向代理服务器，涉及Clash、shadowsocks等多种代理方式，并补充无需代理的翻墙方式
mathjax: True
categories: 学术科研
tags:
- 代理服务器
- 流量转发
- 正向代理
---
"""

# 定义正则表达式模式
pattern = r'---\n(.*?)\n---'

# 使用正则表达式进行匹配
match = re.search(pattern, md_string, re.DOTALL)

if match:
    header_content = match.group(1)
    header_fields = {}
    # 提取每个字段
    for line in header_content.split('\n'):
        if ": " in line:
            key, value = line.split(': ', 1)
            header_fields[key] = value
        elif ":" in line:
            key, value = line.split(':', 1)
            if value is '' and key is 'tags':
                pass

    # 打印提取的字段
    print(header_fields)
else:
    print('未找到md文件头')
