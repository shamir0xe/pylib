<h1 align="center" style="display: block; font-size: 2.5em; font-weight: bold; margin-block-start: 1em; margin-block-end: 1em;">
<a name="logo" href="#"><img align="center" src="https://github.com/shamir0xe/pylib/blob/main/assets/logos/pylib.png?raw=true" alt="pylib" style="width:100%;height:100%"/></a>
<br/><br/><strong>pylib</strong>
</h1>

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
![Python](https://img.shields.io/badge/Python-3.12%2B-blue)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://opensource.org/licenses/MIT)

A python library that helps writing py projects much easier and faster.

## Table of contents

This library covers multiple aspects, including:

<!--toc:start-->

- [Table of contents](#table-of-contents)
- [Installation](#installation)
- [Documentation](#documentation)
  - [I. Config](#i-config)
    - [Usage Example](#usage-example)
    - [Default Values](#default-values)
    - [Reading Environment Configurations](#reading-environment-configurations)
  - [II. Database](#ii-database)
    - [Registering a Database Engine](#registering-a-database-engine)
    - [Using Database Sessions](#using-database-sessions)
    - [Using the Repository Facade](#using-the-repository-facade)
  - [III. Rabbit-MQ Messaging](#iii-rabbit-mq-messaging)
    - [Establishing an Async Connection](#establishing-an-async-connection)
    - [Server Side: Listening to a Queue](#server-side-listening-to-a-queue)
    - [Client Side: Sending Messages](#client-side-sending-messages)
  - [IV. Json](#iv-json)
  - [V. Buffer IO](#v-buffer-io)
  - [VI. Data Structures](#vi-data-structures)
  - [VII. File](#vii-file)
  - [VIII. Path](#viii-path)
  - [IX. Argument](#ix-argument)
  - [X. String](#x-string)
  - [XI. Math](#xi-math)

## Installation

You can simply install this library through pip, via following commad:

```shell
python3 -m pip install pylib-0xe
```

## Documentation

### I. Config

The [`Config`](config/config) facade simplifies reading hierarchical JSON config files. Here's how it works:

#### Usage Example
Assume you have several `.json` config files or folders with configurations under the `configs` directory. To access the `humans.male.height` attribute from `mammals.json`, use the following code:

```python
Config.read('mammals.humans.male.height')
```

#### Default Values
You can specify a default value if the attribute is not found:

```python
Config.read(..., default=180)
```

#### Reading Environment Configurations
The `read_env` property looks for an `env.json` file in the project's directory hierarchy. Once found, it searches for the specified pattern. For example, to access `db.postgres.password`, use:

```python
Config.read_env('db.postgres.password')
```

---

### II. Database

The `Database` facade provides convenient methods for interacting with databases using SQLAlchemy. Follow these steps to set it up:

#### Registering a Database Engine
First, register your database engine with the `EngineMediator`:

```python
from pylib_0xe.database.mediators.engine_mediator import EngineMediator
from pylib_0xe.database.engines.postgres_engine import PostgresEngine

# Register the Postgres engine
EngineMediator().register(DatabaseTypes.I, PostgresEngine().engine)
```

This associates `DatabaseTypes.I` with the SQLAlchemy engine.

> **Note:** Ensure your `env.json` contains the `db.postgres` configuration:

```json
{
  "db": {
    "postgres": {
      "host": "127.0.0.1",
      "port": 1234,
      "user": "",
      "password": "",
      "db": "",
      "test_db": ""
    }
  }
}
```

---

#### Using Database Sessions
You can inject database sessions into functions using the `@db_session` decorator:

```python
from typing import Optional
from sqlalchemy import Session
from pylib_0xe.decorators.db_session import db_session
from pylib_0xe.types.database_types import DatabaseTypes

@db_session(DatabaseTypes.I)
def fn(session: Optional[Session] = None):
    session.query(...)
```

---

#### Using the Repository Facade
Alternatively, use the [`Repository`](repositories/repository.py) facade for simplified CRUD operations:

```python
from pylib_0xe.repositories.repository import Repository
from src.models.user import User

# 'User' should be a SQLAlchemy model inheriting from DecoratedBase
# 'DecoratedBase' is located in pylib_0xe.database.decorated_base

user = Repository(User).read_by_id("123456")
```


### III. Rabbit-MQ Messaging

The `Messaging` facade simplifies creating robust RabbitMQ-based messaging projects. It consists of two main components:

1. **Server Side**
2. **Client Side**

> **Note:** Ensure the `message_broker` section is included in your `env.json` file for full functionality:
> ```json
> {
>   "message_broker": {
>     "host": "127.0.0.1:5672",
>     "url": "amqp://127.0.0.1:5672"
>   }
> }
> ```

Both server and client components support asynchronous and blocking connections. Below, we illustrate examples for the **asynchronous** connection.

---

#### Establishing an Async Connection
Use the `inject_async_connection` decorator to create and inject an async RabbitMQ connection:

```python
from pylib_0xe.decorators.inject_async_connection import inject_async_connection
from pylib_0xe.messaging.rpc.rpc_async_connection import RpcAsyncConnection

@inject_async_connection
def main(connection: Optional[RpcAsyncConnection] = None):
    pass
```

This decorator creates an async connection and injects it into the `main` function.

---

#### Server Side: Listening to a Queue
On the server side, create a RabbitMQ queue, listen to it, and invoke a callback function when a job is received:

```python
from pylib_0xe.messaging.rpc.rpc_async_server import RpcAsyncServer
from pylib_0xe.asynchrone.get_or_create_event_loop import GetOrCreateEventLoop

# Define the callback function
def resolver(*args, **kwargs):
    pass

@inject_async_connection
def main(connection: Optional[RpcAsyncConnection]):
    # Create the server instance
    RpcAsyncServer(
        routing_key="some-random-q",
        connection=connection,
        query_handler=resolver,
    )

    # Start the event loop
    GetOrCreateEventLoop().get_or_create().run_forever()
```

This setup ensures that the server listens for messages on the specified `routing_key` and processes them using the `resolver` function.

---

#### Client Side: Sending Messages
On the client side, send a message to a specific queue using the `ClientCaller` class:

```python
from pylib_0xe.messaging.client.client_caller import ClientCaller

async def fn():
    return await ClientCaller(
        client_name="some-random-q",
        rpc_connection=connection,
    ).call(input={"query": "generate", "payload": ...})
```

The `ClientCaller` sends a message to the `some-random-q` queue and waits for a response asynchronously.

### IV. Json

This facade class helps you operate `get` and `set` operations on a json file. Two main functions are:


1)  [`selector_get_value`](json/json_helper.py)
1)  [`selector_set_value`](json/json_helper.py)

It supports selecting by array indexes (__i) and wild-cards (*) for both `set` and `get` methods.
```json
{
  "a": {
    "b": {
      "c": {
        "f": "g"
      }
    },
    "d": [1, 2],
    "e": {},
    "f": [{"g": 123}, {"k": 3}]
  }
}
```

```python
json_file = File.read_json('file.json')
JsonHelper.selector_get_value(json_file, 'a.b.c.f') # g
JsonHelper.selector_get_value(json_file, 'a.d') # [1, 2]
JsonHelper.selector_set_value(json_file, 'a.f.*.r', 5) # "f": [{"g": 123, "r": 5}, {"k": 3, "r": 5}]
JsonHelper.selector_set_value(json_file, 'a.d.__2', 5) # "d": [1, 5],
```
### V. Buffer IO

This module provides several ways to read, write and edit buffers.
You can define `file`, `str` and `standard-input` buffers.

- [Buffer](buffer_io/buffer.py)
- [BufferReader](buffer_io/buffer_reader.py)
- [BufferWriter](buffer_io/buffer_writer.py)
- [StandardInputBuffer](buffer_io/standard_input_buffer.py)
- [StandardOutputBuffer](buffer_io/standard_output_buffer.py)
- [FileBuffer](buffer_io/file_buffer.py)
- [StringBuffer](buffer_io/string_buffer.py)

for example you can simply read a whole file like this:

```python
reader = BufferReader(FileBuffer(file_path, "r+"))
while not reader.end_of_buffer():
    line = reader.next_line()
```

or you can define a string as a buffer and treat it in the same way:

```python
reader = BufferReader(StringBuffer('some awesome text'))
while not reader.end_of_buffer():
    a, b, c = reader.next_int(), reader.next_string(), reader.next_char()
```

you can also read from `standard_input` and write to `standard_output`
in this way:

```python
reader = BufferReader(StandardInputBuffer())
writer = BufferWriter(StandardOutputBuffer())
while not reader.end_of_buffer():
    a, b, c = reader.next_int(), reader.next_string(), reader.next_char()
    writer.write_line(f"We have recieved these: ({a}, {b}, {c})")
```

### VI. Data Structures
### VII. File

- [File](file/file.py): A class that contains some useful
  functions to deal with files. Some of them are:
  - `read_json(file_path)`
  - `read_csv(file_path)`
  - `append_to_file(file_path, string)`
  - `get_all_files(directory_path, extension)`



### VIII. Path

- [PathHelper](path/path_helper.py):
  Provides absolute pathing for the project. Then you can
  use releative pathing after reaching the project root. As an example:

```python
path = PathHelper.from_root(__file__, 'assets', 'imgs', '1.png')
```

It will construct the path from the root of the project to the desired file,
for this specific example, the file should be accessible under this path:
`$project_root/assets/imgs/1.png`.
This function tries to go back from `__file__` directory to reach the `root`
directory. The default root directories are `src` and `root`. You can
specify the root directory name by passing the `root_name=YOUR_ROOT_DIR_NAME`
as a kwarg.
Then the above example could be rewritten as something like this:

```python
path = PathHelper.from_root(..., root_name="custom_name")
```

The best practice to use it with the custom root directory is to write a new PathHelper
class that extends `PathHelper` and apply your custom `root_name` to it. You can
also get rid of `__file__` argument in this way. It should be implemented
something like this:

```python
from pylib_0xe.path.path_helper import PathHelper as PH


class PathHelper(PH):
  @classmethod
  def root(cls, *path: str) -> str:
    return cls.from_root(__file__, *path, root_name="custom_name")
```

### IX. Argument

- [ArgumentParser](argument/argument_parser.py):
  Useful tool to reading arguments passed to a python program executed via command line interface (terminal).
  for example if you run your program as follow:

```terminal
python3 main.py --color green --size 2 --fast --O2
```

you can access the arguments through:

```python
ArgumentParser.get_value('color') -> green
ArgumentParser.get_value('size') -> 2
ArgumentParser.is_option('O2') -> true
```

### X. String

- [StringHelper](string/string_helper.py)
- [HashGenerator](string/hash_generator.py)
- [GenerateId](string/generate_id.py)



### XI. Math

- [Geometry](algorithms/math/geometry.py): A neat implemented 2d-geometry
  library. Some of the usefull functions that it provides are:
  - `translate(expression, *points)`: recieves arithmatic expression and
    the points afterwards. Returns the answer of the expression. example:
    `translate('* + *.', p1, p2, p3, scalar)` = `((p1 * p2) + p3) *. scalar`
  - `side_sign(p1, p2, p3)`: Returns in which side of the p1->p2 line, p3 is located.
  - `inside_polygon(points, p)`
  - `segment_intersection(l1, l2)`