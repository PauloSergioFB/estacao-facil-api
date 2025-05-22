import json
import uuid

import database.core as db
from serializers.chats import (
    chat_conflict_serializer,
    chat_serializer,
    public_chat_serializer,
)


class ChatTitleAlreadyExists(Exception):
    def __init__(self, message: str):
        super().__init__(message)


def get_chat_by_id(con, id):
    stmt = """
    SELECT
        chat_id,
        chat_code,
        user_id,
        chat_title,
        creation_date,
        chat_context
    FROM
        ef_chat
    WHERE
        chat_id = :chat_id
    """
    return db.select_one(
        con,
        stmt,
        values={"chat_id": id},
        serializer=chat_serializer,
    )


def get_chat_by_code(con, code):
    stmt = """
    SELECT
        chat_id,
        chat_code,
        user_id,
        chat_title,
        creation_date,
        chat_context
    FROM
        ef_chat
    WHERE
        chat_code = :chat_code
    """
    return db.select_one(
        con,
        stmt,
        values={"chat_code": code},
        serializer=chat_serializer,
    )


def get_chats_by_user_id(con, user_id):
    stmt = """
    SELECT
        chat_id,
        chat_code,
        user_id,
        chat_title,
        creation_date
    FROM
        ef_chat
    WHERE
        user_id = :user_id
    ORDER BY
        creation_date DESC
    """
    return db.select_all(
        con,
        stmt,
        values={"user_id": user_id},
        serializer=public_chat_serializer,
    )


def check_chat_conflict(con, user_id, chat_title):
    stmt = """
    SELECT
        chat_id,
        chat_title,
        user_id
    FROM
        ef_chat
    WHERE
        user_id = :user_id
        AND chat_title = :chat_title
    """
    chat = db.select_one(
        con,
        stmt,
        values={"user_id": user_id, "chat_title": chat_title},
        serializer=chat_conflict_serializer,
    )

    if not chat:
        return

    if chat:
        raise ChatTitleAlreadyExists("Chat title already exists")


def check_update_chat_conflict(con, user_id, chat_id, chat_title):
    stmt = """
    SELECT
        chat_id,
        chat_title,
        user_id
    FROM
        ef_chat
    WHERE
        user_id = :user_id
        AND chat_title = :chat_title
        AND chat_id != :chat_id
    """
    chat = db.select_one(
        con,
        stmt,
        values={"chat_id": chat_id, "user_id": user_id, "chat_title": chat_title},
        serializer=chat_conflict_serializer,
    )

    if not chat:
        return

    if chat:
        raise ChatTitleAlreadyExists("Chat title already exists")


def insert_chat(con, chat):
    check_chat_conflict(con, chat["user_id"], chat["title"])

    chat_code = uuid.uuid4().hex[:20]
    chat_id = db.insert(
        con,
        "ef_chat",
        {
            "chat_code": chat_code,
            "user_id": chat["user_id"],
            "chat_title": chat["title"],
        },
        id_key="chat_id",
    )
    return get_chat_by_id(con, chat_id)


def update_chat(con, id, chat):
    check_update_chat_conflict(con, chat["user_id"], id, chat["title"])

    if chat["context"]:
        chat["context"] = json.dumps(chat["context"])

    db.update(
        con,
        id,
        "ef_chat",
        {
            "chat_code": chat["code"],
            "user_id": chat["user_id"],
            "chat_title": chat["title"],
            "chat_context": chat["context"],
        },
        id_key="chat_id",
    )
    return get_chat_by_id(con, id)


def delete_chat(con, chat_id):
    db.delete(con, chat_id, "ef_message", id_key="chat_id")
    db.delete(con, chat_id, "ef_chat", id_key="chat_id")
