import pandas as pd
import pytest
from unittest.mock import patch, MagicMock

from services.youtube import fetch_youtube_metrics
from utils.cleaner import clean_dataframe
from utils.uploader import upload_to_bigquery

# ----------------------------
# 1. Mocks
# ----------------------------
@pytest.fixture
def mock_youtube_api():
    with patch("services.youtube.requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "columnHeaders": [
                {"name": "day"},
                {"name": "video"},
                {"name": "views"},
                {"name": "impressions"},
                {"name": "clicks"},
            ],
            "rows": [
                ["2025-01-01", "vid1", "1000", "10000", "500"],
                ["2025-01-02", "vid2", "2000", "20000", "1200"],
            ],
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        yield mock_get

@pytest.fixture
def mock_secret_manager():
    with patch("utils.auth.secretmanager.SecretManagerServiceClient") as mock_client:
        mock_secret = MagicMock()
        mock_secret.payload.data.decode.return_value = "fake_api_key"
        mock_client.return_value.access_secret_version.return_value = mock_secret
        yield mock_client

@pytest.fixture
def mock_bigquery():
    with patch("utils.uploader.bigquery.Client") as mock_client:
        yield mock_client

# ----------------------------
# 2. Tests
# ----------------------------
def test_youtube_fetch(mock_secret_manager, mock_youtube_api):
    print("Testing YouTube fetch...")
    data = fetch_youtube_metrics()
    
    assert "raw_data" in data
    assert isinstance(data["raw_data"], list)
    assert len(data["raw_data"]) == 2
    assert data["raw_data"][0]["video"] == "vid1"
    print("YouTube fetch test passed!\n")

def test_cleaner():
    print("Testing cleaner...")
    data = [
        {
            "day": "2025-01-01",
            "video": "vid1",
            "views": "1000",
            "impressions": "10000",
            "clicks": "500",
            "estimatedMinutesWatched": "100",
            "averageViewDuration": "60",
        }
    ]
    df = pd.DataFrame(data)
    cleaned = clean_dataframe(df, source="youtube")

    assert "loaded_at" in cleaned.columns
    assert "ctr" in cleaned.columns
    assert cleaned["views"].dtype == "int64"
    assert cleaned["ctr"].iloc[0] == 0.05
    print("Cleaner test passed!\n")

def test_bigquery_upload(mock_bigquery):
    print("Testing BigQuery load...")
    df = pd.DataFrame([{"date": "2025-01-01", "views": 100}])
    table_id = "test-project.marketing_data.youtube"
    
    upload_to_bigquery(df, table_id)

    mock_bigquery.return_value.load_table_from_file.assert_called_once()
    print("BigQuery upload test passed!\n")

if __name__ == "__main__":
    pytest.main([__file__])