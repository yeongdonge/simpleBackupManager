import pymysql
from pymysql.cursors import DictCursor
import repository.dbConnectionRepository as dbConRepo


class DbCon:
    __instance = None
    connection = None

    def __init__(self, schema):
        if DbCon.__instance is not None:
            raise Exception("Singleton class, use instance() method instead")
        else:
            DbCon.__instance = self
            self.connection = pymysql.connect(
                host='localhost',
                port=int(dbConRepo.load().port),
                user=str(dbConRepo.load().user),
                password=str(dbConRepo.load().password),
                db=str(schema),
                charset='utf8mb4',
                # cursorclass=DictCursor
            )

    @staticmethod
    def instance(schema: object) -> object:
        if DbCon.__instance is None:
            DbCon(schema)
        return DbCon.__instance
