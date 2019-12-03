from urllib.request import urlopen
from bs4 import BeautifulSoup
import unittest
import harvest
import logging
import os

events = []
data_test = {'url': 'http://54.174.36.110/utils/trans/webbrowserpassview_arabic.zip',
             'app_name': 'WebBrowserPassView', 'filename': 'webbrowserpassview_arabic.zip',
             'version': '1.60', 'version_type': 'parent'}
url = 'http://54.174.36.110/trans/webbrowserpassview_arabic.zip'
base_url = 'http://54.174.36.110/'
local_storage = "{}\\storage".format(os.getcwd())
config = {'host': 'localhost', 'user': 'postgres', 'db': 'harvest_app', 'port': 5432, 'password': 'novirus123'}


class TestHarvest(unittest.TestCase):
    harvest.setup_yaml()
    logger = logging.getLogger(__name__)

    def test_get_version_type(self):
        assert harvest.get_version_type(url) == data_test['version_type']

    def test_get_filename(self):
        assert harvest.get_filename(url) == data_test['filename']

    def test_open_yaml(self):
        result = harvest.open_yaml()
        assert result == config

