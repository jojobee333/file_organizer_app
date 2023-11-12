import logging
import os
import shutil

from fastapi import APIRouter

from backend.api.routers.format_route import get_all_formats
from backend.api.routers.origin_route import get_folder_items
from backend.api.routers.target_route import get_target_by_id

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s | %(levelname)s | %(funcName)s : %(message)s")
logger = logging.getLogger(__name__)

router = APIRouter(tags=["Move"], prefix="/move")


@router.post("/")
def move_files(origin_id: int, origin_path: str):
    files_moved = 0
    try:
        formats = get_all_formats()
        folder_items = get_folder_items(origin_id)
        format_destinations = {
            fmt.name: get_target_by_id(fmt.target_id).path or "" for fmt in formats
        }
        logging.info(format_destinations)
        for item in folder_items:
            suffix = os.path.splitext(item)[-1]
            destination = format_destinations.get(suffix)

            if destination:
                source = os.path.join(origin_path, item)
                if not os.path.exists(source):
                    logger.warning(f"Source file does not exist: {source}.")
                    continue
                destination_path = os.path.join(destination, item)
                logger.info(f"Moving '{item}' to '{destination}'")
                shutil.move(source, destination_path)
                files_moved += 1
            else:
                logger.warning(f"Unmapped extension found: {suffix}")
        message = f"Operation complete. {files_moved}/{len(folder_items)} files moved."
        logger.info(message)
        return {"message": message}

    except Exception as e:
        logger.error(f"An error occurred: {e}")
