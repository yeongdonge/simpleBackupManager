from domain.connectionInfo import ConnectionInfo
from repository.dbCon import DbCon
import repository.dbConnectionRepository as dbConRepo

con = DbCon.instance('information_schema')
conInfo: ConnectionInfo = dbConRepo.load()


def get_schema():
    with con.connection.cursor() as cursor:
        cursor.execute("SELECT SCHEMA_NAME FROM SCHEMATA")
        result = cursor.fetchall()
        print(result)
        con.connection.close()