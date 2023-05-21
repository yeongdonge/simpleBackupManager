#!/usr/bin/python3.6
import common_util
import signal
import typer
import getpass
import re
import subprocess
import repository.dbConnectionRepository as dbConRepo
import repository.configurationElementsRepository as configRepo
from domain.configurationElements import ConfigElements
from domain.connectionInfo import ConnectionInfo
from backupUtil.common import get_schema
from backupUtil.common import select_schema
from backupUtil.common import get_tables
from backupUtil.mysqldump import MysqlDump

signal.signal(signal.SIGINT, common_util.signal_handler)
print(r"""
 _____  _                    _        ______               _                   ___  ___
/  ___|(_)                  | |       | ___ \             | |                  |  \/  |
\ `--.  _  _ __ ___   _ __  | |  ___  | |_/ /  __ _   ___ | | __ _   _  _ __   | .  . |  __ _  _ __    __ _   __ _   ___  _ __
 `--. \| || '_ ` _ \ | '_ \ | | / _ \ | ___ \ / _` | / __|| |/ /| | | || '_ \  | |\/| | / _` || '_ \  / _` | / _` | / _ \| '__|
/\__/ /| || | | | | || |_) || ||  __/ | |_/ /| (_| || (__ |   < | |_| || |_) | | |  | || (_| || | | || (_| || (_| ||  __/| |
\____/ |_||_| |_| |_|| .__/ |_| \___| \____/  \__,_| \___||_|\_\ \__,_|| .__/  \_|  |_/ \__,_||_| |_| \__,_| \__, | \___||_|
                     | |                                               | |                                    __/ |
                     |_|                                               |_|                                   |___/
                    
                    
                    YOU CAN START SIMPLE BACKUP Tool ( option : init -> load -> backup )
""")


app = typer.Typer()


@app.command()
def init():
    """ 데이터베이스 정보를 입력합니다. (port, user, password, socket) user, password를 제외한 정보는 my.cnf에서 명시적으로 표기되어 있어야 합니다.
    ex)
    [mysqld]
    basedir=/mysql/
    socket=/tmp/mysql.sock
    """
    while True:
        cnf_path = input('Enter Your MySQL(MariaDB) Configuration Absolute Path : ')
        validate = common_util.validate_path(str(cnf_path.strip()))
        if not validate:
            print('Wrong path, try again...')
            cnf_path = ''
            continue
        else:
            cnf_dict = common_util.find_elements(cnf_path)
            if not isinstance(cnf_dict, dict):
                if cnf_dict:
                    print(cnf_dict)

            # Get Connection Info
            port = cnf_dict.get('port')
            user = input('Enter User : ')
            password = getpass.getpass('Enter Password : ')
            socket = cnf_dict.get('socket')

            dbConRepo.save(ConnectionInfo(port, user, password, socket))
            # Get Configuration Info
            basedir = cnf_dict.get('basedir')
            datadir = cnf_dict.get('datadir')
            while True:
                backupdir = input('Enter the Backup Directory : ')
                if not common_util.validate_path(backupdir):
                    print('Wrong path, try again...')
                    backupdir = ''
                    continue
                else:
                    break
            configRepo.save(ConfigElements(basedir, datadir, backupdir))
        break


@app.command()
def load():
    """ init에서 입력한 정보들을 출력합니다. 패스워드는 노출되지 않습니다."""
    print(f'DB Connection Init Info\n'
          f'Port = {dbConRepo.load().port}\n'
          f'User = {dbConRepo.load().user}\n'
          f'Password = Invisible\n\n\n'
          f'Configuration Init Info\n'
          f'Basedir = {configRepo.load().basedir}\n'
          f'Datadir = {configRepo.load().datadir}\n'
          f'Backupdir = {configRepo.load().backupdir}')


