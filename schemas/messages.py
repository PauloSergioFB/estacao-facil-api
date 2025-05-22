from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel


class BaseMessageSchema(BaseModel):
    id: int
    send_date: datetime
    content: str
    reply: str
    chat_id: int


class SendMessageSchema(BaseModel):
    content: str


class MessageSchema(BaseMessageSchema): ...


class SendStatelessMessageSchema(BaseModel):
    content: str
    context: Optional[dict[str, Any]] = None


class StatelessMessageSchema(BaseModel):
    content: str
    reply: str
    context: dict[str, Any]
