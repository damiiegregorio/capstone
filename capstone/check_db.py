import psycopg2

from initial import *
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
existing_data = []


def connect_to_sql():
    mysql = open_yaml()

    connection = psycopg2.connect(
        user=mysql['user'],
        password=mysql['password'],
        host=mysql['host'],
        port=mysql['port'],
        database=mysql['db'],
    )
    return connection


def get_parts():
    """ query parts from the parts table """
    connection = connect_to_sql()
    try:
        cur = connection.cursor()
        cur.execute("SELECT * FROM files")
        rows = cur.fetchall()
        for row in rows:
            app_name = row[1]
            filename = row[2]
            version = row[3]
            compare_data = {'app_name': app_name, 'version': version, 'filename': filename}
            existing_data.append(compare_data)
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            connection.close()


def insert_to_db(file):
    try:
        connection = connect_to_sql()
        cursor = connection.cursor()
        postgres_insert_query = """
            INSERT INTO files
            (APP_NAME, FILENAME, VERSION)
            VALUES (%s,%s,%s)
        """
        record_to_insert = (file['app_name'], file['filename'], file['version'])
        cursor.execute(postgres_insert_query, record_to_insert)
        connection.commit()
        logger.info(" [/] Record inserted to database.")

    except Exception as error:
        logger.error("Failed to insert data into database", error)


def update_file(file):
    try:
        connection = connect_to_sql()
        cursor = connection.cursor()
        postgres_insert_query = """
            UPDATE files
            SET APP_NAME=%s
                FILENAME=%s
                VERSION=%s
            WHERE FILENAME=%s
        """
        record_to_insert = (file['app_name'], file['filename'], file['version'])
        cursor.execute(postgres_insert_query, record_to_insert)
        connection.commit()
        logger.info(" [/] Record updated to database.")

    except Exception as error:
        logger.error("[x] Failed to insert data in database", error)


def create_db():
    mysql = connect_to_sql()
    connection = connect_to_sql()
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)  # <-- ADD THIS LINE

    cur = connection.cursor()
    cur.execute(sql.SQL("CREATE DATABASE {}").format(
        sql.Identifier(mysql['db']))
    )
    logger.info("Database created.")


def create_table():
    try:
        mysql = connect_to_sql()
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
            APP_NAME          varchar         NOT NULL,
            FILENAME          varchar         NOT NULL,
            VERSION         varchar         NOT NULL); 
        """

        cursor.execute(create_table_query)
        connection.commit()
        logger.info("Table created successfully in PostgreSQL")

    except (Exception, psycopg2.Error) as error:
        logger.error("Error while connecting to PostgreSQL", error)