import asyncio
import uvicorn
from fastapi import FastAPI
from backend.routers import origin_route, target_route, format_route, log_route, run_route
from backend.schemas import async_create_classes
from constants import HOST, PORT

app = FastAPI()
app.include_router(origin_route.router)
app.include_router(target_route.router)
app.include_router(format_route.router)
app.include_router(log_route.router)
app.include_router(run_route.router)


def start_backend():
    asyncio.run(async_create_classes())
    uvicorn.run("backend.api_init:app", host=HOST, port=PORT, reload=False)
