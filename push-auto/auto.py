import os
import re
from transformers import AutoTokenizer, AutoModel

# chatGLM
def extract_key_words(md,model):
    return ["demo","123","lucas"]

def extract_abstract(md,model):
    return "demo test"

# stable diffusion
def generate_img(key_words,model):
    return 

# markdown
def replace_local_img_link(content_list):
    # 匹配 Markdown 中的图片链接
    pattern = r"!\[.*?\]\((.*?)\)"
    
    for content in content_list:
        # 替换图片链接为自定义地址
        content = re.sub(pattern, f"![image]({custom_image_url})", content)

def get_md_files(md_dir_path):
    if md_dir_path is None:
        # 获取当前目录路径
        current_directory = os.getcwd()
    else:
        current_directory = md_dir_path

    # 获取当前目录下所有的文件名
    file_names = os.listdir(current_directory)

    # 筛选出以 .md 结尾的文件
    return [file for file in file_names if file.endswith(".md")]

def filter_md_content(md_content):
    # 过滤代码块
    code_block_pattern = r'```[\s\S]*?```'  # 匹配代码块
    content = re.sub(code_block_pattern, '', md_content)

    # 过滤链接
    link_pattern = r'\[.*?\]\(.*?\)'  # 匹配链接
    content = re.sub(link_pattern, '', md_content)

    return content

def read_md_files(md_files):
    content_list = []
    for md_file in md_files:
        with open(md_file, 'r', encoding='utf-8') as file:
            content_list.append(file.read())
    
    return content_list

if __name__ == '__main__':

    md_files = get_md_files()
    content_list = read_md_files(md_files)
    

    # init chatGLM
    tokenizer = AutoTokenizer.from_pretrained("THUDM/chatglm3-6b", trust_remote_code=True)
    model = AutoModel.from_pretrained("THUDM/chatglm3-6b", trust_remote_code=True, device='cuda')
    model = model.eval()
    
    
    response, history = model.chat(tokenizer, "你好", history=[])