import logging
import os
import shutil

from fastapi import APIRouter

from backend.routers.format_route import get_all_formats
from backend.routers.origin_route import get_origin_items
from backend.routers.target_route import get_target_by_id

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s | %(levelname)s | %(funcName)s : %(message)s")
logger = logging.getLogger(__name__)
router = APIRouter(tags=["Run"], prefix="/run")


@router.post("/")
async def move_files(origin_id: int, origin_path: str):
    files_moved = 0
    try:
        query = await get_all_formats()
        formats = query["results"]
        folder_items = await get_origin_items(origin_id)
        message = []

        # Asynchronously populate format_destinations
        format_destinations = {}
        for fmt in formats:
            logger.info(fmt)
            target = await get_target_by_id(fmt.target_id)
            format_destinations[fmt.name] = target.path if target else ""

        for item in folder_items:
            suffix = os.path.splitext(item)[-1]
            destination = format_destinations.get(suffix)

            if destination:
                source = os.path.join(origin_path, item)
                if not os.path.exists(source):
                    alert = f"Source file does not exist: {source}."
                    message.append(alert)
                    logger.warning(alert)
                    continue
                destination_path = os.path.join(destination, item)
                destination_alert = f"Moving '{item}' to '{destination}'"
                logger.info(destination_alert)
                # Could potentially be a bottleneck in performance.
                shutil.move(source, destination_path)
                files_moved += 1
            else:
                warning_alert = f"Unmapped extension found: {suffix}"
                message.append(warning_alert)
                logger.warning(warning_alert)

        final_message = f"Operation complete."
        message.append(final_message)
        logger.info(final_message)
        return {"message": message,
                "origin_id": origin_id,
                "files_moved": files_moved
                }

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return {"error": str(e)}
