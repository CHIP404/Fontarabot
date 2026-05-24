"""FontaraBot — Inline Mode"""
import logging, uuid
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import ContextTypes
from utils.fonts import convert_all, FONT_COUNT
from utils.ui    import trunc

log = logging.getLogger(__name__)
_ICO = {"serif":"🔵","script":"🟣","gothic":"⚫","sans":"🟢",
        "symbol":"🟡","deco":"🔴","special":"🔮","bonus":"💎"}

_ORDER = ["bold","italic","bold_italic","script","bold_script","double",
          "fraktur","bold_fraktur","sans","sans_bold","mono","small_caps",
          "bubble","neg_bubble","wide","square","leet","inverted","mirror",
          "morse","zalgo","superscript","subscript","currency","braille",
          "typewriter","circled","aesthetic","oldeng","wavy","strike",
          "underline","pig_latin","regional","tiny","caps_space","wave",
          "sans_italic","sans_bold_it","neg_square","outlined","bold_symbol",
          "italic_serif","bold_serif_it","dbl_under","overline","dotted",
          "tilde","slash","short_dbl","ring","parenthesized","estrangelo"]

async def on_inline(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.inline_query; raw = (q.query or "").strip()
    if not raw:
        await q.answer([InlineQueryResultArticle(
            id=str(uuid.uuid4()), title="✏️  Type text after @FontaraBot",
            description=f"Get {FONT_COUNT} font styles in any chat!",
            input_message_content=InputTextMessageContent(
                f"Use @FontaraBot followed by text to get {FONT_COUNT} premium font styles instantly! ✨"))],
            cache_time=5); return
    text = trunc(raw)
    bk   = {r["key"]: r for r in convert_all(text)}
    res  = []
    for key in _ORDER:
        r = bk.get(key)
        if not r: continue
        ico = _ICO.get(r["cat"], "◆")
        res.append(InlineQueryResultArticle(
            id=str(uuid.uuid4()), title=f"{ico}  {r['name']}",
            description=r["result"][:100],
            input_message_content=InputTextMessageContent(r["result"])))
    await q.answer(res, cache_time=0, is_personal=True)
