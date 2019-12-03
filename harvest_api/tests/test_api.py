import json
import unittest
import pytest
import harvest
import os
import requests
import config
from config import db

events = []
data_test = {
    'url': 'http://54.174.36.110/utils/trans/webbrowserpassview_arabic.zip',
    'app_name': 'WebBrowserPassView', 'filename': 'webbrowserpassview_arabic.zip',
    'version': '1.60', 'version_type': 'parent', 'file_type': 'zip',
    'sha1': '09197fdf9498be372bee06bbdcc0599754687b8a',
    'md5': '651979f04828bc5144329ea72481c2c8', 'file_size': 235627
}
url = 'http://54.174.36.110/trans/webbrowserpassview_arabic.zip'
base_url = 'http://54.174.36.110/'
metadata = {'filename': 'webbrowserpassview.zip', 'sha1': '679544bf6463b84b83db219277733c1437493e87',
            'md5': '413fc50e56560042ecd341375f63c081', 'file_type': 'zip', 'file_size': 235627}
base_dir = os.path.abspath(os.path.dirname(__file__))
file_path = os.path.join(base_dir, 'storage', metadata['filename'])


class TestHarvestAPI(unittest.TestCase):

    def test_get_file_type(self):
        result = harvest.get_file_type(url)
        assert result == data_test['file_type']

    def test_get_sha1(self):
        result = harvest.get_sha1(data_test['filename'])
        assert result == data_test['sha1']

    def test_get_md5(self):
        result = harvest.get_md5(data_test['filename'])
        assert result == data_test['md5']

    def test_extract_metadata(self):
        result = harvest.extract_metadata(file_path)
        assert result is not None

    def test_get_file_size(self):
        result = harvest.get_file_size(file_path)
        self.assertEqual(result, 235627)


@pytest.fixture(scope='module')
def test_client():
    flask_app = config.connex_app

    flask_app.add_api('swagger.yml')
    # Flask provides a way to test your application by exposing the Werkzeug test Client
    # and handling the context locals for you.
    testing_client = flask_app.app.test_client()

    # Establish an application context before running the tests.
    ctx = flask_app.app.app_context()
    ctx.push()

    yield testing_client  # this is where the testing happens!

    ctx.pop()


def test_home_page(test_client):
    """
    GIVEN a Flask application
    WHEN the '/' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/harvestlog')
    assert response.status_code == 200


def test_sha1(test_client):
    """
    GIVEN a Flask application
    WHEN the '/' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/query/sha1/271c57584c15351e903caa5d13907e1b7c494da0')
    assert response.status_code == 200


def test_md5(test_client):
    """
    GIVEN a Flask application
    WHEN the '/' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/query/md5/ff4dcb04dc3bdc93999dc53715a2d009')
    assert response.status_code == 200


def test_create(test_client):
    """
    GIVEN a Flask application
    WHEN the '/' page is requested (POST)
    THEN check the response is valid
    """

    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    data = {
        'filename': 'create121.zip',
        'sha1': '9f1cf8ca693d2529a23cebc82dfdb3b963214e22',
        'md5': '413fc50e56560042ecd34137aaaaaaaa',
        'file_type': 'zip',
        'file_size': 42
    }

    response = test_client.post('/harvestlog', data=json.dumps(data), headers=headers)
    assert response.status_code == 201


def test_update_sha1(test_client):
    """
    GIVEN a Flask application
    WHEN the '/' page is requested (PUT)
    THEN check the response is valid
    """

    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    data = {
        "file_size": 1447,
        "file_type": "exe",
        "filename": "routerpassview_galician12.exe",
        "id": 38,
        "md5": "d92b3ab03868a1ce61eddd5d92cc5619",
        "sha1": "376ffd6cf8b231f66a94561a63025c11e0603295"
    }

    response = test_client.put('/query/sha1/376ffd6cf8b231f66a94561a63025c11e0603295', data=json.dumps(data), headers=headers)
    assert response.status_code == 200


def test_update_md5(test_client):
    """
    GIVEN a Flask application
    WHEN the '/' page is requested (PUT)
    THEN check the response is valid
    """

    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    data = {
        "file_size": 1437,
        "file_type": "exe",
        "filename": "routerpassview_german1.exe",
        "id": 39,
        "md5": "46355dc39d178a36634a682142005e51",
        "sha1": "9f1cf8ca693d2529a21cebc82dfdb3b59f2e4e22"
    }

    response = test_client.put('/query/md5/46355dc39d178a36634a682142005e51', data=json.dumps(data), headers=headers)
    assert response.status_code == 200


def test_delete_sha1(test_client):
    """
    GIVEN a Flask application
    WHEN the '/' page is requested (DELETE)
    THEN check the response is valid
    """
    response = test_client.delete('/query/sha1/98a4088a61478387e2517496b57eae8650a68ec6')
    assert response.status_code == 200


def test_delete_md5(test_client):
    """
    GIVEN a Flask application
    WHEN the '/' page is requested (DELETE)
    THEN check the response is valid
    """
    response = test_client.delete('/query/md5/3deefc5e93e19a915555cf08d55c430d')
    assert response.status_code == 200

