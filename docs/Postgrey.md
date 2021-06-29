# Postgrey

Main class for database client.

## Parameters

Everything is same with asyncpg Parameters: [Click Here](https://magicstack.github.io/asyncpg/current/api/index.html#asyncpg.connection.connect)

## Attributes

- dns (`str`, `NoneType`): Encoded DNS if given.
- connection_settings (`dict`): Connection settings.
- connection (`asyncpg.connection.Connection`): Current connection object. You can use asyncpg functions from this attribute.

## Functions

### connect

Start the Connection. _This function is coroutine._

#### Returns

- `asyncpg.connection.Connection`: Connection object.

#### Example(s)

```py
connection = postgrey.Postgrey(
    # ...
)

await connection.connect()
# ...
```

<hr>

### execute

Execute a SQL command. _This function is coroutine._

#### Parameters

- query (`str`, `tuple`): SQL command that will be executed.
- `*args`: Parameters if you added.
- timeout (`float`, `int`): Timeout Value.

#### Returns

- `str`: Result.

#### Example(s)

```py
# ...
result = await connection.execute("DROP TABLE users")
# ...
```

<hr>

### fetch

Execute a SQL command and list Records. _This function is coroutine._

#### Parameters

- query (`str`, `tuple`): SQL command that will be executed.
- `*args`: Parameters if you added.
- timeout (`float`, `int`): Timeout Value.

#### Returns

- `list`: List of `asyncpg.Record` object.

#### Example(s)

```py
# ...
records = await connection.fetch("SELECT * FROM users")
# ...
```

<hr>

### create_table

Create a new table. _This function is coroutine._

#### Parameters

- table_name (`str`): Table name.
- columns (`dict`): Column name, type and contraint.

#### Returns

- `str`: Result.

#### Example(s)

```py
# ...
await connection.create_table("users", {
    "id": "serial PRIMARY KEY",
    "name": "text"
})
# ...
```

<hr>

### insert_data

Insert one or many data to table. _This function is coroutine._

#### Parameters

- table_name (`str`): Table name.
- `*args` (`dict`, `tuple`, `list`): One or more data.

#### Returns

- `list`: List of `asyncpg.Record` object.

#### Example(s)

```py
# ...
results = await connection.insert_data("users", {
    "id": 1,
    "name": "dict"
}) # -> [<Record id=1 name='dict'>]
```

```py
# ...
results = await connection.insert_data("users", [2, "list"])
# -> [<Record id=2 name='list'>]
```

```py
# ...
results = await connection.insert_data("users", (3, "tuple", ))
# -> [<Record id=3 name='tuple'>]
```

```py
# ...
results = await connection.insert_data("users",
    [4, "list_2"], (5, "tuple_2", )
) # -> [<Record id=4 name='list_2'>, <Record id=5 name='tuple_2'>]
```

<hr>

### find_data

Find data from table. _This function is coroutine._

#### Parameters

- table_name (`str`): Table name.
- data (`dict`): Data that will be found.
  - **NOTE**: For change operator, use `__key__`.
- limit (`int`): Maximum record limit. _Optional_

#### Returns

- `list`: List of `asyncpg.Record` object.

#### Example(s)

```py
# ...
results = await connection.find_data("users", {
    "id": 1
}) # -> [<Record id=1 name='dict'>]
```

```py
# ...
results = await connection.find_data("users", {
    "id": 1,
    "__id__": ">"
}) # -> [ <Record id=1 name='dict'>, <Record id=2 name='list'>, <Record id=3 name='tuple'>,  ...]
```

```py
# ...
results = await connection.find_data("users", {
    "id": 1,
    "__id__": ">"
}, limit=2) # -> [ <Record id=1 name='dict'>, <Record id=2 name='list'>]
```

<hr>

### update_data

Update data from table. _This function is coroutine._

#### Parameters

- table_name (`str`): Table name.
- data (`dict`): Data that will be found.
  - **NOTE**: For change operator, use `__key__`.
- new\_data (`dict`): New data.

#### Returns

- `list`: List of `asyncpg.Record` object.

#### Example(s)

```py
# ...
results = await connection.update_data("users", {
    "id": 3
}, {
    "name": "new_name"
}) # -> [<Record id=3 name='new_name'>]
```

```py
# ...
results = await connection.update_data("users", {
    "id": 3,
    "__id__": "<"
}, {
    "name": "new_name"
}) # -> [<Record id=1 name='new_name'>, <Record id=2 name='new_name'>]
```

<hr>

### delete_data

Delete data from table. _This function is coroutine._

#### Parameters

- table_name (`str`): Table name.
- data (`dict`): Data that will be found.
  - **NOTE**: For change operator, use `__key__`.

#### Returns

- `list`: List of `asyncpg.Record` object.

#### Example(s)

```py
# ...
results = await connection.delete_data("users", {
    "id": 3
}) # -> [<Record id=3 name='new_name'>]
```

```py
# ...
results = await connection.delete_data("users", {
    "name": "new_name"
}) # -> [<Record id=1 name='new_name'>, <Record id=2 name='new_name'>]
```

<hr>

### find_all_data

Find all data from table. _This function is coroutine._

#### Parameters

- table_name (`str`): Table name.
- limit (`int`): Maximum record limit. _Optional_

#### Returns

- `list`: List of `asyncpg.Record` object.

#### Example(s)

```py
# ...
results = await connection.find_all_data("users") # -> [ <Record id=1 name='dict'>, <Record id=2 name='list'>, <Record id=3 name='tuple'>,  ...]
```

```py
# ...
results = await connection.find_all_data("users", limit=2) # -> [ <Record id=1 name='dict'>, <Record id=2 name='list'>]
```

<hr>

### drop_table

Drop a table. _This function is coroutine._

#### Parameters

- table_name (`str`): Table name.

#### Returns

- `str`: Result.

#### Example(s)

```py
# ...
results = await connection.drop_table("users")
```

<hr>

### disconnect

Close the Connection. _This function is coroutine._

#### Returns

- `None`.

#### Example(s)

```py
# ...
await connection.disconnect()
```
