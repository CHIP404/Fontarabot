"""FontaraBot — UI"""
import re as _re
from telegram import InlineKeyboardButton as B, InlineKeyboardMarkup as K
from config import BRAND, MAX_LEN
from utils.fonts import FONTS, FONT_COUNT

H1 = "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
H2 = "┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄"

CAT = {
    "serif":   ("🔵","SERIF"),   "script":  ("🟣","SCRIPT"),
    "gothic":  ("⚫","GOTHIC"),  "sans":    ("🟢","SANS"),
    "symbol":  ("🟡","SYMBOLS"), "deco":    ("🔴","DECO"),
    "special": ("🔮","SPECIAL"), "bonus":   ("💎","BONUS"),
}

P0 = ["bold","italic","bold_italic","double","script","bold_script",
      "fraktur","bold_fraktur","sans","sans_bold","sans_italic","mono",
      "small_caps","bubble","neg_bubble","wide","square","strike","underline","leet"]
P1 = [k for k,*_ in FONTS if k not in P0]

# Preview chars per style — keeps both pages under 4096 bytes for any input
_P0_MAX = 40
_P1_MAX = 25


def trunc(t: str) -> str:
    return t[:MAX_LEN]+"…" if len(t)>MAX_LEN else t

def _esc(t: str) -> str:
    return t.replace("`","'").replace("*","·").replace("_"," ")

def _safe(t: str) -> str:
    """Callback-data safe: strip bad chars, limit to 48 UTF-8 bytes."""
    s = _re.sub(r"[*_`\n\r\t]", "", t).strip() or t
    enc = s.encode("utf-8")
    return enc[:48].decode("utf-8", errors="ignore").strip() if len(enc)>48 else s

def _cat_hdr(cat, prev):
    if cat==prev: return None
    ico, lbl = CAT.get(cat, ("◆", cat.upper()))
    return f"\n{ico}  _{lbl}_"


# ── Cards ─────────────────────────────────────────────────────

def result_card(results: list[dict], page: int = 0) -> str:
    bk = {r["key"]: r for r in results}
    if page == 0:
        keys = [k for k in P0 if k in bk]
        lines = ["✨  *F O N T A R A B O T*",
                 f"_{FONT_COUNT} Premium Styles · Instant Conversion_", H1, ""]
        prev = None
        for k in keys:
            r = bk[k]; shown = r["result"][:_P0_MAX]+("…" if len(r["result"])>_P0_MAX else "")
            hdr = _cat_hdr(r["cat"], prev)
            if hdr: lines.append(hdr); prev = r["cat"]
            lines.append(f"✦ *{r['name']}*  `{_esc(shown)}`")
        lines += ["", H2,
                  f"_💎 {FONT_COUNT-len(keys)} more — tap *More ▶*_",
                  "_Tap any style button for your full text_",
                  "", f"_{BRAND}_"]
    else:
        valid = [k for k in P1 if k in bk]
        lines = ["✨  *MORE STYLES*", H1, ""]
        prev = None
        for k in valid:
            r = bk[k]; shown = r["result"][:_P1_MAX]+("…" if len(r["result"])>_P1_MAX else "")
            hdr = _cat_hdr(r["cat"], prev)
            if hdr: lines.append(hdr); prev = r["cat"]
            lines.append(f"✦ *{r['name']}*  `{_esc(shown)}`")
        lines += ["", H2, f"_{BRAND}_"]
    return "\n".join(lines)


def single_card(name: str, result: str) -> str:
    return f"✦  *{name}*\n{H2}\n`{_esc(result)}`\n\n_{BRAND}_"


def copy_card(results: list[dict]) -> str:
    plain = "\n".join(f"{r['name']}: {r['result']}" for r in results)
    return f"📋  *All {len(results)} Styles*\n{H2}\n```\n{plain}\n```\n\n_{BRAND}_"


def fav_card(results: list[dict], favs: list) -> str:
    if not favs:
        return f"⭐  *Favourites*\n{H2}\n\n_None saved yet. Tap ⭐ on any style._\n\n_{BRAND}_"
    bk = {r["key"]: r for r in results}
    lines = ["⭐  *YOUR FAVOURITES*", H1, ""]
    for k in favs:
        r = bk.get(k)
        if r: lines += [f"✦ *{r['name']}*", f"`{_esc(r['result'])}`", ""]
    lines += [H2, f"_{BRAND}_"]
    return "\n".join(lines)


def random_card(name: str, result: str, cat: str) -> str:
    ico, _ = CAT.get(cat, ("◆", ""))
    return f"🎲  *Random — {name}*\n{ico}  {H2}\n`{_esc(result)}`\n\n_{BRAND}_"


