import pymysql
import repository.dbConnectionRepository as dbConRepo


class DbCon:
    __instance = None

    def __init__(self, schema):
        if DbCon.__instance is not None:
            raise Exception("Singleton class, use instance() method instead")
        else:
            DbCon.__instance = self
            self.connection = pymysql.connect(
                host=str(dbConRepo.load().host),
                port=int(dbConRepo.load().port),
                user=str(dbConRepo.load().user),
                password=str(dbConRepo.load().password),
                db=str(schema),
                charset='utf8mb4'
            )

    @staticmethod
    def instance(schema: object) -> object:
        if DbCon.__instance is None:
            DbCon(schema)
        return DbCon.__instance
