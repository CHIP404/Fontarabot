"""
FontaraBot Ultimate — Unicode Font Engine
50 premium styles. All tables pre-compiled at import (zero runtime cost).
"""

_L = "abcdefghijklmnopqrstuvwxyz"
_U = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
_D = "0123456789"

# (key, display_name, category, data)
FONTS = [
    # ── SERIF / MATH ────────────────────────────────────────
    ("bold",         "𝗕𝗼𝗹𝗱",           "serif",  {"l":"𝗮𝗯𝗰𝗱𝗲𝗳𝗴𝗵𝗶𝗷𝗸𝗹𝗺𝗻𝗼𝗽𝗾𝗿𝘀𝘁𝘂𝘃𝘄𝘅𝘆𝘇","u":"𝗔𝗕𝗖𝗗𝗘𝗙𝗚𝗛𝗜𝗝𝗞𝗟𝗠𝗡𝗢𝗣𝗤𝗥𝗦𝗧𝗨𝗩𝗪𝗫𝗬𝗭","d":"𝟬𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵"}),
    ("italic",       "𝘐𝘵𝘢𝘭𝘪𝘤",          "serif",  {"l":"𝘢𝘣𝘤𝘥𝘦𝘧𝘨𝘩𝘪𝘫𝘬𝘭𝘮𝘯𝘰𝘱𝘲𝘳𝘴𝘵𝘶𝘷𝘸𝘹𝘺𝘻","u":"𝘈𝘉𝘊𝘋𝘌𝘍𝘎𝘏𝘐𝘑𝘒𝘓𝘔𝘕𝘖𝘗𝘘𝘙𝘚𝘛𝘜𝘝𝘞𝘟𝘠𝘡"}),
    ("bold_italic",  "𝑩𝒐𝒍𝒅 𝑰𝒕𝒂𝒍𝒊𝒄",    "serif",  {"l":"𝙖𝙗𝙘𝙙𝙚𝙛𝙜𝙝𝙞𝙟𝙠𝙡𝙢𝙣𝙤𝙥𝙦𝙧𝙨𝙩𝙪𝙫𝙬𝙭𝙮𝙯","u":"𝘼𝘽𝘾𝘿𝙀𝙁𝙂𝙃𝙄𝙅𝙆𝙇𝙈𝙉𝙊𝙋𝙌𝙍𝙎𝙏𝙐𝙑𝙒𝙓𝙔𝙕"}),
    ("double",       "𝔻𝕠𝕦𝕓𝕝𝕖 𝕊𝕥𝕣𝕦𝕔𝕜",  "serif",  {"l":"𝕒𝕓𝕔𝕕𝕖𝕗𝕘𝕙𝕚𝕛𝕜𝕝𝕞𝕟𝕠𝕡𝕢𝕣𝕤𝕥𝕦𝕧𝕨𝕩𝕪𝕫","u":"𝔸𝔹ℂ𝔻𝔼𝔽𝔾ℍ𝕀𝕁𝕂𝕃𝕄ℕ𝕆ℙℚℝ𝕊𝕋𝕌𝕍𝕎𝕏𝕐ℤ","d":"𝟘𝟙𝟚𝟛𝟜𝟝𝟞𝟟𝟠𝟡"}),
    # ── SCRIPT / CURSIVE ────────────────────────────────────
    ("script",       "𝒮𝒸𝓇𝒾𝓅𝓉",          "script", {"l":"𝒶𝒷𝒸𝒹ℯ𝒻ℊ𝒽𝒾𝒿𝓀𝓁𝓂𝓃ℴ𝓅𝓆𝓇𝓈𝓉𝓊𝓋𝓌𝓍𝓎𝓏","u":"𝒜ℬ𝒞𝒟ℰℱ𝒢ℋℐ𝒥𝒦ℒℳ𝒩𝒪𝒫𝒬ℛ𝒮𝒯𝒰𝒱𝒲𝒳𝒴𝒵"}),
    ("bold_script",  "𝓑𝓸𝓵𝓭 𝓢𝓬𝓻𝓲𝓹𝓽",    "script", {"l":"𝓪𝓫𝓬𝓭𝓮𝓯𝓰𝓱𝓲𝓳𝓴𝓵𝓶𝓷𝓸𝓹𝓺𝓻𝓼𝓽𝓾𝓿𝔀𝔁𝔂𝔃","u":"𝓐𝓑𝓒𝓓𝓔𝓕𝓖𝓗𝓘𝓙𝓚𝓛𝓜𝓝𝓞𝓟𝓠𝓡𝓢𝓣𝓤𝓥𝓦𝓧𝓨𝓩"}),
    # ── GOTHIC / FRAKTUR ────────────────────────────────────
    ("fraktur",      "𝔉𝔯𝔞𝔨𝔱𝔲𝔯",          "gothic", {"l":"𝔞𝔟𝔠𝔡𝔢𝔣𝔤𝔥𝔦𝔧𝔨𝔩𝔪𝔫𝔬𝔭𝔮𝔯𝔰𝔱𝔲𝔳𝔴𝔵𝔶𝔷","u":"𝔄𝔅ℭ𝔇𝔈𝔉𝔊ℌℑ𝔍𝔎𝔏𝔐𝔑𝔒𝔓𝔔ℜ𝔖𝔗𝔘𝔙𝔚𝔛𝔜ℨ"}),
    ("bold_fraktur", "𝕭𝖔𝖑𝖉 𝕱𝖗𝖆𝖐𝖙𝖚𝖗",   "gothic", {"l":"𝖆𝖇𝖈𝖉𝖊𝖋𝖌𝖍𝖎𝖏𝖐𝖑𝖒𝖓𝖔𝖕𝖖𝖗𝖘𝖙𝖚𝖛𝖜𝖝𝖞𝖟","u":"𝕬𝕭𝕮𝕯𝕰𝕱𝕲𝕳𝕴𝕵𝕶𝕷𝕸𝕹𝕺𝕻𝕼𝕽𝕾𝕿𝖀𝖁𝖂𝖃𝖄𝖅"}),
    # ── SANS-SERIF ──────────────────────────────────────────
    ("sans",         "𝖲𝖺𝗇𝗌-𝖲𝖾𝗋𝗂𝖿",      "sans",   {"l":"𝖺𝖻𝖼𝖽𝖾𝖿𝗀𝗁𝗂𝗃𝗄𝗅𝗆𝗇𝗈𝗉𝗊𝗋𝗌𝗍𝗎𝗏𝗐𝗑𝗒𝗓","u":"𝖠𝖡𝖢𝖣𝖤𝖥𝖦𝖧𝖨𝖩𝖪𝖫𝖬𝖭𝖮𝖯𝖰𝖱𝖲𝖳𝖴𝖵𝖶𝖷𝖸𝖹","d":"𝟢𝟣𝟤𝟥𝟦𝟧𝟨𝟩𝟪𝟫"}),
    ("sans_bold",    "𝗦𝗮𝗻𝘀 𝗕𝗼𝗹𝗱",       "sans",   {"l":"𝗮𝗯𝗰𝗱𝗲𝗳𝗴𝗵𝗶𝗷𝗸𝗹𝗺𝗻𝗼𝗽𝗾𝗿𝘀𝘁𝘂𝘃𝘄𝘅𝘆𝘇","u":"𝗔𝗕𝗖𝗗𝗘𝗙𝗚𝗛𝗜𝗝𝗞𝗟𝗠𝗡𝗢𝗣𝗤𝗥𝗦𝗧𝗨𝗩𝗪𝗫𝗬𝗭","d":"𝟬𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵"}),
    ("sans_italic",  "𝘚𝘢𝘯𝘴 𝘐𝘵𝘢𝘭𝘪𝘤",     "sans",   {"l":"𝘢𝘣𝘤𝘥𝘦𝘧𝘨𝘩𝘪𝘫𝘬𝘭𝘮𝘯𝘰𝘱𝘲𝘳𝘴𝘵𝘶𝘷𝘸𝘹𝘺𝘻","u":"𝘈𝘉𝘊𝘋𝘌𝘍𝘎𝘏𝘐𝘑𝘒𝘓𝘔𝘕𝘖𝘗𝘘𝘙𝘚𝘛𝘜𝘝𝘞𝘟𝘠𝘡"}),
    ("sans_bold_it", "𝙎𝙖𝙣𝙨 𝘽𝙤𝙡𝙙 𝙄𝙩",   "sans",   {"l":"𝙖𝙗𝙘𝙙𝙚𝙛𝙜𝙝𝙞𝙟𝙠𝙡𝙢𝙣𝙤𝙥𝙦𝙧𝙨𝙩𝙪𝙫𝙬𝙭𝙮𝙯","u":"𝘼𝘽𝘾𝘿𝙀𝙁𝙂𝙃𝙄𝙅𝙆𝙇𝙈𝙉𝙊𝙋𝙌𝙍𝙎𝙏𝙐𝙑𝙒𝙓𝙔𝙕"}),
    ("mono",         "𝙼𝚘𝚗𝚘𝚜𝚙𝚊𝚌𝚎",      "sans",   {"l":"𝚊𝚋𝚌𝚍𝚎𝚏𝚐𝚑𝚒𝚓𝚔𝚕𝚖𝚗𝚘𝚙𝚚𝚛𝚜𝚝𝚞𝚟𝚠𝚡𝚢𝚣","u":"𝙰𝙱𝙲𝙳𝙴𝙵𝙶𝙷𝙸𝙹𝙺𝙻𝙼𝙽𝙾𝙿𝚀𝚁𝚂𝚃𝚄𝚅𝚆𝚇𝚈𝚉","d":"𝟶𝟷𝟸𝟹𝟺𝟻𝟼𝟽𝟾𝟿"}),
    # ── SYMBOLS ─────────────────────────────────────────────
    ("small_caps",   "Sᴍᴀʟʟ Cᴀᴘs",      "symbol", {"l":"ᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘǫʀsᴛᴜᴠᴡxʏᴢ","u":"ABCDEFGHIJKLMNOPQRSTUVWXYZ"}),
    ("wide",         "Ｗｉｄｅ",            "symbol", {"l":"ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ","u":"ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ","d":"０１２３４５６７８９"}),
    ("bubble",       "Ⓑⓤⓑⓑⓛⓔ",           "symbol", {"l":"ⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓧⓨⓩ","u":"ⒶⒷⒸⒹⒺⒻⒼⒽⒾⒿⓀⓁⓂⓃⓄⓅⓆⓇⓈⓉⓊⓋⓌⓍⓎⓏ","d":"⓪①②③④⑤⑥⑦⑧⑨"}),
    ("neg_bubble",   "🅝🅔🅖 🅑🅤🅑",          "symbol", {"l":"🅐🅑🅒🅓🅔🅕🅖🅗🅘🅙🅚🅛🅜🅝🅞🅟🅠🅡🅢🅣🅤🅥🅦🅧🅨🅩","u":"🅐🅑🅒🅓🅔🅕🅖🅗🅘🅙🅚🅛🅜🅝🅞🅟🅠🅡🅢🅣🅤🅥🅦🅧🅨🅩"}),
    ("square",       "🅂🆀🅄🄰🅁🄴",           "symbol", {"l":"🄰🄱🄲🄳🄴🄵🄶🄷🄸🄹🄺🄻🄼🄽🄾🄿🅀🅁🅂🅃🅄🅅🅆🅇🅈🅉","u":"🄰🄱🄲🄳🄴🄵🄶🄷🄸🄹🄺🄻🄼🄽🄾🄿🅀🅁🅂🅃🅄🅅🅆🅇🅈🅉"}),
    ("neg_square",   "🅽🅴🅶 🆂🆀",           "symbol", {"l":"🅰🅱🅲🅳🅴🅵🅶🅷🅸🅹🅺🅻🅼🅽🅾🅿🆀🆁🆂🆃🆄🆅🆆🆇🆈🆉","u":"🅰🅱🅲🅳🅴🅵🅶🅷🅸🅹🅺🅻🅼🅽🅾🅿🆀🆁🆂🆃🆄🆅🆆🆇🆈🆉"}),
    # ── DECORATIVE ──────────────────────────────────────────
    ("strike",       "S̶t̶r̶i̶k̶e̶t̶h̶r̶o̶u̶g̶h̶",    "deco",   {"c":"\u0336"}),
    ("underline",    "U̲n̲d̲e̲r̲l̲i̲n̲e̲",          "deco",   {"c":"\u0332"}),
    ("dbl_under",    "D̳o̳u̳b̳l̳e̳ ̳U̳n̳d̳e̳r̳",     "deco",   {"c":"\u0333"}),
    ("overline",     "O̅v̅e̅r̅l̅i̅n̅e̅",            "deco",   {"c":"\u0305"}),
    ("wavy",         "W̴a̴v̴y̴ ̴U̴n̴d̴e̴r̴",          "deco",   {"c":"\u0334"}),
    ("dotted",       "Ḋȯṫṫėḋ",             "deco",   {"c":"\u0307"}),
    ("tilde",        "T̃ĩl̃d̃ẽ",              "deco",   {"c":"\u0303"}),
    ("slash",        "S̸l̸a̸s̸h̸e̸d̸",            "deco",   {"c":"\u0338"}),
    ("short_dbl",    "D̤o̤ṳb̤l̤e̤ ̤B̤e̤l̤o̤w̤",       "deco",   {"c":"\u0324"}),
    ("ring",         "R̊i̊n̊g̊",               "deco",   {"c":"\u030a"}),
    # ── SPECIAL TRANSFORMS ──────────────────────────────────
    ("inverted",     "pǝʇɹǝʌuI",          "special",{"fn":"inverted"}),
    ("mirror",       "ɿoɿɿiM",            "special",{"fn":"mirror"}),
    ("morse",        "·−  −···  ·−·",     "special",{"fn":"morse"}),
    ("pig_latin",    "Pig Latin",          "special",{"fn":"piglatin"}),
    ("leet",         "L€€T Sp€@k",        "special",{"fn":"leet"}),
    ("zalgo",        "Z̷̧͖a̵̢͎l̷̨̛g̵̢͘o̸͢",          "special",{"fn":"zalgo"}),
    # ── BONUS ───────────────────────────────────────────────
    ("superscript",  "Sᵘᵖᵉʳˢᶜʳⁱᵖᵗ",       "bonus",  {"fn":"superscript"}),
    ("subscript",    "Sᵤᵦₛ꜀ᵣᵢₚₜ",          "bonus",  {"fn":"subscript"}),
    ("currency",     "₵urrency",           "bonus",  {"fn":"currency"}),
    ("parenthesized","⒫⒜⒭⒠⒩⒯",           "bonus",  {"fn":"parenthesized"}),
    ("regional",     "🇷🇪🇬🇮🇴🇳🇦🇱",         "bonus",  {"fn":"regional"}),
    ("braille",      "⠃⠗⠁⠊⠇⠇⠑",          "bonus",  {"fn":"braille"}),
    # ── EXTRA PREMIUM ───────────────────────────────────────
    ("oldeng",       "𝕺𝖑𝖉 𝕰𝖓𝖌𝖑𝖎𝖘𝖍",      "gothic", {"l":"𝖆𝖇𝖈𝖉𝖊𝖋𝖌𝖍𝖎𝖏𝖐𝖑𝖒𝖓𝖔𝖕𝖖𝖗𝖘𝖙𝖚𝖛𝖜𝖝𝖞𝖟","u":"𝕬𝕭𝕮𝕯𝕰𝕱𝕲𝕳𝕴𝕵𝕶𝕷𝕸𝕹𝕺𝕻𝕼𝕽𝕾𝕿𝖀𝖁𝖂𝖃𝖄𝖅"}),
    ("circled",      "Ⓒⓘⓡⓒⓛⓔⓓ",           "symbol", {"l":"ⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓧⓨⓩ","u":"ⒶⒷⒸⒹⒺⒻⒼⒽⒾⒿⓀⓁⓂⓃⓄⓅⓆⓇⓈⓉⓊⓋⓌⓍⓎⓏ"}),
    ("outlined",     "𝖮𝗎𝗍𝗅𝗂𝗇𝖾𝖽",          "sans",   {"l":"𝖺𝖻𝖼𝖽𝖾𝖿𝗀𝗁𝗂𝗃𝗄𝗅𝗆𝗇𝗈𝗉𝗊𝗋𝗌𝗍𝗎𝗏𝗐𝗑𝗒𝗓","u":"𝖠𝖡𝖢𝖣𝖤𝖥𝖦𝖧𝖨𝖩𝖪𝖫𝖬𝖭𝖮𝖯𝖰𝖱𝖲𝖳𝖴𝖵𝖶𝖷𝖸𝖹","d":"𝟢𝟣𝟤𝟥𝟦𝟧𝟨𝟩𝟪𝟫"}),
    ("typewriter",   "𝚃𝚢𝚙𝚎𝚠𝚛𝚒𝚝𝚎𝚛",       "sans",   {"l":"𝚊𝚋𝚌𝚍𝚎𝚏𝚐𝚑𝚒𝚓𝚔𝚕𝚖𝚗𝚘𝚙𝚚𝚛𝚜𝚝𝚞𝚟𝚠𝚡𝚢𝚣","u":"𝙰𝙱𝙲𝙳𝙴𝙵𝙶𝙷𝙸𝙹𝙺𝙻𝙼𝙽𝙾𝙿𝚀𝚁𝚂𝚃𝚄𝚅𝚆𝚇𝚈𝚉","d":"𝟶𝟷𝟸𝟹𝟺𝟻𝟼𝟽𝟾𝟿"}),
    ("estrangelo",   "ܐܣܛܪܢܓܠܐ",          "gothic", {"l":"𝔞𝔟𝔠𝔡𝔢𝔣𝔤𝔥𝔦𝔧𝔨𝔩𝔪𝔫𝔬𝔭𝔮𝔯𝔰𝔱𝔲𝔳𝔴𝔵𝔶𝔷","u":"𝔄𝔅ℭ𝔇𝔈𝔉𝔊ℌℑ𝔍𝔎𝔏𝔐𝔑𝔒𝔓𝔔ℜ𝔖𝔗𝔘𝔙𝔚𝔛𝔜ℨ"}),
    ("tiny",         "ₜᵢₙᵧ",              "bonus",  {"fn":"tiny"}),
    ("wave",         "~Wαvε~",            "deco",   {"fn":"wave"}),
    ("caps_space",   "S P A C E D",       "bonus",  {"fn":"spaced"}),
    ("aesthetic",    "ａｅｓｔｈｅｔｉｃ",   "symbol", {"l":"ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ","u":"ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ","d":"０１２３４５６７８９"}),
    ("bold_symbol",  "𝐁𝐨𝐥𝐝 𝐒𝐞𝐫𝐢𝐟",       "serif",  {"l":"𝐚𝐛𝐜𝐝𝐞𝐟𝐠𝐡𝐢𝐣𝐤𝐥𝐦𝐧𝐨𝐩𝐪𝐫𝐬𝐭𝐮𝐯𝐰𝐱𝐲𝐳","u":"𝐀𝐁𝐂𝐃𝐄𝐅𝐆𝐇𝐈𝐉𝐊𝐋𝐌𝐍𝐎𝐏𝐐𝐑𝐒𝐓𝐔𝐕𝐖𝐗𝐘𝐙","d":"𝟎𝟏𝟐𝟑𝟒𝟓𝟔𝟕𝟖𝟗"}),
    ("italic_serif", "𝐼𝑡𝑎𝑙𝑖𝑐 𝑆𝑒𝑟𝑖𝑓",    "serif",  {"l":"𝑎𝑏𝑐𝑑𝑒𝑓𝑔ℎ𝑖𝑗𝑘𝑙𝑚𝑛𝑜𝑝𝑞𝑟𝑠𝑡𝑢𝑣𝑤𝑥𝑦𝑧","u":"𝐴𝐵𝐶𝐷𝐸𝐹𝐺𝐻𝐼𝐽𝐾𝐿𝑀𝑁𝑂𝑃𝑄𝑅𝑆𝑇𝑈𝑉𝑊𝑋𝑌𝑍"}),
    ("bold_serif_it","𝑩𝒐𝒍𝒅 𝑺𝒆𝒓𝒊𝒇 𝑰",   "serif",  {"l":"𝒂𝒃𝒄𝒅𝒆𝒇𝒈𝒉𝒊𝒋𝒌𝒍𝒎𝒏𝒐𝒑𝒒𝒓𝒔𝒕𝒖𝒗𝒘𝒙𝒚𝒛","u":"𝑨𝑩𝑪𝑫𝑬𝑭𝑮𝑯𝑰𝑱𝑲𝑳𝑴𝑵𝑶𝑷𝑸𝑹𝑺𝑻𝑼𝑽𝑾𝑿𝒀𝒁"}),
]

