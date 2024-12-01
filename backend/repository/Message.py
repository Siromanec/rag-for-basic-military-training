from typing import Literal, Optional

from pydantic import BaseModel


class Message(BaseModel):
    sender: Literal["user", "bot"]
    text: Optional[str] = None
    imageUrl: Optional[str] = None
    conversationId: str
