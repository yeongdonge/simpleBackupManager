import pickle
from pathlib import Path
from cryptography.fernet import Fernet
from repository.encKey import EncKey
import backupUtil.common as common

path = str(Path(__file__).parent.parent) + '/resources/config.pickle'

enc_key_load = EncKey().instance()


## Save pickle
def save(config_info):
    key = enc_key_load.key
    cipher_key = Fernet(key)
    print(path)
    print(f'save -------------{key}')
    with open(path, "wb") as initInfo:
        encrypted = [bytes(s, 'utf-8') for s in list(config_info.__dict__.values())]
        cipher_text = [cipher_key.encrypt(s) for s in encrypted]
        pickle.dump(cipher_text, initInfo)
        common.create_encKey_info(str(key))



## Load pickle
def load():
    with open(path, "rb") as getInfo:
        key = common.get_encKey()
        cipher_key = Fernet(key)
        print(f'load---------------{key}')
        load = pickle.load(getInfo)
        print(load)
        print(type(load))
        load_ = [cipher_key.decrypt(s).decode('utf-8') for s in load]
        print(load_)

# ## Save pickle
# def save(config_info):
#     print(path)
#     with open(path, "wb") as initInfo:
#         pickle.dump(config_info, initInfo)
#
#
# ## Load pickle
# def load():
#     with open(path, "rb") as getInfo:
#         return pickle.load(getInfo)
