import os
import hashlib
import requests
import pandas as pd
import webbrowser
import wget
from flask import url_for
from numpy.distutils.conv_template import process_file
from werkzeug.utils import secure_filename, redirect
from config import app
from flask import abort

yaml_file = 'config.yaml'
files = []


def get_file_type(file):
    """Get file type"""
    try:
        file_type = file.split('.')[-1]
    except IndexError:
        file_type = "UNKNOWN FILE"
    return file_type


def get_md5(file):
    hd = hashlib.md5(file.encode('utf-8'))
    md5 = str(hd.hexdigest())
    return md5


def get_sha1(file):
    hd = hashlib.sha1(file.encode('utf-8'))
    sha1 = str(hd.hexdigest())
    return sha1


def get_file_size(file):
    """Get file size"""
    if file is None:
        size = "Unknown"
    else:
        size = os.path.getsize(file)
    return size


def delete_file(data):
    f_path = os.path.join(app.config['UPLOAD_FOLDER'], data['filename'])
    try:
        os.remove(f_path)
    except OSError:
        abort(404, f"File {data['filename']} does not exist")


def extract_metadata(f_path):
    sha1 = get_sha1(f_path)
    md5 = get_md5(f_path)
    filename = f_path.split('/')[-1]
    file_type = get_file_type(f_path)
    size = get_file_size(f_path)
    data = {'file_size': size, 'filename': filename, 'sha1': sha1, 'md5': md5, 'file_type': file_type}
    return data
