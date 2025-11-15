import requests
import json
from datetime import datetime, timedelta
import pandas as pd
import pytz

from utils.auth import get_secret


def fetch_youtube_metrics():
    """Fetch raw YouTube metrics from the YouTube Analytics API."""

    # ---------------------------------
    # 1. Load settings & secrets
    # ---------------------------------
    with open("config/settings.json", "r") as f:
        settings = json.load(f)["youtube"]

    api_key = get_secret(settings["secret_api_key"])

    # ---------------------------------
    # 2. Set up API parameters
    # ---------------------------------
    end_date = datetime.now(pytz.UTC).date() - timedelta(days=settings["end_date_days_ago"])
    start_date = datetime.now(pytz.UTC).date() - timedelta(days=settings["start_date_days_ago"])

    params = {
        "ids": "channel==MINE",
        "startDate": start_date.strftime("%Y-%m-%d"),
        "endDate": end_date.strftime("%Y-%m-%d"),
        "metrics": ",".join(settings["metrics"]),
        "dimensions": ",".join(settings["dimensions"]),
        "key": api_key,
    }

    if settings.get("default_filters"):
        params["filters"] = settings["default_filters"]

    # ---------------------------------
    # 3. Make API request
    # ---------------------------------
    response = requests.get(settings["api_url"], params=params)
    response.raise_for_status()
    data = response.json()

    # ---------------------------------
    # 4. Process response
    # ---------------------------------
    if not data.get("rows"):
        print("[WARNING] No data returned from YouTube API")
        return {"platform": "youtube", "raw_data": []}

    df = pd.DataFrame(data["rows"], columns=[h["name"] for h in data["columnHeaders"]])

    return {"platform": "youtube", "raw_data": df.to_dict("records")}
