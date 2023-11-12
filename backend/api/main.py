import flet as ft
import flet_fastapi
import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from flet_core import MainAxisAlignment, FilePickerResultEvent

from backend.api.routers import origin_route, target_route, format_route, move_route
from constants import HOST, PORT

DATABASE_URL = "sqlite+aiosqlite:///mydatabase.db"
SIZE = 15
# uvicorn backend.api.main:app --reload


app = FastAPI()

# add routers.
app.include_router(origin_route.router)
app.include_router(target_route.router)
app.include_router(format_route.router)
app.include_router(move_route.router)

if __name__ == '__main__':
    uvicorn.run("backend.api.main:app", host=HOST, port=PORT, reload=True)