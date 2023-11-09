from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

# Import your processing functions
from src.data_ingestion import load_csv_data
from src.data_processing import create_drug_graph
from src.data_output import write_graph_to_json
from src.utils import log

# These args will be passed on to each operator
# You can override them on a per-task basis during operator initialization
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email": ["samizouirech@gmail.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

# Define the DAG, its schedule, and set it to start in the past
dag = DAG(
    "drug_mentions_pipeline",
    default_args=default_args,
    description="Pipeline for processing drug mentions",
    schedule_interval=timedelta(days=1),
    start_date=datetime(2023, 1, 1),
    catchup=False,
)

# Define the data ingestion task
ingest_task = PythonOperator(
    task_id="data_ingestion",
    python_callable=load_csv_data,
    op_kwargs={
        "drugs_path": "/path/to/drugs.csv",
        "pubmed_path": "/path/to/pubmed.csv",
        "clinical_trials_path": "/path/to/clinical_trials.csv",
        "pubmed_json_path": "/path/to/pubmed.json",
    },
    dag=dag,
)

# Define the data processing task
process_task = PythonOperator(
    task_id="data_processing",
    python_callable=create_drug_graph,
    provide_context=True,
    dag=dag,
)

# Define the data output task
output_task = PythonOperator(
    task_id="data_output",
    python_callable=write_graph_to_json,
    provide_context=True,
    op_kwargs={"output_path": "/path/to/drug_graph.json"},
    dag=dag,
)

# Set the order of tasks in the DAG
ingest_task >> process_task >> output_task
