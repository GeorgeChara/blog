#!/usr/bin/env python3
"""One-time Strava authorization.

Prints the authorize URL, takes the code you get back, exchanges it for a
refresh token, and writes that token into .env. Run once:

    ./.venv/bin/python authorize.py

Requires STRAVA_CLIENT_SECRET to already be set in .env.
"""

import re
import sys
from pathlib import Path

import requests

ENV_PATH = Path(__file__).resolve().parent / ".env"


def load_env():
    env = {}
    if ENV_PATH.exists():
        for line in ENV_PATH.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("=")
                env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def set_env_value(key, value):
    lines = ENV_PATH.read_text().splitlines() if ENV_PATH.exists() else []
    out, found = [], False
    for line in lines:
        if line.strip().startswith(f"{key}="):
            out.append(f"{key}={value}")
            found = True
        else:
            out.append(line)
    if not found:
        out.append(f"{key}={value}")
    ENV_PATH.write_text("\n".join(out) + "\n")


def main():
    env = load_env()
    cid = env.get("STRAVA_CLIENT_ID") or "180279"
    secret = env.get("STRAVA_CLIENT_SECRET")
    if not secret or "your_client_secret" in secret:
        print("Set STRAVA_CLIENT_SECRET in .env first, then re-run.")
        return 1

    url = (
        "https://www.strava.com/oauth/authorize?"
        f"client_id={cid}&response_type=code&redirect_uri=http://localhost"
        "&approval_prompt=force&scope=activity:read_all"
    )
    print("\n1) Open this URL in your browser and click Authorize:\n")
    print("   " + url + "\n")
    print("2) It redirects to a localhost page that won't load, that's fine.")
    print("   Copy the whole URL from the address bar (or just the code) and paste below.\n")

    raw = input("Paste the redirect URL or code: ").strip()
    m = re.search(r"code=([0-9a-fA-F]+)", raw)
    code = m.group(1) if m else raw

    resp = requests.post(
        "https://www.strava.com/oauth/token",
        data={
            "client_id": cid,
            "client_secret": secret,
            "code": code,
            "grant_type": "authorization_code",
        },
        timeout=30,
    )
    if not resp.ok:
        print(f"\nExchange failed ({resp.status_code}): {resp.text}")
        print("If it says the code is invalid, it was already used or expired, "
              "just re-run and authorize again for a fresh code.")
        return 1

    data = resp.json()
    set_env_value("STRAVA_REFRESH_TOKEN", data["refresh_token"])
    print(f"\nSuccess. Scopes granted: {data.get('scope', '')}")
    print("Refresh token saved to .env.")
    print("\nNow run:  ./.venv/bin/python sync.py --full")
    return 0


if __name__ == "__main__":
    sys.exit(main())
