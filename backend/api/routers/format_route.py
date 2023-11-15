import json
import logging
from fastapi import APIRouter
from sqlalchemy.exc import SQLAlchemyError
from backend.api.routers import handle_db_session_exception
from backend.api.routers.base_route import BaseRoute
from backend.schemas import Format
from backend.schemas import async_session

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s | %(levelname)s | %(funcName)s : %(message)s")
logger = logging.getLogger(__name__)
router = APIRouter(tags=["Formats"], prefix="/formats")

base_route = BaseRoute()


@router.get("/")
async def get_all_formats():
    """Retrieves all saved formats."""
    # OK
    try:
        async with async_session() as session:
            formats = await base_route.get_all(session, Format)
            return {"results": formats}
    except SQLAlchemyError as e:
        handle_db_session_exception(e)


@router.post("/")
async def add_new_format(name: str, target_id):
    """Saves a format to database."""
    # OK
    try:
        async with async_session() as session:
            result = await base_route.add_new(session, Format, name=name, target_id=target_id)
            return {"code": 200, "message": "Format added successfully", "id": result.id}
    except SQLAlchemyError as e:
        handle_db_session_exception(e)


@router.get("/{format_id}")
async def get_format_by_id(format_id: int):
    """Gets a format from the database."""
    # OK
    try:
        async with async_session() as session:
            async with session.begin():
                return await base_route.get_by_id(session, Format, format_id)
    except SQLAlchemyError as e:
        handle_db_session_exception(e)


@router.patch("/{format_id}")
async def update_format(format_id: int, name=None, target_id=None):
    # OK
    try:
        async with async_session() as session:
            if name is None or target_id is None:
                current_format = await get_format_by_id(format_id)
                if name is None:
                    name = current_format.name
                if target_id is None:
                    target_id = current_format.target_id

            updated_format = await base_route.update(session, Format, format_id, name=name, target_id=target_id)
            return {"code": 200, "message": "Format updated successfully", "format": updated_format}

    except SQLAlchemyError as e:
        handle_db_session_exception(e)


@router.delete("/{format_id}")
async def delete_format(format_id: int):
    """Delete a format from database."""
    # OK
    try:
        with async_session() as session:
            await base_route.delete(session, Format, format_id)
            return {"code": 200, "message": "Format deleted successfully"}
    except SQLAlchemyError as e:
        handle_db_session_exception(e)
