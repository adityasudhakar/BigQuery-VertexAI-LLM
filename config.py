# config.py
from google.auth import default
from google.cloud import bigquery

# Google Cloud authentication
credentials, project = default()

# Project settings
PROJECT_ID = "spartan-acrobat-536"
LOCATION = "us-central1"
REQUESTS_PER_MINUTE = 100

# BigQuery settings
dataset_id = 'javascript'
table_name = 'pages'
table_uri = f"bigquery://{PROJECT_ID}/{dataset_id}"

# Initialize BigQuery client
client = bigquery.Client(project=PROJECT_ID)
