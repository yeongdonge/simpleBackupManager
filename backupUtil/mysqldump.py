class MysqlDump:
    options_list = ['events', 'triggers', 'routines', 'triggers', 'single-transaction', 'all-databases']

    def __init__(self, username, password, port, socket):
        self.username = username
        self.password = password
        self.port = port
        self.socket = socket

    def schema_backup(self, basedir: str, schema_list: list, option_list: list, backup_name: str):
        schema_prefix = ' '
        option_prefix = '-- '
        schema_join = schema_prefix + ' '.join(schema_list)
        option_join = option_prefix + '-- '.join(option_list)

        os_command = f"""
                        {basedir}/bin/mysqldump -u {self.username} -p {self.password} -S {self.socket} -P {self.port} --databases={schema_join} {option_join} > {backup_name}
                    """
        return os_command
