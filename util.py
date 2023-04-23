import configparser
import os


def validate_cnf_path(my_cnf_path):
    validate = os.path.exists(my_cnf_path)
    return validate


def find_basedir(my_cnf_path):
    config = configparser.ConfigParser(allow_no_value=True, strict=False)
    config.read(my_cnf_path)
    try:
        cnf_dict = {f"basedir : {config.get('mysqld', 'basedir')}",
                    f"port : {config.get('mysqld','port')}",
                    f"socket : {config.get('mysqld','socket')}"}
    except:
        print(f'Not exists Elements (basedir, port, socket) in {my_cnf_path}')
        return f'Backup Manager terminated!'
    return cnf_dict
