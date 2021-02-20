import sys
import os
import django

import airtable
import datetime
import time

import psycopg2

# Turn off bytecode generation
sys.dont_write_bytecode = True

# Django specific settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SetupDjangoORM.SetupDjangoORM')
django.setup()

# Import models for use in script
from therapist_profile.models import Profile

try:
    import db_config as conf
except ImportError:
    exit('DO: copy db_config.py.default in db_config.py and set token')

APP_ID = conf.APP_ID
APP_KEY = conf.APP_KEY
TABLE = conf.TABLE
AIRTABLE_URL = 'https://api.airtable.com/v0/' + APP_ID


def db_connection():
    """ Set up the connection to PostgreSQL """
    postgres_connection = psycopg2.connect(conf.DB_SETUP)
    cursor = postgres_connection.cursor()
    return cursor, postgres_connection


def get_data_from_airtable(app_id=APP_ID, app_key=APP_KEY, table=TABLE):
    """ Get data from Airtable """
    at = airtable.Airtable(app_id, app_key)
    res = at.get(table)
    return res


def convert_string(data_to_convert):
    """ Replace single quote with double quote """
    converted_to_str = str(data_to_convert).replace('\'', '"')
    return converted_to_str


def convert_airtable_data(raw_data):
    """ Convert airtable data from to tuple """
    converted_output = []
    for i, val in enumerate(raw_data['records']):
        methods_list = str(val['fields']['Методы']).replace('\'', '"')
        photo_url = val['fields']['Фотография'][0]['thumbnails']['large']['url']
        row = (i + 1, val['fields']['Имя'], methods_list, photo_url)
        converted_output.append(row)
    return converted_output


def get_data_from_postgres():
    """ Get data from PostgreSQL and convert into tuple """
    data = Profile.objects.all()
    old_data = []
    for row in data:
        old_profile_info = (row.id, row.name, row.methods, row.photo)
        old_data.append(old_profile_info)
    return old_data


def get_changes():
    """
        Compare data from PostgreSQL with data from Airtable.
        If changes detected, then handle it
    """
    # fetch data from postgresql
    old_data = get_data_from_postgres()

    # fetch data from Airtable
    raw_data = get_data_from_airtable(APP_ID, APP_KEY, TABLE)
    new_data = convert_airtable_data(raw_data)

    old_data_id = []
    new_data_id = []

    for i in range(len(old_data)):
        old_data_id.append(old_data[i][0])
    for i in range(len(new_data)):
        new_data_id.append(new_data[i][0])

    # Get difference between old and new data
    diff = list(set(old_data) - set(new_data)) + list(set(new_data) - set(old_data))
    if diff:
        for row in diff:
            if not(row[0] in old_data_id):
                print(row[1], "not in old data, inserting it")
                insert_in_db(row)
            elif not(row[0] in new_data_id):
                print(row[1], "not in new data, deleting it")
                delete_from_db(row)
            else:
                print(row[1], "in both data, updating it")
                update_db_row(row)
    else:
        print('there is no difference')


def insert_in_db(data):
    """ Insert data in table therapist_profile_profile in PostgreSQL """
    profile = Profile(id=data[0], name=data[1], methods=data[2], photo=data[3])
    profile.save()


def delete_from_db(data):
    """ Delete data from table therapist_profile_profile in PostgreSQL """
    profile = Profile.objects.get(id=data[0])
    profile.delete()


def update_db_row(data):
    """ Update data in table therapist_profile_profile in PostgreSQL """
    profile = Profile.objects.get(id=data[0])
    Profile.objects.filter(id=profile.id).update(name=data[1], methods=data[2], photo=data[3])


def create_new_table():
    """ Create new table when running this script """
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
    get_changes()
    create_new_table()


if __name__ == '__main__':
    run()
