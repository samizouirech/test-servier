import os
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python_operator import PythonOperator

# Import your processing functions from the 'src' directory
from src.data_ingestion import load_csv_data
from src.data_output import write_graph_to_json
from src.data_processing import create_drug_graph

current_path = os.getcwd()
# Define default arguments for the DAG
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2023, 1, 1),
    "email": ["samizouirech@gmail.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

# Instantiate the DAG
dag = DAG(
    "drug_mentions_pipeline",
    default_args=default_args,
    description="Pipeline for processing drug mentions",
    schedule_interval=timedelta(days=1),
    catchup=False,
)


def ingestion(**kwargs):
    # Call the data ingestion function and get the data
    drugs_data, pubmed_data, clinical_trials_data = load_csv_data(
        drugs_path=kwargs["drugs_path"],
        pubmed_csv_path=kwargs["pubmed_csv_path"],
        clinical_trials_path=kwargs["clinical_trials_path"],
        pubmed_json_path=kwargs["pubmed_json_path"],
    )

    # return the dictionary of DataFrames directly
    return {
        "drugs_data": drugs_data,
        "pubmed_data": pubmed_data,
        "clinical_trials_data": clinical_trials_data,
    }


ingestion_task = PythonOperator(
    task_id="ingestion_task",
    python_callable=ingestion,
    op_kwargs={
        "drugs_path": current_path + "/data/drugs.csv",
        "pubmed_csv_path": current_path + "/data/pubmed.csv",
        "clinical_trials_path": current_path + "/data/clinical_trials.csv",
        "pubmed_json_path": current_path + "/data/pubmed.json",
    },
    dag=dag,
)


# Define the data processing task
def processing(**context):
    ti = context["ti"]

    # Pull the data dictionary from the previous task
    data_dict = ti.xcom_pull(task_ids="ingestion_task")

    # Call the data processing function with the extracted data
    graph = create_drug_graph(
        drugs_data=data_dict["drugs_data"],
        pubmed_data=data_dict["pubmed_data"],
        clinical_trials_data=data_dict["clinical_trials_data"],
    )

    # Assume create_drug_graph returns a JSON serializable object
    return graph


processing_task = PythonOperator(
    task_id="processing_task",
    python_callable=processing,
    provide_context=True,
    dag=dag,
)


# Define the data output task
def output(**kwargs):
    ti = kwargs["ti"]

    # Pull the processed data from the previous task
    graph = ti.xcom_pull(task_ids="processing_task")

    # Call the data output function
    write_graph_to_json(graph, current_path + "/data_output/drug_graph.json")


output_task = PythonOperator(
    task_id="output_task",
    python_callable=output,
    provide_context=True,
    dag=dag,
)

# Set up the task dependencies
ingestion_task >> processing_task >> output_task
