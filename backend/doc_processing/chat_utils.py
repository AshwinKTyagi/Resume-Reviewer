from typing import List
from pydantic import BaseModel

class Message(BaseModel):
    type: str 
    text: str

class ChatSession(BaseModel):
    messages: List[Message]
    resume: str
    feedback: str