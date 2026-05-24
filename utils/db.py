"""FontaraBot — Database"""
import sqlite3, time, json, logging
from datetime import datetime, timezone
from config import DB_PATH

log = logging.getLogger(__name__)
_db = None

def _c():
    global _db
    if _db is None:
        _db = sqlite3.connect(DB_PATH, check_same_thread=False)
        _db.row_factory = sqlite3.Row
        _db.execute("PRAGMA journal_mode=WAL")
        _db.execute("PRAGMA synchronous=NORMAL")
        _db.execute("PRAGMA cache_size=10000")
        _db.execute("PRAGMA temp_store=MEMORY")
    return _db

def init_db():
    _c().executescript("""
        CREATE TABLE IF NOT EXISTS users(
            uid       INTEGER PRIMARY KEY,
            username  TEXT,
            fname     TEXT,
            last_seen REAL NOT NULL,
            msg_count INTEGER NOT NULL DEFAULT 0,
            joined_at REAL NOT NULL,
            favorites TEXT DEFAULT '[]'
        );
        CREATE TABLE IF NOT EXISTS banned(
            uid       INTEGER PRIMARY KEY,
            reason    TEXT,
            banned_at REAL NOT NULL
        );
        CREATE TABLE IF NOT EXISTS admins(
            uid      INTEGER PRIMARY KEY,
            fname    TEXT,
            role     TEXT NOT NULL DEFAULT 'mod',
            perms    TEXT NOT NULL DEFAULT '[]',
            added_by INTEGER,
            added_at REAL NOT NULL
        );
        CREATE TABLE IF NOT EXISTS logs(
            id     INTEGER PRIMARY KEY AUTOINCREMENT,
            ts     REAL NOT NULL,
            actor  INTEGER,
            action TEXT NOT NULL,
            detail TEXT
        );
    """)
    log.info("✅ DB ready: %s", DB_PATH)

# Roles
ROLE_PERMS = {
    "superadmin": ["stats","broadcast","ban","unban","userinfo","bans","logs","manage_admins","maintenance"],
    "admin":      ["stats","broadcast","ban","unban","userinfo","bans","logs"],
    "mod":        ["ban","unban","userinfo","bans"],
}
ROLE_EMOJI = {"superadmin":"👑","admin":"🛡","mod":"⚔️","none":"👤"}

def get_role(uid, sadmins):
    if uid in sadmins: return "superadmin"
    r = _c().execute("SELECT role FROM admins WHERE uid=?", (uid,)).fetchone()
    return r["role"] if r else "none"

def has_perm(uid, perm, sadmins):
    if uid in sadmins: return True
    r = _c().execute("SELECT perms FROM admins WHERE uid=?", (uid,)).fetchone()
    if not r: return False
    try: return perm in json.loads(r["perms"] or "[]")
    except: return False

def add_admin(uid, fname, role, added_by):
    perms = json.dumps(ROLE_PERMS.get(role, []))
    _c().execute("INSERT INTO admins(uid,fname,role,perms,added_by,added_at) VALUES(?,?,?,?,?,?) ON CONFLICT(uid) DO UPDATE SET role=excluded.role,perms=excluded.perms,fname=excluded.fname",
                 (uid, fname, role, perms, added_by, time.time()))
    _c().commit()

def remove_admin(uid, by):
    _c().execute("DELETE FROM admins WHERE uid=?", (uid,)); _c().commit()

def list_admins():
    return _c().execute("SELECT * FROM admins ORDER BY added_at").fetchall()

# Users
def upsert(uid, uname, fname) -> bool:
    now = time.time(); exists = get_user(uid)
    _c().execute("""INSERT INTO users(uid,username,fname,last_seen,msg_count,joined_at)
        VALUES(?,?,?,?,1,?) ON CONFLICT(uid) DO UPDATE SET
        username=excluded.username,fname=excluded.fname,
        last_seen=excluded.last_seen,msg_count=msg_count+1""",
        (uid, uname, fname, now, now))
    _c().commit(); return exists is None

def get_user(uid):    return _c().execute("SELECT * FROM users WHERE uid=?", (uid,)).fetchone()
def all_uids():       return [r[0] for r in _c().execute("SELECT uid FROM users").fetchall()]
def count_users():    return _c().execute("SELECT COUNT(*) FROM users").fetchone()[0]
def active_users(h=24): return _c().execute("SELECT COUNT(*) FROM users WHERE last_seen>=?", (time.time()-h*3600,)).fetchone()[0]
def total_msgs():     return _c().execute("SELECT SUM(msg_count) FROM users").fetchone()[0] or 0
def top_users(n=5):   return _c().execute("SELECT uid,fname,msg_count FROM users ORDER BY msg_count DESC LIMIT ?", (n,)).fetchall()
def new_today():      return _c().execute("SELECT COUNT(*) FROM users WHERE joined_at>=?", (time.time()-86400,)).fetchone()[0]

# Bans
def ban(uid, reason=""): _c().execute("INSERT OR REPLACE INTO banned VALUES(?,?,?)", (uid,reason,time.time())); _c().commit()
def unban(uid):          _c().execute("DELETE FROM banned WHERE uid=?", (uid,)); _c().commit()
def unban_all():         _c().execute("DELETE FROM banned"); _c().commit()
def is_banned(uid):      return _c().execute("SELECT 1 FROM banned WHERE uid=?", (uid,)).fetchone() is not None
def ban_info(uid):       return _c().execute("SELECT * FROM banned WHERE uid=?", (uid,)).fetchone()
def all_banned():        return _c().execute("SELECT * FROM banned ORDER BY banned_at DESC").fetchall()

# Favourites
def get_favs(uid):
    r = get_user(uid)
    if not r: return []
    try: return json.loads(r["favorites"] or "[]")
    except: return []
def set_favs(uid, favs):
    _c().execute("UPDATE users SET favorites=? WHERE uid=?", (json.dumps(favs[:10]), uid)); _c().commit()

# Logs
def log_act(actor, action, detail=""):
    _c().execute("INSERT INTO logs(ts,actor,action,detail) VALUES(?,?,?,?)", (time.time(),actor,action,detail)); _c().commit()
def recent_logs(n=15):
    return _c().execute("SELECT * FROM logs ORDER BY ts DESC LIMIT ?", (n,)).fetchall()

def ts(t): return datetime.fromtimestamp(t, tz=timezone.utc).strftime("%d %b %Y %H:%M UTC")
