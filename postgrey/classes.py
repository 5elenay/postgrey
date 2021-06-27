import enum
from urllib.parse import quote
from asyncpg import connect as pg_connect
from asyncpg import Record
from postgrey.utils import raise_error
from typing import Union


class Postgrey:
    def __init__(self, dns: str = None, **kwargs) -> None:
        self.dns = quote(dns) if dns is not None else None
        self.connection_settings = kwargs or {}

    async def connect(self):
        """Start the connection.

        Parameters:

        Returns:
            asyncpg.connection.Connection: New Connection
        """

        self.connection = await pg_connect(self.dns, **self.connection_settings)
        return self.connection

    async def execute(self, query: Union[str, tuple], *args, timeout: Union[float, int] = None) -> str:
        """Execute SQL command.

        Parameters:
            query (str, tuple): SQL.
            *args: Parameters if you added.
            timeout (float, int): Timeout Value.

        Returns:
            str: Result.
        """

        raise_error(query, "query", (str, tuple))

        if timeout is not None:
            raise_error(timeout, "timeout", (int, float))
            timeout = float(timeout)

        if isinstance(query, tuple):
            query = " ".join(str(i) for i in query)

        return await self.connection.execute(query, *args, timeout=timeout)

    async def create_table(self, table_name: str, **kwargs) -> str:
        """Create a new table.

        Parameters:
            table_name (str): Table name.
            **kwargs: column name - type and contraint.
                Example:
                    id = "serial PRIMARY KEY", name = "text"

        Returns:
            str: Result.
        """

        raise_error(table_name, "table_name", str)

        formatted = [f"{key} {value}" for key,
                     value in kwargs.items()]

        formatted = f"""
            CREATE TABLE {table_name} (
                {', '.join(formatted)}
            )
        """

        return await self.execute(formatted)

    async def insert(self, table_name: str, *args) -> str:
        """Insert one/many item to the table.

        Parameters:
            table_name (str): Table name.
            *args: key - value dict

        Returns:
            str: Result.
        """

        raise_error(table_name, "table_name", str)

        keys, count, formatted = [], 1, ""

        for arg in args:
            raise_error(arg, "arg", dict)
            keys.extend(list(arg.values()))

            formatted += "("
            for _ in arg.values():
                formatted += f"${count},"
                count += 1

            formatted = f"{formatted[:-1]}),"

        formatted = formatted[:-1]

        formatted = f"""
            INSERT INTO {table_name}
            VALUES
                {formatted}
        """

        return await self.execute(formatted, *keys)

    async def find(self, table_name: str, **kwargs) -> list:
        """Find records from table.

        Parameters:
            table_name (str): Table name.
            **kwargs: keys and operators.
                Example:
                    id=5 (Will find records that has id 5.)
                    id=5, __id__=">" (Will find records that has id bigger that 5)

        Returns:
            list: One or more result.
        """

        raise_error(table_name, "table_name", str)

        keys, values, count = [], [], 1

        for key in kwargs.keys():
            if not key.startswith("__") and not key.endswith("__"):
                keys.append(
                    f"{key} {kwargs.get(f'__{key}__') or '='} ${count}")
                values.append(kwargs.get(key))
                count += 1

        formatted = f"""
        SELECT * FROM {table_name}
            WHERE {' AND '.join(keys)}
        """

        return await self.connection.fetch(formatted, *values)

    async def drop_table(self, table_name: str) -> str:
        """Drop a table.

        Parameters:
            table_name (str): Table name.

        Returns:
            str: Result.
        """

        raise_error(table_name, "table_name", str)
        return await self.execute(f"DROP TABLE {table_name}")

    async def disconnect(self, timeout: Union[float, int] = None):
        """Close the connection.

        Parameters:
            timeout (float, int): Timeout Value.

        Returns:
            None
        """

        if timeout is not None:
            raise_error(timeout, "timeout", (int, float))
            timeout = float(timeout)

        await self.connection.close(timeout=timeout)
