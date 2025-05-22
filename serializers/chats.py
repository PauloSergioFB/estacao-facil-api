import json


def chat_serializer(values):
    chat_id, chat_code, user_id, chat_title, creation_date, chat_context = values
    if chat_context:
        chat_context = json.loads(chat_context.read())

    return {
        "id": chat_id,
        "code": chat_code,
        "user_id": user_id,
        "title": chat_title,
        "creation_date": creation_date,
        "context": chat_context,
    }


def public_chat_serializer(values):
    return dict(zip(["id", "code", "user_id", "title", "creation_date"], values))


def chat_conflict_serializer(values):
    return dict(zip(["id", "title", "user_id"], values))
