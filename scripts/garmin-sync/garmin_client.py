"""Garmin Connect API client wrapper."""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path

from garminconnect import Garmin


def create_client():
    """Create and authenticate a Garmin Connect client."""
    email = os.environ["GARMIN_EMAIL"]
    password = os.environ["GARMIN_PASSWORD"]
    token_path = str(Path(os.environ.get("GARMIN_TOKEN_PATH", "/tmp/garmin_tokens")))

    # prompt_mfa lets Garmin ask for the 2FA code interactively when needed.
    def _prompt_mfa():
        return input("Enter Garmin MFA code: ").strip()

    client = Garmin(email, password, prompt_mfa=_prompt_mfa)
    # Passing the token path makes login() reuse a saved session if one exists
    # (no MFA), otherwise log in fresh and save the session for next time.
    client.login(token_path)
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
