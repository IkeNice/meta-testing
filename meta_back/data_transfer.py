import airtable
import datetime
import time

import psycopg2

APP_ID = 'appbssvSnF3Oq5dgI'
APP_KEY = 'key2opSCUNgWPJ6x0'
TABLE = 'Psychotherapists'
AIRTABLE_URL = 'https://api.airtable.com/v0/' + APP_ID


def db_connection():
    postgres_connection = psycopg2.connect("dbname=therapists user=postgres password=admin")
    cursor = postgres_connection.cursor()
    return cursor, postgres_connection


def get_data_from_airtable(app_id=APP_ID, app_key=APP_KEY, table=TABLE):
    at = airtable.Airtable(app_id, app_key)
    res = at.get(table)
    return res


def convert_string(data_to_convert):
    converted_to_str = str(data_to_convert).replace('\'', '"')
    return converted_to_str


def convert_airtable_data(raw_data):
    converted_output = []
    for i, val in enumerate(raw_data['records']):
        methods_list = str(val['fields']['Методы']).replace('\'', '"')
        photo_url = val['fields']['Фотография'][0]['thumbnails']['large']['url']
        row = (i + 1, val['fields']['Имя'], methods_list, photo_url)
        converted_output.append(row)
    return converted_output


def get_changes():
    # данные из таблицы postrgesql
    cur, conn = db_connection()
    cur.execute("select * from therapist_profile_profile")
    old_data = cur.fetchall()

    # данные из таблицы Airtable
    raw_data = get_data_from_airtable(APP_ID, APP_KEY, TABLE)
    new_data = convert_airtable_data(raw_data)
    # print(old_data)
    # print(new_data)
    diff = list(set(new_data) - set(old_data)) + list(set(old_data) - set(new_data))
    if diff:
        #     if len(old_data) == len(new_data):
        #         # need to be update
        #         print('same len', diff)
        #         # update_db_row(diff)
        #     elif len(old_data) < len(new_data):
        #         # need to insert
        #         print('more row in airtable! need to insert\n', diff)
        #         # insert_in_db(diff)
        #     else:
        #         # need to delete
        #         print('more row in postgresql! need to delete\n', diff)
        #         # delete_from_db(diff)
        for row in diff:
            print(row)
    else:
        print('no diff')


def insert_in_db(data):
    try:
        cur, conn = db_connection()

        for _, row in enumerate(data):
            insert_query = "insert into therapist_profile_profile(name, methods, photo) values (" \
                           "'" + row[1] + "', '" + row[2] + "', '" + row[3] + "');"
            cur.execute(insert_query)
            conn.commit()

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def delete_from_db(data):
    try:
        cur, conn = db_connection()

        for _, row in enumerate(data):
            delete_query = "delete from therapist_profile_profile where id=" + str(row[0])
            cur.execute(delete_query)
            conn.commit()

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def update_db_row(data):
    print(data)
    # try:
    #     cur, conn = db_connection()
    #
    #     for _, row in enumerate(data):
    #         update_query = "update therapist_profile_profile " + \
    #                        " set name=" + row[1] + ", methods=" + row[2] + ", photo=" + row[3] + \
    #                        "where id=" + row[0]
    #         cur.execute(update_query)
    #         conn.commit()
    #
    #     cur.close()
    # except (Exception, psycopg2.DatabaseError) as error:
    #     print(error)
    # finally:
    #     if conn is not None:
    #         conn.close()


def create_new_table():
    table_creation_time = round(time.time())
    table_name = 'new_data' + str(table_creation_time)

    try:
        cur, conn = db_connection()

        sql_create_table = "create table " \
                           + table_name + \
                           " (id SERIAL PRIMARY KEY, running_date timestamp without time zone, raw_data text);"
        cur.execute(sql_create_table)
        conn.commit()

        running_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        raw_data = get_data_from_airtable(APP_ID, APP_KEY, TABLE)
        raw_data_convert = convert_string(raw_data)

        sql_query = "insert into " + table_name + "(running_date, raw_data) values('" \
                    + running_date + "', '" \
                    + str(raw_data_convert) + "')"
        cur.execute(sql_query)
        conn.commit()

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def run():
    pass


if __name__ == '__main__':
    # create_new_table()
    get_changes()
