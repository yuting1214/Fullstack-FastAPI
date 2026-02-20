from pydantic import BaseModel, ConfigDict


class MessageBase(BaseModel):
    content: str


class MessageCreate(MessageBase):
    pass


class MessageSchema(MessageBase):
    id: str

    model_config = ConfigDict(from_attributes=True)
