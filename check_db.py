from initial import *
existing_data = []


def get_parts():
    """ query parts from the parts table """
    connection = connect_to_sql()
    try:
        cur = connection.cursor()
        cur.execute("SELECT * FROM files")
        rows = cur.fetchall()
        for row in rows:
            url = row[1]
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


def check_if_data_exist():
    get_parts()
    print(existing_data)


if __name__ == '__main__':
    # setup_yaml()
    # logger = logging.getLogger(__name__)
    check_if_data_exist()
