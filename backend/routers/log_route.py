import logging
from fastapi import APIRouter
from sqlalchemy.exc import SQLAlchemyError
from backend.routers import handle_db_session_exception
from backend.routers.base_route import BaseRoute
from backend.schemas import async_session, Log
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s | %(levelname)s | %(funcName)s : %(message)s")
logger = logging.getLogger(__name__)

router = APIRouter(tags=["Logs"], prefix="/logs")

base_route = BaseRoute()


@router.get("/")
async def get_all_logs():
    """Retrieves all saved target folders."""
    # OK
    try:
        async with async_session() as session:
            async with session.begin():
                logs = await base_route.get_all(session, Log)
                return {"results": logs}
    except SQLAlchemyError as e:
        handle_db_session_exception(e)


@router.get("/{log_id:int}")
async def get_log_by_id(log_id: int):
    """Gets a target from the database."""
    # OK
    try:
        async with async_session() as session:
            async with session.begin():
                return await base_route.get_by_id(session, Log, log_id)
    except SQLAlchemyError as e:
        handle_db_session_exception(e)


@router.post("/")
async def add_new_log(origin_name: str, files_moved: int):
    try:
        async with async_session() as session:
            result = await base_route.add_new(session, Log, origin_name=origin_name, files_moved=files_moved)
            return {"code": 200, "message": "Target added successfully", "id": result.id}
    except SQLAlchemyError as e:
        handle_db_session_exception(e)


@router.delete("/{log_id:int}")
async def delete_log(log_id: int):
    """Delete a log from database."""
    try:
        async with async_session() as session:
            async with session.begin():
                await base_route.delete(session, Log, log_id)
                return {"code": 200, "message": "Log deleted successfully"}
    except SQLAlchemyError as e:
        handle_db_session_exception(e)

