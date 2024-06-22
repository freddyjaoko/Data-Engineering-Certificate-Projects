from datetime import timedelta
# The DAG object; we'll need this to instantiate a DAG
from airflow.models import DAG
# Operators; you need this to write tasks!
from airflow.operators.bash_operator import BashOperator
# This makes scheduling easy
from airflow.utils.dates import days_ago

#defining DAG arguments

# You can override them on a per-task basis during operator initialization
default_args = {
    'owner': 'fred',
    'start_date': days_ago(0),
    'email': ['dummy@gmail.com'],
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# defining the DAG

# define the DAG
dag = DAG(
    'ETL_toll_data',
    default_args=default_args,
    description='Apache Airflow Final Assignment',
    schedule_interval=timedelta(days=1),
)

# Define tasks

# Unzip data

unzip_data = BashOperator(
    task_id = 'unzip_data',
    bash_command = 'tar -zxf /home/project/airflow/dags/finalassignment/tolldata.tgz',
    dag = dag
)


# Extract data from csv

extract_data_from_csv = BashOperator(
    task_id = 'extract_data_from_csv',
    bash_command = 'cut -d"," -f1-4 vehicle-data.csv > csv_data.csv',
    dag = dag
) 

# Extract data from tsv

extract_data_from_tsv = BashOperator(
    task_id = 'extract_data_from_tsv',
    bash_command = 'cut -f5-7 tollplaza-data.csv > csv_data.csv',
    dag = dag
) 

# Extract data from fixed width

extract_data_from_fixed_width = BashOperator(
    task_id = 'extract_data_from_fixed_width',
    bash_command = "cat payment-data.txt | tr -s '[:space:]' | cut -d' ' -f11,12 > fixed_width_data.csv",
    dag = dag
)

# Consolidate data

consolidate_data = BashOperator(
    task_id = 'consolidate_data',
    bash_command = 'paste csv_data.csv tsv_data.csv fixed_width_data.csv > extracted_data.csv',
    dag = dag
)

# Transform data

transform_data = BashOperator(
    task_id = 'transform_data',
    bash_command = 'tr "[a-z]" "[A-Z]" < extracted_data.csv > transformed_data.csv')

# Task pipeline

unzip_data >> extract_data_from_csv >> extract_data_from_tsv >> extract_data_from_fixed_width >> consolidate_data >> transform_data