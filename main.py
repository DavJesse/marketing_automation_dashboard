import json
import base64
import pandas as pd

from services.youtube import fetch_youtube_metrics
from utils.cleaner import clean_dataframe
from utils.uploader import upload_to_bigquery


def entry_point(event, context):
    """
    Cloud Function triggered by Pub/Sub.
    Determines which marketing source to fetch (YouTube, Google Ads, Meta, etc).
    """

    # ----------------------------
    # 1. Read Pub/Sub message
    # ----------------------------
    if "data" not in event:
        raise ValueError("Missing Pub/Sub data")

    message = base64.b64decode(event["data"]).decode("utf-8")
    payload = json.loads(message)

    source = payload.get("source")
    if not source:
        raise ValueError("Missing 'source' in payload")

    print(f"[INFO] Starting fetch for: {source}")

    # ----------------------------
    # 2. Route to correct service
    # ----------------------------
    if source == "youtube":
        raw_df = fetch_youtube_metrics()
    elif source == "google_ads":
        # raw_df = fetch_google_ads_metrics()
        raise NotImplementedError("Google Ads handler not yet implemented.")
    else:
        raise ValueError(f"Unknown source: {source}")

    # ----------------------------
    # 3. Clean data
    # ----------------------------
    raw_df = pd.DataFrame(raw_df["raw_data"])
    cleaned_df = clean_dataframe(raw_df, source)

    # ----------------------------
    # 4. Load to BigQuery
    # ----------------------------
    with open("config/big_query_schema.json", "r") as f:
        schema = json.load(f)

    upload_to_bigquery(
        df=cleaned_df,
        table_id=schema["youtube"]["table_id"]
    )

    print("[SUCCESS] Pipeline completed")
