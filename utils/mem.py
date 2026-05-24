"""FontaraBot — Rate limiter + per-user memory"""
import time
from collections import defaultdict, deque
from config import RATE_N, RATE_W, HIST_SIZE

_stamps: dict[int,deque] = defaultdict(lambda: deque(maxlen=RATE_N))
_hist:   dict[int,deque] = defaultdict(lambda: deque(maxlen=HIST_SIZE))

def ok(uid:int) -> bool:
    now=time.monotonic(); dq=_stamps[uid]
    while dq and now-dq[0]>RATE_W: dq.popleft()
    if len(dq)>=RATE_N: return False
    dq.append(now); return True

def wait(uid:int) -> float:
    dq=_stamps[uid]
    return max(0.0, RATE_W-(time.monotonic()-dq[0])) if dq else 0.0

def push(uid:int, text:str):
    dq=_hist[uid]
    if not dq or dq[-1]!=text: dq.append(text)

def hist(uid:int) -> list[str]:
    return list(reversed(_hist[uid]))
