---
name: weatherprogrammer-pages
description: Static site chrome for weatherprogrammer.com. Product forecast folders are owned by misc publish pipelines, not this repo's seed.
---

# weatherprogrammer.com (GitHub Pages mirror)

## Site ownership

Live **weatherprogrammer.com** is **S3 + CloudFront**, not GitHub Pages alone.

| What | Edit where | Publish how |
|------|------------|-------------|
| Homepage, layouts, assets, static tools | this repo (`github_pages`) | Jekyll Pages deploy and/or `misc/site_publish/seed_site.sh` |
| `tropical_forcing/`, `polar_vortex/`, `subseasonal/`, `seasonal/`, `fog/` | **`misc/<product>/site/`** (HTML) + Action outputs (PNGs/meta) | `python -m <product>.publish_pages --s3` from **misc** |
| `vp200_regression_maps/mjo-rmm.json` | `misc/site_publish/fetch_mjo.py` | Hetzner timer at 1:00 PM America/Chicago → S3 |

## Hard rules

- Do **not** treat `tropical_forcing/index.html` (or other product `index.html` files) in this repo as source of truth if they disagree with `misc/<product>/site/index.html`.
- Do **not** run a full S3 seed that uploads product folders. `seed_site.sh` excludes them; do not bypass that.
- Favicon / chrome changes may touch product HTML only for shared head tags; if you change product page body/controls, change **misc** first and republish with `--s3`.
- After editing product HTML in misc, keep this repo's copy in sync (or leave it alone and rely on the seed exclude) so a future agent does not "restore" a stale ECMWF-only page.
