"""FontaraBot — Core: text + callbacks"""
import logging, random as _rnd
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from telegram.error import BadRequest

from utils.guard import is_member, join_kb, join_msg, join_ok, join_fail, banned_msg, bust, maintenance_msg
from utils.fonts import convert_all, convert, get_font, FONTS
from utils.mem   import ok as rate_ok, wait as rate_wait, push
from utils.db    import upsert, is_banned, get_favs, set_favs, log_act
from utils.ui    import (trunc, _safe, result_card, result_kb, single_card,
                          copy_card, fav_card, fav_kb, fav_added, fav_removed,
                          random_card, random_kb, compare_card, compare_kb,
                          e_empty, e_long, e_rate, styles_msg)
from config import MAX_LEN, ADMIN_IDS, BRAND
import config as _cfg

log = logging.getLogger(__name__)

_CMP = {
    "serif":  ["bold","italic","bold_italic","double","bold_symbol","italic_serif"],
    "script": ["script","bold_script","fraktur","bold_fraktur","oldeng","estrangelo"],
    "fun":    ["bubble","neg_bubble","leet","inverted","morse","zalgo"],
}


async def on_text(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    u   = update.effective_user
    raw = (update.message.text or "").strip()
    if not raw:
        await update.message.reply_text(e_empty(), parse_mode=ParseMode.MARKDOWN); return

    upsert(u.id, u.username, u.first_name)

    if is_banned(u.id):
        await update.message.reply_text(banned_msg(), parse_mode=ParseMode.MARKDOWN); return
    if _cfg.MAINTENANCE_MODE and u.id not in ADMIN_IDS:
        await update.message.reply_text(maintenance_msg(), parse_mode=ParseMode.MARKDOWN); return
    if not await is_member(ctx.bot, u.id):
        await update.message.reply_text(join_msg(u.first_name), parse_mode=ParseMode.MARKDOWN,
                                         reply_markup=join_kb(), disable_web_page_preview=True); return
    if len(raw) > MAX_LEN:
        await update.message.reply_text(e_long(len(raw)), parse_mode=ParseMode.MARKDOWN); return
    if not rate_ok(u.id):
        await update.message.reply_text(e_rate(rate_wait(u.id)), parse_mode=ParseMode.MARKDOWN); return

    text = trunc(raw)
    push(u.id, text)
    results = convert_all(text)
    favs    = get_favs(u.id)
    await update.message.reply_text(
        result_card(results, 0), parse_mode=ParseMode.MARKDOWN,
        reply_markup=result_kb(_safe(text), 0, favs),
        disable_web_page_preview=True)


async def on_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query; u = q.from_user; d = q.data or ""
    await q.answer()
    upsert(u.id, u.username, u.first_name)
    if is_banned(u.id): await q.answer(banned_msg(), show_alert=True); return
    if _cfg.MAINTENANCE_MODE and u.id not in ADMIN_IDS:
        await q.answer("🔧 Maintenance", show_alert=True); return

    try:
        if d == "join:verify":
            bust(u.id)
            if await is_member(ctx.bot, u.id):
                try: await q.edit_message_text(join_ok(u.first_name), parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
                except BadRequest: await q.message.reply_text(join_ok(u.first_name), parse_mode=ParseMode.MARKDOWN)
            else: await q.answer(join_fail(), show_alert=True)
            return

        # Start shortcuts
        if d == "cmd:styles":
            res = convert_all("FontaraBot")
            await q.message.reply_text(styles_msg(res), parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True); return
        if d == "cmd:favs":
            favs = get_favs(u.id); res = convert_all("FontaraBot")
            await q.message.reply_text(fav_card(res, favs), parse_mode=ParseMode.MARKDOWN,
                                        reply_markup=fav_kb("FontaraBot", res, favs)); return
        if d == "cmd:random":
            k, n, c, _ = _rnd.choice(FONTS)
            await q.message.reply_text(random_card(n, convert("FontaraBot", k), c),
                parse_mode=ParseMode.MARKDOWN, reply_markup=random_kb("FontaraBot")); return

        if not await is_member(ctx.bot, u.id):
            await q.answer("Please join the required channels first.", show_alert=True); return

        parts = d.split("|", 2); act = parts[0]

        if act=="ca" and len(parts)>=2:
            await q.message.reply_text(copy_card(convert_all(parts[1])), parse_mode=ParseMode.MARKDOWN)

        elif act=="rf" and len(parts)>=2:
            if not rate_ok(u.id): await q.answer(f"⏳ {rate_wait(u.id):.0f}s", show_alert=True); return
            text=parts[1]; page=int(parts[2]) if len(parts)>=3 else 0
            res=convert_all(text); favs=get_favs(u.id)
            try:
                await q.edit_message_text(result_card(res,page), parse_mode=ParseMode.MARKDOWN,
                    reply_markup=result_kb(text,page,favs), disable_web_page_preview=True)
                await q.answer("✓ Refreshed!")
            except BadRequest as e:
                if "not modified" not in str(e).lower(): raise

        elif act=="pg" and len(parts)>=3:
            page=int(parts[1]); text=parts[2]
            res=convert_all(text); favs=get_favs(u.id)
            try:
                await q.edit_message_text(result_card(res,page), parse_mode=ParseMode.MARKDOWN,
                    reply_markup=result_kb(text,page,favs), disable_web_page_preview=True)
            except BadRequest as e:
                if "not modified" not in str(e).lower(): raise

        elif act=="st" and len(parts)>=3:
            key=parts[1]; text=parts[2]; entry=get_font(key)
            if entry:
                _, name, _ = entry
                await q.message.reply_text(single_card(name, convert(text,key)), parse_mode=ParseMode.MARKDOWN)

        elif act=="fv" and len(parts)>=2:
            text=parts[1]; res=convert_all(text); favs=get_favs(u.id)
            await q.message.reply_text(fav_card(res,favs), parse_mode=ParseMode.MARKDOWN,
                                        reply_markup=fav_kb(text,res,favs))

        elif act=="ft" and len(parts)>=3:
            key=parts[1]; text=parts[2]; favs=get_favs(u.id)
            entry=get_font(key); name=entry[1] if entry else key
            if key in favs: favs.remove(key); set_favs(u.id,favs); await q.answer(fav_removed(name))
            else:           favs.append(key); set_favs(u.id,favs); await q.answer(fav_added(name))
            res=convert_all(text); favs=get_favs(u.id)
            try: await q.edit_message_text(fav_card(res,favs), parse_mode=ParseMode.MARKDOWN,
                                            reply_markup=fav_kb(text,res,favs))
            except BadRequest as e:
                if "not modified" not in str(e).lower(): raise

        elif act=="rnd" and len(parts)>=2:
            text=parts[1]; k,n,c,_=_rnd.choice(FONTS)
            await q.message.reply_text(random_card(n,convert(text,k),c),
                parse_mode=ParseMode.MARKDOWN, reply_markup=random_kb(text))

        elif act=="cmp" and len(parts)>=2:
            text=parts[1]
            await q.message.reply_text(f"🔍  *Compare styles:*\n\n_{BRAND}_",
                parse_mode=ParseMode.MARKDOWN, reply_markup=compare_kb(text))

        elif act=="cmpset" and len(parts)>=3:
            setname=parts[1]; text=parts[2]
            keys=_CMP.get(setname, list(_CMP.values())[0])
            await q.message.reply_text(compare_card(convert_all(text),keys), parse_mode=ParseMode.MARKDOWN)

    except BadRequest as e: log.warning("BadRequest: %s", e)
    except Exception as e:
        log.error("Callback error: %s", e, exc_info=True)
        await q.answer("Something went wrong.", show_alert=True)
