from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from check_db import *
import psycopg2
import hashlib
import wget
import os
import logging
import logging.config
import requests
import yaml
import time

# Global Variables
base_url = 'http://54.174.36.110/'
yaml_file = 'config.yaml'
all_files = []
main_versions = []
parent_urls = []
child_v = []


def get_url(base_url):
    try:
        with closing(get(base_url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.text
            else:
                return None

    except RequestException as e:
        logger.error('Error during requests to {0} : {1}'.format(base_url, str(e)))
        return None


def is_good_response(resp):
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


def get_parent_url():
    """Getting parent directories"""
    response = get_url(base_url)

    if response is not None:
        soup = BeautifulSoup(response, 'html.parser')
        download_links = soup.find_all('li')

        for ref_link in download_links:
            home_link = ref_link.a.get('href')
            if not str(home_link).endswith('html'):
                continue
            else:
                parent_urls.append(home_link)
                recursive(ref_link, base_url)
    else:
        # Raise an exception if we failed to get any data from the url
        raise Exception('Error retrieving contents at {}'.format(base_url))


def recursive(urls, new_url):
    """Recursive files"""
    link = urls.a.get('href')
    if link.endswith('html'):
        new_url += link
        response = get_url(new_url)

        if response is not None:
            soup = BeautifulSoup(response, 'html.parser')
            links = soup.find_all('a')
            for link in links:
                file = link.get('href')
                if not str(file).endswith('.zip') | str(file).endswith('.exe'):
                    continue
                if str(file).startswith('http'):
                    continue
                else:
                    # Main requirements for record tracking
                    url = get_urls(base_url, file)
                    version_type = get_version_type(url)
                    version = get_all_versions(version_type, url, file)
                    app_name = get_app_name(file)
                    filename = get_filename(file)
                    download_file(url, filename, version, app_name)
                    data = {'url': url, 'app_name': app_name, 'filename': filename, 'version': version}
                    logger.info(data)
                    insert_to_db(data)
                    all_files.append(data)

                    # # Extracting metadata to local
                    # sha1 = get_sha1(file)
                    # md5 = get_md5(file)
                    # file_type = get_file_type(file)
                    # size = get_file_size(file_path)
                    # data = {'url': url, 'filename': filename, 'sha1': sha1, 'md5': md5,
                    #         'file_type': file_type, 'size': size, 'version': version}
            return all_files

    else:
        logger.info('[x] Error downloading files.')
        logger.info('[x] No files found to download.')
        return None


def get_version_type(url):
    if 'iecookies.html' in url:
        v_type = 'parent'
    elif '/utils/trans/' in url:
        v_type = 'language'
    else:
        v_type = 'parent'
    return v_type


def get_all_versions(version_type, url, file):
    if version_type == 'parent':
        ver = get_parent_version(url)
    else:
        ver = get_child_version(file)
    return ver


def get_app_name(file):
    download_link = "{}{}".format(base_url, parent_urls[-1])
    response = get_url(download_link)

    if response is not None:
        soup = BeautifulSoup(response, 'lxml')
        table = soup.find('table', {"class": "utilcaption"})
        td = table.find_all('td')
        data = td[1].text
        app_name = data.split('</td>')[0]
        app_name = app_name.split('\n')[0]
        if '-' in app_name:
            app_name = app_name.split('-')[0]
        else:
            app_name = app_name
        return app_name


def get_parent_version(file):
    app_name = get_app_name(file)
    if ' v' in app_name:
        version = app_name.split(' v')[1]
    else:
        version = app_name
    return version


def get_child_version(file):
    download_link = "{}{}".format(base_url, parent_urls[-1])
    response = get_url(download_link)
    if response is not None:
        soup = BeautifulSoup(response, 'lxml')
        a = soup.find('a', href=file)
        tr = a.find_parent('tr')
        td = tr.find_all('td')
        row = str(td)
        ver = row.split(', ')[-1]
        ver = ver.split('<td>')[1]
        ver = ver.split('\n')[0]
        if '</td>' in ver:
            ver = ver.split('</td>')[0]
        elif ver == '':
            ver = 'No version'
        else:
            ver = ver
        return ver


def get_file_size(file_path):
    """Get file size"""
    if file_path is None:
        size = "Unknown"
    else:
        size = os.path.getsize(file_path)
    return size


def get_urls(u_link, file):
    """Get download url"""
    if file.startswith('..'):
        file = file.split('../')[-1]
        url = "{}{}".format(u_link, file)
    else:
        raw_url = "{}utils/".format(base_url)
        url = "{}{}".format(raw_url, file)
    return url


def get_filename(file):
    """Get file name"""
    try:
        filename = file.split('/')[-1]
    except IndexError:
        filename = "Unknown file"
    return filename


def get_file_type(file):
    """Get file type"""
    try:
        file_type = file.split('.')[-1]
    except IndexError:
        file_type = "UNKNOWN FILE"
    return file_type


def get_sha1(file):
    hd = hashlib.sha1(file.encode('utf-8'))
    sha1 = str(hd.hexdigest())
    return sha1


def get_md5(file):
    hd = hashlib.md5(file.encode('utf-8'))
    md5 = str(hd.hexdigest())
    return md5


def download_file(url, filename, version, app_name):
    try:
        local_storage = "{}\\storage".format(os.getcwd())
        r = requests.get(url, allow_redirects=True)
        if r.status_code == 200:
            logger.info(" [Currently downloading {} APP_NAME: {} VERSION: {}]".format(url, app_name, version))

            if len(existing_data) > 0:
                # Dictionary for comparing from website to database
                comp = {'app_name': app_name, 'version': version, 'filename': filename}
                if comp in existing_data:
                    # If the app name and version is existing in DB
                    logger.error("[File exists. APP_NAME: {} VERSION: {}]".format(app_name, version))
                else:
                    # Download the updated app
                    download(url, local_storage, filename)
            else:
                # If the local DB is empty, download everything.
                download(url, local_storage, filename)
        else:
            # If file is not downloadable
            logger.info("[Currently downloading from {} (APP_NAME: {} VERSION: {})]".format(url, app_name, version))
            logger.error("[x] Failed to download {}".format(filename))
    except Exception as e:
        print(e)


def download(url, local_storage, filename):
    wget.download(url, local_storage)
    logger.info("[/] Successfully downloaded {}".format(filename))
    # file_path = "{}{}{}".format(local_storage, os.sep, filename)
    # return file_path


def setup_yaml():
    """Setup logging configuration """
    global yaml_file
    default_level = logging.DEBUG
    value = os.getenv("LOG_CFG", None)

    if value:
        yaml_file = value
    if os.path.exists(yaml_file):
        with open(yaml_file, 'rt') as f:
            try:
                config = yaml.safe_load(f.read())
                logging.config.dictConfig(config)
                # Disable Logging of Imported Module Chardet
                logging.getLogger('chardet.charsetprober').setLevel(logging.INFO)
            except Exception as e:
                print(e)
                print('Error in Logging Configuration. Using default configs')
                logging.basicConfig(level=default_level, filename="error.log")
    else:
        logging.basicConfig(level=default_level, filename="debug.log")
        print('Failed to load configuration file. Using default configs')


def open_yaml():
    global yaml_file
    with open(yaml_file, 'rt') as f:
        config = yaml.safe_load(f.read())
    mysql = config['mysql']
    return mysql


def connect_to_sql():
    mysql = open_yaml()

    connection = psycopg2.connect(
        user=mysql['user'],
        password=mysql['password'],
        host=mysql['host'],
        port=mysql['port'],
        database=mysql['db'],
    )
    return connection


def insert_to_db(file):
    try:
        connection = connect_to_sql()
        cursor = connection.cursor()
        postgres_insert_query = """
                                    INSERT INTO files
                                    (URL, APP_NAME, FILENAME, VERSION)
                                    VALUES (%s,%s,%s,%s)
                                """
        record_to_insert = (file['url'], file['app_name'], file['filename'], file['version'])
        cursor.execute(postgres_insert_query, record_to_insert)
        connection.commit()
        logger.info("[/] Record inserted to database.")

    except Exception as error:
        print("Failed to insert data into sqlite table", error)


def main():
    logger.info('Harvesting your files.')
    logger.info('Please wait.')
    start_time = time.time()
    get_parts()
    get_parent_url()
    duration = time.time() - start_time
    logger.info("Total: {} record/s inserted successfully into file table".format(len(all_files)))
    logger.info("Downloaded data in {} seconds".format(duration))


if __name__ == '__main__':
    setup_yaml()
    logger = logging.getLogger(__name__)
    main()
