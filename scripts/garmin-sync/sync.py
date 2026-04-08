#!/usr/bin/env python3
"""Sync cycling activities from Garmin Connect to Hugo blog.

Usage:
    python sync.py                   # Sync new activities since last sync
    python sync.py --full            # Re-sync all activities
    python sync.py --days 30         # Sync last 30 days
"""

import argparse
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

from garmin_client import create_client, download_gpx, get_activities_since
from hugo_writer import ACTIVITIES_DIR, DATA_DIR, update_summary, write_activity

SYNC_STATE_PATH = DATA_DIR / "last_sync.json"


def load_sync_state():
    """Load the last sync state."""
    if SYNC_STATE_PATH.exists():
        return json.loads(SYNC_STATE_PATH.read_text())
    return {"last_sync": None, "known_ids": []}


def save_sync_state(state):
    """Save sync state."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    SYNC_STATE_PATH.write_text(json.dumps(state, indent=2))


def collect_existing_summaries():
    """Read existing activity JSON files to build the full ride list."""
    summaries = []
    if not ACTIVITIES_DIR.exists():
        return summaries

    for json_file in ACTIVITIES_DIR.glob("*.json"):
        try:
            data = json.loads(json_file.read_text())
            summaries.append({
                "id": data["id"],
                "name": data["name"],
                "date": data["date"][:10],  # YYYY-MM-DD
                "distance_km": data["distance_km"],
                "elevation_gain_m": data.get("elevation_gain_m", 0),
                "duration": _format_duration(data.get("duration_seconds", 0)),
                "avg_speed_kmh": data.get("avg_speed_kmh", 0),
                "slug": json_file.stem,  # Will be overwritten by write_activity
            })
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Warning: skipping {json_file.name}: {e}")

    return summaries


def _format_duration(seconds):
    """Format seconds to human-readable duration."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    if hours > 0:
        return f"{hours}h {minutes:02d}m"
    return f"{minutes}m"


def main():
    parser = argparse.ArgumentParser(description="Sync Garmin activities to Hugo")
    parser.add_argument("--full", action="store_true", help="Re-sync all activities")
    parser.add_argument("--days", type=int, default=None, help="Sync last N days")
    args = parser.parse_args()

    print("Authenticating with Garmin Connect...")
    client = create_client()

    state = load_sync_state()
    known_ids = set(state.get("known_ids", []))

    # Determine sync start date
    if args.full:
        since_date = "2020-01-01"
    elif args.days:
        since_date = (datetime.now() - timedelta(days=args.days)).strftime("%Y-%m-%d")
    elif state["last_sync"]:
        since_date = state["last_sync"]
    else:
        since_date = (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")

    print(f"Fetching activities since {since_date}...")
    activities = get_activities_since(client, since_date)
    print(f"Found {len(activities)} cycling activities")

    new_count = 0
    new_summaries = []

    for activity in activities:
        activity_id = str(activity["activityId"])

        if activity_id in known_ids and not args.full:
            continue

        name = activity.get("activityName") or "Ride"
        print(f"  Processing: {name} ({activity_id})")

        try:
            gpx_xml = download_gpx(client, activity["activityId"])
            summary = write_activity(activity, gpx_xml)
            new_summaries.append(summary)
            known_ids.add(activity_id)
            new_count += 1
        except Exception as e:
            print(f"  Error processing {activity_id}: {e}")
            continue

    if new_count > 0:
        # Rebuild summary from all existing + new activities
        all_summaries = collect_existing_summaries()
        # Merge new summaries (update if already exists)
        existing_ids = {s["id"] for s in all_summaries}
        for s in new_summaries:
            if s["id"] not in existing_ids:
                all_summaries.append(s)

        update_summary(all_summaries)
        print(f"Added {new_count} new activities, updated summary")
    else:
        print("No new activities to sync")

    # Save sync state
    state["last_sync"] = datetime.now().strftime("%Y-%m-%d")
    state["known_ids"] = list(known_ids)
    save_sync_state(state)

    print("Sync complete!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
