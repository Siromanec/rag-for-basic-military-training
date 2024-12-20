from contextlib import asynccontextmanager
from typing import Annotated

import fastapi
from pydantic import AfterValidator

from service import *

# import service.service import init_service
from repository.Message import Message


@asynccontextmanager
async def lifespan(router: fastapi.APIRouter):
    # init_service()
    init_service()
    yield

router = fastapi.APIRouter(lifespan=lifespan)


def validate_conversation(conversation: list[Message]) -> list[Message]:
    if len(conversation) == 0:
        raise fastapi.HTTPException(status_code=422, detail={
            "loc": ["conversation"],
            "msg": "Conversation must have at least one message",
            "type": "value_error"
        })
    if conversation[-1].sender != "user":
        raise fastapi.HTTPException(status_code=422, detail={
            "loc": [len(conversation) - 1],
            "msg": "Last message must be sent by user",
            "type": "value_error"
        })

    conversation_id = conversation[0].conversationId
    for i, message in enumerate(conversation):
        if message.conversationId != conversation_id:
            raise fastapi.HTTPException(status_code=422, detail={
                "loc": [i],
                "msg": "All messages must belong to the same conversation",
                "type": "value_error"
            })

        if (message.text is None and message.imageUrl is None) or (
                message.text is not None and message.imageUrl is not None):
            raise fastapi.HTTPException(status_code=422, detail={
                "loc": [i],
                "msg": "Message must have either text or imageUrl",
                "type": "value_error"
            })

    return conversation


@router.post("/generate-response")
def generate_response(conversation: Annotated[list[Message], AfterValidator(validate_conversation)]) -> list[Message]:
    conversation = service.generate_response(conversation)
    return conversation
