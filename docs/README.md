# Quick Start

## Installation

Just type `pip install postgrey` and you are ready to go!

## Documentation Links

- [Postgrey](https://github.com/5elenay/postgrey/blob/main/docs/Postgrey.md)
- [Types](https://magicstack.github.io/asyncpg/current/usage.html#type-conversion)

## Example Usage

```py
# Import asyncio for run the async function
import asyncio
# Import postgrey
from postgrey import Postgrey


async def main():
    # Connection config
    connection = Postgrey(
        user="postgres",
        password="secret_password",
        database="testing",
        host="localhost"
    )

    # Start the connection
    await connection.connect()

    # Find all users has name "example" from users table.
    results = await connection.find_data("users", {
        "name": "example"
    })

    # Print all users id to the console that found.
    print([
        i.get("id") for i in results
    ])

    # Close the connection
    await connection.disconnect()

# Run the function.
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```
