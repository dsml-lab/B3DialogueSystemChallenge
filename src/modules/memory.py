from langchain.schema import (SystemMessage, HumanMessage, AIMessage)

def to_message(role:str="human", content:str='hello'):
    if role == "system":
        return SystemMessage(content=content)
    elif role == "human":
        return HumanMessage(content=content)
    elif role == "AI":
        return AIMessage(content=content)
class Memory:
    def __init__(self):
        self.messages = []
    #対話履歴を保存する関数
    def add(self,role:str, content:str):
        self.messages.append(to_message(role, content))
        return self.messages
