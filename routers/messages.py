from http import HTTPStatus
from oracledb import Connection
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from database import chats
from database.core import get_connection
from schemas.messages import (
    MessageSchema,
    SendMessageSchema,
    SendStatelessMessageSchema,
    StatelessMessageSchema,
)
from services.security import get_current_user
from services import watson


router = APIRouter(prefix="/messages", tags=["messages"])

DBConnection = Annotated[Connection, Depends(get_connection)]
CurrentUser = Annotated[dict, Depends(get_current_user)]


@router.post("/", response_model=StatelessMessageSchema)
def send_message(message: SendStatelessMessageSchema, con: DBConnection):
    message = message.model_dump()
    return watson.send_stateless_message(
        con, message["content"], message.get("context", None)
    )


@router.post("/{chat_code}", response_model=MessageSchema, status_code=201)
def send_logged_message(
    chat_code: str,
    message: SendMessageSchema,
    con: DBConnection,
    current_user: CurrentUser,
):
    chat = chats.get_chat_by_code(con, chat_code)
    if not chat:
        raise "Chat not found"

    if current_user["id"] != chat["user_id"]:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail="Not enough permission"
        )

    message = message.model_dump()
    return watson.send_message(con, message["content"], chat)
