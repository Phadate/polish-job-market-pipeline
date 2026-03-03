from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
sys.path.insert(0, '/opt/airflow/pipelines')


from upload_to_blob import upload_all
from justjoin import main

default_args = {
    'owner': 'dunsin',
    'retries': 1,
    'retry_delay' : timedelta(minutes=5)
}

# define the DAG

with DAG(
    dag_id = 'polish_job_market_pipeline',
    default_args=default_args,
    description='Daily pipeline scraping Polish job market data',
    schedule_interval='0 6 * * *',
    start_date=datetime(2026, 1, 1),
    catchup=False
) as dag:
    
    scrape_task = PythonOperator(
        task_id='scrape_website',
        provide_context=True,
        python_callable=main
    )

    upload_task = PythonOperator(
        task_id='upload_to_blob_storage',
        provide_context=True,
        python_callable=upload_all
    )

    # define order
    scrape_task >> upload_task
