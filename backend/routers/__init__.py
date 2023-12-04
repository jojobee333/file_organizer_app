import logging
import sqlite3

from fastapi import HTTPException

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s | %(levelname)s | %(funcName)s : %(message)s")
logger = logging.getLogger(__name__)


def handle_db_session_exception(e, status_code=500):
    logger.error(f"Database error occurred: {e}")
    raise HTTPException(status_code=status_code, detail=f"{e}")

