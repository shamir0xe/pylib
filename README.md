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

- [Table of contents](#table-of-contents)
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


## Documentation
### Buffer IO
This module provides several ways to read, write and edit buffers. You can define `file`, `str` and `standard-input` buffers.
- [Buffer](buffer_io/buffer.py)
- [BufferReader](buffer_io/buffer_reader.py)
- [BufferWriter](buffer_io/buffer_writer.py)
- [StandardInputBuffer](buffer_io/standard_input_buffer.py)
- [FileBuffer](buffer_io/file_buffer.py)
- [StringBuffer](buffer_io/string_buffer.py)

for example you can simply read a whole file like this:

```python
reader = BufferReader(FileBuffer(file_path))
while not reader.end_of_buffer():
    line = reader.next_line()
```

or you can define a string as a buffer and treat it in the same way:
```python
reader = BufferReader(StringBuffer('some awesome text'))
while not reader.end_of_buffer():
    a, b, c = reader.next_int(), reader.next_string(), reader.next_char()
```
### Data
- [DataTransferObject](data/data_transfer_object.py): A tool for converting dictionaries to objects. example: 
 ```python
 obj = DataTransferObject.from_dict({'a': 123})
 print(obj.a)
#  123
 ```
- [VariableTypeModifier](data/variable_type_modifier.py): Converting types by casting it in a better way.

### Debug Tools

- [debug_text](debug_tools/debug_text.py): Alternative way to debuging the code via prints into the stderr. example:
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


- [TerminalProcess](debug_tools/terminal_process.py): A neat progress bar for long tasks.

### Config
- [Config](config/config.py): A facade class to read json config files easily. I'ts so powerful when you provide your configs in the hierarchical pattern.
example usage:
under the `configs` folder, you have several .json config files, or folders containing configs. Let's assume we want to access `humans.male.height` attribute from `mammals.json`. We have two approaches to achieve it:
    1. `Config('mammals').get('humans.male.height)`
    2. `Config.read('mammals.humans.male.height)`

  It could have default value if there is no correspond attribute was found. like we could have written `Config.read(..., default=180)`
### File
- [File](file/file.py): A class that contains some useful functions to deal with files. Some of them are:
  - `read_json(file_path)`
  - `read_csv(file_path)`
  - `append_to_file(file_path, string)`
  - `get_all_files(directory_path, extension)`
### Json
- [JsonHelper](json/json_helper.py): With this class, you can read, write and merge `json` files with dot notations. Selector example (for `file.json`):
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
- [PathHelper](path/path_helper.py): Provides absolute pathing for the project. Then you can use releative pathing after reaching the project root. As an example:
```python
path = PathHelper.from_root('assets', 'imgs', '1.png')
```
  It will construct the path from the root of the project to the desired file, for this specific example, the file should be accessible under this path: `$project_root/assets/imgs/1.png`.
  You can also provide how much this function should go back inorder to reach the root of the project. By default, it's assumed this library is been placed in 2 layers away from the root of the project. Something like `$project_root/libs/pylib`. If you placed it rather than 2 layers away, you can specify the exact amount of layers it sould went back to reach the root as an `backward_times` argument. Then the above example could be rewritten as something like this:
```python
path = PathHelper.from_root(..., backward_times=4)
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
- [Geometry](algorithms/math/geometry.py): A neat implemented 2d-geometry library. Some of the usefull functions that it provides are:
    - `translate(expression, *points)`: recieves arithmatic expression and the points afterwards. Returns the answer of the expression. example:
    `translate('* + *.', p1, p2, p3, scalar)` = `((p1 * p2) + p3) *. scalar`
    - `side_sign(p1, p2, p3)`: Returns in which side of the p1->p2 line, p3 is located.
    - `inside_polygon(points, p)`
    - `segment_intersection(l1, l2)`
#### Paradigms
- [DevideAndConquer](algorithms/paradigms/divide_and_conquer): Implementation of D&D algorithmic paradigm.
#### String Processing
- [LIS](algorithms/string_processing/lis.py): Longest Increasing Subsequence implementation.
#### Trees
- [AvlTree](algorithms/trees/avl_tree)

