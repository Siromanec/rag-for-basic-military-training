from repository.Message import Message


def generate_response(conversation: list[Message]) -> list[Message]:

    conversation.append(Message(sender="bot", text="Hello, world!", conversationId=conversation[0].conversationId))

    return conversation