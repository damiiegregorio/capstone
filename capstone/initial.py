from contextlib import closing

from bs4 import BeautifulSoup
from requests import RequestException, get

from check_db import *
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
base_dir = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(base_dir, 'storage')


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
        soup = BeautifulSoup(response, 'lxml')
        download_links = soup.find_all('li')

        for ref_link in download_links:
            home_link = ref_link.a.get('href')
            if not str(home_link).endswith('html'):
                continue
            else:
                if home_link not in parent_urls:
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
            soup = BeautifulSoup(response, 'lxml')
            links = soup.find_all('a')
            for link in links:
                file = link.get('href')
                file = str(file)
                if not file.endswith('zip') | file.endswith('exe'):
                    continue
                elif file.startswith('http'):
                    continue
                else:
                    # Main requirements for record tracking
                    url = get_urls(base_url, file)
                    version_type = get_version_type(url)
                    version = get_all_versions(version_type, file)
                    app_name = get_app_name()
                    filename = get_filename(file)
                    download_resp = download_file(url, filename, version, app_name)
                    data = {'app_name': app_name, 'filename': filename, 'version': version}
                    insert_db(download_resp, data)
                    send_data_to_server(filename, download_resp)
                    all_files.append(data)
            return all_files

    else:
        logger.error(' [x] DOWNLOAD - Error downloading files. No files found to download.')


def send_data_to_server(filename, download_resp):
    global yaml_file
    with open(yaml_file, 'rt') as f:
        config = yaml.safe_load(f.read())
    api = config['api']

    if download_resp is True:
        filename = os.path.join(UPLOAD_FOLDER, filename)
        files = {'files': open(filename, 'rb')}
        response = requests.post(api['uploader'], files=files)
        logger.info(' [/] API - Data sent to API. Status response is {}'.format(response))
    else:
        logger.error('[x] API - Record exists.')


def insert_db(download_resp, data):
    if download_resp is True:
        logger.info(" {}".format(data))
        insert_to_db(data)
    else:
        logger.error("[x] DB - File exists. APP_NAME: {} VERSION: {}".format(data['app_name'], data['version']))


def insert_to_db(file):
    try:
        connection = connect_to_sql()
        cursor = connection.cursor()
        postgres_insert_query = """
            INSERT INTO files
            (APP_NAME, FILENAME, VERSION)
            VALUES (%s,%s,%s)
        """
        record_to_insert = (file['app_name'], file['filename'], file['version'])
        cursor.execute(postgres_insert_query, record_to_insert)
        connection.commit()
        logger.info(" [/] Record inserted to database.")

    except Exception as error:
        logger.error("Failed to insert data into database", error)


def get_version_type(url):
    if '/utils/trans/' in url:
        v_type = 'language'
    else:
        v_type = 'parent'
    return v_type


def get_all_versions(version_type, file):
    if version_type == 'parent':
        ver = get_parent_version()
    else:
        ver = get_child_version(file)
    return ver


def get_app_name():
    download_link = "{}{}".format(base_url, parent_urls[-1])
    response = get_url(download_link)

    if response is not None:
        soup = BeautifulSoup(response, 'lxml')
        table = soup.find('table', {"class": "utilcaption"})
        td = table.find_all('td')
        data = td[1].text
        app_name = data.split('</td>')[0]
        app_name = app_name.split('\n')
        if app_name[0] == '':
            app_name = app_name[1]
            app_name = app_name.split(' v')[0]
        else:
            app_name = app_name[0]
            if '-' in app_name:
                app_name = app_name.split('-')[0]
                app_name = app_name.split(' v')[0]
            else:
                app_name = app_name.split(' v')[0]
                app_name = app_name
        return app_name


def get_parent_version():
    download_link = "{}{}".format(base_url, parent_urls[-1])
    response = get_url(download_link)

    if response is not None:
        soup = BeautifulSoup(response, 'lxml')
        table = soup.find('table', {"class": "utilcaption"})
        td = table.find_all('td')
        data = td[1].text
        app_name = data.split('</td>')[0]
        app_name = app_name.split('\n')[0]
        try:
            if '-' in app_name:
                app_name = app_name.split('-')[0]
                app_name = app_name.split(' v')[1]
            else:
                app_name = app_name.split(' v')[1]
                app_name = app_name
        except IndexError:
            app_name = app_name
        return app_name


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
            ver = ''
        elif ver == '\xa0':
            ver = ''
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
        r = requests.get(url, allow_redirects=True)
        if r.status_code == 200:
            logger.info(" [Currently downloading {} APP_NAME: {} VERSION: {}]".format(url, app_name, version))

            if len(existing_data) > 0:
                # Dictionary for comparing from website to database
                comp = {'app_name': app_name, 'version': version, 'filename': filename}
                if comp in existing_data:
                    # If the app name and version is existing in DB
                    logger.error("[File exists. APP_NAME: {} VERSION: {}]".format(app_name, version))
                    logger.error("[Failed to download. APP_NAME: {} VERSION: {}]".format(app_name, version))
                    return False
                else:
                    # Download the updated app
                    download(url, UPLOAD_FOLDER, filename)
                    return True
            else:
                # If the local DB is empty, download everything.
                download(url, UPLOAD_FOLDER, filename)
                return True
        else:
            # If file is not downloadable
            logger.error(" [Currently downloading from {} (APP_NAME: {} VERSION: {})]".format(url, app_name, version))
            logger.error(" [x] Failed to download {}".format(filename))
            return False
    except Exception as e:
        print(e)
        return False


def download(url, UPLOAD_FOLDER, filename):
    wget.download(url, UPLOAD_FOLDER)
    logger.info(" [/] Successfully downloaded {}".format(filename))


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


def make_storage_dir():
    if not os.path.exists(UPLOAD_FOLDER):
        os.mkdir(UPLOAD_FOLDER)


def main():
    logger.info('Harvesting your files.')
    start_time = time.time()
    make_storage_dir()
    get_parts()
    get_parent_url()
    duration = time.time() - start_time
    logger.info("Total: {} record/s inserted successfully into file table".format(len(all_files)))
    logger.info("Downloaded data in {} seconds".format(duration))


if __name__ == '__main__':
    setup_yaml()
    logger = logging.getLogger(__name__)
    main()
