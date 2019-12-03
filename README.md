# Harvest (Production)
The Harvest application scrapes web pages for information and download files.

## Features
* Harvest application to scrape web pages for information and download files
* The application saves website information into a database and stores the downloaded files to disk
* The application extracts metadata from file uploads and allows users to read the metadata, update/correct the metadata and delete submissions.

## Harvest Application
The application should then submit the downloaded file to the REST API and record the response in the database.

```python
# Docker container database configuration
mysql:
  host: harvest_db_docker    # Docker container
  user: postgres             # Postgres user
  db: harvest_application    # Database name inside the container
  port: 5432                 # Port used
  password: novirus123       # Password
```

```python
api:
  uploader: http://<IPv4>:<PORT>/uploader    # Dockerized API and Port
# sample: http://172.19.0.3:8000/uploader 
```

### Sample Output
```cmd
2019-12-03 07:22:17,162 - __main__ - INFO -  [Currently downloading http://54.174.36.110/utils/trans/mylastsearch_dutch1.zip APP_NAME: MyLastSearch VERSION: 1.41]
2019-12-03 07:22:17,677 - __main__ - INFO -  [/] Successfully downloaded mylastsearch_dutch1.zip
2019-12-03 07:22:17,678 - __main__ - INFO -  {'app_name': 'MyLastSearch', 'filename': 'mylastsearch_dutch1.zip', 'version': '1.41'}
2019-12-03 07:22:17,693 - __main__ - INFO -  [/] Record inserted to database.
2019-12-03 07:22:17,722 - __main__ - INFO -  [/] API - Data sent to API. Status response is <Response [200]>
```

## REST API
The applications should be running in a docker container so that deployment and dependencies are easily managed. The REST API also use WSGI server to handle HTTP connections.

```python
# Docker container database configuration
mysql:
  host: harvest_db_docker    # Docker container same as Harvest App 
  user: postgres             # Postgres user
  db: harvest_api_docker     # Database name inside the container
  port: 5432                 # Port used
  password: novirus123       # Password

```


## Dockerfile
```text
FROM python:3
ADD . /app
WORKDIR /app

RUN pip install -r requirements.txt
RUN pip install flask gunicorn
EXPOSE 8000
CMD ["gunicorn", "server:app", "-b",  "0.0.0.0:8000"]
```

## Testing
```python
pytest --cov=harvest tests/test_harvest.py
```

## License
[MIT](https://choosealicense.com/licenses/mit/)
