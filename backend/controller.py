import fastapi

import service.service
from repository.Message import Message

router = fastapi.APIRouter()

@router.post("/generate-response")
def generate_response(conversation: list[Message]) -> list[Message]:
    conversation = service.service.generate_response(conversation)
    return conversation