# ── Special maps ────────────────────────────────────────────
_INV = {'a':'ɐ','b':'q','c':'ɔ','d':'p','e':'ǝ','f':'ɟ','g':'ƃ','h':'ɥ','i':'ı','j':'ɾ','k':'ʞ','l':'l','m':'ɯ','n':'u','o':'o','p':'d','q':'b','r':'ɹ','s':'s','t':'ʇ','u':'n','v':'ʌ','w':'ʍ','x':'x','y':'ʎ','z':'z','A':'∀','B':'ᗺ','C':'Ɔ','D':'ᗡ','E':'Ǝ','F':'Ⅎ','G':'פ','H':'H','I':'I','J':'ſ','K':'ʞ','L':'˥','M':'W','N':'N','O':'O','P':'Ԁ','Q':'Q','R':'ᴚ','S':'S','T':'┴','U':'∩','V':'Λ','W':'M','X':'X','Y':'⅄','Z':'Z','0':'0','1':'Ɩ','2':'ᘕ','3':'Ɛ','4':'ᔭ','5':'ϛ','6':'9','7':'ㄥ','8':'8','9':'6','.':'˙',',':'\'','?':'¿','!':'¡','&':'⅋',' ':' '}
_MIR = {'a':'ɒ','b':'d','c':'ɔ','d':'b','e':'ɘ','f':'Ꞙ','g':'ᵷ','h':'ʜ','j':'ᒐ','k':'ʞ','n':'ᴎ','p':'q','q':'p','r':'ɿ','s':'ƨ','y':'ʏ','z':'ƹ','A':'A','B':'ꓭ','C':'Ɔ','D':'ꓷ','E':'Ǝ','F':'ꓞ','G':'ꓨ','J':'Ꞁ','K':'ꓘ','L':'ꓶ','N':'И','P':'ꟼ','Q':'Ꝺ','R':'Я','S':'Ƨ','Y':'ꓤ','Z':'Ƹ'}
_MRS = {'A':'·−','B':'−···','C':'−·−·','D':'−··','E':'·','F':'··−·','G':'−−·','H':'····','I':'··','J':'·−−−','K':'−·−','L':'·−··','M':'−−','N':'−·','O':'−−−','P':'·−−·','Q':'−−·−','R':'·−·','S':'···','T':'−','U':'··−','V':'···−','W':'·−−','X':'−··−','Y':'−·−−','Z':'−−··','0':'−−−−−','1':'·−−−−','2':'··−−−','3':'···−−','4':'····−','5':'·····','6':'−····','7':'−−···','8':'−−−··','9':'−−−−·',' ':'/'}
_LEET = {'a':'4','b':'8','c':'(','e':'3','g':'9','h':'#','i':'1','l':'1','o':'0','s':'5','t':'7','z':'2','A':'4','B':'8','C':'(','E':'3','G':'9','H':'#','I':'1','L':'1','O':'0','S':'5','T':'7','Z':'2'}
_CUR  = {'a':'₳','b':'฿','c':'₵','d':'ð','e':'€','f':'ƒ','g':'₲','h':'Ħ','i':'ł','j':'J','k':'₭','l':'£','m':'₥','n':'₦','o':'Ø','p':'₱','q':'Q','r':'₹','s':'$','t':'₸','u':'µ','v':'V','w':'₩','x':'✕','y':'¥','z':'Ƶ'}
_PAR  = {**{chr(0x61+i):chr(0x249c+i) for i in range(26)}, **{chr(0x41+i):chr(0x1f110+i) for i in range(26)}}
_REG  = {chr(0x41+i):chr(0x1f1e6+i) for i in range(26)}
_BRL  = {'a':'⠁','b':'⠃','c':'⠉','d':'⠙','e':'⠑','f':'⠋','g':'⠛','h':'⠓','i':'⠊','j':'⠚','k':'⠅','l':'⠇','m':'⠍','n':'⠝','o':'⠕','p':'⠏','q':'⠟','r':'⠗','s':'⠎','t':'⠞','u':'⠥','v':'⠧','w':'⠺','x':'⠭','y':'⠽','z':'⠵',' ':'⠀'}
_SUP  = str.maketrans("abcdefghijklmnoprstuvwxyz0123456789+-=()", "ᵃᵇᶜᵈᵉᶠᵍʰⁱʲᵏˡᵐⁿᵒᵖʳˢᵗᵘᵛʷˣʸᶻ⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾")
_SUB  = str.maketrans("aehijklmnoprstuvx0123456789+-=()", "ₐₑₕᵢⱼₖₗₘₙₒₚᵣₛₜᵤᵥₓ₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎")
_TINY = str.maketrans("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ", "ᵃᵇᶜᵈᵉᶠᵍʰⁱʲᵏˡᵐⁿᵒᵖᵠʳˢᵗᵘᵛʷˣʸᶻᴬᴮᶜᴰᴱᶠᴳᴴᴵᴶᴷᴸᴹᴺᴼᴾQᴿˢᵀᵁᵛᵂˣʸᶻ")
_ZALGO_UP = ['\u030d','\u030e','\u0304','\u0305','\u033f','\u0311','\u0306','\u0310','\u0352','\u0357']
_ZALGO_DN = ['\u0316','\u0317','\u0318','\u0319','\u031c','\u031d','\u0332','\u0333','\u0339','\u033b']

