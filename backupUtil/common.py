from domain.connectionInfo import ConnectionInfo
from repository.dbCon import DbCon
import repository.dbConnectionRepository as dbConRepo
import pprint

con = DbCon.instance('information_schema')

def get_schema():
    with con.connection.cursor() as cursor:
        cursor.execute("SELECT SCHEMA_NAME FROM SCHEMATA")
        result = cursor.fetchall()
        schema = [row[0] for row in result]
        schema_list: [] = list(schema)
        con.connection.close()
        return schema_list

def create_encKey_info(key):
    try:
        with con.connection.cursor() as cursor:
            create_schema_query = f"CREATE DATABASE enc_database"
            cursor.execute(create_schema_query)

            con.select_db("enc_database")
            create_table_query = """
            CREATE TABLE enc_key(
                id INT PRIMARY KEY AUTO_INCREMENT,
                enc_key VARCHAR(50) NOT NULL
                )
            """
            cursor.execute(create_table_query)

            insert_query = "INSERT INTO {}(key) VALUES({})".format("enc_database", str(key))
            cursor.execute(insert_query)
            con.commit()
    finally:
        con.close()

def get_encKey():
    try:
        with con.connection.cursor() as cursor:
            select_encKey = "SELECT enc_key FROM enc_database ORDER BY id DESC LIMIT 1"
            cursor.execute(select_encKey)
            row = cursor.fetchone()
            return row
    finally:
        con.close()

def select_schema(schema_list: [], selected_schema_index: []):
    schema_name_list = []
    print(selected_schema_index)
    for i in range(len(selected_schema_index)):
        schema_name_list.append(schema_list[int(selected_schema_index[i])-1])
        print(schema_list[i])
    return schema_name_list





