from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.hotels.router import get_hotels_by_location


router = APIRouter(prefix="/pages", tags=["Фронт"])

templates = Jinja2Templates(directory="app/templates")


@router.get("/hotels")
async def get_hotels_page(request: Request, hotels=Depends(get_hotels_by_location)):
    return templates.TemplateResponse(
        name="hotels.html", context={"request": request, "hotels": hotels}
    )


@router.get("/login", response_class=HTMLResponse)
async def get_login_page(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request})


@router.get("/register", response_class=HTMLResponse)
async def get_register_page(request: Request):
    return templates.TemplateResponse("auth/register.html", {"request": request})
