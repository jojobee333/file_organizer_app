import logging

from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from backend.api.routers import handle_db_session_exception
from backend.api.routers.base_route import BaseRoute
from backend.schemas import Target, Session

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s | %(levelname)s | %(funcName)s : %(message)s")
logger = logging.getLogger(__name__)
router = APIRouter(tags=["Targets"], prefix="/targets")

base_route = BaseRoute()


@router.get("/")
def get_all_targets():
    """Retrieves all saved target folders."""
    # OK
    try:
        with Session() as session:
            return {"results": base_route.get_all(session, Target)}
    except SQLAlchemyError as e:
        handle_db_session_exception(e)


@router.post("/")
def add_new_target(name: str, path: str):
    """Saves an target folder to database."""
    # OK
    try:
        with Session() as session:
            result = base_route.add_new(session, Target, name=name, path=path)
            return {"code": 200, "message": "Target added successfully", "id": result.id}
    except SQLAlchemyError as e:
        handle_db_session_exception(e)


@router.get("/{origin_id}/items")
def get_folder_items(target_id: int):
    """Retrieves all items from a specified folder based on id."""
    # OK
    try:
        with Session() as session:
            results = base_route.get_items(session, Target, target_id)
            return results
    except OSError as e:
        logger.error(f"OS error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{target_id}")
def get_target_by_id(target_id: int):
    """Gets a target from the database."""
    # OK
    try:
        with Session() as session:
            return base_route.get_by_id(session, Target, target_id)
    except SQLAlchemyError as e:
        handle_db_session_exception(e)


@router.patch("/{target_id}")
def update_target(target_id: int, name=None, path=None):
    try:
        with Session() as session:
            if name is None:
                name = get_target_by_id(target_id).name
            if path is None:
                path = get_target_by_id(target_id).path
            return base_route.update(session, Target, target_id, name=name, path=path)
    except SQLAlchemyError as e:
        handle_db_session_exception(e)


@router.delete("/{target_id}")
def delete_target(target_id: int):
    """Delete a target folder from database."""
    try:
        with Session() as session:
            base_route.delete(session, Target, target_id)
            return {"code": 200, "message": "Target deleted successfully"}
    except SQLAlchemyError as e:
        handle_db_session_exception(e)
