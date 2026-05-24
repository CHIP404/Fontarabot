"""FontaraBot — Admin Panel (/fa — secret)"""
import asyncio, logging, time
from telegram import Update, InlineKeyboardButton as B, InlineKeyboardMarkup as K
from telegram.ext import ContextTypes, ConversationHandler, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from telegram.constants import ParseMode
from telegram.error import TelegramError
from config import ADMIN_IDS, BRAND, BC_BATCH, BC_DELAY
import config as _cfg
from utils.db import (get_user, all_uids, count_users, active_users, total_msgs,
                       ban, unban, unban_all, is_banned, ban_info, all_banned,
                       log_act, recent_logs, ts, top_users, new_today,
                       add_admin, remove_admin, list_admins, get_role, has_perm,
                       ROLE_PERMS, ROLE_EMOJI)

log = logging.getLogger(__name__)
H  = "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
L  = "┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄"
BC_WAIT = 1

def is_admin(uid): return uid in ADMIN_IDS or get_role(uid, ADMIN_IDS) != "none"
def perm(uid, p):  return has_perm(uid, p, ADMIN_IDS)
def role(uid):     return get_role(uid, ADMIN_IDS)


def dash_kb(uid):
    rows = []
    r1 = []
    if perm(uid,"stats"):     r1.append(B("📊 Stats",    callback_data="adm:stats"))
    if perm(uid,"broadcast"): r1.append(B("📢 Broadcast",callback_data="adm:bc"))
    if r1: rows.append(r1)
    r2 = []
    if perm(uid,"userinfo"):  r2.append(B("👤 User Info",  callback_data="adm:uid_ask"))
    if perm(uid,"bans"):      r2.append(B("🚫 Bans",       callback_data="adm:bans"))
    if r2: rows.append(r2)
    r3 = []
    if perm(uid,"logs"):      r3.append(B("📋 Logs",       callback_data="adm:logs"))
    if perm(uid,"maintenance"):r3.append(B("🔧 Maintenance",callback_data="adm:maint"))
    if r3: rows.append(r3)
    if perm(uid,"manage_admins"):
        rows.append([B("👑 Manage Admins", callback_data="adm:admins")])
    rows.append([B("🔄 Refresh", callback_data="adm:home")])
    return K(rows)

def back_kb(): return K([[B("🏠 Dashboard", callback_data="adm:home")]])

def dash_txt(uid, name):
    maint = "\n  ⚠️  *MAINTENANCE ON*" if _cfg.MAINTENANCE_MODE else ""
    r = role(uid); ico = ROLE_EMOJI.get(r, "👤")
    return (
        f"⚙️  *FONTARABOT ADMIN*\n{H}\n\n"
        f"  {ico}  *{name}*  —  _{r}_\n\n"
        f"  👥 Users:    *{count_users():,}*\n"
        f"  🆕 Today:    *{new_today():,}*\n"
        f"  🟢 Active:   *{active_users():,}*\n"
        f"  💬 Messages: *{total_msgs():,}*\n"
        f"  🚫 Banned:   *{len(all_banned()):,}*"
        f"{maint}\n\n{L}\n_Select action:_"
    )


