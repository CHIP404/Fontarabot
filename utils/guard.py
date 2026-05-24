"""FontaraBot — Join Guard"""
import time, logging
from telegram import InlineKeyboardButton as B, InlineKeyboardMarkup as K
from telegram.error import TelegramError
from config import CHANNELS, BRAND, CACHE_OK, CACHE_NO

log = logging.getLogger(__name__)
_cache: dict[int, tuple[bool,float]] = {}

def bust(uid): _cache.pop(uid, None)

async def is_member(bot, uid: int) -> bool:
    e = _cache.get(uid)
    if e and time.monotonic() < e[1]: return e[0]
    ok = True
    for ch in CHANNELS:
        try:
            m = await bot.get_chat_member(ch["id"], uid)
            if m.status in ("left","kicked","banned"): ok = False; break
        except TelegramError as ex:
            if "chat not found" in str(ex).lower() or "inaccessible" in str(ex).lower(): continue
            ok = False; break
    _cache[uid] = (ok, time.monotonic() + (CACHE_OK if ok else CACHE_NO))
    return ok

def join_kb() -> K:
    rows = [[B(ch["label"], url=ch["url"])] for ch in CHANNELS]
    rows.append([B("✅  Joined — Verify Now", callback_data="join:verify")])
    return K(rows)

def join_msg(name: str) -> str:
    chs = "\n".join(f"  {ch['label']}  ·  {ch['id']}" for ch in CHANNELS)
    return (
        f"🔐  *Access Required*\n{'━'*30}\n\n"
        f"Hey *{name}!* Join our channels first:\n\n{chs}\n\n"
        f"{'─'*30}\n"
        f"  ① Tap each button to join\n"
        f"  ② Tap  *✅ Joined — Verify Now*\n\n"
        f"_{BRAND}_"
    )

def join_ok(name: str) -> str:
    return f"🎉  *Welcome, {name}!*\n\nSend any text to convert it into *53 premium font styles*! ✨\n\n_{BRAND}_"

def join_fail() -> str:
    return "❌  *Not joined yet!*\n\n_Please join both channels, then tap Verify._"

def banned_msg() -> str:
    return "🚫  *You are banned from this bot.*"

def maintenance_msg() -> str:
    return f"🔧  *Bot Under Maintenance*\n\n_Back soon!_\n\n_{BRAND}_"
