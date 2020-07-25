import time
from typing import Any, ItemsView, List, Optional

from koia.connector import Database
from koia.QueryBuilder import QueryBuilder


class FetchBuilder(QueryBuilder):
    def __init__(self, database: Database):
        super().__init__(database=database)

    def __order_of_commands(self) -> list:
        """Order of attributes"""
        return [
            "innerJoin",
            "where",
            "orWhere",
            "whereIn",
            "whereNotNull",
            "orderBy",
            "take",
        ]

    def _formalize_sql(self) -> str:
        """Formalize sql query by set attributes from query_conf"""
        sql_query: str = ""
        order_of_commands: list = self.__order_of_commands()
        query_operations: list = []
        query_items: str
        element: str
        key: int
        elem: str

        for query_items in order_of_commands:
            if query_items == "innerJoin":
                query_operations += [
                    element for element in self.query_conf[query_items]
                ]

            else:
                if "where" in query_items:  # Handle where case
                    if len(self.query_conf[query_items]) > 0:
                        query_operations += [
                            element.replace("WHERE", "AND")
                            if len(
                                [elem for elem in query_operations if "WHERE" in elem]
                            )
                            > 0
                            or key > 0
                            else element
                            for key, element in enumerate(self.query_conf[query_items])
                        ]

                if "order" in query_items:
                    if len(self.query_conf[query_items]) > 0:
                        query_operations += [
                            element.replace("ORDER BY", ",")
                            if len(
                                [
                                    elem
                                    for elem in query_operations
                                    if "ORDER BY" in elem
                                ]
                            )
                            > 0
                            or key > 0
                            else element
                            for key, element in enumerate(self.query_conf[query_items])
                        ]

                if "take" in query_items:
                    if len(self.query_conf[query_items]) > 0:
                        query_operations += [
                            element for element in self.query_conf[query_items]
                        ]
                    if len(self.query_conf[query_items]) > 1:
                        raise Exception("You can only once set LIMIT attribute")

        query_operation: str
        for query_operation in query_operations:
            sql_query += f" {query_operation}"

        return sql_query

    def _fetch(self, sql_query) -> Optional[list]:
        """Execute sql query

        Output: List[Any] or None
        Return None if sql query is INSERT OR UPDATE"""
        while True:
            try:
                self.database.cursor.execute(sql_query)
                self.database.connection.commit()
                data = self.database.cursor.fetchall()
                return data
            except Exception as e:
                if str(e) == "2013: Lost connection to MySQL server during query":
                    self.__await_db(error=str(e))
                    self.database.reconnect()
                else:
                    raise Exception(e)

    def __await_db(self, error: str):
        """Sleep for a 3 second"""
        print(error)
        print("Try to reconnect after 3 sec. Zzzz...")
        time.sleep(3)

    def get(self) -> Optional[List[Any]]:
        """Imitize sql SELECT feature"""
        sql_query: str = f"SELECT * FROM {self.query_conf['table']} {self._formalize_sql()}"
        data: Optional[List[Any]] = self._fetch(sql_query=sql_query)
        self.__reload_query_conf()

        return data

    def insert(self, values: dict) -> None:
        """Imitize sql INSERT feature"""
        values_items: ItemsView = values.items()
        sql_columns: str = ",".join(f"`{column[0]}`" for column in values_items)
        sql_values: str = ",".join(str(value[1]) for value in values_items)

        sql_query: str = f"INSERT INTO {self.query_conf['table']} ({sql_columns}) VALUES ({sql_values})"
        self._fetch(sql_query=sql_query)
        self.__reload_query_conf()

    def update(self, values: dict) -> None:
        """Imitize sql UPDATE feature"""
        sql_query: str = self._formalize_sql()
        update_sql_query: str = f"UPDATE {self.query_conf['table']} SET"

        for key, value_item in enumerate(values.items()):
            if key == len(values) - 1:
                update_sql_query += (
                    f""" {value_item[0]}='{value_item[1].replace("'", " ")}'"""
                )
            else:
                update_sql_query += (
                    f""" {value_item[0]}='{value_item[1].replace("'", " ")}',"""
                )
        sql_query = update_sql_query + sql_query

        self._fetch(sql_query=sql_query)
        self.__reload_query_conf()
