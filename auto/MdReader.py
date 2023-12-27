from transformers import AutoTokenizer, AutoModel
from Markdown import Categories

from langchain.chat_models import ChatOpenAI
from langchain.chains.conversation.memory import ConversationEntityMemory
from langchain.chains.conversation.prompt import ENTITY_MEMORY_CONVERSATION_TEMPLATE
from langchain.chains import ConversationChain

class ChatGLM3_OpenAI:
    def __init__(self, web_url = "http://localhost:8000/v1"):
        self._web_url = web_url
        self._conversation = self.generate_conversation(self._web_url)
                
    def generate_conversation(self, url):
        #指定ChatGLM2-6B的API endpoint url，用langchain的ChatOpanAI类初始化一个ChatGLM的chat模型
        llm = ChatOpenAI(
            model_name="chatglm",
            openai_api_base=url,
            openai_api_key="EMPTY",
            streaming=False,
        )

        #使用会话实体内存，利用ChatGLM在会话过程中分析提到的实体(Entity)
        entity_memory = ConversationEntityMemory(llm=llm, k=5 )

        #生成会话链
        return  ConversationChain(
                    llm=llm, 
                    prompt=ENTITY_MEMORY_CONVERSATION_TEMPLATE,
                    memory=entity_memory,
                    verbose=True,
                )

    def read_md(self, md):
        md_read = '请你阅读并理解下面给出的markdown文章：\n'
        return self._conversation.predict(input = md_read + md)
    
    def extract_title(self):
        demand = "针对上面的markdown文章提取1个不超过50字的中文标题："
        return self._conversation.predict(input = demand).strip()
    
    def extract_keyword(self):
        demand = "针对上面的markdown文章提取3个关键词，且将这3个关键词以严格的','分隔方式输出："
        response = self._conversation.predict(input = demand)
        return [item.strip() for item in response.split(',')]
    
    def extract_abstract(self):
        demand = '针对上面的markdown文章写50字中文摘要，注意保证摘要的字数不多于50个中文汉字：' 
        return self._conversation.predict(input = demand).strip()
    
    def extract_category(self):
        demand = '从 '+Categories.str_v()+' 几个类别中选择最符合这篇markdown文章内容的一个类别，并原封不动的输出类别：'
        return self._conversation.predict(input = demand).strip()
    
    #region setter&getter
    @property
    def conversation(self):
        return self._conversation

    @conversation.setter
    def conversation(self, value):
        self._conversation = value
    
    @property
    def web_url(self):
        return self._web_url

    @web_url.setter
    def web_url(self, value):
        self._web_url = value
    #endregion setter&getter

class ChatGLM3_LocalCode:
    def __init__(self, model_path):
        self._model_path = model_path
        self._tokenizer = AutoTokenizer.from_pretrained(self._model_path, trust_remote_code=True)
        self._model = AutoModel.from_pretrained(self._model_path, trust_remote_code=True).quantize(4).cuda()
        self._model = self._model.eval()
    
    def read_md(self, md, hist=[]):
        md_read = '请你阅读并理解下面给出的markdown文章：\n'
        return self._model.chat(self._tokenizer, md_read + md, history = hist)
    
    def extract_title(self, md, hist=[]):
        if len(hist) == 0:
            _, hist = self.read_md(md)
        
        demand = "针对上面的markdown文章提取1个不超过50字的中文标题："
        response, H = self._model.chat(self._tokenizer, demand, history=hist)
        return response.split(","), H
    
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
    
    #region setter&getter
    @property
    def model_path(self):
        return self._model_path

    @model_path.setter
    def model_path(self, value):
        self._model_path = value    
    #endregion setter&getter