#!/usr/bin/env python3
# Fetches the near-real-time OMI (ROMI) MJO index from NOAA PSL and writes
# the latest PC1/PC2/amplitude as JSON next to the VP200 tool's static
# assets, for vp200_regression_maps/index.html to read same-origin.
#
# The original source, BOM's RMM feed, explicitly blocks all automated
# access -- its 403 page states "The Bureau of Meteorology website does
# not support web scraping: if you are trying to access Bureau data
# through automated means, you should stop." ROMI is NOAA's openly served
# near-real-time OMI index, built by Kiladis et al. (2014) to reproduce
# the same 8-phase convention as BOM's RMM index, with no such policy.
import json
import sys
import urllib.request
from pathlib import Path

URL = "https://psl.noaa.gov/mjo/mjoindex/romi.cpcolr.1x.txt"
OUTPUT = Path(__file__).resolve().parent.parent.parent / "vp200_regression_maps" / "mjo-rmm.json"


def main() -> None:
    req = urllib.request.Request(URL, headers={"User-Agent": "vp200-mjo-fetch/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            body = resp.read().decode("utf-8")
    except Exception as exc:
        print(f"fetch failed: {exc}", file=sys.stderr)
        sys.exit(1)

    lines = [ln for ln in body.strip().splitlines() if ln.strip()]
    if not lines:
        print("response was empty", file=sys.stderr)
        sys.exit(1)

    fields = lines[-1].split()
    if len(fields) < 7:
        print(f"unexpected line format: {lines[-1]!r}", file=sys.stderr)
        sys.exit(1)

    year, month, day, _hour, pc1, pc2, amplitude = fields[:7]
    out = {
        "source": "NOAA PSL ROMI (near-real-time OMI, CPC blended OLR)",
        "date": f"{int(year):04d}-{int(month):02d}-{int(day):02d}",
        "pc1": float(pc1),
        "pc2": float(pc2),
        "amplitude": float(amplitude),
    }

    OUTPUT.write_text(json.dumps(out, indent=2) + "\n")
    print(f"wrote {OUTPUT}: {out}")


if __name__ == "__main__":
    main()
