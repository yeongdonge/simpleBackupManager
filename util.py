import subprocess
import configparser
import os


def validate_cnf_path(my_cnf_path):
    validate = os.path.exists(my_cnf_path)
    return validate


def find_elements(my_cnf_path):
    config = configparser.ConfigParser(allow_no_value=True, strict=False)
    config.read(my_cnf_path)
    try:
        cnf_dict = {'basedir': f"{config.get('mysqld', 'basedir')}",
                    'port': f"{config.get('mysqld','port')}",
                    'socket': f"{config.get('mysqld','socket')}"}
    except:
        print(f'Not exists Elements (basedir, port, socket) in {my_cnf_path}')
        return f'Backup Manager terminated!'
    return cnf_dict


def print_backup_tool(basedir):
    tool_sample = ['mysqldump', 'mysqlbackup', 'mariabackup']
    exists_tool = []

    for tool in tool_sample:
        if os.path.exists(f'{basedir}/bin/{tool}'):
            exists_tool.append(tool)

    return exists_tool