async def cmd_admin(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    u = update.effective_user
    if not is_admin(u.id): return
    await update.message.reply_text(dash_txt(u.id, u.first_name),
        parse_mode=ParseMode.MARKDOWN, reply_markup=dash_kb(u.id))

async def cmd_ban(update, ctx):
    u = update.effective_user
    if not perm(u.id, "ban"): return
    args = ctx.args
    if not args or not args[0].lstrip("-").isdigit():
        await update.message.reply_text("Usage: `/ban <id> [reason]`", parse_mode=ParseMode.MARKDOWN); return
    uid = int(args[0]); reason = " ".join(args[1:])
    ban(uid, reason); log_act(u.id, "BAN", f"uid={uid}")
    await update.message.reply_text(f"✅ Banned `{uid}`", parse_mode=ParseMode.MARKDOWN)

async def cmd_unban(update, ctx):
    u = update.effective_user
    if not perm(u.id, "unban"): return
    args = ctx.args
    if not args or not args[0].lstrip("-").isdigit():
        await update.message.reply_text("Usage: `/unban <id>`", parse_mode=ParseMode.MARKDOWN); return
    unban(int(args[0])); log_act(u.id, "UNBAN", f"uid={args[0]}")
    await update.message.reply_text(f"✅ Unbanned `{args[0]}`", parse_mode=ParseMode.MARKDOWN)

async def cmd_unbanall(update, ctx):
    u = update.effective_user
    if not perm(u.id, "ban"): return
    n = len(all_banned()); unban_all(); log_act(u.id, "UNBAN_ALL", f"n={n}")
    await update.message.reply_text(f"✅ Removed all {n} bans.", parse_mode=ParseMode.MARKDOWN)

async def cmd_uinfo(update, ctx):
    u = update.effective_user
    if not perm(u.id, "userinfo"): return
    args = ctx.args
    if not args or not args[0].lstrip("-").isdigit():
        await update.message.reply_text("Usage: `/uinfo <id>`", parse_mode=ParseMode.MARKDOWN); return
    uid = int(args[0]); row = get_user(uid); bi = ban_info(uid)
    if not row:
        await update.message.reply_text(f"❌ User `{uid}` not found.", parse_mode=ParseMode.MARKDOWN); return
    st = "🚫 BANNED" if bi else "✅ Active"
    un = f"@{row['username']}" if row["username"] else "_none_"
    txt = (f"👤  *USER INFO*\n{L}\n\n"
           f"  🆔  `{row['uid']}`\n  📛  *{row['fname']}*\n"
           f"  🔗  {un}\n  💬  {row['msg_count']:,} msgs\n"
           f"  📅  Joined: {ts(row['joined_at'])}\n  🔰  {st}")
    if bi: txt += f"\n  📝  Reason: _{bi['reason'] or 'none'}_"
    await update.message.reply_text(txt, parse_mode=ParseMode.MARKDOWN, reply_markup=back_kb())

async def cmd_addadmin(update, ctx):
    u = update.effective_user
    if not perm(u.id, "manage_admins"): return
    args = ctx.args
    if not args or not args[0].lstrip("-").isdigit():
        await update.message.reply_text("Usage: `/addadmin <id> [role]`\nRoles: `admin` `mod`", parse_mode=ParseMode.MARKDOWN); return
    target = int(args[0]); r = args[1].lower() if len(args)>1 else "admin"
    if r not in ROLE_PERMS: r = "admin"
    row = get_user(target); fname = row["fname"] if row else str(target)
    add_admin(target, fname, r, u.id)
    await update.message.reply_text(f"✅ Added `{target}` as *{r}*", parse_mode=ParseMode.MARKDOWN)

async def cmd_removeadmin(update, ctx):
    u = update.effective_user
    if not perm(u.id, "manage_admins"): return
    args = ctx.args
    if not args or not args[0].lstrip("-").isdigit(): return
    target = int(args[0])
    if target in ADMIN_IDS:
        await update.message.reply_text("❌ Cannot remove config superadmin.", parse_mode=ParseMode.MARKDOWN); return
    remove_admin(target, u.id)
    await update.message.reply_text(f"✅ Removed admin `{target}`", parse_mode=ParseMode.MARKDOWN)

async def cmd_admins(update, ctx):
    u = update.effective_user
    if not is_admin(u.id): return
    lines = [f"👑  *ADMINS*\n{L}\n"]
    for sid in ADMIN_IDS:
        row = get_user(sid); n = row["fname"] if row else "?"
        lines.append(f"  👑 `{sid}`  {n}  _superadmin_")
    for a in list_admins():
        ico = ROLE_EMOJI.get(a["role"], "👤")
        lines.append(f"  {ico} `{a['uid']}`  {a['fname']}  _{a['role']}_")
    await update.message.reply_text("\n".join(lines), parse_mode=ParseMode.MARKDOWN)

async def cmd_myrole(update, ctx):
    u = update.effective_user; r = role(u.id); ico = ROLE_EMOJI.get(r, "👤")
    perms = ROLE_PERMS.get(r, [])
    txt = f"{ico}  *Your role: {r}*\n{L}\n\n" + ("\n".join(f"  ✦ {p}" for p in perms) if perms else "_No permissions_")
    await update.message.reply_text(txt, parse_mode=ParseMode.MARKDOWN)

async def cmd_maintenance(update, ctx):
    u = update.effective_user
    if not perm(u.id, "maintenance"): return
    args = ctx.args
    if not args or args[0].lower() not in ("on","off"):
        st = "ON" if _cfg.MAINTENANCE_MODE else "OFF"
        await update.message.reply_text(f"🔧 Maintenance is *{st}*\n\nUsage: `/maintenance on|off`", parse_mode=ParseMode.MARKDOWN); return
    _cfg.MAINTENANCE_MODE = args[0].lower()=="on"
    st = "ON ⚠️" if _cfg.MAINTENANCE_MODE else "OFF ✅"
    await update.message.reply_text(f"🔧 Maintenance: *{st}*", parse_mode=ParseMode.MARKDOWN)

async def cmd_msguser(update, ctx):
    u = update.effective_user
    if not perm(u.id, "broadcast"): return
    args = ctx.args
    if not args or len(args)<2 or not args[0].lstrip("-").isdigit(): return
    target = int(args[0]); text = " ".join(args[1:])
    try:
        await ctx.bot.send_message(target, f"📬  *Message from FontaraBot Admin:*\n\n{text}\n\n_{BRAND}_", parse_mode=ParseMode.MARKDOWN)
        await update.message.reply_text(f"✅ Sent to `{target}`", parse_mode=ParseMode.MARKDOWN)
    except TelegramError as e:
        await update.message.reply_text(f"❌ Failed: `{e}`", parse_mode=ParseMode.MARKDOWN)


async def on_adm_cb(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query; uid = q.from_user.id; d = q.data or ""
    if not is_admin(uid): await q.answer("🚫", show_alert=True); return
    await q.answer()

    async def edit(txt, kb=None):
        try: await q.edit_message_text(txt, parse_mode=ParseMode.MARKDOWN, reply_markup=kb or back_kb())
        except: await q.message.reply_text(txt, parse_mode=ParseMode.MARKDOWN, reply_markup=kb or back_kb())

    if   d=="adm:home":  await edit(dash_txt(uid, q.from_user.first_name), dash_kb(uid))
    elif d=="adm:stats":
        if not perm(uid,"stats"): await q.answer("🚫",show_alert=True); return
        tu = "\n".join(f"  {i+1}. {r['fname'][:16]}  {r['msg_count']:,}" for i,r in enumerate(top_users(5)))
        txt = (f"📊 *STATS*\n{L}\n\n"
               f"  👥 Total: *{count_users():,}*\n  🆕 Today: *{new_today():,}*\n"
               f"  🟢 24h: *{active_users():,}*\n  💬 Msgs: *{total_msgs():,}*\n"
               f"  🚫 Banned: *{len(all_banned()):,}*\n\n  🏆 *Top Users:*\n{tu}\n\n_{BRAND}_")
        await edit(txt)
    elif d=="adm:bans":
        if not perm(uid,"bans"): await q.answer("🚫",show_alert=True); return
        bl = all_banned()
        if not bl: await edit(f"🚫  *No banned users.*"); return
        lines = [f"🚫  *BANNED ({len(bl)})*\n{L}\n"]
        for b in bl[:20]:
            row = get_user(b["uid"]); n = row["fname"] if row else "?"
            lines.append(f"  • `{b['uid']}`  {n}")
        await edit("\n".join(lines))
    elif d=="adm:logs":
        if not perm(uid,"logs"): await q.answer("🚫",show_alert=True); return
        rows = recent_logs(10)
        if not rows: await edit("📋  *No logs.*"); return
        lines = [f"📋  *LOGS*\n{L}\n"]
        for r in rows: lines.append(f"  `{ts(r['ts'])}`  [{r['actor']}]  *{r['action']}*  {r['detail'] or ''}")
        await edit("\n".join(lines))
    elif d=="adm:maint":
        if not perm(uid,"maintenance"): await q.answer("🚫",show_alert=True); return
        _cfg.MAINTENANCE_MODE = not _cfg.MAINTENANCE_MODE
        st = "ON ⚠️" if _cfg.MAINTENANCE_MODE else "OFF ✅"
        await q.answer(f"🔧 {st}"); await edit(dash_txt(uid, q.from_user.first_name), dash_kb(uid))
    elif d=="adm:admins":
        if not perm(uid,"manage_admins"): await q.answer("🚫",show_alert=True); return
        lines = [f"👑  *ADMINS*\n{L}\n"]
        for sid in ADMIN_IDS:
            row = get_user(sid); n = row["fname"] if row else "?"
            lines.append(f"  👑 `{sid}`  {n}")
        for a in list_admins():
            ico = ROLE_EMOJI.get(a["role"],"👤"); lines.append(f"  {ico} `{a['uid']}`  {a['fname']}  _{a['role']}_")
        await edit("\n".join(lines))
    elif d=="adm:uid_ask":
        if not perm(uid,"userinfo"): await q.answer("🚫",show_alert=True); return
        await q.message.reply_text("👤 Send the user ID:", parse_mode=ParseMode.MARKDOWN)
    elif d=="adm:bc":
        if not perm(uid,"broadcast"): await q.answer("🚫",show_alert=True); return
        await q.message.reply_text(f"📢 Send broadcast message to *{count_users():,}* users:\n_(or /cancel)_",
                                    parse_mode=ParseMode.MARKDOWN)
        return BC_WAIT


async def recv_bc(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    u = update.effective_user
    if not perm(u.id, "broadcast"): return ConversationHandler.END
    msg = update.message; ids = all_uids(); total = len(ids); sent = failed = 0
    prog = await msg.reply_text(f"📢 Sending to {total:,}…", parse_mode=ParseMode.MARKDOWN)
    for i, uid in enumerate(ids, 1):
        try:
            if msg.photo:
                await ctx.bot.send_photo(uid, msg.photo[-1].file_id, caption=msg.caption or "", parse_mode=ParseMode.MARKDOWN)
            else:
                await ctx.bot.send_message(uid, msg.text or "", parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
            sent += 1
        except TelegramError: failed += 1
        await asyncio.sleep(BC_DELAY)
        if i % BC_BATCH == 0 or i == total:
            try: await prog.edit_text(f"📢 {i}/{total}  ✅{sent}  ❌{failed}", parse_mode=ParseMode.MARKDOWN)
            except: pass
    log_act(u.id, "BROADCAST", f"sent={sent} fail={failed}")
    await prog.edit_text(f"✅ *Done!*\n\n  📤 Sent: *{sent:,}*\n  ❌ Failed: *{failed:,}*", parse_mode=ParseMode.MARKDOWN)
    return ConversationHandler.END

async def cancel(update, ctx):
    await update.message.reply_text("✅ Cancelled."); return ConversationHandler.END


def build_conv():
    return ConversationHandler(
        entry_points=[CallbackQueryHandler(on_adm_cb, pattern=r"^adm:")],
        states={BC_WAIT: [
            CallbackQueryHandler(on_adm_cb, pattern=r"^adm:"),
            MessageHandler(filters.TEXT & ~filters.COMMAND | filters.PHOTO, recv_bc),
        ]},
        fallbacks=[CommandHandler("cancel", cancel)],
        per_user=True, per_chat=True, allow_reentry=True,
    )
