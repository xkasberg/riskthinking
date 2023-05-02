# riskthinking.ai

## Problem One

Problem one involves downloading a dataset from kaggle, creating a data structure to store the data, and converting the resulting dataset into a structured format. 

The dataset is from kaggle. To download datasets directly from kaggle, the kaggle python package needs access to your api key & user name by providing a file called "kaggle.json" in the kaggle folder in your virtualenv's site-packages directory.

Since our's is going to be in a docker container you should download your kaggle.json file, and place it in the root directory of this repo (the file is included in the .gitignore already, so it won't be accidently pushed to github), then the  Dockerfile will move it into the container when you build the image. <b>If you neglect this step the pipeline will not run! </b>


### Step 1: Running Airflow with Docker
https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html

After Docker is installed: 

check if you have enough memory allocated (ideally 8gb):

```
docker run --rm "debian:bullseye-slim" bash -c 'numfmt --to iec $(echo $(($(getconf _PHYS_PAGES) * $(getconf PAGE_SIZE))))'

>>>7.8G
```

To deploy Airflow on Docker Compose, you should fetch docker-compose.yaml.

```
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.6.0/docker-compose.yaml'
```

Set the airflow user

```
mkdir -p ./dags ./logs ./plugins
echo -e "AIRFLOW_UID=$(id -u)" > .env
```

Run DB migrations / Initialize DB

```
docker compose up airflow-init
```

Start the service

```
docker compose up
```

### Step 2: Create a connection to Postgres

We will also need to create a connection to the postgres db. To create one via the web UI, from the “Admin” menu, select “Connections”, then click the Plus sign to “Add a new record” to the list of connections.

Connection Id: pg_conn
Connection Type: postgres
Host: postgres
Schema: airflow
Login: airflow
Password: airflow
Port: 5432


### Step 3: Clean up existing DAGS

When I started my airflow docker image, it booted up with 48 default dags. t 

