from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.backend.dependencies.database import get_async_db
from src.backend.models import Message
from src.backend.schemas import MessageBase, MessageCreate


class MessageService:
    def __init__(self, db: AsyncSession = Depends(get_async_db)):
        self.db = db

    async def create_message(self, message_data: MessageCreate) -> Message:
        db_message = Message(**message_data.model_dump())
        self.db.add(db_message)
        await self.db.commit()
        await self.db.refresh(db_message)
        return db_message

    async def get_messages(self, skip: int = 0, limit: int = 30) -> list[Message]:
        result = await self.db.execute(select(Message).offset(skip).limit(limit))
        return list(result.scalars().all())

    async def get_message(self, message_id: str) -> Message:
        result = await self.db.execute(select(Message).where(Message.id == str(message_id)))
        db_message = result.scalar_one_or_none()
        if db_message is None:
            raise HTTPException(status_code=404, detail="Message not found")
        return db_message

    async def update_message(self, message_id: str, message_data: MessageBase) -> Message:
        db_message = await self.get_message(message_id)
        for key, value in message_data.model_dump(exclude_unset=True).items():
            setattr(db_message, key, value)
        await self.db.commit()
        await self.db.refresh(db_message)
        return db_message

    async def delete_message(self, message_id: str) -> Message:
        db_message = await self.get_message(message_id)
        await self.db.delete(db_message)
        await self.db.commit()
        return db_message


async def create_message_dict_async(db: AsyncSession, data: dict) -> Message:
    db_data = Message(**data)
    db.add(db_data)
    await db.commit()
    await db.refresh(db_data)
    return db_data
