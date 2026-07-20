"""Strava API client.

Uses a stored refresh token to mint short-lived access tokens, so it runs
headless with no login prompts, no MFA. Credentials come from the environment:
STRAVA_CLIENT_ID, STRAVA_CLIENT_SECRET, STRAVA_REFRESH_TOKEN.
"""

import os
from datetime import datetime

import requests

API = "https://www.strava.com/api/v3"
RIDE_TYPES = {"Ride", "VirtualRide", "GravelRide", "MountainBikeRide", "EBikeRide"}


def get_access_token():
    """Exchange the refresh token for a short-lived access token."""
    resp = requests.post(
        "https://www.strava.com/oauth/token",
        data={
            "client_id": os.environ["STRAVA_CLIENT_ID"],
            "client_secret": os.environ["STRAVA_CLIENT_SECRET"],
            "refresh_token": os.environ["STRAVA_REFRESH_TOKEN"],
            "grant_type": "refresh_token",
        },
        timeout=30,
    )
    if not resp.ok:
        raise SystemExit(
            f"Strava token exchange failed ({resp.status_code}): {resp.text}\n"
            "Check STRAVA_CLIENT_SECRET and STRAVA_REFRESH_TOKEN in .env "
            "(it must be the refresh_token, not the code or the access_token)."
        )
    return resp.json()["access_token"]


def _headers(token):
    return {"Authorization": f"Bearer {token}"}


def get_rides_since(token, since_date):
    """List ride activities on or after a YYYY-MM-DD date."""
    after = int(datetime.fromisoformat(since_date).timestamp())
    rides, page = [], 1
    while True:
        resp = requests.get(
            f"{API}/athlete/activities",
            headers=_headers(token),
            params={"after": after, "per_page": 50, "page": page},
            timeout=30,
        )
        if not resp.ok:
            raise SystemExit(
                f"Strava activities fetch failed ({resp.status_code}): {resp.text}"
            )
        batch = resp.json()
        if not batch:
            break
        rides.extend(
            a for a in batch
            if a.get("type") in RIDE_TYPES or a.get("sport_type") in RIDE_TYPES
        )
        if len(batch) < 50:
            break
        page += 1
    return rides


def get_activity_detail(token, activity_id):
    """Full activity detail (calories, weighted_average_watts, etc.)."""
    resp = requests.get(
        f"{API}/activities/{activity_id}",
        headers=_headers(token),
        params={"include_all_efforts": "false"},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()


def get_streams(token, activity_id):
    """Per-point streams for the map and charts. Returns {} if none."""
    keys = "latlng,altitude,heartrate,watts,cadence,velocity_smooth,distance,time"
    resp = requests.get(
        f"{API}/activities/{activity_id}/streams",
        headers=_headers(token),
        params={"keys": keys, "key_by_type": "true"},
        timeout=30,
    )
    if resp.status_code == 404:
        return {}
    resp.raise_for_status()
    return resp.json()
