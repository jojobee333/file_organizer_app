import json
import logging
import os
import shutil

from fastapi import APIRouter
from sqlalchemy.exc import SQLAlchemyError
from backend.api.routers import handle_db_session_exception
from backend.api.routers.base_route import BaseRoute
from backend.api.routers.origin_route import get_folder_items
from backend.api.routers.target_route import get_target_by_id
from backend.schemas import Format, Origin
from backend.schemas import Session

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s | %(levelname)s | %(funcName)s : %(message)s")
logger = logging.getLogger(__name__)
router = APIRouter(tags=["Formats"], prefix="/formats")

base_route = BaseRoute()


@router.get("/")
def get_all_formats():
    """Retrieves all saved formats."""
    try:
        with Session() as session:
            return {"results": base_route.get_all(session, Format)}
    except SQLAlchemyError as e:
        handle_db_session_exception(e)


@router.post("/")
def add_new_format(name: str, target_id):
    """Saves a format to database."""
    # OK
    try:
        with Session() as session:
            result = base_route.add_new(session, Format, name=name, target_id=target_id)
            return json.dumps({"code": 200, "message": "Format added successfully", "id": result.id})
    except SQLAlchemyError as e:
        handle_db_session_exception(e)


@router.get("/{format_id}")
def get_format_by_id(format_id: int):
    """Gets a format from the database."""
    # OK
    try:
        with Session() as session:
            return base_route.get_by_id(session, Format, format_id)
    except SQLAlchemyError as e:
        handle_db_session_exception(e)


@router.patch("/{format_id}")
def update_format(format_id: int, name=None, target_id=None):
    try:
        with Session() as session:
            if name is None:
                name = get_format_by_id(format_id).name
            if target_id is None:
                target_id = get_format_by_id(format_id).target_id
            return base_route.update(session, Format, format_id, name=name, target_id=target_id)
    except SQLAlchemyError as e:
        handle_db_session_exception(e)


@router.delete("/{format_id}")
def delete_format(format_id: int):
    """Delete a format from database."""
    try:
        with Session() as session:
            base_route.delete(session, Format, format_id)
            return {"code": 200, "message": "Format deleted successfully"}
    except SQLAlchemyError as e:
        handle_db_session_exception(e)



