from uuid import UUID
from pydantic import BaseModel, ConfigDict


class MessageBase(BaseModel):
    content: str


class MessageCreate(MessageBase):
    pass


class MessageSchema(MessageBase):
    id: UUID

    model_config = ConfigDict(from_attributes=True)