def compare_card(results: list[dict], keys: list) -> str:
    bk = {r["key"]: r for r in results}
    lines = ["🔍  *COMPARE*", H1, ""]
    for k in keys[:6]:
        r = bk.get(k)
        if r: lines += [f"✦ *{r['name']}*", f"`{_esc(r['result'])}`", ""]
    lines += [H2, f"_{BRAND}_"]
    return "\n".join(lines)


def start_msg(name: str) -> str:
    return (
        f"✨  *Hey {name}!*\n{H1}\n\n"
        f"*FontaraBot* — {FONT_COUNT} premium Unicode font styles.\n\n"
        f"  → Send any text to convert\n"
        f"  → `@FontaraBot text` in any chat\n"
        f"  → ⭐ Save favourites · 🎲 Random style\n\n"
        f"{H2}\n_{BRAND}_"
    )

def start_kb() -> K:
    return K([[
        B("🎨 All Styles",  callback_data="cmd:styles"),
        B("⭐ Favourites",  callback_data="cmd:favs"),
        B("🎲 Random",      callback_data="cmd:random"),
    ],[
        B("⚡ NeuroParallax", url="https://t.me/NeuroParallax"),
        B("🔥 LaceraBots",    url="https://t.me/LaceraBots"),
    ]])

def help_msg() -> str:
    return (
        f"📖  *FONTARABOT — HOW TO USE*\n{H1}\n\n"
        f"*Send any text* → get {FONT_COUNT} styles instantly\n\n"
        f"*Buttons on result card:*\n"
        f"  📋 Copy All — all styles in one block\n"
        f"  🔄 Refresh — re-render\n"
        f"  ⭐ Favourites — save top styles\n"
        f"  🎲 Random — surprise style\n"
        f"  🔍 Compare — compare style sets\n"
        f"  Style buttons — tap for full text\n"
        f"  💎 More ▶ — 33 extra styles\n\n"
        f"*Inline:*  `@FontaraBot your text` — works in any chat\n\n"
        f"*Commands:*  /styles  /favourites  /stats  /about\n\n"
        f"{H2}\n_{BRAND}_"
    )

def about_msg() -> str:
    return (
        f"ℹ️  *FONTARABOT*\n{H1}\n\n"
        f"  🔵 {FONT_COUNT}+ premium font styles\n"
        f"  🟣 Inline mode in any chat\n"
        f"  🟢 Favourites system\n"
        f"  🔮 Zalgo · Morse · Pig Latin · L33T\n"
        f"  💎 Braille · Superscript · Currency\n\n"
        f"{H2}\n*Powered by*\n  ⚡ @NeuroParallax  ·  🔥 @LaceraBots\n\n{H2}\n_{BRAND}_"
    )

def styles_msg(results: list[dict]) -> str:
    lines = [f"🎨  *ALL {FONT_COUNT} STYLES*", H1, ""]
    prev = None
    for r in results:
        hdr = _cat_hdr(r["cat"], prev)
        if hdr: lines.append(hdr); prev = r["cat"]
        lines.append(f"  ✦ *{r['name']}*  →  {r['result']}")
    lines += ["", H2, f"_{BRAND}_"]
    return "\n".join(lines)

def stats_msg(s: dict) -> str:
    top_u = ""
    if s.get("top"):
        top_u = "\n\n  🏆 *Top Users:*\n" + "\n".join(
            f"  {i+1}. {r['fname'][:18]}  {r['msg_count']:,} msgs"
            for i,r in enumerate(s["top"]))
    return (
        f"📊  *STATISTICS*\n{H1}\n\n"
        f"  👥  Total users:  *{s['total']:,}*\n"
        f"  🆕  New today:   *{s['new']:,}*\n"
        f"  🟢  Active 24h:  *{s['active']:,}*\n"
        f"  💬  Messages:    *{s['msgs']:,}*\n"
        f"  🚫  Banned:      *{s['banned']:,}*\n"
        f"  ⏱   Uptime:      *{s['uptime']}*"
        f"{top_u}\n\n{H2}\n_{BRAND}_"
    )

# ── Keyboards ─────────────────────────────────────────────────

