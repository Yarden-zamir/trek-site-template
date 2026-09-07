"""Shared helpers for the trek tools: Overpass with backoff, haversine, GPX namespaces."""
import math
import sys
import time

import requests

UA = {"User-Agent": "trek-site-template/1.0 (personal hiking plan; https://github.com/Yarden-zamir/trek-site-template)"}
NS = "http://www.topografix.com/GPX/1/1"
OSMAND = "https://osmand.net"


def overpass(query: str, timeout: int = 240) -> dict:
    """Run an Overpass query; back off on 429/504 which the public server returns often."""
    for attempt in range(8):
        r = requests.post("https://overpass-api.de/api/interpreter", data={"data": query}, headers=UA, timeout=timeout)
        if r.status_code in (429, 504, 502):
            wait = 15 * (attempt + 1)
            print(f"overpass {r.status_code}, retry in {wait}s", file=sys.stderr)
            time.sleep(wait)
            continue
        r.raise_for_status()
        time.sleep(3)
        return r.json()
    raise SystemExit("Overpass keeps rate limiting; wait a few minutes and rerun")


def hav(a, b) -> float:
    """Metres between two (lat, lon) pairs."""
    R = 6371000
    la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 2 * R * math.asin(math.sqrt(h))
