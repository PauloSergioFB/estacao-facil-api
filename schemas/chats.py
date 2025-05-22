from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from schemas.messages import MessageSchema


class BaseChatSchema(BaseModel):
    code: str
    title: str


class CreateChatSchema(BaseModel):
    title: str
    force_title: Optional[bool] = False


class UpdateChatSchema(CreateChatSchema): ...


class ChatSchema(BaseChatSchema):
    id: int
    creation_date: datetime
    user_id: int


class FullChatSchema(ChatSchema):
    messages: List[MessageSchema]
