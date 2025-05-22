import json
import re

from ibm_watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

from database import chats, messages
from .response_handlers import RESPONSE_HANDLERS
from settings import Settings


settings = Settings()


def get_watson_assistant():
    authenticator = IAMAuthenticator(settings.WATSON_API_KEY)

    assistant = AssistantV2(version="2024-08-25", authenticator=authenticator)
    assistant.set_service_url(settings.WATSON_URL)

    return assistant


def send_message_watson(con, assistant, message, context):
    response = assistant.message_stateless(
        environment_id="default",
        assistant_id=settings.WATSON_ASSISTANT_ID,
        context=context,
        input={"message_type": "text", "text": message},
    ).get_result()

    text_response = response["output"]["generic"][0]["text"]
    if "$%" in text_response:
        match = re.search(
            r"\$%([a-zA-Z_][a-zA-Z0-9_]*)\$%(.*)", text_response, re.DOTALL
        )

        handler_key = match.group(1).strip()
        raw_values = match.group(2).strip()

        values = json.loads(raw_values)

        text_response = RESPONSE_HANDLERS[handler_key](con, values)

    return {"content": text_response, "context": response["context"]}


def send_stateless_message(con, message_content, message_context):
    assistant = get_watson_assistant()
    response = send_message_watson(con, assistant, message_content, message_context)

    return {
        "content": message_content,
        "reply": response["content"],
        "context": response["context"],
    }


def send_message(con, message_content, chat):
    assistant = get_watson_assistant()
    response = send_message_watson(con, assistant, message_content, chat["context"])

    db_message = messages.insert_message(
        con,
        {
            "chat_id": chat["id"],
            "content": message_content,
            "reply": response["content"],
        },
    )

    chat["context"] = response["context"]
    chats.update_chat(con, chat["id"], chat)

    return db_message
