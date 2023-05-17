from domain.connectionInfo import ConnectionInfo
from repository.dbCon import DbCon
import repository.dbConnectionRepository as dbConRepo
import pprint


def get_schema():
    con = DbCon.instance('information_schema')
    with con.connection.cursor() as cursor:
        cursor.execute("SELECT SCHEMA_NAME FROM SCHEMATA")
        result = cursor.fetchall()
        schema = [row[0] for row in result]
        schema_list: [] = list(schema)
        con.connection.close()
        return schema_list


def select_schema(schema_list: [], selected_schema_index: []):
    schema_name_list = []
    print(selected_schema_index)
    for i in range(len(selected_schema_index)):
        schema_name_list.append(schema_list[int(selected_schema_index[i])-1])
    return schema_name_list





