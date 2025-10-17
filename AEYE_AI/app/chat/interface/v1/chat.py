from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from AEYE_langchain.application.search import AEYE_langchain_search

templates = Jinja2Templates(directory="AEYE_langchain/interface/v1/")

router = APIRouter()




@router.get("/chat", response_class=HTMLResponse)
async def get_chat_page(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request, "chat_history": []})


@router.post("/chat", response_class=HTMLResponse)
async def post_chat(request: Request, user_input: str = Form(...)):
    langchain = AEYE_langchain_search.get_instance()

    response = langchain.search(user_input)
    return templates.TemplateResponse(
        "chat.html",
        {"request": request, "user_input": user_input, "response": response}
    )