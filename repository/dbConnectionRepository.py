import pickle
from pathlib import Path

path = str(Path(__file__).parent.parent) + '/resources/db.pickle'


## Save pickle
def save(conncetion_info):
    print(path)
    with open(path, "wb") as initInfo:
        pickle.dump(conncetion_info, initInfo)


## Load pickle
def load():
    with open(path, "rb") as getInfo:
        return pickle.load(getInfo)
