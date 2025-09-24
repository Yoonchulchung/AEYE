from fastapi import APIRouter, Request

router = APIRouter()

@router.post("/upload")
async def upload(requests : Request):
    ...