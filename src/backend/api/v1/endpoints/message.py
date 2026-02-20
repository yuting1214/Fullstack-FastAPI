from uuid import UUID
from fastapi import status, APIRouter, Depends
from src.backend.crud import MessageService
from src.backend.schemas import MessageBase, MessageCreate, MessageSchema

router = APIRouter()


@router.post("/messages/", response_model=MessageSchema, status_code=status.HTTP_201_CREATED)
async def create_message(message_data: MessageCreate, service: MessageService = Depends()):
    return await service.create_message(message_data)


@router.get("/messages/", response_model=list[MessageSchema], status_code=status.HTTP_200_OK)
async def get_messages(skip: int = 0, limit: int = 30, service: MessageService = Depends()):
    return await service.get_messages(skip, limit)


@router.get("/messages/{message_id}", response_model=MessageSchema, status_code=status.HTTP_200_OK)
async def get_message(message_id: UUID, service: MessageService = Depends()):
    return await service.get_message(message_id)


@router.put("/messages/{message_id}", response_model=MessageSchema, status_code=status.HTTP_200_OK)
async def update_message(message_id: UUID, message_data: MessageBase, service: MessageService = Depends()):
    return await service.update_message(message_id, message_data)


@router.delete("/messages/{message_id}", response_model=MessageSchema, status_code=status.HTTP_200_OK)
async def delete_message(message_id: UUID, service: MessageService = Depends()):
    return await service.delete_message(message_id)
