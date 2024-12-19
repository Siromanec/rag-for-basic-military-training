import os.path

from repository import convert_image_to_base64_url, read_config_file
from repository.Message import Message
from service.chatbot.chill_chatbot import TextAndImagesChatBot, ChillChatBot


from pathlib import Path
qa: TextAndImagesChatBot | None = None


def init_service() -> None:
    global qa

    files = read_config_file()

    files = [file.strip() for file in files]
    files = [file for file in files if file.endswith(".pdf")]
    files = [Path(os.path.join("data", file)) for file in files]
    qa = ChillChatBot(files)
    print("Service initialized")

init_service()

IMAGE_RESPONSE_TEXT = "Знайдено наступні релевантні зображення:"


def generate_response(conversation: list[Message]) -> list[Message]:
    text, images = qa.answer_query(conversation[-1].text)

    conversation.append(Message(sender="bot", text=text, conversationId=conversation[0].conversationId))
    if len(images) == 0:
        return conversation

    conversation.append(Message(sender="bot", text=IMAGE_RESPONSE_TEXT, conversationId=conversation[0].conversationId))
    for image in images:
        conversation.append(Message(sender="bot", imageUrl=convert_image_to_base64_url(image),
                                    conversationId=conversation[0].conversationId))
    return conversation
