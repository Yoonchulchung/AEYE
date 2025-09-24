from fastapi import APIRouter, Request

router = APIRouter()

@router.get("/result")
async def result(request : Request):
    ...
