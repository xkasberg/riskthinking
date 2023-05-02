FROM apache/airflow:2.6.0
COPY requirements.txt /requirements.txt
COPY kaggle.json /home/airflow/.kaggle/kaggle.json
RUN pip install --user --upgrade pip
RUN pip install --user -r /requirements.txt