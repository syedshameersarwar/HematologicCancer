from airflow import DAG
from airflow.sensors.sql import SqlSensor
from pg_custom import CheckPostgresTableExistence
from dag_custom import CustomTriggerDagRunOperator
from datetime import datetime, timedelta

DATA_THRESHOLD = 10

DB_CONN_ID = "hematology"
DB_SCHEMA = "public"
DB_TARGET_TABLE = "reports"
RECORD_UTILIZED_KEY = "utilized"

DEFAULT_DAG_ARGS = {
    'owner': 'sqube',
    'depends_on_past': True,
    'start_date': datetime.utcnow() - timedelta(days=1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=1),
    'description': 'Monitor new records for training and trigger training pipeline if threshold is reached.'
}

with DAG(dag_id='data_sensor',
         default_args=DEFAULT_DAG_ARGS,
         schedule_interval=None
         ) as dag:

    check_table_existence = CheckPostgresTableExistence(
        task_id="check_table_existence",
        conn_id=DB_CONN_ID,
        schema=DB_SCHEMA,
        table=DB_TARGET_TABLE,
        cause_failure=True,
        dag=dag
    )

    check_data_threshold = SqlSensor(
        task_id="check_data_threshold",
        conn_id=DB_CONN_ID,
        sql=f"""SELECT COUNT(*) FROM {DB_SCHEMA}.{DB_TARGET_TABLE} 
                WHERE {RECORD_UTILIZED_KEY} = FALSE""",
        success=lambda x: x >= DATA_THRESHOLD,
        timeout=60 * 5,
        fail_on_empty=True,
        dag=dag
    )

    trigger_training_pipeline = CustomTriggerDagRunOperator(
        task_id="trigger_training_pipeline",
        trigger_dag_id="ml_pipeline",
        wait_for_completion=False
    )

    check_table_existence >> check_data_threshold >> trigger_training_pipeline