import random as _rnd

def _piglatin(text):
    def pl(w):
        if not w.isalpha(): return w
        v = "aeiouAEIOU"
        for i,c in enumerate(w):
            if c in v: return w[i:]+w[:i]+"ay" if i else w+"way"
        return w+"ay"
    return " ".join(pl(w) for w in text.split())

def _wave(text):
    result=[]
    for i,c in enumerate(text):
        if c.isalpha():
            result.append(c.upper() if i%2==0 else c.lower())
        else:
            result.append(c)
    return "".join(result)

def _zalgo_fn(text):
    out=[]
    for c in text:
        out.append(c)
        if c.strip() and c.isalpha():
            out.append(_rnd.choice(_ZALGO_UP))
            out.append(_rnd.choice(_ZALGO_DN))
    return "".join(out)

# ── Pre-compile tables ───────────────────────────────────────
_TBL: dict[str,dict] = {}
def _build(lo,up,di=None):
    t={}
    for i,c in enumerate(_L):
        if i<len(lo): t[c]=lo[i]
    for i,c in enumerate(_U):
        if i<len(up): t[c]=up[i]
    if di:
        for i,c in enumerate(_D):
            if i<len(di): t[c]=di[i]
    return t

for _k,_n,_c,_d in FONTS:
    if "l" in _d: _TBL[_k]=_build(_d["l"],_d["u"],_d.get("d"))


