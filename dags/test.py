import pendulum
from datetime import timedelta
from airflow.decorators import dag


@dag(
    dag_id="test-dag",
    schedule_interval="0 0 * * *",
    start_date=pendulum.datetime(2023, 5, 1, tz="UTC"),
    catchup=False,
    dagrun_timeout=timedelta(minutes=60),
) 
def test_dag():
    """
       dummy dag
    """
    print("test")

dag = test_dag()