import os
from Markdown import Markdown
from StableDiffusion import StableDiffusion
from ChatGLM import ChatGLM


if __name__ == '__main__':
    md_files_path = 'C:\\Users\\Failurer\\Desktop\\test'
    chatGLM_model_path = 'D:\\ChatGLM3\\chatglm3-6b-32k'

    # prepare markdown
    md_files = Markdown.get_md_files(md_files_path)

    md_objects = [Markdown(content=md, static = stat) for md, stat in md_files]
    
    # chat
    chat = ChatGLM(chatGLM_model_path)
    for obj in md_objects:
        
        _, history = chat.read_md(obj.filter_content())

        resp, _ =chat.extract_abstract(md = None, hist = history)
        obj.abstract = resp

        resp, _ =chat.extract_keyword(md = None, hist = history)
        obj.tags = resp

        resp, _ =chat.extract_category(md = None, hist = history)
        obj.categories = resp

    # stable diffusion
    cover_path = '../source/cover/'
    sd = StableDiffusion()

    # finish pic gen and cp
    for obj in md_objects:
        img_path = os.path.join(cover_path, obj.title + '.png')
        if os.path.exists(img_path):
            obj.cover = '/cover/'+obj.title+'.png'
            continue

        for image in sd.generate_imgs():
            image.save(img_path)
            obj.cover = '/cover/'+obj.title+'.png'

    # finish everything's cp
    for obj in md_objects:
        obj.save_md('../source/_posts')

    # call hexo command to upload