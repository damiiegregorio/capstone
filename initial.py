from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import hashlib
import wget
import os
import logging
import logging.config
import requests
import yaml
import psycopg2
import time
import sys

# Global Variables
base_url = 'http://3.228.218.197/'
yaml_file = 'config.yaml'
all_files = []


def get_url(base_url):
    try:
        with closing(get(base_url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
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
        # Skip this array of links
        except_links = ['http://www.nirsoft.net/utils/index.html#internet_utils',
                        'http://www.nirsoft.net/utils/index.html#password_utils',
                        'http://www.nirsoft.net/utils/index.html#network_utils']

        for ref_link in download_links:

            if ref_link.a.get('href') in except_links:
                continue
            else:
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
                    url = get_urls(base_url, file)
                    filename = get_filename(file)
                    sha1 = get_sha1(file)
                    md5 = get_md5(file)
                    file_type = get_file_type(file)
                    file_path = download_file(url, filename)
                    size = get_file_size(file_path)
                    version = '1'
                    data = {'url': url, 'filename': filename, 'sha1': sha1, 'md5': md5,
                            'file_type': file_type, 'size': size, 'version': version}
                    logger.info(data)
                    all_files.append(data)
            return all_files

    else:
        logger.info('[x] Error downloading files.')
        logger.info('[x] No files found to download.')


def get_version(file_path):
    pass


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


def download_file(url, filename):
    try:
        local_storage = 'C:\\Users\\TEU_USER\\PycharmProjects\\capstone\\storage'
        r = requests.get(url, allow_redirects=True)

        if r.status_code is 200:
            logger.info("[Currently downloading {}]".format(url))
            wget.download(url, local_storage)
            logger.info("[/] Successfully downloaded {}".format(filename))
            file_path = "{}{}{}".format(local_storage, os.sep, filename)
            return file_path
        else:
            logger.info("[Currently downloading {}]".format(url))
            logger.error("[x] Failed to download {}".format(filename))
    except Exception as e:
        print(e)


def extract_sha1(hash_path):
    """Extract sha1"""
    sha1_extractor = hashlib.sha1()

    with open(hash_path, 'rb') as afile:
        buf = afile.read()
        sha1_extractor.update(buf)
        sha1 = sha1_extractor.hexdigest()
    return sha1


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


def connect_to_sql():
    global yaml_file
    with open(yaml_file, 'rt') as f:
        config = yaml.safe_load(f.read())
    mysql = config['mysql']

    connection = psycopg2.connect(
        user=mysql['user'],
        password=mysql['password'],
        host=mysql['host'],
        port=mysql['port'],
        database=mysql['db'],
    )
    return connection


def insert_to_db():
    try:
        connection = connect_to_sql()
        cursor = connection.cursor()
        for a_file in all_files:
            postgres_insert_query = """
                                        INSERT INTO files
                                        (URL, FILENAME, SHA1, MD5, FILE_TYPE, SIZE, VERSION)
                                        VALUES (%s,%s,%s,%s,%s,%s,%s)
                                    """
            record_to_insert = (a_file['url'], a_file['filename'], a_file['sha1'], a_file['md5'], a_file['file_type'],
                                a_file['size'], a_file['version'])
            cursor.execute(postgres_insert_query, record_to_insert)
            connection.commit()
            logger.info(a_file)
            logger.info("[/] Record inserted to database.")
        logger.info("Total: {} record/s inserted successfully into file table".format(len(all_files)))

    except Exception as error:
        print("Failed to insert data into sqlite table", error)


def main():
    logger.info('Harvesting your files.')
    logger.info('Please wait.')
    get_parent_url()
    # logger.info('Getting ready to insert your files to database.')
    # insert_to_db()


if __name__ == '__main__':
    setup_yaml()
    logger = logging.getLogger(__name__)
    main()
