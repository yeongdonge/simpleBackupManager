import base64

from repository.dbCon import DbCon


def get_schema():
    con = DbCon.instance('information_schema')
    with con.connection.cursor() as cursor:
        cursor.execute("SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME not in ('PERFORMANCE_SCHEMA', 'INFORMATION_SCHEMA');")
        schema = list([row[0] for row in cursor.fetchall()])
        con.connection.close()
        return schema

def get_tables(schema: str):
    con = DbCon.instance('information_schema')
    with con.connection.cursor() as cursor:
        cursor.execute("""
            SELECT TABLE_NAME FROM INFORMATION_SCHEMA_TABLES WHERE TABLE_SCHEMA = {}""".format(schema))
        tables = list([row[0] for row in cursor.fetchall()])
        con.connection.clse()
        return tables


def select_schema(schema_list: [], selected_schema_index: []):
    schema_name_list = []
    print(selected_schema_index)
    for i in range(len(selected_schema_index)):
        schema_name_list.append(schema_list[int(selected_schema_index[i]) - 1])
        print(schema_list[i])
    return schema_name_list

# def init_enc_schema():
#     con = DbCon.instance('information_schema')
#     try:
#         with con.connection.cursor() as cursor:
#             drop_schema_query = """
#                 DROP DATABASE IF EXISTS enc_database
#                 """
#             cursor.execute(drop_schema_query)
#
#             create_schema_query = """
#                 CREATE DATABASE enc_database
#                 """
#             cursor.execute(create_schema_query)
#
#             con.connection.select_db("enc_database")
#             drop_table_query = """
#             DROP TABLE IF EXISTS enc_database.enc_key_tb
#             """
#             cursor.execute(drop_table_query)
#             create_table_query = """
#             CREATE TABLE enc_key_tb(
#                 id INT PRIMARY KEY AUTO_INCREMENT,
#                 name VARCHAR(20) NOT NULL,
#                 enc_key VARCHAR(100) NOT NULL
#              )
#             """
#             cursor.execute(create_table_query)
#     finally:
#         con.connection.close()
#
#
# def create_encKey_info(name, key):
#     con = DbCon.instance('information_schema')
#     try:
#         with con.connection.cursor() as cursor:
#             print(f'name----------{name}----------key-----------{key}')
#             insert_query = """
#             INSERT INTO enc_database.enc_key_tb(name, enc_key) VALUES(%s, %s)
#              """
#                 # .format(name, base64.urlsafe_b64encode(key).decode())
#             cursor.execute(insert_query, (name, key,))
#             con.connection.commit()
#     finally:
#         pass
#
# def get_encKey(name):
#     con = DbCon.instance('enc_database')
#     try:
#         with con.connection.cursor() as cursor:
#             selected_encKey = "SELECT enc_key FROM enc_key_tb WHERE name = %s ORDER BY id DESC LIMIT 1"
#             cursor.execute(selected_encKey, (name,))
#             row = cursor.fetchone()
#             encrypted_key = row["enc_key"]
#             return encrypted_key
#     finally:
#         pass
