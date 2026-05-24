"""FontaraBot — Config"""
import os

BOT_TOKEN   = os.getenv("BOT_TOKEN", "8888241754:AAFQ4finYefgOy7XDGflwLjkVyCxT95pIOw")
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "")
PORT        = int(os.getenv("PORT", "8080"))

ADMIN_IDS: list[int] = [8127675696]

CHANNELS = [
    {"id": "@MindRupture", "label": "⚡ Mindrupture", "url": "https://t.me/MindRupture"},
    {"id": "@LaceraBots",    "label": "🔥 LaceraBots",    "url": "https://t.me/LaceraBots"},
]

CACHE_OK  = 300
CACHE_NO  = 30
RATE_N    = 8
RATE_W    = 10
HIST_SIZE = 7
MAX_LEN   = 4096
FAVS_SIZE = 10

BC_BATCH = 25
BC_DELAY = 0.05

DB_PATH = os.getenv("DB_PATH", "fontara.json")
BRAND   = "⚡ @NeuroParallax  ·  🔥 @LaceraBots"

MAINTENANCE_MODE = False