def convert(text:str, key:str) -> str:
    e = next((x for x in FONTS if x[0]==key), None)
    if not e: return text
    _,_,_,d = e
    fn = d.get("fn")
    if fn:
        if fn=="inverted":     return "".join(_INV.get(c,c) for c in reversed(text))
        if fn=="mirror":       return "".join(_MIR.get(c,c) for c in reversed(text))
        if fn=="morse":        return "  ".join(_MRS[c] for c in text.upper() if c in _MRS) or text
        if fn=="leet":         return "".join(_LEET.get(c,c) for c in text)
        if fn=="piglatin":     return _piglatin(text)
        if fn=="zalgo":        return _zalgo_fn(text)
        if fn=="superscript":  return text.lower().translate(_SUP)
        if fn=="subscript":    return text.lower().translate(_SUB)
        if fn=="currency":     return "".join(_CUR.get(c.lower(),c) for c in text)
        if fn=="parenthesized":return "".join(_PAR.get(c,c) for c in text)
        if fn=="regional":     return " ".join(_REG.get(c.upper(),c) for c in text if c.strip())
        if fn=="braille":      return "".join(_BRL.get(c.lower(),c) for c in text)
        if fn=="tiny":         return text.translate(_TINY)
        if fn=="wave":         return _wave(text)
        if fn=="spaced":       return " ".join(list(text))
        return text
    if "c" in d:
        cb=d["c"]; return "".join(c+cb if c.strip() else c for c in text)
    tbl=_TBL.get(key,{})
    return "".join(tbl.get(c,c) for c in text)


def convert_all(text:str) -> list[dict]:
    out=[]
    for key,name,cat,_ in FONTS:
        try: result=convert(text,key)
        except Exception: result=text
        out.append({"key":key,"name":name,"cat":cat,"result":result})
    return out


def get_font(key:str):
    for k,n,c,_ in FONTS:
        if k==key: return k,n,c
    return None


FONT_COUNT = len(FONTS)
FONT_KEYS  = [k for k,*_ in FONTS]
