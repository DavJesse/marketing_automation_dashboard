import pandas as pd
from google.cloud import bigquery
import json

def upload_to_bigquery(
    df: pd.DataFrame,
    table_id: str,
    write_disposition: str = "WRITE_APPEND"
):
    """
    Load dataframe directly into BigQuery.
    table_id example: "project_id.dataset.table"
    """

    if df.empty:
        raise ValueError("Cannot load empty DataFrame to BigQuery")

    # ---------------------------------
    # 1. Load BigQuery schema from config
    # ---------------------------------
    with open("config/big_query_schema.json", "r") as f:
        schema_config = json.load(f)
    
    table_key = table_id.split(".")[-1]
    if table_key not in schema_config:
        raise ValueError(f"Schema not found for table: {table_key}")

    schema = [
        bigquery.SchemaField(f["name"], f["type"], f["mode"])
        for f in schema_config[table_key]["schema"]
    ]

    # ---------------------------------
    # 2. Set up BigQuery load job
    # ---------------------------------
    client = bigquery.Client()

    job_config = bigquery.LoadJobConfig(
        schema=schema,
        write_disposition=write_disposition,
        source_format=bigquery.SourceFormat.PARQUET,
    )

    # ---------------------------------
    # 3. Convert df and upload
    # ---------------------------------
    parquet_bytes = df.to_parquet(index=False)

    load_job = client.load_table_from_file(
        file_obj=parquet_bytes,
        destination=table_id,
        job_config=job_config,
        rewind=True,
    )

    load_job.result()  # Wait for job to finish

    print(f"Loaded {df.shape[0]} rows into {table_id}")