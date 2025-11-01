from fastapi import APIRouter, Request

router = APIRouter()

router.post("/insert")
async def insert(reqeust : Request):
    
    