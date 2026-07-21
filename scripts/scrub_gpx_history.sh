#!/usr/bin/env bash
# Purge every historical GPX blob from git history and re-commit only the
# current (privacy-trimmed) versions, then force-push.
#
# RUN ORDER (important):
#   1. scripts/home.json set with your real home  (gitignored)
#   2. python scripts/trim_privacy.py             (trims working tree)
#   3. git add -A && git commit                   (commit the trimmed GPX)
#   4. bash scripts/scrub_gpx_history.sh          (this script)
#
# This REWRITES history (all commit SHAs change) and FORCE-PUSHES. Old,
# untrimmed GPX blobs are removed from every past commit. GitHub may keep old
# objects reachable by SHA in caches for a while; for total removal contact
# GitHub Support after this runs.
set -euo pipefail
cd "$(dirname "$0")/.."

echo ">> Verifying GPX are trimmed (home.json present)..."
if [ ! -f scripts/home.json ]; then
  echo "ERROR: scripts/home.json missing. Set it and run trim_privacy first." >&2
  exit 1
fi

tmp="$(mktemp -d)"
echo ">> Backing up current (trimmed) GPX to $tmp ..."
[ -d static/cycling/gpx ] && cp -r static/cycling/gpx "$tmp/gpx"
[ -d static/cycling/routes ] && cp -r static/cycling/routes "$tmp/routes"

origin="$(git remote get-url origin)"
echo ">> Remote: $origin"

echo ">> Purging GPX paths from ALL history (git-filter-repo)..."
git filter-repo --path static/cycling/gpx --path static/cycling/routes --invert-paths --force

echo ">> Restoring trimmed GPX..."
mkdir -p static/cycling
[ -d "$tmp/gpx" ] && cp -r "$tmp/gpx" static/cycling/gpx
[ -d "$tmp/routes" ] && cp -r "$tmp/routes" static/cycling/routes
rm -rf "$tmp"

echo ">> Committing trimmed GPX afresh..."
git add static/cycling/gpx static/cycling/routes 2>/dev/null || true
git commit -m "Re-add privacy-trimmed route/ride GPX (history purged)" || echo "(nothing to commit)"

echo ">> Re-adding origin and force-pushing main..."
git remote add origin "$origin" 2>/dev/null || git remote set-url origin "$origin"
git push --force --no-verify origin main

echo ">> Done. Untrimmed GPX purged from history and force-pushed."
