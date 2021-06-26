from urllib.parse import quote
from asyncpg import connect as pg_connect
from postgrey.utils import raise_error
from typing import Union


class Postgrey:
    def __init__(self, dns: str = None, **kwargs) -> None:
        self.dns = quote(dns) if dns is not None else None
        self.connection_settings = kwargs or {}

    async def connect(self):
        """Start the Connection.

        Parameters:

        Returns:
            asyncpg.connection.Connection: New Connection
        """

        self.connection = await pg_connect(self.dns, **self.connection_settings)
        return self.connection

    async def execute(self, query: Union[str, tuple], *args, timeout: Union[float, int] = None) -> str:
        """Execute SQL.

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
        """Create a New Table.

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

    async def insert_one(self, table_name: str, **kwargs) -> str:
        """Insert new item to the table.

        Parameters:
            table_name (str): Table name.
            **kwargs: key - value

        Returns:
            str: Result.
        """

        raise_error(table_name, "table_name", str)

        formatted = f"""
            INSERT INTO {table_name} VALUES (
                {', '.join(f'${index + 1}' for index, _ in enumerate(kwargs.keys()))}
            )
        """

        return await self.execute(formatted, *kwargs.values())

    async def disconnect(self, timeout: Union[float, int] = None):
        """Close the Connection.

        Parameters:
            timeout (float, int): Timeout Value.

        Returns:
            None
        """

        if timeout is not None:
            raise_error(timeout, "timeout", (int, float))
            timeout = float(timeout)

        await self.connection.close(timeout=timeout)