@app.command()
def backup():
    """ backup을 수행합니다."""
    backup_common_util_list = common_util.get_backup_util(configRepo.load().basedir)
    print(f'Select Backup Tools\n')
    for i in range(len(backup_common_util_list)):
        print(f'{i + 1}. {backup_common_util_list[i]}')

    while True:
        try:
            selected_tool = int(input('Enter index of Backup Tool : '))
            break
        except IndexError:
            print('Wrong index, try again...')
            pass
    prefix_util = str(f'[{backup_common_util_list[selected_tool - 1]}]')
    print(f'{prefix_util} Schema list in MySQL(MariaDB)')
    schema_list: [] = get_schema()
    for i in range(len(schema_list)):
        print(f"{str(str((i + 1)) + '.').ljust(3)} {(schema_list[i])}")
    print(f"{str('99.').ljust(2)} ALL Schemas")
    selected_index = input(f"Select backup schemas \n"
                           f"(separated by commas, spaces are ignored, '99' input means all schemas)\n"
                           f": ")
    splitted_index = re.split(r',s*', selected_index)
    if '99' in splitted_index:
        length = len(schema_list)
        schema_name_list = select_schema(schema_list, list(range(0, length)))
    else:
        while True:
            try:
                output_list = [index.strip() for index in splitted_index]
                schema_name_list = select_schema(schema_list, output_list)
                break
            except IndexError:
                print('Wrong index, try again...')
                pass

    print('The selected schemas are as follows... ')
    print(schema_name_list)

    export_backup_filename = input(f'Enter export Backup filename [{configRepo.load().backupdir}]'
                                   ': ')
    if len(schema_name_list) == 1:
        while True:
            try:
                option = input(f'You have selected one schema. Please select an option.\n'
                               f'1. Schema Backup\n'
                               f'2. Table Backup\n'
                               f': ')
                if int(option) == 1:
                    dump_schema_backup(configRepo.load().basedir, schema_name_list, configRepo.load().backupdir,
                                       export_backup_filename)
                else:
                    print(schema_name_list[0])
                    table_list = get_tables(str(schema_name_list[0]))

                    for i in range(len(table_list)):
                        print(f"{str(str((i + 1)) + '.').ljust(3)} {(table_list[i])}")
                    print(f"{str('99.').ljust(2)} ALL Tables")
                    selected_index = input(f"Select backup tables \n"
                                           f"(separated by commas, spaces are ignored, '99' input means all schemas)\n"
                                           f": ")

                    splitted_index = re.split(r',s*', selected_index)
                    if '99' in splitted_index:
                        length = len(table_list)
                        table_name_list = select_schema(table_list, list(range(0, length)))
                    else:
                        while True:
                            try:
                                output_list = [index.strip() for index in splitted_index]
                                table_name_list = select_schema(table_list, output_list)
                                break
                            except IndexError:
                                print('Wrong index, try again...')
                                pass
                    mysqldump = get_mysqldump_instance(dbConRepo.load().user, dbConRepo.load().password,
                                                      dbConRepo.load().port, dbConRepo.load().socket)
                    os_command = mysqldump.table_backup(configRepo.load().basedir, schema_name_list[0],
                                                        table_name_list,
                                                        f'{configRepo.load().backupdir}/{export_backup_filename}')
                    print(f'................{os_command}')
                    subprocess.run(os_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                break
            except IndexError:
                print('Wrong index, try again...')
                pass
    else:
        dump_schema_backup(configRepo.load().basedir, schema_name_list, configRepo.load().backupdir,
                           export_backup_filename)


def get_mysqldump_instance(user, password, port, socket):
    mysqldump = MysqlDump(dbConRepo.load().user, dbConRepo.load().password, dbConRepo.load().port,
                          dbConRepo.load().socket)
    return mysqldump


def dump_schema_backup(basedir, table_name_list, backupdir, export_backup_filename):
    mysqldump = get_mysqldump_instance(dbConRepo.load().user, dbConRepo.load().password, dbConRepo.load().port,
                                      dbConRepo.load().socket)
    option = input(f'Select option during processing mysqldump.\n'
                   f'1. event - Include Event Scheduler events for the dumped databases in the output. This option requires the EVENT privileges for those databases.\n'
                   f'2. routine - Include stored routines (procedures and functions) for the dumped databases in the output. This option requires the global SELECT privilege.\n'
                   f'3. single-transaction - This option sets the transaction isolation mode to REPEATABLE READ and sends a START TRANSACTION SQL statement to the server before dumping data.\n'
                   f'(separated by commas, spaces are ignored)\n'
                   f':  ')
    splitted_option = re.split(r',s*', option)

    os_command = mysqldump.schema_backup(configRepo.load().basedir, table_name_list, splitted_option,
                                         f'{configRepo.load().backupdir}/{export_backup_filename}')
    print(os_command)
    subprocess.run(os_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


if __name__ == "__main__":
    app()
