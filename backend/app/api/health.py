from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def check_health() -> dict:
    return {"status": "ok"}
