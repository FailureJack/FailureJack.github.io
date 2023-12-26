'''
先将本markdown定位为适用与私人自动化发布文章，暂不考虑各种异常情况，
1. 发布时一定会提供文章所在的路径，该路径保证真实存在
2. 上述路径下的文件一定符合预定要求结构，每个md都存在对应的static文件夹
3. 每个md都为一般正常书写博客，都有实际内容
4. 无法保证的是每个md的头是正确书写的，仅解析能够识别的部分，不能解析的使用None或者空（字符串、列表）代替
5. 类中设计的函数仅考虑在本项目中调用的情况，不用考虑别其他代码调用的情况
'''
from enum import Enum, unique
from datetime import datetime
import platform
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
    def __init__(self, title = None, cover=None, date=None, comments=True, feature=False, abstracts=None, categories=None, tags=None):
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
    def parse_datetime(cls, s):
        # all allowed format
        datetimePatterns = [
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d",
            "%Y/%m/%d",
            "%Y年%m月%d日",
            "%Y %m %d"
        ]
        for p in datetimePatterns:
            try:
                return datetime.strptime(s, p)
            except ValueError:
                pass

    @classmethod                
    def filter_invalid_char(cls, s):
        # 1. character ':' with a space follow would cause parse exception
        s = s.replace(": ", ":")

        # 2. a unclosed str would lead to 'full text string'
        i = 0
        while i < len(s) and (s[i] == "'" or s[i] == '"'):
            if s[i] == "'" and s.find("'", i + 1) != -1:
                break
            if s[i] == '"' and s.find('"', i + 1) != -1:
                break
            i += 1

        s = s[i:] if i < len(s) else ''

        return s

    @classmethod
    def parse_front(cls, content):
        obj = Front()
        # 定义正则表达式模式
        pattern = r'---\n(.*?)\n---'
        match = re.search(pattern, content, re.DOTALL)

        if not match:
            return obj
        
        lines = match.group(1).split('\n')

        i = 0
        while(i < len(lines)):
            key, value = lines[i].split(':', 1)
            key = key.strip()
            value = value.strip()
            
            try:
                if key == 'title':
                    obj.title = Front.filter_invalid_char(value)
                elif key == 'abstracts':
                    obj.abstracts = Front.filter_invalid_char(value)
                elif key == 'categories':
                    obj.categories = Front.filter_invalid_char(value)

                elif key == 'cover':
                    # user should write the correct path, absolute path recom
                    _ = Image.open(value)
                    obj.cover = value

                elif key == 'comments':
                    obj.comments = Front.parse_boolean(value)
                elif key == 'feature':
                    obj.feature = Front.parse_boolean(value)
                elif key == 'date':
                    obj.date = Front.parse_datetime(value)

                elif key == 'tags':
                    obj.tags = []
                    while i + 1 < len(lines) and lines[i + 1].strip()[0] == '-':
                        tag = lines[i][lines[i].find('-') + 1].strip()
                        obj.tags.append(Front.filter_invalid_char(tag))
                        i += 1
            except Exception as e:
                print(e)            
            finally:
                i += 1
        
        return obj
    
    def generate_front(self):
        if not self.verify_front():
            return None
        resA = "---\n"
        resB = "mathjax: true\n---\n"

        if self._title.bool():
            resA += "title: " + self._title + "\n"
        elif self._cover.bool():
            resA += "cover: " + self._cover + "\n"
        elif self._date.bool():
            resA += "date: " + self._date.strftime('%Y-%m-%d %H:%M:%S') + "\n"
        elif self._comments is not None:
            resA += "comments: " + self._comments + "\n"
        elif self._feature is not None:
            resA += "feature: " + self._feature + "\n"
        elif self._abstracts.bool():
            resA += "abstracts: " + self._abstracts + "\n"
        elif self._categories.bool():
            resA += "categories: " + self._categories + "\n"
        elif self._tags.bool():
            taglist = "\n".join(["- " + tag for tag in self._tags])
            resA += "tags:\n" + taglist + "\n"
        
        return resA + resB
    
    #region setter&getter
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
    #endregion

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

        if self._front._title:
            self._title = self.filter_invalid_path(self._front._title)
        else:
            self._front._title = self._front.filter_invalid_char(self.extract_title())
            self._title = self.filter_invalid_path(self._front._title)
        
    # title processing
    def extract_title(self):
        #TODO: assume there is and only one H1 and won't be null str
        # 如果没有H1，选择第一个H最高的那级标题作为标题，如果没有H开头的，让gpt拟一个标题
        pattern = r'^#\s+(.*)'  # 匹配以#开头的行，并提取标题内容
        match = re.search(pattern, self._content, re.MULTILINE)
        if match:
            return match.group(1).strip()
        else:
            return None
        
    # local img processing
    def replace_local_img_link(self):
        # 使用正则表达式替换图片链接
        def replace_img_link(match):
            image_path = match.group(1)  # 获取图片路径
            image_name = image_path.split('/')[-1]  # 提取图片文件名
            # 构建新的HTML标签
            new_image_tag = f'<p align="center"><img src="/img/{self._title}/{image_name}" ></p>'
            return new_image_tag

        # 使用正则表达式替换图片链接
        self._content = re.sub(r'!\[.*?\]\((.*?)\)', replace_img_link, self._content)

    # filepath processing
    def filter_invalid_path(self, path):
        sysstr = platform.system()
        if sysstr =="Windows":
            pattern=r'[\\/:*?"<>|\r\n]+'
        elif sysstr == "Linux":
            print ("Call Linux tasks")
        elif sysstr == "Darwin":
            print ("Call Mac tasks")
        
        return re.sub(pattern, '', path)#去掉非法字符  

    # content processing
    def filter_content(self):
        # 过滤代码块
        code_block_pattern = r'```[\s\S]*?```'  # 匹配代码块
        content = re.sub(code_block_pattern, '', self._content)

        # 过滤链接
        link_pattern = r'\[.*?\]\(.*?\)'  # 匹配链接
        content = re.sub(link_pattern, '', content)

        # 过滤公式
        latex_pattern = r'(\$\$).*?(\$\$)|(\$).*?(\$)'
        content = re.sub(latex_pattern, '', content, flags=re.DOTALL)
        
        return content
    
    def save(self, path):
        if not self._date.bool():
            self._date = datetime.now()
        
        self.replace_local_img_link()

        # 在文件头添加字符串
        new_content = self._front.generate_front() + self._content
        
        path_file = os.path.join(path, self._title + '.md')
        path_dir = os.path.join('../source/img', self._title)

        # 将修改后的内容保存为新的Markdown文件
        with open(path_file, 'w', encoding = 'utf-8') as file:
            file.write(new_content)

        if os.path.exists(path_dir):
            shutil.rmtree(path_dir)
        shutil.copytree(self._static, path_dir)

    #region setter&getter
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
    #endregion