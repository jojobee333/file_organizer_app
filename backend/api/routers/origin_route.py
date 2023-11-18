import logging
import os

from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from backend.api.routers import handle_db_session_exception
from backend.api.routers.base_route import BaseRoute
from backend.schemas import Origin, async_session

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s | %(levelname)s | %(funcName)s : %(message)s")
logger = logging.getLogger(__name__)
router = APIRouter(tags=["Origins"], prefix="/origins")

base_route = BaseRoute()


@router.get("/")
async def get_all_origins():
    """Retrieves all saved origin folders."""
    try:
        async with async_session() as session:
            origins = await base_route.get_all(session, Origin)
            return {"results": origins}
    except SQLAlchemyError as e:
        handle_db_session_exception(e)


@router.post("/")
async def add_new_origin(path: str):
    """Saves an origin folder to database."""
    # OK
    try:
        async with async_session() as session:
            result = await base_route.add_new(session, Origin, path=path)
            return {"code": 200,
                    "message": "Origin added successfully",
                    "id": result.id, "path": result.path}
    except SQLAlchemyError as e:
        handle_db_session_exception(e)


@router.get("/{origin_id:int}/items")
async def get_folder_items(origin_id: int):
    """Retrieves all items from a specified folder based on id."""
    # OK
    try:
        async with async_session() as session:
            results = await base_route.get_items(session, Origin, origin_id)
            return results
    except OSError as e:
        logger.error(f"OS error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{origin_id:int}")
async def get_origin_by_id(origin_id: int):
    """Gets an origin folder from the database."""
    # OK
    try:
        async with async_session() as session:
            async with session.begin():
                return await base_route.get_by_id(session, Origin, origin_id)
    except SQLAlchemyError as e:
        handle_db_session_exception(e)


@router.get("/{origin_path}")
async def get_origin_by_path(origin_path: str):
    try:
        async with async_session() as session:
            async with session.begin():
                return await base_route.get_by_path(session, Origin, origin_path)
    except SQLAlchemyError as e:
        handle_db_session_exception(e)


@router.delete("/{origin_id:int}")
async def delete_origin(origin_id: int):
    """Delete an origin folder from database."""
    try:
        async with async_session() as session:
            async with session.begin():
                await base_route.delete(session, Origin, origin_id)
                return {"code": 200, "message": "Origin deleted successfully"}
    except SQLAlchemyError as e:
        handle_db_session_exception(e)
