"""FontaraBot — Config"""
import os

BOT_TOKEN = os.getenv("BOT_TOKEN", "")          # Set on Railway
ADMIN_IDS: list[int] = [8127675696]

CHANNELS = [
    {"id": "@NeuroParallax", "label": "⚡ NeuroParallax", "url": "https://t.me/NeuroParallax"},
    {"id": "@LaceraBots",    "label": "🔥 LaceraBots",    "url": "https://t.me/LaceraBots"},
]

CACHE_OK  = 300   # seconds member status cached
CACHE_NO  = 30
RATE_N    = 8     # requests
RATE_W    = 10    # per seconds
MAX_LEN   = 4096  # Telegram max
FAVS_SIZE = 10

BC_BATCH = 25
BC_DELAY = 0.05

DB_PATH = os.getenv("DB_PATH", "fontara.json")   # .json = pella/railway friendly
BRAND   = "⚡ @NeuroParallax  ·  🔥 @LaceraBots"

MAINTENANCE_MODE = False
