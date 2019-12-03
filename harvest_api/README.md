# Harvest API

### Running the app:

#### Local environment
Setup database URI using config.py, then run the build_database.py to create database and table.
```python
# config.py
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://<USERNAME>:<PASSWORD>@localhost:<PORT>/<DATABASE_NAME>'
```

Run server.py to start.
```python
python server.py
```
