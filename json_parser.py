import json
from .buffer_io import BufferReader, StringBuffer

class JsonParser:
    def __init__(self, json_file):
        self.json = json_file
    
    def parse(self, selectors):
        rev_map = {}
        for key, value, in selectors.items():
            rev_map['.' + value] = key
        self.__selectors = rev_map
        self.__out = {}
        self.__traverse('', self.json)
        return self.__out

    def __traverse(self, path, obj):
        # print('{}: {}'.format(path, json.dumps(obj)))
        if path in self.__selectors:
            self.__add_to_output(path, obj)
        if isinstance(obj, list):
            for next_obj in obj:
                self.__traverse(path + '.*', next_obj)
        elif isinstance(obj, dict):
            for attr, next_obj in obj.items():
                self.__traverse(path + '.' + attr, next_obj)
    
    def __add_to_output(self, path, obj):
        key = self.__selectors[path]
        if '*' in path:
            if key in self.__out:
                self.__out[key].append(obj)
            else:
                self.__out[key] = [obj]
        else:
            self.__out[key] = obj
