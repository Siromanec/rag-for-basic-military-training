import numpy as np

from repository import convert_image_to_base64_url
from repository.Message import Message


def generate_response(conversation: list[Message]) -> list[Message]:
    text = qa.run_text(conversation[-1].text)
    image = qa.run_image(conversation[-1])
    image = convert_image_to_base64_url(image)
    conversation.append(Message(sender="bot", text=text, imageUrl=image, conversationId=conversation[0].conversationId))
    return conversation
