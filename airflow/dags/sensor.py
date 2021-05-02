from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

DEFAULT_DAG_ARGS = {
    'owner': 'sqube',
    'depends_on_past': True,
    'start_date': datetime.utcnow() - timedelta(days=1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=1),
    'description': 'ML pipeline.'
}


with DAG(dag_id='ml_pipeline',
         default_args=DEFAULT_DAG_ARGS,
         schedule_interval=None
         ) as dag:

    start_sample_step = BashOperator(
        task_id="start_sample_step",
        bash_command="echo 'Running Training Pipeline' && sleep 60s",
        dag=dag
    )
