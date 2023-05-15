from repository.dbCon import DbCon

db = DbCon.instance('information_schema')

with db.connection.cursor() as cursor:
    cursor.execute("SELECT sum(index_length+data_length)/1024/1024/1024 from tables")
    result = cursor.fetchall()
    print(result)
db.connection.close()
