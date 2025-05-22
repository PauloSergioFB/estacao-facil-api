from http import HTTPStatus
from oracledb import Connection
from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException

from database import chats
from database import messages
from database.core import get_connection
from schemas.chats import CreateChatSchema, ChatSchema, FullChatSchema, UpdateChatSchema
from services.security import get_current_user


router = APIRouter(prefix="/chats", tags=["chats"])

DBConnection = Annotated[Connection, Depends(get_connection)]
CurrentUser = Annotated[dict, Depends(get_current_user)]


@router.get("/", response_model=List[ChatSchema])
def get_chats(con: DBConnection, current_user: CurrentUser):
    return chats.get_chats_by_user_id(con, current_user["id"])


@router.get("/{chat_code}", response_model=FullChatSchema)
def get_chat(chat_code: str, con: DBConnection, current_user: CurrentUser):
    chat = chats.get_chat_by_code(con, chat_code)
    if not chat:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Chat not found")

    if current_user["id"] != chat["user_id"]:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail="Not enough permission"
        )

    chat["messages"] = messages.get_messages_by_chat_id(con, chat["id"])

    return chat


@router.post("/", response_model=ChatSchema, status_code=201)
def create_chat(chat: CreateChatSchema, con: DBConnection, current_user: CurrentUser):
    chat = chat.model_dump()
    force_title = chat.pop("force_title")
    chat["user_id"] = current_user["id"]

    i = 1
    original_title = chat["title"]
    while True:
        try:
            return chats.insert_chat(con, chat)
        except chats.ChatTitleAlreadyExists as e:
            if not force_title:
                raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(e))

            chat["title"] = f"{original_title} {i}"
            i += 1


@router.put("/{chat_code}", response_model=ChatSchema)
def update_chat(
    chat_code: str, chat: UpdateChatSchema, con: DBConnection, current_user: CurrentUser
):
    db_chat = chats.get_chat_by_code(con, chat_code)
    if not db_chat:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Chat not found")

    if current_user["id"] != db_chat["user_id"]:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail="Not enough permission"
        )

    try:
        db_chat["title"] = chat.title
        return chats.update_chat(con, db_chat["id"], db_chat)
    except chats.ChatTitleAlreadyExists as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(e))


@router.delete("/{chat_code}", status_code=204)
def delete_chat(chat_code: str, con: DBConnection, current_user: CurrentUser):
    chat = chats.get_chat_by_code(con, chat_code)
    if not chat:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Chat not found")

    if current_user["id"] != chat["user_id"]:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail="Not enough permission"
        )

    chats.delete_chat(con, chat["id"])
