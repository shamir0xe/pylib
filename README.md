
<h1 align="center" style="display: block; font-size: 2.5em; font-weight: bold; margin-block-start: 1em; margin-block-end: 1em;">
<a name="logo" href="#"><img align="center" src="https://github.com/shamir0xe/pylib/blob/main/assets/logos/pylib.png?raw=true" alt="pylib" style="width:100%;height:100%"/></a>
<br/><br/><strong>pylib</strong>
</h1>

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
![Python](https://img.shields.io/badge/Python-3.6%2B-blue)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://opensource.org/licenses/MIT)

A python library that helps writing py projects much easier and faster.

## Table of contents

This library covers multiple aspects, including:
<!--toc:start-->
- [Table of contents](#table-of-contents)
- [Installation](#installation)
- [Documentation](#documentation)
  - [Buffer IO](#buffer-io)
  - [Data](#data)
  - [Debug Tools](#debug-tools)
  - [Config](#config)
  - [File](#file)
  - [Json](#json)
  - [Path](#path)
  - [Argument](#argument)
  - [String](#string)
  - [Algorithms](#algorithms)
    - [Graph](#graph)
    - [Math](#math)
    - [Paradigms](#paradigms)
    - [String Processing](#string-processing)
    - [Trees](#trees)
<!--toc:end-->

## Installation

  You can simply install this library through pip, via following commad:

  ```shell
python3 -m pip install pylib-0xe
  ```

## Documentation

### Buffer IO

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

### Data

- [DataTransferObject](data/data_transfer_object.py):
A tool for converting dictionaries to objects. example:

 ```python
 obj = DataTransferObject.from_dict({'a': 123})
 print(obj.a)
#  123
 ```

DataTransferObject is a dataclass itself. The best practice to use
this dto class is inheritting it as the base
class for your model. For example If your new model is named Bob and
has two parameters `name` and `height` with types `str` and `Optional[int]`
respectively, it should be implemented like this:

```python
@dataclass
class Bob(DataTransferObject):
  name: str
  height: int | None = 185
```

and then you can instantiate it in this way:

```python
  bob_marley = Bob({name: "Bob Marley"})
```

and you can use `bob_marley.name` and `bob_marley.height` in your code
since now on.
Another cool feature of this dto is implementing `mapper` function for
any variable of your choice. It works this way that you can define a
mapper function with this style: `VARIABLENAME_mapper`. It recieves
it's argument from the dictionary you provided to instantiate it and convert
the input to whatever you implement it in the function. This could be
useful if the types of the input data differs from the expected type
provided in the class or if you want to change the value of the variable
in some way before creating it. For example if you want `Bob` to convert it's
name to upper_case letters, it could be implemented like this:

```python
@dataclass
class Bob(DataTransferObject):
  name: str
  height: int | None = 185

  def name_mapper(name: str) -> str:
    return name.lower()

```

- [VariableTypeModifier](data/variable_type_modifier.py):
Converting types by casting it in a better way.

### Debug Tools

- [debug_text](debug_tools/debug_text.py): Alternative way to debuging
the code via prints into the stderr. example:

```python
debug_text('%B%USome Object%E [%c#%%E] -> %r%%E', 12, {"a": 34})
```

<pre>[<u style="text-decoration-style:single"><b>Some Object</b></u> [<font color="#34E2E2">#12</font>] -&gt; <font color="#EF2929">{&apos;a&apos;: 34}</font>]</pre>

- list of options:
  1. %c: cyan color
  1. %r: red color
  1. %b: blue color
  1. %g: green color
  1. %y: yellow color
  1. %H: alternative color
  1. %B: bold text
  1. %U: underlined text
  1. %E: clear modifiers

- [TerminalProcess](debug_tools/terminal_process.py):
A neat progress bar for long tasks.

### Config

- [Config](config/config.py): A facade class to read
json config files easily. I'ts so powerful when you
provide your configs in the hierarchical pattern.
example usage:
under the `configs` folder, you have several .json config files,
or folders containing configs. Let's assume we want to access
`humans.male.height` attribute from `mammals.json`.
We have two approaches to achieve it:
    1. `Config('mammals').get('humans.male.height)`
    2. `Config.read('mammals.humans.male.height)`

  It could have default value if there is no correspond
  attribute was found. like we could have written
  `Config.read(..., default=180)`

### File

- [File](file/file.py): A class that contains some useful
functions to deal with files. Some of them are:
  - `read_json(file_path)`
  - `read_csv(file_path)`
  - `append_to_file(file_path, string)`
  - `get_all_files(directory_path, extension)`

### Json

- [JsonHelper](json/json_helper.py): With this class, you can read,
write and merge `json` files with dot notations.
Selector example (for `file.json`):

```json
{
    "a": {
        "b": {
            "c": {
                "f": "g"
            }
        },
        "d": [1, 2],
        "e": {}
    }
}
```

```python
json_file = File.read_json('file.json')
JsonHelper.selector_get_value(json_file, 'a.b.c.f') # g
JsonHelper.selector_get_value(json_file, 'a.d') # [1, 2]
```

### Path

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

### Argument

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

### String

- [StringHelper](string/string_helper.py)
- [HashGenerator](string/hash_generator.py)

### Algorithms

#### Graph

- [flows](algorithms/graph/flows): provides algorithms in max-flow problem, including:
  - [MaxFlow](algorithms/graph/flows/maxflow.py)
- [MST](algorithms/graph/mst.py)
- [TSP](algorithms/graph/tsp.py)

#### Math

- [Geometry](algorithms/math/geometry.py): A neat implemented 2d-geometry
library. Some of the usefull functions that it provides are:
  - `translate(expression, *points)`: recieves arithmatic expression and
  the points afterwards. Returns the answer of the expression. example:
    `translate('* + *.', p1, p2, p3, scalar)` = `((p1 * p2) + p3) *. scalar`
  - `side_sign(p1, p2, p3)`: Returns in which side of the p1->p2 line, p3 is located.
  - `inside_polygon(points, p)`
  - `segment_intersection(l1, l2)`

#### Paradigms

- [DevideAndConquer](algorithms/paradigms/divide_and_conquer):
Implementation of D&D algorithmic paradigm.

#### String Processing

- [LIS](algorithms/string_processing/lis.py): Longest Increasing Subsequence implementation.

#### Trees

- [AvlTree](algorithms/trees/avl_tree)
