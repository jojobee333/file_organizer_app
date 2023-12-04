import flet as ft

# Server Configuration
HOST = "127.0.0.1"
PORT = 8010
url_base = f"http://{HOST}:{PORT}"

# Database Configuration
DATABASE_URL = "sqlite+aiosqlite:///mydatabase.db"

# HTTP Headers
HEADERS = {'Content-Type': 'application/json'}

# Page Layout and Dimensions
MAX_HEIGHT = 900
ROW_HEIGHT = 30
MIN_MODULE = 100
MAX_MODULE = 200


# Text Sizes
TEXT_SIZE = 12
HEADING_ONE = 20

# Padding and Margins
SMALL_PADDING = 5
LARGE_PADDING = 10
RADIUS = 5

# Icon and Logo Sizes
LARGEST_ICON = 90
LARGE_ICON = 50
SMALL_ICON = 15

# Colors
CARD_COLOR = ft.colors.GREY_900
