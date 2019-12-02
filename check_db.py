from initial import *
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
            app_name = row[2]
            filename = row[3]
            version = row[4]
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
            (URL, APP_NAME, FILENAME, VERSION)
            VALUES (%s,%s,%s,%s)
        """
        record_to_insert = (file['url'], file['app_name'], file['filename'], file['version'])
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
            SET URL=%s
                APP_NAME=%s
                FILENAME=%s
                VERSION=%s
            WHERE FILENAME=%s
        """
        record_to_insert = (file['url'], file['app_name'], file['filename'], file['version'])
        cursor.execute(postgres_insert_query, record_to_insert)
        connection.commit()
        logger.info(" [/] Record updated to database.")

    except Exception as error:
        logger.error("Failed to insert data in database", error)
