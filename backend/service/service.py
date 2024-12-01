import numpy as np

from repository import convert_image_to_base64_url
from repository.Message import Message


def generate_response(conversation: list[Message]) -> list[Message]:
    conversation.append(Message(sender="bot", text="Hello, world!", conversationId=conversation[0].conversationId))
    conversation.append(Message(sender="bot",
                                imageUrl=convert_image_to_base64_url(
                                    (np.random.random((200, 200, 3)) * 255).astype(np.uint8)
                                ),
                                conversationId=conversation[0].conversationId))
    return conversation
