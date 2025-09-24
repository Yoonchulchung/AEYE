from fastapi import APIRouter, Request


router = APIRouter()

@router.get("/health")
def aeye_health(request : Request) :

    return {"status" : "Good"}
