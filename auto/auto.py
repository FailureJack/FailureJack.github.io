import os
from Markdown import Markdown
from PicGen import StableDiffusion
from MdReader import ChatGLM


if __name__ == '__main__':
    # prepare markdown
    md_files_path = 'C:\\Users\\Failurer\\Desktop\\test'
    
    md_files = Markdown.get_md_files(md_files_path)

    md_objects = [Markdown(content=md, static = stat) for md, stat in md_files]
    
    # get the reader
    chatGLM_model_path = 'D:\\ChatGLM3\\chatglm3-6b-32k'
    reader = ChatGLM(chatGLM_model_path)
    for obj in md_objects:
        
        _, history = reader.read_md(obj.filter_content())

        if not obj.abstract.bool():
            resp, _ =reader.extract_abstract(md = None, hist = history)
            obj.abstract = resp

        if not obj.tags.bool():
            resp, _ =reader.extract_keyword(md = None, hist = history)
            obj.tags = resp
        
        if not obj.categories.bool():
            resp, _ =reader.extract_category(md = None, hist = history)
            obj.categories = resp

    # stable diffusion
    cover_path = '../source/cover/'
    web_url = 'http://127.0.0.1:7860'
    sd = StableDiffusion(web_url)

    # finish pic gen and cp
    for obj in md_objects:
        if obj.cover.bool():
            continue

        img_path = os.path.join(cover_path, obj.title + '.png')
        if os.path.exists(img_path):
            obj.cover = '/cover/'+obj.title+'.png'
            continue

        for image in sd.generate_imgs():
            image.save(img_path)
            obj.cover = '/cover/'+obj.title+'.png'

    # finish everything's cp
    for obj in md_objects:
        obj.save('../source/_posts')

    # call hexo command to upload