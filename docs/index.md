# Marketing Automation Dashboard Documentation

This documentation provides a detailed overview of the Marketing Automation Dashboard project.

## Table of Contents

- [Project Overview](#project-overview)
- [Architecture](#architecture)
- [Getting Started](#getting-started)
- [Configuration](#configuration)
- [Running the Pipeline](#running-the-pipeline)
- [Testing](#testing)
- [Contributing](#contributing)

## Project Overview

The Marketing Automation Dashboard is a data pipeline that automates the daily collection and reporting of marketing data from various sources like YouTube. The collected data is cleaned, processed, and uploaded to Google BigQuery for analysis and visualization in tools like Looker Studio.

## Architecture

The pipeline is designed to be a serverless, event-driven architecture running on Google Cloud Platform.

1.  **Trigger**: A Pub/Sub message triggers the Cloud Function. The message contains the data source to be processed (e.g., `{"source": "youtube"}`).
2.  **Fetch**: The Cloud Function calls the appropriate service (e.g., `services/youtube.py`) to fetch the data from the marketing API.
3.  **Clean**: The raw data is passed to a cleaning module (`utils/cleaner.py`) that cleans, transforms, and enriches the data.
4.  **Load**: The cleaned data is loaded into a BigQuery table using the `utils/uploader.py` module.

## Getting Started

Please refer to the main [README.md](https://github.com/jesse/marketing-automation-dashboard/blob/main/README.md) for instructions on how to set up and install the project.

## Configuration

The project is configured through the following files:

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

## Running the Pipeline

Please refer to the main [README.md](https://github.com/jesse/marketing-automation-dashboard/blob/main/README.md) for instructions on how to run the pipeline locally or deploy it to Google Cloud.

## Testing

Please refer to the main [README.md](https://github.com/jesse/marketing-automation-dashboard/blob/main/README.md) for instructions on how to run the tests.

## Contributing

We welcome contributions from the community. Please read our [CONTRIBUTING.md](https://github.com/jesse/marketing-automation-dashboard/blob/main/CONTRIBUTING.md) file for guidelines on how to contribute to the project.

We also have a [CODE_OF_CONDUCT.md](https://github.com/jesse/marketing-automation-dashboard/blob/main/CODE_OF_CONDUCT.md) that we expect all contributors to adhere to.
