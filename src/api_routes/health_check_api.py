from fastapi import APIRouter

health_check_router = APIRouter()

@health_check_router.get("/health")
def health_check():
    return {"status": "ok"}
