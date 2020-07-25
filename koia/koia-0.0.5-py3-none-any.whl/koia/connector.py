import mysql.connector


class Database:
    """
    Create MySQLdbConnectoion instance with cursor
    """

    def __init__(self, config: dict = None, autocommit: bool = False) -> None:
        """Initialize connection and cursor"""
        self.config = config
        self.automcommit = autocommit
        self.connection = self._connect(autocommit=self.automcommit)
        self.cursor = self._cursor()

    def _connect(self, autocommit: bool):
        """Connect to db"""
        _connection = mysql.connector.connect(**self.config)
        _connection.autocommit = autocommit
        return _connection

    def _cursor(self):
        """Create cursor"""
        _cursor = self.connection.cursor(buffered=True)
        return _cursor

    def reconnect(self):
        """Re initialize instance"""
        self.connection.close()
        self.cursor.close()
        self.__init__(config=self.config, autocommit=self.automcommit)

    def close(self):
        """Close instance session"""
        self.connection.close()
        self.cursor.close()
