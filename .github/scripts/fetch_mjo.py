#!/usr/bin/env python3
# Fetches NOAA PSL's near-real-time CORe VPM (Velocity Potential MJO) index
# and writes the latest PC1/PC2/amplitude as JSON next to the VP200 tool's
# static assets, for vp200_regression_maps/index.html to read same-origin.
#
# BOM's RMM feed blocks automated access. ROMI (OLR-only) is openly served
# but can disagree with velocity-potential diagnostics. VPM is built like
# Wheeler-Hendon RMM, replacing OLR with 200 hPa velocity potential plus
# U200 and U850 (Ventrice et al. 2013), from the CORe reanalysis — a better
# match for the VP200 correlation maps on this page.
import json
import sys
import urllib.request
from pathlib import Path

URL = "https://www.psl.noaa.gov/mjo/mjoindex/vpm.1x.CORe.txt"
OUTPUT = Path(__file__).resolve().parent.parent.parent / "vp200_regression_maps" / "mjo-rmm.json"


def main() -> None:
    req = urllib.request.Request(URL, headers={"User-Agent": "vp200-mjo-fetch/1.1"})
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
        "source": "NOAA PSL CORe VPM (velocity potential MJO index)",
        "date": f"{int(year):04d}-{int(month):02d}-{int(day):02d}",
        "pc1": float(pc1),
        "pc2": float(pc2),
        "amplitude": float(amplitude),
    }

    OUTPUT.write_text(json.dumps(out, indent=2) + "\n")
    print(f"wrote {OUTPUT}: {out}")


if __name__ == "__main__":
    main()
