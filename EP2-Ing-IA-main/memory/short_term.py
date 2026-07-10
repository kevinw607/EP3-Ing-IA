from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.messages import BaseMessage
from typing import List

class ShortTermMemory:

    def __init__(self):
        self.history = ChatMessageHistory()

    def get_messages(self) -> List[BaseMessage]:
        return self.history.messages

    def add_user_message(self, message: str) -> None:
        self.history.add_user_message(message)

    def add_message(self, message: BaseMessage) -> None:
        self.history.add_message(message)

    def clear(self) -> None:
        self.history.clear()