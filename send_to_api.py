# import requests
# import os
#
# # upload_files = "{}\storage".format(os.getcwd())
#
#
# def send_data_to_server(file_path):
#     filename = "storage\{}".format(file_path)
#     # print(filename)
#
#     files = {'files': open(filename, 'rb')}
#     response = requests.post('http://localhost:8000/uploader', files=files)
#     print(response.status_code)
#
#
# # send_data_to_server("webbrowserpassview_hungarian.zip")
