from typing import Generator

from cardinal import AssistantMessage, BaseCollector, ChatOpenAI, HumanMessage, Template

from .protocol import History


class ChatEngine:
    def __init__(self, engine) -> None:
        self._chat_model = None
        self._collector = None
        self._kbqa_template = Template("充分理解以下事实描述：{context}\n\n回答下面的问题：{query}")
        self.engine = engine
        
    def get_history(self):
        ret = [[None, "您好，有什么我可以帮助您的吗？"]]
        if self._collector is None:
            return ret
        histories = self._collector.dump()
        if not len(histories):
            return ret
        for history in histories:
            messages = [message.content for message in history.messages]
            ret.append(messages)
        return ret
    
    def clear_history(self):
        try:
            self._collector._storage.destroy()
            self._collector = BaseCollector[History](storage_name=self._storage_name)
        except:
            return
    
    def stream_chat(self, history, query, threshold, top_k, template, **kwargs) -> Generator[str, None, None]:
        if self._chat_model is None:
            try:
                self._chat_model = ChatOpenAI()
            except:
                import gradio as gr
                raise gr.Error("Cannot connect to openai, please check your url and api_key")
        if self._collector is None:
            self._collector = BaseCollector[History](storage_name=self._storage_name)
        search_result = self.engine.search(query, threshold=threshold, top_k=top_k)
        if any(search_result):
            documents = search_result["content"].tolist()
            query = Template(str(template)).apply(context="\n".join(documents), query=query)

        augmented_messages = [HumanMessage(content=query)]
        history += [[query, None]]
        history[-1][1] = ""
        for new_token in self._chat_model.stream_chat(augmented_messages, **kwargs):
            history[-1][1] += new_token
            yield history
        self._collector.collect(History(messages=(augmented_messages + [AssistantMessage(content=history[-1][1])])))
