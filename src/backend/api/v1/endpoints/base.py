from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def onboard_message():
    return {"message": "You've been onboarded!"}


@router.get("/health")
async def health():
    """Liveness probe for platform healthchecks (Railway, k8s, etc.)."""
    return {"status": "ok"}
