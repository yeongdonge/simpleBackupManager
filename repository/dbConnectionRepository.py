import pickle
from pathlib import Path

path = str(Path(__file__).parent.parent) + '/resources/db.pickle'

## Save pickle
def save(connection_info):
    print(path)
    with open(path, "wb") as initInfo:
        pickle.dump(connection_info, initInfo)


## Load pickle
def load():
    with open(path, "rb") as getInfo:
        return pickle.load(getInfo)

# def save_encrypted_pickle(filename, key, data):
#     encrypted_data = encrypt_data(key, data)
#     with open(filename, 'wb') as file:
#         file.write(encrypted_data)
