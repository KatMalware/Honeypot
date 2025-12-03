import asyncio
import random
import time


async def random_delay(min_s=0.1, max_s=1.2):
# small random delay to appear more realistic
await asyncio.sleep(random.uniform(min_s, max_s))


def friendly_banner():
return (
"Welcome to Ubuntu 18.04.6 LTS\n"
"This system is for authorized use only.\n"
)


# simple sanitizer for display
def sanitize(s: bytes) -> str:
try:
return s.decode('utf-8', errors='ignore').strip()
except Exception:
return repr(s)

