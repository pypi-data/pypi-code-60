import logging

import pyodbc

from .abstract import Abstract_DB
from soft_collect.config import settings

logger = logging.getLogger(__name__)


class SQLServer(Abstract_DB):
    def select(self, sql):
        c = self.set_up_connection()
        c.execute(sql)
        row = c.fetchone()
        while row:
            yield row
            row = c.fetchone()

    def fetch_all(self, sql):
        c = self.set_up_connection()

        return c.execute(sql).fetchall()

    def set_up_connection(self):
        s = settings
        logger.info(f"Creating connection to SQL Server in {s.ip}")

        driver = "ODBC Driver 17 for SQL Server"
        pyodbc_drivers = [dri for dri in pyodbc.drivers() if "SQL Server" in dri]
        if pyodbc_drivers:
            driver = pyodbc_drivers[0]

        connection = pyodbc.connect(
            "Trusted_Connection=yes",
            driver="{" + driver + "}",
            server=s.ip,
            database=s.base,
        )
        return connection.cursor()
