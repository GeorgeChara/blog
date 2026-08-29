#!/usr/bin/env python3
"""Log in to Garmin once and load the token blob into the GitHub secret.

    python scripts/garmin-sync/mint-token.py

Asks for your Garmin email, password and MFA code, then sets GARMIN_TOKEN_B64
directly via gh. Nothing goes near the clipboard: an earlier version copied the
blob for you to paste, and when the login failed it left the *previous*
clipboard contents in place, which sailed into the secret and failed in CI as
"base64: invalid input". Setting it here means a failed login sets nothing.

The token pair Garmin issues is good for roughly a year, but only if the
refreshed copy is kept. The workflow unpacks it to /tmp and throws the refresh
away with the runner, so it goes stale in weeks unless the persist-back step
is wired up.
"""

import base64
import getpass
import io
import json
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path

REPO = "GeorgeChara/blog"
SECRET = "GARMIN_TOKEN_B64"

try:
    from garminconnect import Garmin
except ImportError:
    # Homebrew python is externally managed, so a plain "pip install" here is
    # refused (PEP 668). Re-exec under the sibling venv rather than making the
    # caller remember which interpreter has the library.
    import os
    venv = Path(__file__).resolve().parent / ".venv" / "bin" / "python"
    if venv.exists() and not os.environ.get("_GARMIN_REEXEC"):
        os.environ["_GARMIN_REEXEC"] = "1"
        os.execv(str(venv), [str(venv), str(Path(__file__).resolve()), *sys.argv[1:]])
    sys.exit("Missing garminconnect. Run:\n"
             "  python3 -m venv scripts/garmin-sync/.venv\n"
             "  scripts/garmin-sync/.venv/bin/pip install garminconnect")


def die(msg):
    sys.exit(f"\nFAILED: {msg}\nThe secret was not touched.")


def main():
    if not sys.stdin.isatty():
        sys.exit("This asks for your password and an MFA code, so it needs a real\n"
                 "terminal. Run it in a normal shell, not through a wrapper.")

    out = Path(tempfile.mkdtemp()) / "garmin_tokens"
    email = input("Garmin email: ").strip()
    password = getpass.getpass("Garmin password: ")

    client = Garmin(email, password, prompt_mfa=lambda: input("MFA code: ").strip())
    try:
        client.login(str(out))
    except Exception as e:
        die(f"Garmin login: {type(e).__name__}: {e}")

    if not out.is_dir():
        die("login returned but wrote no token directory")

    # ._ files are macOS resource forks that tar adds; they are not tokens, and
    # seeing one in the runner log is what made a stale token look like a good one.
    files = sorted(p.name for p in out.iterdir() if not p.name.startswith("._"))
    if not files:
        die("token directory is empty")
    print(f"\nLogged in. Token files: {', '.join(files)}")

    # garminconnect 0.3.x dropped the oauth1/oauth2 file pair for a single
    # garmin_tokens.json holding di_token + di_refresh_token. The refresh token
    # is the long-lived half: without it the session cannot renew itself.
    store = out / "garmin_tokens.json"
    if not store.exists():
        die(f"expected garmin_tokens.json, got: {', '.join(files)}")
    try:
        data = json.loads(store.read_text())
    except Exception as e:
        die(f"token file is not valid JSON: {e}")
    if not data.get("di_refresh_token"):
        die("no di_refresh_token. Without it the session cannot refresh itself\n"
            "        and would expire early. Not worth storing - try again.")
    print("Token has: " + ", ".join(k for k, v in sorted(data.items()) if v))

    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w:gz") as tar:
        for f in sorted(out.iterdir()):
            if f.name.startswith("._"):
                continue
            tar.add(f, arcname=f"garmin_tokens/{f.name}")
    blob = base64.b64encode(buf.getvalue()).decode()

    # Decode it back the way the runner will, so a bad blob fails here and not
    # in CI twenty minutes later.
    try:
        with tarfile.open(fileobj=io.BytesIO(base64.b64decode(blob, validate=True))) as tar:
            members = sorted(tar.getnames())
    except Exception as e:
        die(f"blob did not round-trip: {type(e).__name__}: {e}")
    print(f"Blob is {len(blob)} chars and unpacks to: {', '.join(members)}")

    if input(f"\nSet {SECRET} on {REPO}? [y/N] ").strip().lower() != "y":
        sys.exit("Nothing set.")

    r = subprocess.run(["gh", "secret", "set", SECRET, "--repo", REPO],
                       input=blob.encode())
    if r.returncode != 0:
        die("gh secret set failed - is gh logged in?")
    print(f"\nDone. {SECRET} updated.")
    print("Run the sync with:  gh workflow run 'Sync Garmin Activities' --repo " + REPO)


if __name__ == "__main__":
    main()
