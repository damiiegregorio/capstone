
## Usage
Setup local database configuration
```python
mysql:
  host: localhost
  user: postgres
  db: <DATABASE_NAME>
  port: <PORT>
  password: <PASSWORD>
api:
  uploader: http://localhost:8000/uploader # api uploader
```
Run
```
python initial.py
```
