import logging

from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from backend.api.routers import handle_db_session_exception
from backend.api.routers.base_route import BaseRoute
from backend.schemas import Target, async_session

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s | %(levelname)s | %(funcName)s : %(message)s")
logger = logging.getLogger(__name__)
router = APIRouter(tags=["Targets"], prefix="/targets")

base_route = BaseRoute()


@router.get("/")
async def get_all_targets():
    """Retrieves all saved target folders."""
    # OK
    try:
        async with async_session() as session:
            async with session.begin():
                targets = await base_route.get_all(session, Target)
                return {"results": targets}
    except SQLAlchemyError as e:
        handle_db_session_exception(e)


@router.post("/")
async def add_new_target(name: str, path: str):
    """Saves an target folder to database."""
    # OK
    try:
        async with async_session() as session:
                result = await base_route.add_new(session, Target, name=name, path=path)
                return {"code": 200, "message": "Target added successfully", "id": result.id}
    except SQLAlchemyError as e:
        handle_db_session_exception(e)


@router.get("/{target_id:int}/items")
async def get_folder_items(target_id: int):
    """Retrieves all items from a specified folder based on id."""
    # OK
    try:
        async with async_session() as session:
            async with session.begin():
                results = await base_route.get_items(session, Target, target_id)
                return results
    except OSError as e:
        logger.error(f"OS error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{target_id:int}")
async def get_target_by_id(target_id: int):
    """Gets a target from the database."""
    # OK
    try:
        async with async_session() as session:
            async with session.begin():
                return await base_route.get_by_id(session, Target, target_id)
    except SQLAlchemyError as e:
        handle_db_session_exception(e)


@router.get("/{target_name}")
async def get_target_by_name(target_name: str):
    try:
        async with async_session() as session:
            async with session.begin():
                return await base_route.get_by_name(session=session, model=Target, name=target_name)
    except SQLAlchemyError as e:
        handle_db_session_exception(e)


@router.patch("/{target_id:int}")
async def update_target(target_id: int, name=None, path=None):
    # OK
    try:
        async with async_session() as session:
            async with session.begin():
                if name is None or path is None:
                    current_target = await get_target_by_id(target_id)
                if name is None:
                    name = current_target.name
                if path is None:
                    path = current_target.path
                return await base_route.update(session, Target, target_id, name=name, path=path)
    except SQLAlchemyError as e:
        handle_db_session_exception(e)


@router.delete("/{target_id:int}")
async def delete_target(target_id: int):
    """Delete a target folder from database."""
    try:
        async with async_session() as session:
            async with session.begin():
                await base_route.delete(session, Target, target_id)
                return {"code": 200, "message": "Target deleted successfully"}
    except SQLAlchemyError as e:
        handle_db_session_exception(e)
