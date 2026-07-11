import uuid

from sqlalchemy import Uuid, String
from sqlalchemy.orm import Mapped, mapped_column
from uuid_utils.compat import uuid7

from src.backend.dependencies.database import Base


class Message(Base):
    __tablename__ = "messages"

    # Time-ordered UUIDv7 keys insert at the right edge of the B-tree
    # (sequential-like locality) while staying generate-anywhere unique.
    # Generated client-side so it works on both SQLite (dev) and
    # PostgreSQL (prod). On PostgreSQL 18+ you can instead use the native
    # server default: mapped_column(server_default=func.uuidv7()).
    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid7)
    content: Mapped[str] = mapped_column(String)

    def __repr__(self) -> str:
        return f"<Message(id={self.id}, content={self.content})>"
