from enum import Enum, unique
from datetime import datetime
import re, os
import shutil

@unique
class Categories(Enum):
    CATEGORY1 = '工作生活'
    CATEGORY2 = '学术科研'
    CATEGORY3 = '工程技术'
    CATEGORY4 = '理论研究'
    CATEGORY5 = '文化娱乐'

    @classmethod
    def dict_n_v(cls):
        return {m.name: m.value for m in cls}

    @classmethod
    def dict_v_n(cls):
        return {m.value: m.name for m in cls}
    
    @classmethod
    def list_v(cls):
        return [m.value for m in cls]
    
    @classmethod
    def list_n(cls):
        return [m.name for m in cls]
    
    @classmethod
    def str_v(cls):
        return '，'.join(Categories.list_v())
    
    @classmethod
    def str_n(cls):
        return '，'.join(Categories.list_n())

class Markdown:
    
    @classmethod
    def get_md_files(cls, md_dir_path):
        # 目录结构
        # md_dir_path
        # |--a
        # |  |--*.md
        # |  |--static
        # |  |  |--*.png
        # |--b
        # |--c 

        if md_dir_path is None:
            # 获取当前目录路径
            dir = os.getcwd()
        else:
            dir = md_dir_path

        res = []
        # 遍历所有文件和文件夹，筛选出文件夹
        for d in os.listdir(dir):
            if not os.path.isdir(os.path.join(dir, d)):
                continue

            # 拼接md文件路径
            md_file_path = os.path.join(dir, d, d + '.md')
            # 读取md文件内容
            with open(md_file_path, 'r', encoding='utf-8') as md_file:
                md_content = md_file.read()
                
            # 拼接static文件夹路径
            static_folder_path = os.path.join(dir, d, 'static')

            res.append((md_content, static_folder_path))
        
        return res

    def __init__(self, title=None, cover=None, date=None, comments=True, abstract=None, categories=None, tags=None, content=None, static=None):
        self._title = title
        self._cover = cover
        self._date = date
        self._comments = comments
        self._abstract = abstract
        self._categories = categories
        self._tags = tags
        self._content = content
        self._static = static

        if self._content is not None and self._title is None:
            self.set_title()

    # name format: {action}_{object}
    # action format:
    
    # title processing
    def extract_title(self):
        pattern = r'^#\s+(.*)'  # 匹配以#开头的行，并提取标题内容
        match = re.search(pattern, self._content, re.MULTILINE)
        if match:
            return match.group(1).strip()
        else:
            return None

    def fix_invalid_title(self):
        if not self._title[0].isalnum():
            return self._title[1:].replace(": ", ":")
        return self._title.replace(": ", ":")

    def set_title(self):
        self._title = self.extract_title()

    # local img processing
    def replace_local_img_link(self):
        # 使用正则表达式替换图片链接
        def replace_image_link(match):
            image_path = match.group(1)  # 获取图片路径
            image_name = image_path.split('/')[-1]  # 提取图片文件名
            new_image_tag = f'<p align="center"><img src="/img/{self.fix_invalid_path(self._title)}/{image_name}" ></p>'  # 构建新的HTML标签
            return new_image_tag

        # 使用正则表达式替换图片链接
        self._content = re.sub(r'!\[.*?\]\((.*?)\)', replace_image_link, self._content)

    def fix_invalid_path(self, path):
        invalid_chars = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']
        for char in invalid_chars:
            directory_name = re.sub(rf'(?<!\s){re.escape(char)}|{re.escape(char)}(?!\s)', ' ', directory_name)
            path = path.replace(char, ' ')
        return path

    # content processing
    def filter_content(self):
        # 过滤代码块
        code_block_pattern = r'```[\s\S]*?```'  # 匹配代码块
        content = re.sub(code_block_pattern, '', self._content)

        # 过滤链接
        link_pattern = r'\[.*?\]\(.*?\)'  # 匹配链接
        content = re.sub(link_pattern, '', content)

        latex_pattern = r'(\$\$).*?(\$\$)|(\$).*?(\$)'
        content = re.sub(latex_pattern, '', content, flags=re.DOTALL)
        return content

    # front
    def extract_front(self):
        pass

    def generate_front(self):

        return  "---\n"\
                "title: {title}\n"\
                "cover: {cover}\n"\
                "date: {date}\n"\
                "comments: {comments}\n"\
                "abstracts: {abstracts}\n"\
                "mathjax: true\n"\
                "categories: {categories}\n"\
                "tags:\n{tags}\n"\
                "---\n".format(
                    title=self.fix_invalid_title(),
                    cover=self._cover,
                    date=self._date,
                    comments=self._comments,
                    abstracts=self._abstract,
                    categories=self._categories,
                    tags="\n".join(["- " + tag for tag in self._tags])
                )
    
    def save(self, path):  
        self._date = datetime.now()
        self.replace_local_img_link()

        # 在文件头添加字符串
        new_content = self.generate_front() + self._content
        
        valid_title = self.fix_invalid_path(self._title)
        path_file = os.path.join(path, valid_title + '.md')
        path_dir = os.path.join('../source/img', valid_title)

        # 将修改后的内容保存为新的Markdown文件
        with open(path_file, 'w', encoding = 'utf-8') as file:
            file.write(new_content)

        if os.path.exists(path_dir):
            shutil.rmtree(path_dir)
        shutil.copytree(self._static, path_dir)
    
    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value

    @property
    def cover(self):
        return self._cover

    @cover.setter
    def cover(self, value):
        self._cover = value

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, value):
        self._date = value
    
    @property
    def comments(self):
        return self._comments

    @comments.setter
    def comments(self, value):
        self._comments = value

    @property
    def abstract(self):
        return self._abstract

    @abstract.setter
    def abstract(self, value):
        self._abstract = value

    @property
    def categories(self):
        return self._categories

    @categories.setter
    def categories(self, value):
        self._categories = value

    @property
    def tags(self):
        return self._tags

    @tags.setter
    def tags(self, value):
        self._tags = value

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        self._content = value
    
    @property
    def static(self):
        return self._static

    @static.setter
    def static(self, value):
        self._static = value