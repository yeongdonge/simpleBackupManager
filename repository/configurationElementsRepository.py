import base64
import pickle
from pathlib import Path
from cryptography.fernet import Fernet
from repository.encKey import EncKey
import backupUtil.common as common
from domain.configurationElements import ConfigElements

path = str(Path(__file__).parent.parent) + '/resources/config.pickle'


## Save pickle
def save(config_info):
    print(path)
    with open(path, "wb") as initInfo:
        pickle.dump(config_info, initInfo)


## Load pickle
def load():
    with open(path, "rb") as getInfo:
        return pickle.load(getInfo)
