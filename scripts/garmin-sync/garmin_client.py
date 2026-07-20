"""Garmin Connect API client wrapper."""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path

from garminconnect import Garmin


def create_client():
    """Create and authenticate a Garmin Connect client."""
    token_path = str(Path(os.environ.get("GARMIN_TOKEN_PATH", "/tmp/garmin_tokens")))

    # If a saved session token exists, use it: no credentials, no MFA. This is
    # what lets the GitHub Action run headlessly.
    if Path(token_path).exists():
        try:
            client = Garmin()
            client.login(token_path)
            return client
        except Exception as e:
            print(f"Saved token login failed ({e}); trying a fresh login.")

    # Fresh login needs credentials and a one-time MFA code, so this path only
    # works interactively on your own machine, not in CI.
    email = os.environ["GARMIN_EMAIL"]
    password = os.environ["GARMIN_PASSWORD"]

    def _prompt_mfa():
        return input("Enter Garmin MFA code: ").strip()

    client = Garmin(email, password, prompt_mfa=_prompt_mfa)
    client.login(token_path)  # loads if present, else logs in and saves
    return client


def get_activities_since(client, since_date):
    """Fetch activities since a given date.

    Args:
        client: Authenticated Garmin client
        since_date: ISO date string (YYYY-MM-DD)

    Returns:
        List of activity dicts, newest first
    """
    start = datetime.fromisoformat(since_date)
    end = datetime.now()

    activities = client.get_activities_by_date(
        start.strftime("%Y-%m-%d"),
        end.strftime("%Y-%m-%d"),
        "cycling",
    )
    return activities


def download_gpx(client, activity_id):
    """Download GPX data for an activity.

    Returns:
        GPX XML string
    """
    gpx_data = client.download_activity(activity_id, dl_fmt=client.ActivityDownloadFormat.GPX)
    if isinstance(gpx_data, bytes):
        return gpx_data.decode("utf-8")
    return gpx_data


def get_activity_details(client, activity_id):
    """Get detailed metrics for an activity."""
    return client.get_activity(activity_id)
