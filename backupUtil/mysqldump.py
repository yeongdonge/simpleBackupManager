class MysqlDump:
    options_sample = {'1': 'events', '2': 'routines', '3': 'single-transaction'}

    def __init__(self, username, password, port, socket):
        self.username = username
        self.password = password
        self.port = port
        self.socket = socket

    def schema_backup(self, basedir: str, schema_list: list, option_list: list, backup_name: str):
        option_values = []
        for i in range(len(option_list)):
            option_values.append(self.options_sample[option_list[i]])
        option_prefix = ' --'
        schema_join = ' '.join(schema_list)
        option_join = option_prefix + ' --'.join(option_values)

        os_command = f"""
                        {basedir}/bin/mysqldump -u{self.username} -p{self.password} -S {self.socket} -P {self.port} --databases {schema_join} {option_join} --set-gtid-purged=off > {backup_name} 
                    """
        return os_command

    def table_backup(self, basedir: str, schema: str, table_list: list, backup_name: str):
        table_join = ' '.join(table_list)

        os_command = f"""
                        {basedir}/bin/mysqldump -u{self.username} -p{self.password} -S {self.socket} -P {self.port} {schema} {table_join} --set-gtid-purged=off > {backup_name}"""
        return os_command

