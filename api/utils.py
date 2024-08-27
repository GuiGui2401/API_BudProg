 
import cx_Oracle
from decouple import config


DBUSER = config('DB_USER')
DBPASSWORD = config('DB_PASS')
DBHOST = config('DB_HOST')
DBPORT = config('DB_PORT')
DBSID = config('DB_SID')
DBDSN = cx_Oracle.makedsn(host=DBHOST, port=DBPORT, service_name=DBSID)


def query_db(query, args={}, one=False):
    try: 
        connection = cx_Oracle.connect(user=DBUSER, password=DBPASSWORD, dsn=DBDSN, encoding="UTF-8")
        print(connection.version)
    except cx_Oracle.Error as error:
        print(error, 'Une errur est survenu')
    with connection.cursor() as cursor:
        cursor.execute(query, args)
        data = cursor.fetchall()
        r = [dict((cursor.description[i][0], value) \
        for i, value in enumerate(row)) for row in data]
        return r