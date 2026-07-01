"""
Главный модуль FastAPI: роутеры, шаблоны, статика.
"""

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path

from app.config import settings
from app.routers import permits, references, violations, dashboard, export

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=settings.APP_DESCRIPTION,
)

static_path = Path(__file__).parent.parent / "static"
app.mount("/static", StaticFiles(directory=str(static_path)), name="static")

templates_path = Path(__file__).parent / "templates"
templates = Jinja2Templates(directory=str(templates_path))

app.include_router(permits.router, prefix="/api/permits", tags=["Permits"])
app.include_router(references.router, prefix="/api/references", tags=["References"])
app.include_router(violations.router, prefix="/api/violations", tags=["Violations"])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["Dashboard"])
app.include_router(export.router, prefix="/api/export", tags=["Export"])


@app.get("/")
def page_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/permits")
def page_permits(request: Request):
    return templates.TemplateResponse("permits.html", {"request": request})


@app.get("/references")
def page_references(request: Request):
    return templates.TemplateResponse("references.html", {"request": request})


@app.get("/violations")
def page_violations(request: Request):
    return templates.TemplateResponse("violations.html", {"request": request})


@app.get("/health")
def health_check():
    return {"status": "ok", "app": settings.APP_NAME, "version": settings.APP_VERSION}
