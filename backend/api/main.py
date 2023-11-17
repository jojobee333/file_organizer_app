import asyncio
import uvicorn
import threading
from fastapi import FastAPI
from backend.api.routers import origin_route, target_route, format_route, move_route
from backend.schemas import async_create_classes
from constants import HOST, PORT

# uvicorn backend.api.main:app --reload

app = FastAPI()
app.include_router(origin_route.router)
app.include_router(target_route.router)
app.include_router(format_route.router)
app.include_router(move_route.router)


def start_backend():
    asyncio.run(async_create_classes())
    uvicorn.run("backend.api.main:app", host=HOST, port=PORT, reload=False)
