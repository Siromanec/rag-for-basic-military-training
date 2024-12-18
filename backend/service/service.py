import numpy as np

from repository import convert_image_to_base64_url
from repository.Message import Message
from repository.abstract_chatbot import TextAndImagesChatBot

qa: TextAndImagesChatBot = TextAndImagesChatBot()

IMAGE_RESPONSE_TEXT = "Знайдено наступні релевантні зображення:"

def generate_response(conversation: list[Message]) -> list[Message]:
    text, images = qa.answer_query(conversation[-1].text)

    conversation.append(Message(sender="bot", text=text, conversationId=conversation[0].conversationId))
    if len(images) == 0:
        return conversation

    conversation.append(Message(sender="bot", text=IMAGE_RESPONSE_TEXT, conversationId=conversation[0].conversationId))
    for image in images:
        conversation.append(Message(sender="bot", imageUrl=convert_image_to_base64_url(image), conversationId=conversation[0].conversationId))
    return conversation
