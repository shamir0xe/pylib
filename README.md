&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
![Python](https://img.shields.io/badge/Python-3.6%2B-blue)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://opensource.org/licenses/MIT)

A python library that helps writing py projects much easier and faster.


## Table of contents
This library covers multiple aspects, including:

- [Table of contents](#table-of-contents)
- [Documentation](#documentation)
  - [Algorithms](#algorithms)
    - [Graph](#graph)
    - [Math](#math)
    - [Paradigms](#paradigms)
    - [String Processing](#string-processing)
    - [Trees](#trees)
  - [Argument](#argument)
  - [Buffer IO](#buffer-io)
  - [Data](#data)
  - [Debug Tools](#debug-tools)
  - [Facades](#facades)
    - [Config](#config)
    - [File](#file)
    - [Json](#json)
    - [Path](#path)
    - [String](#string)


## Documentation
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
# output:
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

### Facades
#### Config
- [Config](facades/config/config.py)
#### File
- [File](facades/file/file.py)
#### Json
- [JsonHelper](facades/json/json_helper.py)
#### Path
- [PathHelper](facades/path/path_helper.py)
#### String
- [StringHelper](facades/string/string_helper.py)
- [HashGenerator](facades/string/hash_generator.py)

