from enum import Enum, unique
from datetime import datetime
import re, os
import shutil
from PIL import Image

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

class Front:
    def __init__(self, title=None, cover=None, date=None, comments=True, feature=False, abstracts=None, categories=None, tags=None):
        self._title = title
        self._cover = cover
        self._date = date
        self._comments = comments
        self._feature = feature
        self._abstracts = abstracts
        self._categories = categories
        self._tags = tags
    
    @classmethod
    def parse_boolean(cls, s):
        if s.lower() == 'true':
            return True
        elif s.lower() == 'false':
            return False
        else:
            raise ValueError('Invalid boolean value!')

    @classmethod                
    def filter_invalid_char(cls, s):
        s = s.replace(": ", ":")
        i = 0
        while i < len(s) and (s[i] == "'" or s[i] == '"'):
            if s[i] == "'" and s.find("'", i + 1) != -1:
                break
            if s[i] == '"' and s.find('"', i + 1) != -1:
                break
            i += 1

        return s[i:] if i < len(s) else None

    @classmethod
    def parse_front(cls, content):
        obj = Front()
        # 定义正则表达式模式
        pattern = r'---\n(.*?)\n---'
        match = re.search(pattern, content, re.DOTALL)

        if not match:
            return
        
        lines = match.group(1).split('\n')

        i = 0
        while(i < len(lines)):
            key, value = lines[i].split(':', 1)
            key = key.strip()
            value = value.strip()
            
            try:
                if key == 'title':
                    obj._title = obj.filter_invalid_char(value)
                elif key == 'abstracts':
                    obj._abstracts = obj.filter_invalid_char(value)
                elif key == 'categories':
                    obj._categories = obj.filter_invalid_char(value)

                elif key == 'cover':
                    _ = Image.open(value)
                    obj._cover = value

                elif key == 'comments':
                    obj._comments = obj.parse_boolean(value)
                elif key == 'feature':
                    obj._feature = obj.parse_boolean(value)

                elif key == 'date':
                    datetimePatterns = [
                        "%Y-%m-%d %H:%M:%S",
                        "%Y-%m-%d",
                        "%Y/%m/%d",
                        "%Y年%m月%d日",
                        "%Y %m %d"
                    ]
                    for p in datetimePatterns:
                        try:
                            obj._date = datetime.strptime(value, p)
                        

                elif key == 'tags':
                    tags = []
                    i += 1
                    while i < len(lines) and lines[i].find('-') != -1:
                        tags.append(lines[i][lines[i].find('-') + 1:].strip())
                        i += 1
                    if len(tags) > 0:
                        obj._tags = tags         
            except Exception as e:
                print(e)            
            finally:
                i += 1
        
        return obj

    def verify_front(self):
        return  self._title is not None and \
                self._cover is not None and \
                self._date is not None and \
                self._comments is not None and \
                self._feature is not None and \
                self._abstracts is not None and \
                self._categories is not None and \
                self._tags is not None and len(self._tags) > 0
    
    def generate_front(self):
        if not self.verify_front():
            return None
        
        return  "---\n"\
                "title: {title}\n"\
                "cover: {cover}\n"\
                "date: {date}\n"\
                "comments: {comments}\n"\
                "feature: {feature}\n"\
                "abstracts: {abstracts}\n"\
                "mathjax: true\n"\
                "categories: {categories}\n"\
                "tags:\n{tags}\n"\
                "---\n".format(
                    title=self.fix_invalid_title(),
                    cover=self._cover,
                    date=self._date.strftime('%Y-%m-%d %H:%M:%S'),
                    comments=self._comments,
                    feature=self._feature,
                    abstracts=self._abstracts,
                    categories=self._categories,
                    tags="\n".join(["- " + tag for tag in self._tags])
                )

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
    def feature(self):
        return self._feature

    @feature.setter
    def feature(self, value):
        self._feature = value

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

class Markdown():
    
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

    def __init__(self, content, static):
        self._content = content
        self._static = static
        self._front = Front.parse_front(content)

        if self._content is None:
            self._title = None
        elif self._front._title is not None:
            self._title = self.filter_invalid_path(self._front._title)
        else:
            self._front._title = self._front.filter_invalid_char(self.extract_title())
            self._title = self.filter_invalid_path(self._front._title)

    # def __init__(self, title=None, cover=None, date=None, comments=True, feature=False, abstract=None, categories=None, tags=None, content=None, static=None):
    #     # 默认此接口下传的数据都是正确的
    #     self._front = Front(title, cover, date, comments, feature, abstract, categories, tags)
    #     self._content = content
    #     self._static = static
    #     self._title = title

    #     if self._content is not None and self._front._title is None:
    #         self.set_title()
        
    # title processing
    def extract_title(self):
        pattern = r'^#\s+(.*)'  # 匹配以#开头的行，并提取标题内容
        match = re.search(pattern, self._content, re.MULTILINE)
        if match:
            return match.group(1).strip()
        else:
            return None
        
    # local img processing
    def replace_local_img_link(self):
        # 使用正则表达式替换图片链接
        def replace_image_link(match):
            image_path = match.group(1)  # 获取图片路径
            image_name = image_path.split('/')[-1]  # 提取图片文件名
            new_image_tag = f'<p align="center"><img src="/img/{self._title}/{image_name}" ></p>'  # 构建新的HTML标签
            return new_image_tag

        # 使用正则表达式替换图片链接
        self._content = re.sub(r'!\[.*?\]\((.*?)\)', replace_image_link, self._content)

    # filepath processing
    def filter_invalid_path(self, path):
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

        # 匹配公式
        latex_pattern = r'(\$\$).*?(\$\$)|(\$).*?(\$)'
        content = re.sub(latex_pattern, '', content, flags=re.DOTALL)
        return content
    
    def save(self, path):  
        self._date = datetime.now()
        self.replace_local_img_link()

        # 在文件头添加字符串
        new_content = self._front.generate_front() + self._content
        
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

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value