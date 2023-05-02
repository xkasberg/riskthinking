import os
import pendulum
import datetime
import pandas as pd
from pandas import DataFrame
import kaggle
from tqdm import tqdm

from airflow.decorators import dag, task
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook

DATA_PATH = f"{os.getcwd()}/data/"
os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)


# !!! Problem 1 !!! 
@dag(
    dag_id="process-equities",
    schedule="0 0 * * *",
    start_date=pendulum.datetime(2023, 5, 1, tz="UTC"),
    catchup=False,
    dagrun_timeout=datetime.timedelta(minutes=60),
) 
def process_equities():
    """
        Creates our postgres table to store our data on equities
    """
    create_equities_table = PostgresOperator(
        task_id="create_equities_table",
        postgres_conn_id="pg_conn",
        sql="""
            CREATE TABLE IF NOT EXISTS equities (
                "id" SERIAL PRIMARY KEY,
                "Symbol" TEXT,
                "Security Name" TEXT,
                "Date" TEXT,
                "Open" DOUBLE PRECISION,
                "High" DOUBLE PRECISION,
                "Low" DOUBLE PRECISION,
                "Close" DOUBLE PRECISION,
                "Adj Close" DOUBLE PRECISION,
                "Volume" INTEGER
            );"""
    )


    @task
    def get_stock_market_data() -> None:
        """
        downloads dataset from kaggle
        """
        kaggle.api.authenticate()
        kaggle.api.dataset_download_files(
            'jacksoncrow/stock-market-dataset', 
            path=DATA_PATH, 
            unzip=True
        )


    @task
    def load_stock_market_data():
        """
            builds a pandas datframe from all the csvs in the created data folder
            loads the dataframe into the SQL table
        """
        metadata_df = pd.read_csv(f'{DATA_PATH}/symbols_valid_meta.csv')
        tickers = []

        print("getting tickers")
        for dirname, _, filenames in os.walk(DATA_PATH):
            for filename in tqdm(filenames[1:]): # skip meta data file
                ticker = filename[:-4] # cut off '.csv' to get the ticker
                name = metadata_df[metadata_df['NASDAQ Symbol'] == ticker]['Security Name'].iloc[0] 
                ticker_path = os.path.join(dirname, filename)
                ticker_df = pd.read_csv(ticker_path)
                ticker_df['Symbol'] = ticker
                ticker_df['Security Name'] = name 
                tickers.append(ticker_df)

        print("building equities df")
        equities_df = pd.concat(tickers)
        print(equities_df.head())
        print(equities_df.shape)


        
        print("building equities df")
        equities_df = pd.concat(tickers)

        print("loading equities")
        postgres_hook = PostgresHook(postgres_conn_id="pg_conn")
        conn = postgres_hook.get_conn()
        equities_df.to_sql('equities', postgres_hook.get_sqlalchemy_engine(), chunksize=1000)
        conn.commit()

    [create_equities_table] >> get_stock_market_data() >> load_stock_market_data()

dag = process_equities()