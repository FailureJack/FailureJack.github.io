import os
from Markdown import Markdown
from PicGen import StableDiffusion
from MdReader import ChatGLM3_LocalCode, ChatGLM3_OpenAI

#TODO: 2.值没赋上去
if __name__ == '__main__':
    # prepare markdown
    md_files_path = 'C:\\Users\\Failurer\\Desktop\\test'
    
    md_files = Markdown.get_md_files(md_files_path)

    md_objects = [Markdown(content=md, static = stat) for md, stat in md_files]
    
    # get the reader
    # chatGLM_model_path = 'D:\\ChatGLM3\\chatglm3-6b-32k'
    # reader = ChatGLM3_LocalCode(chatGLM_model_path)
    # web_url = "http://localhost:8000/v1"
    web_url = "http://10.77.110.155:8000/v1"
    reader = ChatGLM3_OpenAI(web_url=web_url)
    for obj in md_objects:
        
        # _, history = reader.read_md(obj.filter_content())
        _ = reader.read_md(obj.filter_content())

        if not obj.front.abstracts:
            # resp, _ = reader.extract_abstract(md = None, hist = history)
            resp = reader.extract_abstract()
            obj.front.abstracts = resp

        if not obj.front.tags:
            # resp, _ =reader.extract_keyword(md = None, hist = history)
            resp = reader.extract_keyword()
            obj.front.tags = resp
        
        if not obj.front.categories:
            # resp, _ =reader.extract_category(md = None, hist = history)
            resp = reader.extract_category()
            obj.front.categories = resp

    # stable diffusion
    cover_path = '../source/cover/'
    # web_url = 'http://127.0.0.1:7860'
    web_url = 'http://10.77.110.155:7860'
    sd = StableDiffusion(web_url=web_url, checkpoint="CounterfeitV30_v30.safetensors")

    # finish pic gen and cp
    for obj in md_objects:
        if obj.front.cover:
            continue

        img_path = os.path.join(cover_path, obj.title + '.png')
        if os.path.exists(img_path):
            obj.front.cover = '/cover/'+obj.title+'.png'
            continue

        for image in sd.generate_imgs():
            image.save(img_path)
            obj.front.cover = '/cover/'+obj.title+'.png'

    # finish everything's cp
    for obj in md_objects:
        obj.save('../source/_posts')

    # call hexo command to upload