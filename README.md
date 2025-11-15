# Marketing Data Automation Pipeline

This project is a data pipeline that automates the daily collection and reporting of marketing data from various sources like YouTube. The collected data is cleaned, processed, and uploaded to Google BigQuery for analysis and visualization in tools like Looker Studio.

## Features

- **Automated Data Collection**: Fetches marketing data from various APIs (currently supports YouTube Analytics).
- **Data Cleaning and Transformation**: Cleans and transforms the raw data into a structured format for analysis.
- **BigQuery Integration**: Loads the cleaned data into Google BigQuery.
- **Cloud Function Ready**: Designed to be deployed as a Google Cloud Function, triggered by Pub/Sub messages.
- **Extensible**: Easily extensible to support more data sources.
- **Testing**: Includes a suite of tests to ensure data integrity and pipeline reliability.

## Architecture

The pipeline is designed to be a serverless, event-driven architecture running on Google Cloud Platform.

1.  **Trigger**: A Pub/Sub message triggers the Cloud Function. The message contains the data source to be processed (e.g., `{"source": "youtube"}`).
2.  **Fetch**: The Cloud Function calls the appropriate service (e.g., `services/youtube.py`) to fetch the data from the marketing API.
3.  **Clean**: The raw data is passed to a cleaning module (`utils/cleaner.py`) that cleans, transforms, and enriches the data.
4.  **Load**: The cleaned data is loaded into a BigQuery table using the `utils/uploader.py` module.

## Setup and Installation

### Prerequisites

- Python 3.10 or higher
- Google Cloud SDK installed and configured on your local machine.

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/marketing-automation-dashboard.git
cd marketing-automation-dashboard
```

### 2. Create a Virtual Environment

It is recommended to use a virtual environment to manage the project's dependencies.

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the Project

You need to configure the following files:

- **`config/settings.json`**:
  - `start_date_days_ago` and `end_date_days_ago`: Define the date range for the data to be fetched.
  - `secret_api_key`: The full resource ID of your YouTube API key secret in Google Secret Manager.
- **`config/big_query_schema.json`**:
  - `table_id`: The full BigQuery table ID where the data will be loaded (e.g., `your-project-id.your_dataset.your_table`).
  - `schema`: The schema of the BigQuery table.
- **`.env.yaml`** (create this file in the root directory):
    ```yaml
    GCP_PROJECT: 'YOUR_PROJECT_ID'
    ```

### 5. Google Cloud Authentication

Authenticate your local environment with Google Cloud:

```bash
gcloud auth application-default login
```

## Running the Pipeline

### Running Locally

You can run the pipeline locally for testing and development using the `run_local.py` script.

```bash
python run_local.py
```

### Deploying to Google Cloud

This program is designed to be deployed as a Google Cloud Function.

1.  **Deploy the function**:

    ```bash
    gcloud functions deploy marketing-automation-pipeline \
        --runtime python312 \
        --trigger-topic marketing-data-topic \
        --entry-point entry_point \
        --source . \
        --env-vars-file .env.yaml
    ```

2.  **Trigger the function**:

    Publish a message to the Pub/Sub topic to trigger the function:

    ```bash
    gcloud pubsub topics publish marketing-data-topic --message '{"source": "youtube"}'
    ```

## Testing

The project includes a suite of tests to ensure the pipeline is working correctly. To run the tests, you need to install `pytest` and `pytest-mock`:

```bash
pip install pytest pytest-mock
```

Then, run the tests using the following command:

```bash
python -m pytest tests/test_local.py
```

## Project Structure

```
.
├── config
│   ├── big_query_schema.json     # BigQuery table schema
│   └── settings.json             # Pipeline settings
├── main.py                     # Cloud Function entry point
├── requirements.txt            # Python dependencies
├── run_local.py                # Script to run the pipeline locally
├── services
│   ├── __init__.py
│   └── youtube.py                # YouTube data fetching logic
├── tests
│   └── test_local.py             # Local tests
└── utils
    ├── __init__.py
    ├── auth.py                   # Google Secret Manager authentication
    ├── cleaner.py                # Data cleaning and transformation logic
    └── uploader.py               # BigQuery data loading logic
```
