from typing import TYPE_CHECKING, Generator, Sequence

from cardinal import AssistantMessage, BaseCollector, ChatOpenAI, HumanMessage, Template

from ..utils.protocol import History

if TYPE_CHECKING:
    from cardinal import BaseMessage
    

class ChatEngine:
    def __init__(self, engine, name) -> None:
        self.engine = engine
        self.chat_model = None
        self.name = name
        # 可能还未确定database
        try:
            self.collector = BaseCollector[History](storage_name=name)
        except:
            self.collector = None
        self.hello = "您好，有什么我可以帮助您的吗？"
        self.kbqa_template = Template("充分理解以下事实描述：{context}\n\n回答下面的问题：{query}")
        self.window_size = 6
        self.top_k = 2
        self.threshold = 1.0
        self.with_doc = False
        
    def update(self, top_k, threshold, template):
        self.kbqa_template = Template(template)
        self.top_k = top_k
        self.threshold = threshold
        
    def dump_history(self):
        histories = [[message.model_dump()
                    for message in history.messages]
                    for history in self.collector.dump()
                    ]
        return histories
        
    def dump_history_ui(self):
        histories = [
            
        ]
    
    def clear_history(self):
        try:
            self.collector._storage.destroy()
            self.collector = BaseCollector[History](storage_name=self.name)
        except:
            return
            
    def rag_chat(self, messages: Sequence["BaseMessage"], **kwargs) -> Generator[str, None, None]:
        if self.chat_model is None:
            self.chat_model = ChatOpenAI()
        if self.collector is None:
            self.collector = BaseCollector[History](storage_name=self.name)
        messages = messages[-(self.window_size * 2 + 1) :]
        query = messages[-1].content

        documents = self.engine.search(query=query, threshold=self.threshold, top_k=self.top_k)
        if len(documents):
            documents = documents["content"].tolist()
            query = self.kbqa_template.apply(context="\n".join(documents), query=query)

        augmented_messages = messages[:-1] + [HumanMessage(content=query)]
        response = ""
        for new_token in self.chat_model.stream_chat(augmented_messages, **kwargs):
            yield new_token
            response += new_token
        self.collector.collect(History(messages=(augmented_messages + [AssistantMessage(content=response)])))
            
    def ui_chat(self, history, query):
        if self.collector is None:
            self.collector = BaseCollector[History](storage_name=self.name)

        messages = self.collector.dump()[0].messages + [HumanMessage(content=query)]
        history += [[query, ""]]
        for new_token in self.rag_chat(messages=messages):
            history[-1][1] += new_token
            yield history
