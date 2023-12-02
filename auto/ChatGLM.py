from transformers import AutoTokenizer, AutoModel
from Markdown import Categories

class ChatGLM:
    def __init__(self, model_path):
        self._model_path = model_path
        self._tokenizer = AutoTokenizer.from_pretrained(self._model_path, trust_remote_code=True)
        self._model = AutoModel.from_pretrained(self._model_path, trust_remote_code=True).quantize(4).cuda()
        self._model = self._model.eval()
    
    def read_md(self, md, hist=[]):
        md_read = '请你阅读并理解下面给出的markdown文章：\n'
        return self._model.chat(self._tokenizer, md_read + md, history = hist)
    
    def extract_keyword(self, md, hist=[]):
        if len(hist) == 0:
            _, hist = self.read_md(md)
        
        demand = "针对上面的markdown文章提取3个关键词，且将这3个关键词以严格的','分隔方式输出："
        response, H = self._model.chat(self._tokenizer, demand, history=hist)
        return response.split(","), H
    
    def extract_abstract(self, md, hist=[]):
        if len(hist) == 0:
            _, hist = self.read_md(md)
        
        demand = '针对上面的markdown文章写50字中文摘要，注意保证摘要的字数不多于50个中文汉字：' 
        return self._model.chat(self._tokenizer, demand, history=hist)
    
    def extract_category(self, md, hist=[]):
        if len(hist) == 0:
            _, hist = self.read_md(md)
        
        demand = '从 '+Categories.str_v()+' 几个类别中选择最符合这篇markdown文章内容的一个类别，并原封不动的输出类别：'
        return self._model.chat(self._tokenizer, demand, history=hist)
    
    @property
    def model_path(self):
        return self._model_path

    @model_path.setter
    def model_path(self, value):
        self._model_path = value    