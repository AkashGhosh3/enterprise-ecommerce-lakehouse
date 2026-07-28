from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    "owner": "Akash",
}

with DAG(
    dag_id="enterprise_ecommerce_pipeline",
    default_args=default_args,
    description="Enterprise E-Commerce Data Pipeline",
    start_date=datetime(2026, 7, 24),
    schedule=None,
    catchup=False,
    tags=["enterprise", "aws", "ecommerce"],
) as dag:

    ingest_products = BashOperator(
        task_id="ingest_products",
        bash_command="cd /opt/airflow/project && python -m scripts.tests_orders_ingestion",
    )

    bronze_to_silver = BashOperator(
        task_id="bronze_to_silver",
        bash_command="cd /opt/airflow/project && python -m scripts.test_bronze_reader",
    )

    silver_to_gold = BashOperator(
        task_id="silver_to_gold",
        bash_command="cd /opt/airflow/project && python -m transformations.gold_transform",
    )

    ingest_products >> bronze_to_silver >> silver_to_gold