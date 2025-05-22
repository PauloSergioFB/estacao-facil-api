import database.core as db
from serializers.messages import message_serializer


def get_message_by_id(con, id):
    stmt = """
    SELECT 
        message_id,
        send_date,
        message_content,
        message_reply,
        chat_id
    FROM
        ef_message
    WHERE
        message_id = :message_id
    """
    return db.select_one(
        con, stmt, values={"message_id": id}, serializer=message_serializer
    )


def get_messages_by_chat_id(con, chat_id):
    stmt = """
    SELECT
        message_id,
        send_date,
        message_content,
        message_reply,
        chat_id
    FROM
        ef_message
    WHERE
        chat_id = :chat_id
    ORDER BY
        send_date
    """
    return db.select_all(
        con,
        stmt,
        values={"chat_id": chat_id},
        serializer=message_serializer,
    )


def insert_message(con, message):
    message_id = db.insert(
        con,
        "ef_message",
        {
            "message_content": message["content"],
            "message_reply": message["reply"],
            "chat_id": message["chat_id"],
        },
        id_key="message_id",
    )
    return get_message_by_id(con, message_id)
