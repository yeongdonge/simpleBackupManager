#!/usr/bin/python3.6
import util

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

while True:
    cnf_path = input('Enter Your MySQL(MariaDB) Configuration Absolute Path : ')
    validate = util.validate_cnf_path(cnf_path)
    if not validate:
        print('Wrong path, try again...')
        cnf_path = ''
    else:
        cnf_dict = util.find_elements(cnf_path)
        print(cnf_dict)
        backup_util_list = util.get_backup_util(cnf_dict.get('basedir'))
        break

print('Detected Backup Util List')
for i in range(len(backup_util_list)):
    print(f'{i+1}. {backup_util_list[i]}')

selected_tool = int(input('Enter index of Backup Tool : '))

print(backup_util_list[selected_tool-1])

