import uuid
from sqlalchemy import Uuid, String
from sqlalchemy.orm import Mapped, mapped_column
from src.backend.dependencies.database import Base


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    content: Mapped[str] = mapped_column(String)

    def __repr__(self) -> str:
        return f"<Message(id={self.id}, content={self.content})>"