_P0_BTNS = [
    ("bold","🔵 Bold"),         ("italic","🔵 Italic"),
    ("bold_italic","🔵 Bold It"),("double","🔵 Double"),
    ("script","🟣 Script"),     ("bold_script","🟣 Bold Sc"),
    ("fraktur","⚫ Fraktur"),   ("bold_fraktur","⚫ Bold Fr"),
    ("sans","🟢 Sans"),         ("sans_bold","🟢 Sans B"),
    ("sans_italic","🟢 Sans I"),("mono","🟢 Mono"),
    ("small_caps","🟡 SmCaps"), ("bubble","🟡 Bubble"),
    ("neg_bubble","🟡 NgBubl"), ("wide","🟡 Wide"),
    ("square","🟡 Square"),     ("strike","🔴 Strike"),
    ("underline","🔴 Under"),   ("leet","🔮 L33T"),
]
_P1_BTNS = [
    ("neg_square","🟡 NgSqr"),    ("sans_bold_it","🟢 SnsBI"),
    ("typewriter","🟢 Type"),     ("oldeng","⚫ OldEng"),
    ("circled","🟡 Circle"),      ("outlined","🟢 Outln"),
    ("aesthetic","🟡 Aesth"),     ("bold_symbol","🔵 BoldS"),
    ("italic_serif","🔵 ItalS"),  ("bold_serif_it","🔵 BldSI"),
    ("dbl_under","🔴 DblUnd"),    ("overline","🔴 Over"),
    ("wavy","🔴 Wavy"),           ("dotted","🔴 Dot"),
    ("tilde","🔴 Tilde"),         ("slash","🔴 Slash"),
    ("short_dbl","🔴 ShDbl"),     ("ring","🔴 Ring"),
    ("inverted","🔮 Invert"),     ("mirror","🔮 Mirror"),
    ("morse","🔮 Morse"),         ("pig_latin","🔮 Pig"),
    ("zalgo","🔮 Zalgo"),         ("superscript","💎 Super"),
    ("subscript","💎 Sub"),       ("currency","💎 Cash"),
    ("parenthesized","💎 Paren"), ("regional","💎 Flag"),
    ("braille","💎 Brl"),         ("tiny","💎 Tiny"),
    ("wave","💎 Wave"),           ("caps_space","💎 Space"),
    ("estrangelo","⚫ Estng"),
]

def result_kb(text: str, page: int = 0, favs: list = None) -> K:
    s = _safe(text); favs = favs or []; rows = []
    rows.append([B("📋 Copy All",   callback_data=f"ca|{s}"),
                 B("🔄 Refresh",    callback_data=f"rf|{s}|{page}"),
                 B("⭐ Favs",       callback_data=f"fv|{s}")])
    rows.append([B("🎲 Random",     callback_data=f"rnd|{s}"),
                 B("🔍 Compare",    callback_data=f"cmp|{s}")])
    btns = _P0_BTNS if page==0 else _P1_BTNS
    row = []
    for key, lbl in btns:
        row.append(B(lbl, callback_data=f"st|{key}|{s}"))
        if len(row)==3: rows.append(row); row=[]
    if row: rows.append(row)
    rows.append([B("💎 More ▶", callback_data=f"pg|1|{s}")] if page==0
                else [B("◀ Back",  callback_data=f"pg|0|{s}")])
    return K(rows)

def fav_kb(text: str, results: list, favs: list) -> K:
    s = _safe(text); bk = {r["key"]:r for r in results}
    toggles = [B(("⭐ " if k in favs else "☆ ")+n[:10],
                 callback_data=f"ft|{k}|{s}")
               for k,n,c,_ in FONTS if k in bk]
    rows = [toggles[i:i+3] for i in range(0,len(toggles),3)]
    rows.append([B("◀ Back", callback_data=f"pg|0|{s}")])
    return K(rows)

def random_kb(text: str) -> K:
    s = _safe(text)
    return K([[B("🎲 Another", callback_data=f"rnd|{s}"),
               B("◀ Back",    callback_data=f"pg|0|{s}")]])

def compare_kb(text: str) -> K:
    s = _safe(text)
    return K([[B("📝 Serif",   callback_data=f"cmpset|serif|{s}"),
               B("✍️ Script",  callback_data=f"cmpset|script|{s}"),
               B("🎨 Fun",     callback_data=f"cmpset|fun|{s}")],
              [B("◀ Back",     callback_data=f"pg|0|{s}")]])

# Error messages
def e_empty(): return f"✏️  *Send me some text!*\n\n_Example: `Hello World`_\n\n_{BRAND}_"
def e_long(n): return f"📏  *Too long!*  ({n} chars, max {MAX_LEN})"
def e_rate(w): 
    bar = "█"*int((10-w)/10*10)+"░"*int(w/10*10) if w<=10 else "░"*10
    return f"⏳  *Slow down!*\n\n`{bar}`\n_Wait {w:.0f}s_"
def fav_added(name):   return f"⭐ {name} saved!"
def fav_removed(name): return f"💔 {name} removed."
