import os
import logging
import logging.config
import yaml
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

yaml_file = 'config.yaml'


def access_yaml():
    global yaml_file
    with open(yaml_file, 'rt') as f:
        config = yaml.safe_load(f.read())
    mysql = config['mysql']
    return mysql


def connect_to_sql():
    mysql = access_yaml()

    connection = psycopg2.connect(
        user=mysql['user'],
        password=mysql['password'],
        host=mysql['host'],
        port=mysql['port'],
    )
    return connection


def create_db():
    mysql = access_yaml()
    connection = connect_to_sql()
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)  # <-- ADD THIS LINE

    cur = connection.cursor()
    cur.execute(sql.SQL("CREATE DATABASE {}").format(
        sql.Identifier(mysql['db']))
    )
    logger.info("Database created.")


def create_table():
    try:
        mysql = access_yaml()
        connection = psycopg2.connect(
            user=mysql['user'],
            password=mysql['password'],
            host=mysql['host'],
            port=mysql['port'],
            database=mysql['db']
        )
        # Create cursor
        cursor = connection.cursor()

        create_table_query = """
        CREATE TABLE files
            (ID       SERIAL  PRIMARY KEY     NOT NULL,
            URL              varchar         NOT NULL,
            APP_NAME          varchar         NOT NULL,
            FILENAME          varchar         NOT NULL,
            VERSION         varchar         NOT NULL); 
        """

        cursor.execute(create_table_query)
        connection.commit()
        logger.info("Table created successfully in PostgreSQL")

    except (Exception, psycopg2.Error) as error:
        logger.error("Error while connecting to PostgreSQL", error)


def setup_yaml():
    """Setup logging configuration """
    default_level = logging.DEBUG
    yaml_path = 'config.yaml'
    value = os.getenv("LOG_CFG", None)

    if value:
        yaml_path = value
    if os.path.exists(yaml_path):
        with open(yaml_path, 'rt') as f:
            try:
                config = yaml.safe_load(f.read())
                logging.config.dictConfig(config)
            except Exception as e:
                print(e)
                print('Error in Logging Configuration. Using default configs')
                logging.basicConfig(level=default_level, filename="debug.log")
    else:
        logging.basicConfig(level=default_level, filename="debug.log")
        print('Failed to load configuration file. Using default configs')


def main():
    # create_db()
    create_table()


if __name__ == "__main__":
    setup_yaml()
    logger = logging.getLogger(__name__)
    main()
