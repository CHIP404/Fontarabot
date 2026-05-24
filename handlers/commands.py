"""FontaraBot — User Commands"""
import logging, time
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from utils.guard import is_member, join_kb, join_msg, banned_msg, maintenance_msg
from utils.fonts import convert_all, convert, FONTS
from utils.mem   import hist
from utils.db    import upsert, is_banned, get_favs, count_users, active_users, total_msgs, top_users, new_today, all_banned
from utils.ui    import (_safe, start_msg, start_kb, help_msg, about_msg, styles_msg,
                          fav_card, fav_kb, random_card, random_kb, stats_msg, e_empty)
from config import ADMIN_IDS
import config as _cfg

log = logging.getLogger(__name__)
_t0 = time.monotonic()
import random as _rnd


async def _gate(update, ctx) -> bool:
    u = update.effective_user; upsert(u.id, u.username, u.first_name)
    if is_banned(u.id):
        await update.message.reply_text(banned_msg(), parse_mode=ParseMode.MARKDOWN); return True
    if _cfg.MAINTENANCE_MODE and u.id not in ADMIN_IDS:
        await update.message.reply_text(maintenance_msg(), parse_mode=ParseMode.MARKDOWN); return True
    if not await is_member(ctx.bot, u.id):
        await update.message.reply_text(join_msg(u.first_name), parse_mode=ParseMode.MARKDOWN,
                                         reply_markup=join_kb(), disable_web_page_preview=True); return True
    return False


async def cmd_start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    u = update.effective_user; upsert(u.id, u.username, u.first_name)
    if is_banned(u.id):
        await update.message.reply_text(banned_msg(), parse_mode=ParseMode.MARKDOWN); return
    if _cfg.MAINTENANCE_MODE and u.id not in ADMIN_IDS:
        await update.message.reply_text(maintenance_msg(), parse_mode=ParseMode.MARKDOWN); return
    if not await is_member(ctx.bot, u.id):
        await update.message.reply_text(join_msg(u.first_name), parse_mode=ParseMode.MARKDOWN,
                                         reply_markup=join_kb(), disable_web_page_preview=True); return
    await update.message.reply_text(start_msg(u.first_name), parse_mode=ParseMode.MARKDOWN,
                                     reply_markup=start_kb(), disable_web_page_preview=True)

async def cmd_help(update, ctx):
    if await _gate(update, ctx): return
    await update.message.reply_text(help_msg(), parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)

async def cmd_about(update, ctx):
    if await _gate(update, ctx): return
    await update.message.reply_text(about_msg(), parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)

async def cmd_styles(update, ctx):
    if await _gate(update, ctx): return
    res = convert_all("FontaraBot")
    await update.message.reply_text(styles_msg(res), parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)

async def cmd_favourites(update, ctx):
    if await _gate(update, ctx): return
    u = update.effective_user; favs = get_favs(u.id); res = convert_all("FontaraBot")
    await update.message.reply_text(fav_card(res, favs), parse_mode=ParseMode.MARKDOWN,
                                     reply_markup=fav_kb("FontaraBot", res, favs))

async def cmd_random(update, ctx):
    if await _gate(update, ctx): return
    u = update.effective_user; h = hist(u.id); text = h[0] if h else "FontaraBot"
    k, n, c, _ = _rnd.choice(FONTS)
    await update.message.reply_text(random_card(n, convert(text, k), c),
        parse_mode=ParseMode.MARKDOWN, reply_markup=random_kb(text))

async def cmd_stats(update, ctx):
    if await _gate(update, ctx): return
    s = int(time.monotonic()-_t0); h,r=divmod(s,3600); m,sc=divmod(r,60)
    data = {"total":count_users(),"new":new_today(),"active":active_users(24),
            "msgs":total_msgs(),"banned":len(all_banned()),
            "uptime":f"{h}h {m}m {sc}s","top":top_users(5)}
    await update.message.reply_text(stats_msg(data), parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
