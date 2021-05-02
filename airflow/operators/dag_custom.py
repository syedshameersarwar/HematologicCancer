from typing import Dict

from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.utils.decorators import apply_defaults
from airflow.models import DagRun
from airflow.utils.state import State


class CustomTriggerDagRunOperator(TriggerDagRunOperator):

    @apply_defaults
    def __init__(self, return_if_running: bool = True, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.return_if_running = return_if_running

    def execute(self, context: Dict) -> None:
        if self.return_if_running:
            queued = DagRun.find(
                dag_id=self.trigger_dag_id, state=State.QUEUED)
            running = DagRun.find(
                dag_id=self.trigger_dag_id, state=State.RUNNING)
            if len(queued) > 0 or len(running) > 0:
                self.log.info(
                    f"Dag {self.trigger_dag_id} is already running or queued, Skipping new execution call.")
                return
        super().execute(context)
