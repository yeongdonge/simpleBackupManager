import common_util
import signal
import typer
import getpass
import repository.dbConnectionRepository as dbConRepo
import repository.configurationElementsRepository as configRepo
from domain.configurationElements import ConfigElements
from domain.connectionInfo import ConnectionInfo
from repository.dbCon import DbCon

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
        validate = common_util.validate_cnf_path(cnf_path)
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
            backupdir = input('Enter the Backup Directory : ')

            configRepo.save(ConfigElements(basedir, datadir, backupdir))

            backup_common_util_list = common_util.get_backup_common_util(cnf_dict.get('basedir'))
            print(f' {backup_common_util_list}')
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
    backup_common_util_list: [] = common_util.get_backup_util(str(configRepo.load().basedir))
    print(f'Select Backup Tools\n')
    for i in range(len(backup_common_util_list)):
        print(f'{i + 1}. {backup_common_util_list[i]}')

    while True:
        try:
            selected_tool = int(input('Enter index of Backup Tool : '))
            break
        except ValueError:
            print('Wrong index, try again...')
            pass
    print(backup_common_util_list[selected_tool - 1])

if __name__ == "__main__":
    app()
