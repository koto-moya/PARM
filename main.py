from fastapi import FastAPI, Request, Response
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from config import limiter
from routers import items, system_status, user_management

app = FastAPI(docs_url=None, redoc_url="/docs", openapi_url="/api/openapi.json")
templates = Jinja2Templates(directory="templates")

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.include_router(items.router)
app.include_router(system_status.router)
app.include_router(user_management.router)

app.mount("/assets", StaticFiles(directory="assets"), name="assets")

app.mount("/styling", StaticFiles(directory="styling"), name="styling")

@app.get("/")
def landing_page(request: Request, response: Response):
    response = templates.TemplateResponse("landing_page.html", {"request": request})
    response.delete_cookie(key="access_token",  path="/")
    return response