from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.routes.user_routes import router as user_router

app = FastAPI(title="User Management API", description="API для управления пользователями", version="1.0.0")

app.include_router(user_router, tags=["Users"])

@app.get("/", summary="Главная ручка", tags=["Основные ручки"])
async def read_root():
    return "Welcome!"

app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("static/favicon.ico")