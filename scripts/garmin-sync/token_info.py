#!/usr/bin/env python3
"""Validate a garmin token store and report what it holds and when it expires.

    python token_info.py /tmp/garmin_tokens

Exits non-zero if the store is unusable. Used by the sync workflow so a token
problem is reported as a token problem, rather than surfacing later as an
opaque auth error in the middle of a sync.
"""

import base64
import json
import sys
import time
from pathlib import Path


def jwt_exp(token):
    """Expiry epoch from a JWT, or None if it isn't one / has no exp."""
    try:
        parts = str(token).split(".")
        if len(parts) < 2:
            return None
        pad = parts[1] + "=" * (-len(parts[1]) % 4)
        return json.loads(base64.urlsafe_b64decode(pad.encode()).decode()).get("exp")
    except Exception:
        return None


def describe(name, token):
    if not token:
        return f"  {name}: absent"
    exp = jwt_exp(token)
    if not exp:
        # An opaque refresh token is normal; only the access token is a JWT.
        return f"  {name}: present (opaque, expiry not readable)"
    left = exp - time.time()
    when = time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime(exp))
    if left <= 0:
        return f"  {name}: EXPIRED at {when}"
    days, hours = int(left // 86400), int(left % 86400 // 3600)
    return f"  {name}: valid until {when} ({days}d {hours}h left)"


def main():
    path = Path(sys.argv[1] if len(sys.argv) > 1 else "/tmp/garmin_tokens")
    store = path / "garmin_tokens.json" if path.is_dir() else path
    if not store.exists():
        sys.exit(f"::error::No token at {store}. Run scripts/garmin-sync/mint-token.py")
    try:
        data = json.loads(store.read_text())
    except Exception as e:
        sys.exit(f"::error::Token file is not valid JSON: {e}")

    print("Garmin token store:")
    print(describe("di_token        ", data.get("di_token")))
    print(describe("di_refresh_token", data.get("di_refresh_token")))
    print(f"  di_client_id: {'present' if data.get('di_client_id') else 'absent'}")

    # di_token is short-lived and refreshes itself from di_refresh_token, so an
    # expired one is routine. Losing di_refresh_token is what forces a re-login.
    if not data.get("di_refresh_token"):
        sys.exit("::error::No di_refresh_token - the session cannot renew itself. "
                 "Re-run scripts/garmin-sync/mint-token.py")

    exp = jwt_exp(data.get("di_refresh_token"))
    if exp and exp - time.time() < 7 * 86400:
        print("::warning::Garmin refresh token expires within 7 days. "
              "Run scripts/garmin-sync/mint-token.py to renew it.")


if __name__ == "__main__":
    main()
