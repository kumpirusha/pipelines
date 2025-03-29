# Open Weather integration pipeline

## What?
This is a PoC python data application. It is fetching data from OpenWeather current weather data API
(https://openweathermap.org/current#one), storing it locally and writing a processed data into a local
PostgreSQL database. 

## Details

### Ingestion
Data ingestion is done in two parts. First we define the cities that we would like to get the data for
in `CITIES_TO_MONITOR` constant located in `pipeline/constants.py`. Then we run the calls to the `CITY_URL`
API since it provides us with the geographical coordinates of the cities defined in `CITIES_TO_MONITOR`.
City coordinates are then stored in `data/cities.json` file.

This is a prerequisite to fetching the actual weather data since we must pass the latitude and longitude
along with the city name to the weather URL defined in `WEATHER_URL` constant. Code for this is provided
in the `pipeline/fetch.py` file. 

The raw data is stored locally as NdJson files in `data/raw_data/` directory stamped with the ingestion 
timestamp for easier tracking. This is done to simulated cloud environment where ingestion data is 
often stored in structured or semi-structured form (such as AWS S3).

### Metrics
As part of the ingestion process API metrics from weather data API responses are collected and stored
in the postgres database in `tw_test.api_metrics`. Table details can be found in the `pipeline/utils.py`
directory.

Logging is provided throughout the application and the logs are both display at runtime and stored
in the `data/logs` directory.

### ETL
Raw data is then passed on to the transformation phase. Here the data structure is flattened and 
normalized. Irrelevant columns are dropped, columns given proper names and timestamps converted to a
consistent format. Clean data is pushed to local storage in a json format and to the database in
`tw_test.weather_data_clean`. Details of the transformation can be found in `pipelines/transform.py`
file.

### Deployment
Docker compose is used to deploy the application. Volumes are mounted (`postgres_data`) as part of 
the compose process in order to make the database persistent. The postgres_data volume will persist 
across container restarts. To check volume existence run `docker volume ls -f name=tw_weather`.

Python application is run every 30 seconds in the 
following order:
1. Geographical API is called to collect city coordinate
2. Weather API is called to collect current weather data
3. Raw data is saved locally
4. Processed data is stored locally
5. Queries are run on the database

Quick start:
* To start the application copy the project locally and run `docker compose up -d --build`
* To connect to the database using `docker exec -it postgres_db psql -U myuser -d tw_test`

## Production 
### Reliability
* Implement retry mechanism on failed API calls (exponential backoff)
* Move cities out of constants to a config file (such as YAML)
* Move secrets to ansible-vault or a credentials manager
* Decouple Extract, Transform and Load steps making each one more fault tolerant
* Add monitoring and DQ checks on destination tables
* Run application in CI

### Scalability
* Run application with cronjobs or a scheduler app (Airflow)
* Optimise DB and tables (partitioning, indexing, etc.)
* Switch to apache-parquet for raw data format to improve query performance

### Cloud-Native Deployment
* ECS with Fargate/EC2 and images stored in ECR
* Simple EC2 instance runs
* AWS Lambda for small tasks

### Storage
* S3 for raw data with life-cycle rules

### Analytics
* Redshift for OLAP workload
* Glue and Athena along with Apache-parquet for big data workloads

### Deployment
* Ansible for local deploys (or via Tower)
* CI/CD deployment to push data to cloud

### Monitoring
* AWS CloudWatch to capture logs from applications
* Prometheus and Grafana for Metrics
