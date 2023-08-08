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
- [Geometry](algorithms/graph/tsp.py): A neat implemented 2d-geometry library. Some of the usefull functions that it provides are:
    - `translate(expression, *points)`: recieves arithmatic expression and the points afterwards. Returns the answer of the expression. example:
    `translate('* + *.', p1, p2, p3, scalar)` = `((p1 * p2) + p3) *. scalar`
    - `side_sign(p1, p2, p3)`: Returns in which side of the p1->p2 line, p3 is located.
    - `inside_polygon(points, p)`
    - `segment_intersection(l1, l2)`
#### Paradigms
- [DevideAndConquer](algorithms/graph/tsp.py): Implementation of D&D algorithmic paradigm.
#### String Processing
- [LIS](algorithms/graph/tsp.py): Longest Increasing Subsequence implementation.
#### Trees
- [AvlTree](algorithms/graph/tsp.py)

### Argument
- [ArgumentParser](algorithms/graph/tsp.py):
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
- [Buffer](algorithms/graph/tsp.py)
- [BufferReader](algorithms/graph/tsp.py)
- [BufferWriter](algorithms/graph/tsp.py)
- [StandardInputBuffer](algorithms/graph/tsp.py)
- [FileBuffer](algorithms/graph/tsp.py)
- [StringBuffer](algorithms/graph/tsp.py)

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
- [DataTransferObject](algorithms/graph/tsp.py)
- [VariableTypeModifier](algorithms/graph/tsp.py)

### Debug Tools
- [debug_text](algorithms/graph/tsp.py)
- [TerminalProcess](algorithms/graph/tsp.py)

### Facades
#### Config
- [Config](algorithms/graph/tsp.py)
#### File
- [File](algorithms/graph/tsp.py)
#### Json
- [JsonHelper](algorithms/graph/tsp.py)
#### Path
- [PathHelper](algorithms/graph/tsp.py)
#### String
- [StringHelper](algorithms/graph/tsp.py)
- [HashGenerator](algorithms/graph/tsp.py)

