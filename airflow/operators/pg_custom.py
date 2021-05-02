from typing import Dict, Optional

from airflow.models.baseoperator import BaseOperator
from airflow.hooks.base import BaseHook
from airflow.exceptions import AirflowException
from airflow.utils.decorators import apply_defaults


class CheckPostgresTableExistence(BaseOperator):

    __QUERY = """
        SELECT * FROM pg_tables
        WHERE schemaname = '{schema}' AND tablename = '{table}'
    """

    @apply_defaults
    def __init__(self, table: str, *args, conn_id: str = 'postgres_default',
                 schema: str = 'public', cause_failure: bool = True, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.conn_id = conn_id
        self.schema = schema
        self.table = table
        self.cause_failure = cause_failure

    def _get_hook(self):
        conn = BaseHook.get_connection(self.conn_id)

        allowed_conn_type = 'postgres'
        if conn.conn_type != allowed_conn_type:
            raise AirflowException(
                "The connection type is not supported by SqlSensor. "
                f"Supported connection types: {allowed_conn_type}"
            )
        return conn.get_hook()

    def execute(self, context: Dict) -> Optional[bool]:
        hook = self._get_hook()
        query = hook.get_first(
            sql=CheckPostgresTableExistence.__QUERY.format(schema=self.schema, table=self.table))
        exist = bool(query)
        self.log.info(
            f"Existence status for table `{self.table}` in schema `{self.schema}`: {exist}")
        if self.cause_failure:
            if not exist:
                raise AirflowException(
                    f"Table `{self.table}` in schema `{self.schema}` does not exist.")
        return exist
