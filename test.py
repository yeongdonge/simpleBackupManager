
import pickle
import repository.encKey as encAndDec
from pathlib import Path
from cryptography.fernet import Fernet

# from repository.dbCon import DbCon
#
# db = DbCon.instance('information_schema')
#
# with db.connection.cursor() as cursor:
#     cursor.execute("SELECT sum(index_length+data_length)/1024/1024/1024 from tables")
#     result = cursor.fetchall()
#     print(result)
# db.connection.close()

key = Fernet.generate_key()

cipher_key = Fernet(key)

path = str(Path(__file__).parent) + '/resources/test.pickle'
print(path)

col1 = '아아아'


# Save pickle
def save(data: str):
    print(path)
    with open(path, "wb") as initInfo:
        encrypted = bytes(data, 'utf-8')
        cipher_text = cipher_key.encrypt(encrypted)
        pickle.dump(cipher_text, initInfo)


## Load pickle
def load():
    with open(path, "rb") as getInfo:
        load = pickle.load(getInfo)
        print(type(load))
        print(str(load))
        return cipher_key.decrypt(load)


save(col1)

load1 = load()
print(load1.decode('utf-8'))

# from cryptography.fernet import Fernet
#
# key = Fernet.generate_key()
#
# cipher_suite = Fernet(key)
#
# cipher_text = cipher_suite.encrypt(b"A really secret message. Not for prying eyes.")
#
# plain_text = cipher_suite.decrypt(cipher_text)
#
# print("encrypt_text : ", cipher_text)
# print("decrypt_text : ", plain_text)
