"""
FontaraBot — Main Entry Point
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Railway deploy: set BOT_TOKEN environment variable
Admin panel:    /fa  (secret)
Superadmin ID:  8127675696
"""
import logging, os, traceback
from telegram import BotCommand, Update
from telegram.ext import (Application, CommandHandler, MessageHandler,
                           CallbackQueryHandler, InlineQueryHandler,
                           filters, ContextTypes)
from config import BOT_TOKEN, WEBHOOK_URL, PORT
from utils.db import init_db, log_act

from handlers.commands import (cmd_start, cmd_help, cmd_about, cmd_styles,
                                cmd_favourites, cmd_random, cmd_stats)
from handlers.core   import on_text, on_callback
from handlers.inline import on_inline
from handlers.admin  import (cmd_admin, cmd_ban, cmd_unban, cmd_unbanall,
                              cmd_uinfo, cmd_addadmin, cmd_removeadmin,
                              cmd_admins, cmd_myrole, cmd_maintenance,
                              cmd_msguser, build_conv)

logging.basicConfig(
    format  = "%(asctime)s | %(levelname)-8s | %(name)s — %(message)s",
    datefmt = "%Y-%m-%d %H:%M:%S",
    level   = logging.INFO,
)
for lib in ("httpx","telegram","aiohttp"):
    logging.getLogger(lib).setLevel(logging.WARNING)
log = logging.getLogger("FontaraBot")

COMMANDS = [
    BotCommand("start",      "✨ Start"),
    BotCommand("styles",     "🎨 All 53 font styles"),
    BotCommand("random",     "🎲 Random style"),
    BotCommand("favourites", "⭐ Your saved styles"),
    BotCommand("stats",      "📊 Statistics"),
    BotCommand("help",       "📖 How to use"),
    BotCommand("about",      "ℹ️  About"),
]


async def on_error(update: object, ctx: ContextTypes.DEFAULT_TYPE):
    tb = "".join(traceback.format_exception(type(ctx.error), ctx.error, ctx.error.__traceback__))
    log.error("Exception:\n%s", tb)
    try: log_act(None, "ERROR", str(ctx.error)[:200])
    except: pass
    if isinstance(update, Update):
        msg = update.message or (update.callback_query and update.callback_query.message)
        if msg:
            try: await msg.reply_text("⚠️ Something went wrong. Please try again.")
            except: pass


async def on_startup(app: Application):
    init_db()
    await app.bot.set_my_commands(COMMANDS)
    log.info("✅ DB + commands ready")
    log_act(None, "BOT_START", "")

    # Keep-alive for Railway / Render
    port = int(os.getenv("PORT", PORT))
    if os.getenv("RAILWAY_ENVIRONMENT") or os.getenv("RENDER") or WEBHOOK_URL:
        try:
            from aiohttp import web
            async def health(_): return web.Response(text="FontaraBot ✅")
            wa = web.Application()
            wa.router.add_get("/", health)
            wa.router.add_get("/health", health)
            runner = web.AppRunner(wa)
            await runner.setup()
            await web.TCPSite(runner, "0.0.0.0", port).start()
            log.info("Keep-alive on :%d", port)
        except Exception as e:
            log.warning("Keep-alive skipped: %s", e)


def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN environment variable not set!")
    log.info("🚀 FontaraBot starting…")
    app = Application.builder().token(BOT_TOKEN).post_init(on_startup).build()

    # Admin conversation handler (broadcast)
    app.add_handler(build_conv())

    # Secret admin commands (not in public /commands menu)
    app.add_handler(CommandHandler("fa",           cmd_admin))
    app.add_handler(CommandHandler("ban",          cmd_ban))
    app.add_handler(CommandHandler("unban",        cmd_unban))
    app.add_handler(CommandHandler("unbanall",     cmd_unbanall))
    app.add_handler(CommandHandler("uinfo",        cmd_uinfo))
    app.add_handler(CommandHandler("addadmin",     cmd_addadmin))
    app.add_handler(CommandHandler("removeadmin",  cmd_removeadmin))
    app.add_handler(CommandHandler("admins",       cmd_admins))
    app.add_handler(CommandHandler("myrole",       cmd_myrole))
    app.add_handler(CommandHandler("maintenance",  cmd_maintenance))
    app.add_handler(CommandHandler("msguser",      cmd_msguser))

    # Public commands
    app.add_handler(CommandHandler("start",        cmd_start))
    app.add_handler(CommandHandler("help",         cmd_help))
    app.add_handler(CommandHandler("about",        cmd_about))
    app.add_handler(CommandHandler("styles",       cmd_styles))
    app.add_handler(CommandHandler("random",       cmd_random))
    app.add_handler(CommandHandler("favourites",   cmd_favourites))
    app.add_handler(CommandHandler("fav",          cmd_favourites))
    app.add_handler(CommandHandler("stats",        cmd_stats))

    app.add_handler(CallbackQueryHandler(on_callback))
    app.add_handler(InlineQueryHandler(on_inline))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_text))
    app.add_error_handler(on_error)

    if WEBHOOK_URL:
        log.info("📡 Webhook: %s", WEBHOOK_URL)
        app.run_webhook(listen="0.0.0.0", port=int(os.getenv("PORT", PORT)),
                        webhook_url=f"{WEBHOOK_URL}/tg", url_path="tg",
                        drop_pending_updates=True)
    else:
        log.info("🔄 Polling mode")
        app.run_polling(drop_pending_updates=True,
                        allowed_updates=[Update.MESSAGE, Update.CALLBACK_QUERY, Update.INLINE_QUERY])

if __name__ == "__main__":
    main()
