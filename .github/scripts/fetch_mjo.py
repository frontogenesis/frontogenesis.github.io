#!/usr/bin/env python3
# Fetches the BOM MJO RMM index server-side. BOM's endpoint sits behind an
# Akamai WAF that 403s direct/cross-origin browser requests, so this can't
# be fetched client-side from vp200_regression_maps/index.html. This script
# runs from a scheduled GitHub Action instead, and the result is committed
# as a same-origin static file the page fetches directly.
import json
import sys
import urllib.request
from pathlib import Path

URL = "https://www.bom.gov.au/jtwc/mjo/bamford-rmm-1-2.json"
OUTPUT = Path(__file__).resolve().parent.parent.parent / "vp200_regression_maps" / "mjo-rmm.json"

# Deliberately NOT a spoofed browser User-Agent: a UA string claiming to be
# Chrome/Firefox but sent over curl/urllib's actual TLS handshake trips
# Akamai's bot detection into a silent connection hold (15s+ with no
# response) rather than a fast reject. A plain/identifying UA gets a fast
# 403 instead, which is what we want in CI.
HEADERS = {
    "User-Agent": "vp200-mjo-fetch/1.0 (+https://weatherprogrammer.com)",
    "Referer": "https://www.bom.gov.au/jtwc/mjo/",
    "Accept": "application/json, text/plain, */*",
}


def main() -> None:
    req = urllib.request.Request(URL, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            body = resp.read()
    except Exception as exc:
        print(f"fetch failed: {exc}", file=sys.stderr)
        sys.exit(1)

    try:
        data = json.loads(body)
    except json.JSONDecodeError as exc:
        print(f"response was not valid JSON: {exc}", file=sys.stderr)
        sys.exit(1)

    if not isinstance(data.get("data"), list) or not data["data"]:
        print("response JSON missing expected 'data' array", file=sys.stderr)
        sys.exit(1)

    OUTPUT.write_text(json.dumps(data, indent=2) + "\n")
    print(f"wrote {OUTPUT} ({len(data['data'])} records)")


if __name__ == "__main__":
    main()
