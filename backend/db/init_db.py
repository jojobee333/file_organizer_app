import logging
from backend.schemas import Format, Origin, Session

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s | %(levelname)s | %(funcName)s : %(message)s")
logger = logging.getLogger(__name__)


def add_formats():
    with Session() as session:
        formats = [
            Format(name=".exe"),
            Format(name=".pdf"),
            Format(name=".doc"),
            Format(name=".jpg"),
        ]
        for item in formats:
            session.add(item)
        logging.debug("Default formats added")
    session.commit()


add_formats()
