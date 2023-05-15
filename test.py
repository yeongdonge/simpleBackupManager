from repository.dbCon import DbCon

db = DbCon.instance('information_schema')
print(db.host)