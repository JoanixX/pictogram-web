from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class ChatMessageBase(BaseModel):
    sender: str
    content: str


class ChatMessageCreate(ChatMessageBase):
    conversation_id: int


class ChatMessageOut(ChatMessageBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class ConversationCreate(BaseModel):
    user_id: int
    title: Optional[str] = None


class ConversationOut(BaseModel):
    id: int
    user_id: int
    title: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True


class ConversationDetail(ConversationOut):
    messages: List[ChatMessageOut] = []
