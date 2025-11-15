import pandas as pd

def clean_youtube_df(df: pd.DataFrame) -> pd.DataFrame:
    """Specific cleaning for YouTube data."""

    if df.empty:
        return df

    # Rename columns for consistency
    df = df.rename(
        columns={
            "day": "date",
            "video": "video_id",
            "channel": "channel_id",
            "deviceType": "device_type",
            "trafficSourceType": "traffic_source_type",
            "estimatedMinutesWatched": "estimated_minutes_watched",
            "averageViewDuration": "average_view_duration",
        }
    )

    # Convert data types
    for col in ["views", "impressions", "clicks", "estimated_minutes_watched"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)

    # Safely calculate Click-Through Rate (CTR)
    df["ctr"] = df.apply(
        lambda row: row["clicks"] / row["impressions"] if row["impressions"] > 0 else 0,
        axis=1,
    )

    df["average_view_duration"] = (
        pd.to_numeric(df["average_view_duration"], errors="coerce").fillna(0).astype(float)
    )
    df["date"] = pd.to_datetime(df["date"])

    return df


def clean_dataframe(df: pd.DataFrame, source: str) -> pd.DataFrame:
    """
    Standard cleaning pipeline for all marketing sources.
    Normalizes col names, adds timestamps, enforces data types.
    """

    if df is None or df.empty:
        raise ValueError("No data returned from API")

    cleaned = df.copy()

    # Source-specific cleaning
    if source == "youtube":
        cleaned = clean_youtube_df(cleaned)

    # Generic cleaning
    cleaned.columns = (
        cleaned.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )
    cleaned["loaded_at"] = pd.Timestamp.utcnow()
    cleaned = cleaned.dropna(axis=1, how="all")

    return cleaned