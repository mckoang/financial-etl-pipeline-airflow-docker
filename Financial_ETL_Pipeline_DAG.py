from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine

#Extracting the data
def load_to_postgres():
    engine = create_engine("postgresql://postgres:Aspirine68%23@host:5432/Financial Pipeline")

df=pd.read_csv("C:\\Users\\first\\Desktop\\Puthon Revision\\ETL Mike\\airflow_docker\\data\\transaction.csv")


#This is the cleaning process
def transform():
    df=pd.read_csv("C:\\Users\\first\\Desktop\\Puthon Revision\\ETL Mike\\airflow_docker\\data\\transaction.csv")


    #converting timestamp to standard date format
df['timestamp']=pd.to_datetime(df['timestamp'])
print(df.head())

#checking for number of missing values
df.isnull().sum()

#checking for duplicate values
df.duplicated().sum()

#column standardization
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
#cleaning transaction_types
df['transaction_type']=df['transaction_type'].str.strip().str.lower()
#cleaning location column
df['location'] = df['location'].str.strip().str.title()


#creating new columns for data categorization
#high value flag
high_value_threshold=10000
df['is high value']=df['amount'] > high_value_threshold

#Extracting hour
df['hour'] = df['timestamp'].dt.hour

start_hour=6
end_hour=22

#defining unusual columns
df['is_unusual_time'] = (df['hour'] < start_hour) | (df['hour'] > end_hour)

def load():
    df=pd.read_csv("C:\\Users\\first\\Desktop\\Puthon Revision\\ETL Mike\\airflow_docker\\data\\transaction.csv")
    df.to_sql("staging_transactions", engine, if_exists="append", index=False)

with DAG(
    dag_id="etl_pipeline",
    start_date=datetime(2025, 8, 31),
    schedule_interval="@daily",
    catchup=False,
) as dag:


 task_extract = PythonOperator(
        task_id="extract",
        python_callable=extract,
    )

task_transform = PythonOperator(
        task_id="transform",
        python_callable=transform,
    )

task_load = PythonOperator(
        task_id="load",
        python_callable=load,
    )

task_extract >> task_transform >> task_load