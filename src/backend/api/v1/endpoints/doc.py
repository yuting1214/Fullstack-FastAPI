from fastapi import Form, Request, APIRouter
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from src.backend.security.authentication import authenticate_user

router = APIRouter()
templates = Jinja2Templates(directory="src/frontend/login/templates")


@router.get("/login", response_class=HTMLResponse)
async def login_form(request: Request):
    return templates.TemplateResponse(request, "login.html")


@router.post("/login", response_class=HTMLResponse)
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    if authenticate_user(username, password):
        request.session["authenticated"] = True
        return RedirectResponse(url="/docs", status_code=303)
    return templates.TemplateResponse(request, "login.html", {"message": "Invalid credentials"})


@router.get("/logout", response_class=HTMLResponse)
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/login")
