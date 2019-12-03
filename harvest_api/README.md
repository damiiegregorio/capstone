# Harvest API

#### To test
```
pytest --cov=harvest tests/test_api.py
```

### Sample data for fixtures:

```
# test_sha1:
{
    "file_size": 235627,
    "file_type": "zip",
    "filename": "webbrowserpassview.zip",
    "id": 1,
    "md5": "51ccf174229144e15ae8f5d03c77378a",
    "sha1": "c518e88e90e237fc6e6b73ad2b8162012df158bb"
  },
# test_md5
  {
    "file_size": 279147,
    "file_type": "exe",
    "filename": "webbrowserpassview_setup.exe",
    "id": 2,
    "md5": "a34b4914a2c42ebdae417c290ebe7b2e",
    "sha1": "03056314007cb8d35b25cd71029f8a48afbdd562"
  },
# test_create:
{
    "file_size": 1449,
    "file_type": "zip",
    "filename": "webbrowserpassview_arabic.zip",
    "id": 3,
    "md5": "f97c7444c89b7c0c0ed924ad18d47eb2",
    "sha1": "2a43bdb48fc6a96d14d242e8108b1520f22df50b"
  },
  # test_update_sha1
  {
    "file_size": 1800,
    "file_type": "zip",
    "filename": "webbrowserpassview_brazilian_portuguese.zip",
    "id": 4,
    "md5": "6198ed28a09e6aea01cdc5ac9b37ab56",
    "sha1": "ff29ee1c1b59a857f761f09a4fa10852682e18ab"
  },
  # test_update_md5
  {
    "file_size": 1413,
    "file_type": "zip",
    "filename": "webbrowserpassview_croatian.zip",
    "id": 5,
    "md5": "5b49fc7225065ebd31a94d4c9574622a",
    "sha1": "ace6a0133df9da09b6a5a87ee59d2de45c08d8e2"
  },
 #  test_delete_sha1 
  {
    "file_size": 1623,
    "file_type": "zip",
    "filename": "webbrowserpassview_czech.zip",
    "id": 6,
    "md5": "4dd1831e893624ffee94f3a3f2e1e6fe",
    "sha1": "1ea261fcc06c5ef3f729e4eac25c5f01675afcea"
  },
  # test_delete_md5
  {
    "file_size": 1461,
    "file_type": "zip",
    "filename": "webbrowserpassview_dutch.zip",
    "id": 7,
    "md5": "ceb9d13a9850426576b7b99b8034083b",
    "sha1": "27702abd6b353d3d82ca46214155e78c3bf53308"
  },
  {
    "file_size": 1393,
    "file_type": "zip",
    "filename": "webbrowserpassview_french.zip",
    "id": 8,
    "md5": "99a5afd4a5d145ea7c597e7729b93806",
    "sha1": "56cb6acdef094e890bf1434cfbb5f3036b1d1d5f"
  },
  {
    "file_size": 1577,
    "file_type": "zip",
    "filename": "webbrowserpassview_french1.zip",
    "id": 9,
    "md5": "b527075621de7824ea44c030373f8e73",
    "sha1": "a73b8071c13082d24c6f1eb111e5555dbec995ce"
  },
  {
    "file_size": 1669,
    "file_type": "zip",
    "filename": "webbrowserpassview_georgian.zip",
    "id": 10,
    "md5": "5b6fa91e014ce3cd788b1aed334b0583",
    "sha1": "49d44f5b91052d8a41a57005f4570c39db5fb97b"
  },

```
