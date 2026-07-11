from fastapi import Form, Request, APIRouter
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi.templating import Jinja2Templates
from src.backend.security.authentication import authenticate_user

router = APIRouter()
templates = Jinja2Templates(directory="src/frontend/login/templates")


def _is_htmx(request: Request) -> bool:
    return request.headers.get("hx-request") == "true"


@router.get("/login", response_class=HTMLResponse)
async def login_form(request: Request):
    return templates.TemplateResponse(request, "login.html")


@router.post("/login", response_class=HTMLResponse)
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    if authenticate_user(username, password):
        request.session["authenticated"] = True
        if _is_htmx(request):
            # htmx submits via fetch; a 303 would be swapped inline instead
            # of navigating, so instruct a client-side redirect.
            return Response(status_code=200, headers={"HX-Redirect": "/docs"})
        return RedirectResponse(url="/docs", status_code=303)
    context = {"message": "Invalid credentials"}
    if _is_htmx(request):
        # Swap only the card (hx-target="#login-card"), not the full page.
        return templates.TemplateResponse(request, "_login_card.html", context)
    return templates.TemplateResponse(request, "login.html", context)


@router.get("/logout", response_class=HTMLResponse)
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/login")
