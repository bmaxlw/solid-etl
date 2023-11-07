import os 
import plugins.helpers as helper
import plugins.parsers as parser
import plugins.compilers as compiler
from datetime import datetime
from pathlib import Path
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.postgres_operator import PostgresOperator

environment: str  = os.environ.get('ENV', 'dev')
dag_name: str     = Path(os.path.basename(__file__)).stem
config: dict      = parser.parse_config(f'/opt/airflow/config/{dag_name}.yaml')[environment].get(dag_name)
api_endpoint: str = config.get('api')
data_path: str    = f"{config.get('data')}/{dag_name}"
sql_path: str     = f"{config.get('sql')}/{dag_name}"

default_args = {
    'owner': 'Max',
    'start_date': datetime(2023, 11, 6),
    'schedule_interval': None, 
}

with DAG(dag_name, 
         default_args=default_args, 
         catchup=False, 
         max_active_runs=1) as dag:

    get_api = PythonOperator(
        task_id='get_api',
        python_callable=parser.parse_api,
        op_kwargs={'source': api_endpoint, 
                   'target': f'{data_path}/json'},
        dag=dag
    )

    compile_queries = PythonOperator(
        task_id='compile_queries',
        python_callable=compiler.compile_sql_from_json,
        op_kwargs={'source': f'{data_path}/json'},
        dag=dag
    )

    create_target = PostgresOperator(
        task_id='create_target',
        sql=parser.parse_sql(f'{sql_path}/create_jokes_table.sql'),
        postgres_conn_id='postgres',  
        autocommit=True
    )
    
    create_staging = PostgresOperator(
        task_id='create_staging',
        sql=parser.parse_sql(f'{sql_path}/create_staging_table.sql'),
        postgres_conn_id='postgres',  
        autocommit=True
    )

    populate_staging = PostgresOperator(
        task_id='populate_staging',
        sql="{{ ti.xcom_pull(key='queries', task_ids='compile_queries') }}",
        postgres_conn_id='postgres',  
        autocommit=True
    )

    load_csv = PythonOperator(
        task_id='load_csv',
        python_callable=compiler.compile_csv_from_api,
        op_kwargs={'target': f'{data_path}/csv'},
        dag=dag
    )

    populate_target= PostgresOperator(
        task_id='populate_target',
        sql=parser.parse_sql(f'{sql_path}/merge_into_jokes.sql'),
        postgres_conn_id='postgres',  
        autocommit=True
    )

    # populate_<...> = <...>Operator(
    # ... pulling xcom from get_api: 
    # ... - any new compiler can be added to transform the pulled data
    # ... - any new target connector can be integrated to ingest the data
    # ) -> 

    drop_staging = PostgresOperator(
        task_id='drop_staging',
        sql=parser.parse_sql(f'{sql_path}/drop_staging_table.sql'),
        postgres_conn_id='postgres',  
        autocommit=True
    )

    clean_up_data = PythonOperator(
        task_id='clean_up_data',
        python_callable=helper.clean_up_folder,
        op_kwargs={'target': f'{data_path}/json'},
        dag=dag
    )

clean_up_data >> get_api >> compile_queries >> [create_target, create_staging] >> populate_staging >> [load_csv, populate_target] >> drop_staging

if __name__ == "__main__":
    dag.cli()
