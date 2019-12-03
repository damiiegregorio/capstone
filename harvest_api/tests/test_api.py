import unittest
import harvest
import os
import requests

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
local_storage = "{}\\storage{}".format(os.getcwd(), data_test['filename'])
metadata = {'filename': 'webbrowserpassview.zip', 'sha1': '679544bf6463b84b83db219277733c1437493e87', 'md5': '413fc50e56560042ecd341375f63c081', 'file_type': 'zip', 'file_size': 235627}


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

    def test_create(self):
        result = harvest.create(metadata)
        assert result == 'something'