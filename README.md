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

Harvest logger
```cmd
2019-12-03 07:22:17,162 - __main__ - INFO -  [Currently downloading http://54.174.36.110/utils/trans/mylastsearch_dutch1.zip APP_NAME: MyLastSearch VERSION: 1.41]
2019-12-03 07:22:17,677 - __main__ - INFO -  [/] Successfully downloaded mylastsearch_dutch1.zip
2019-12-03 07:22:17,678 - __main__ - INFO -  {'app_name': 'MyLastSearch', 'filename': 'mylastsearch_dutch1.zip', 'version': '1.41'}
2019-12-03 07:22:17,693 - __main__ - INFO -  [/] Record inserted to database.
2019-12-03 07:22:17,722 - __main__ - INFO -  [/] API - Data sent to API. Status response is <Response [200]>
```
##### Database Docker

```html
id  |                  filename                   |                   sha1                   |               md5                | file_type | file_size
----+---------------------------------------------+------------------------------------------+----------------------------------+-----------+-----------
  1 | webbrowserpassview.zip                      | bcef891405a0e103e7093078cf5acf4d2a752095 | fd4ecb62da6d7744c46e36ba4d55ad0a | zip       | 235627
  2 | webbrowserpassview_setup.exe                | cd399e0802be0c4d46bf9a21ad7fd1cc1d813947 | 9cd9ff81270f9c635245fed4bf562d38 | exe       | 279147
  3 | webbrowserpassview_arabic.zip               | b963792a4d65f1a507c3ee97d3fd786f1437422d | e08c7389a61cddc87084961967ef8fd3 | zip       | 1449
  4 | webbrowserpassview_brazilian_portuguese.zip | 0dc4f7cdb4623b2b8c733cc9c7666fb504f17aec | 0e4994e9990cbf4cb2b447adfcdf3cc0 | zip       | 1800
  5 | webbrowserpassview_croatian.zip             | 33dab78cce7112e9af74d89c948271a49b545362 | 2a1e0c07091e5181815877be7eae2ccd | zip       | 1413
  6 | webbrowserpassview_czech.zip                | 4619927dcb7f23398dee0f89945906141f386a73 | 652b8a16e8989227572943cc1e03c50a | zip       | 1623
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

##### Database Docker

```
id   |        app_name          |                   filename           |    version
-----+--------------------------+--------------------------------------+--------------
   1 | WebBrowserPassView       | webbrowserpassview.zip               | 1.92
   2 | WebBrowserPassView       |webbrowserpassview_hebrew.zip         | 1.92
   3 | WebBrowserPassView       | webbrowserpassview_greek.zip         | 1.92
   4 | WebBrowserPassView       | webbrowserpassview_setup.exe         | 1.92
   5 | WebBrowserPassView       | webbrowserpassview_arabic.zip        | 1.60
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
```
pytest --cov=harvest tests/test_harvest.py
```

## License
[MIT](https://choosealicense.com/licenses/mit/)
