import configparser
import os
import exception
import pickle

def validate_path(my_cnf_path):
    try:
        validate = os.path.exists(my_cnf_path)
        return validate
    except:
        exception.WrongConfigurationPathError('Failed to read value, please remove space if correct path.')



def find_elements(my_cnf_path):
    config = configparser.ConfigParser(allow_no_value=True, strict=False)
    config.read(my_cnf_path)
    try:
        cnf_dict = {'basedir': f"{config.get('mysqld', 'basedir')}",
                    'datadir': f"{config.get('mysqld', 'datadir')}",
                    'port': f"{config.get('mysqld', 'port')}",
                    'socket': f"{config.get('mysqld', 'socket')}"
                    }
    except configparser.NoOptionError:
        return exception.WrongConfigurationPathError(f'Not exists Elements (basedir, port, socket) in {my_cnf_path}'
                                                     f'Backup Manager is terminated')
    return cnf_dict


def get_backup_util(basedir):
    util_sample = ['mysqldump', 'mysqlbackup', 'mariabackup']
    exists_util = []

    for tool in util_sample:
        if os.path.exists(f'{basedir}/bin/{tool}'):
            exists_util.append(tool)

    return exists_util


def signal_handler(sig, frame):
    return exception.DetectedSignalKeyError('\n\n\n'
                                            'You pressed Ctrl+C!'
                                            '\n\n\n')
