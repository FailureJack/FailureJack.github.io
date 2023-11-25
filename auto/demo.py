import re

class MarkdownFile:
    def __init__(self, title, content):
        self._title = title
        self._content = content

    def replace_local_img_link(self):
        # 使用正则表达式替换图片链接
        def replace_image_link(match):
            image_path = match.group(1)  # 获取图片路径
            image_name = image_path.split('/')[-1]  # 提取图片文件名
            new_image_tag = f'<p align="center"><img src="{self._title}/{image_name}" ></p>'  # 构建新的HTML标签
            return new_image_tag

        # 使用正则表达式替换图片链接
        self._content = re.sub(r'!\[.*?\]\((.*?)\)', replace_image_link, self._content)

# 创建MarkdownFile实例并调用replace_local_img_link方法进行测试
title = "example"
content = "This is an example content with an image: ![image](static/image.jpg)"
markdown = MarkdownFile(title, content)
markdown.replace_local_img_link()

# 打印替换后的内容
print(markdown._content)