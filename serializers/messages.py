def message_serializer(values):
    message_id, send_date, message_content, message_reply, chat_id = values
    return {
        "id": message_id,
        "send_date": send_date,
        "content": message_content.read(),
        "reply": message_reply.read(),
        "chat_id": chat_id,
    }
