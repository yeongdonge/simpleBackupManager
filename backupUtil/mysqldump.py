class MysqlDump:
    options_list = ['events', 'triggers', 'routines', 'triggers', 'single-transaction', 'all-databases']

    def __init__(self, username, password, port, socket, databases, options):
        self.username = username
        self.password = password
        self.port = port
        self.socket = socket
        self.databases = databases
        self.options = options


    def
