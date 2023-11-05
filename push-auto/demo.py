import re

def replace_image_links(markdown_content, custom_image_url):
    # 匹配 Markdown 中的图片链接
    pattern = r"!\[.*?\]\((.*?)\)"
    
    # 替换图片链接为自定义地址
    replaced_content = re.sub(pattern, f"![image]({custom_image_url})", markdown_content)
    
    return replaced_content

# 示例用法
markdown_content = """
# 标题

这是一张图片：

![alt text](local_image.jpg)
"""

custom_image_url = "https://example.com/images/image.jpg"

replaced_content = replace_image_links(markdown_content, custom_image_url)
print(replaced_content)