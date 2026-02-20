from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def onboard_message():
    return {"message": "You've been onboarded!"}
