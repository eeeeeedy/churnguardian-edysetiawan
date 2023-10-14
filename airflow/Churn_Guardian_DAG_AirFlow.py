import pandas as pd
import numpy as np
import psycopg2 as db
from sqlalchemy import create_engine
from airflow import DAG
from airflow.hooks.postgres_hook import PostgresHook
from airflow.operators.python_operator import PythonOperator
from datetime import datetime

def load_data():
    # String koneksi untuk PostgreSQL
    conn_string = "dbname='finalproject' host='postgres' user='airflow' password='airflow'"
    conn = db.connect(conn_string)
    # Membaca data dari tabel 'table_fp' ke dalam DataFrame
    df = pd.read_sql("select * from table_fp", conn)
    df.to_csv('/opt/airflow/dags/final_project_data_raw.csv', index=False)
    
def cleaning_data():
    df = pd.read_csv('/opt/airflow/dags/final_project_data_raw.csv')
    # Kolom yang akan digunakan
    # columns =["Customer ID", "Gender", "Age", "Married", "Number of Dependents",
    #             "City", "Zip Code", "Latitude", "Longitude", "Number of Referrals",
    #             "Tenure in Months", "Offer", "Phone Service",
    #             "Avg Monthly Long Distance Charges", "Multiple Lines",
    #             "Internet Service", "Internet Type", "Avg Monthly GB Download",
    #             "Online Security", "Online Backup", "Device Protection Plan",
    #             "Premium Tech Support", "Streaming TV", "Streaming Movies",
    #             "Streaming Music", "Unlimited Data", "Contract", "Paperless Billing",
    #             "Payment Method", "Monthly Charge", "Total Charges", "Total Refunds",
    #            "Total Extra Data Charges", "Total Long Distance Charges",
    #             "Total Revenue", "Customer Status", "Churn Category", "Churn Reason"]
    # Mengganti spasi dengan underscore pada nama kolom dan membuat seluru nama kolom menjadi lowercase
    df.columns = df.columns.str.lower().str.replace(' ', '_')
    # Replace NaN with 0.0
    df['avg_monthly_gb_download'] = df['avg_monthly_gb_download'].replace(np.nan,0.0)
    df['avg_monthly_long_distance_charges'] = df['avg_monthly_long_distance_charges'].replace(np.nan,0.0)
    df[['internet_type', 'online_security', 'online_backup', 'device_protection_plan', 
           'premium_tech_support', 'streaming_tv', 'streaming_movies','streaming_music','unlimited_data']] = df[['internet_type', 'online_security', 'online_backup', 'device_protection_plan', 
           'premium_tech_support', 'streaming_tv', 'streaming_movies','streaming_music','unlimited_data']].replace(np.nan,'No Internet')
    df['multiple_lines'] = df['multiple_lines'].replace(np.nan,'No phone Pervice')
    # Drop Customer ID
    df = df.drop(['customer_id'],axis=1)
    # Mengubah tipe data zip_code menjadi object
    df['zip_code']=df['zip_code'].astype('object')
    # Menyimpan dataframe yang telah dibersihkan ke file CSV
    df.to_csv('/opt/airflow/dags/final_project_data_clean.csv', index=False)
    print("-------Data Saved------")


def push_postgres ():
    # Memanggil fungsi cleaning_data untuk membersihkan dataframe
    df_cleaned = pd.read_csv('/opt/airflow/dags/final_project_data_clean.csv') # import csv clean
    # Database connection parameters
    db_params = {
        "user": "airflow",
        "password": "airflow",
        "host": "postgres",
        "port": "5434",
        "database": "finalproject",
    }

    # Create an SQLAlchemy engine
    engine = create_engine(f"postgresql+psycopg2://{db_params['user']}:{db_params['password']}@{db_params['host']}/{db_params['database']}")
    table_name = "table_finalproject"
    # Push the DataFrame to PostgreSQL
    df_cleaned.to_sql(table_name, engine, if_exists="replace", index=False)

default_args= {
    'owner': 'Irfan',
    'start_date': datetime(2023, 9, 29) }

with DAG(
    "finalproject",
    description='finalproject',
    schedule_interval='@yearly',
    default_args=default_args, 
    catchup=False) as dag:

    # Task 1
    load_data = PythonOperator(
        task_id='load_data',
        python_callable=load_data

    )

    # Task 2
    cleaning_data = PythonOperator(
        task_id='cleaning_data',
        python_callable=cleaning_data

    )
    
    # Task 3
    push_postgres = PythonOperator(
        task_id='push_postgres',
        python_callable=push_postgres

    )
    
load_data >> cleaning_data >> push_postgres