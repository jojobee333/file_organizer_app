import uvicorn
from fastapi import FastAPI

from backend.api.routers import origin_route, target_route, format_route, move_route
# from constants import HOST, PORT

# uvicorn backend.api.main:app --reload

app = FastAPI()
app.include_router(origin_route.router)
app.include_router(target_route.router)
app.include_router(format_route.router)
app.include_router(move_route.router)

