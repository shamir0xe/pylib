import json
import re
from .buffer_io import BufferReader, StringBuffer
from .utils import debug_text

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

    def __currected_path(self, path):
        if len(path) < 2:
            return ''
        path = re.sub(r'(\.__\d+)(\.|$)+', '.*.', path)
        path = path[:-1] if path[-1] == '.' else path
        return path

    def __check_path(self, path):
        return self.__currected_path(path) in self.__selectors

    def __traverse(self, path, obj):
        if self.__check_path(path):
            self.__add_to_output(path, obj)
        if isinstance(obj, list):
            cur = 0
            for next_obj in obj:
                self.__traverse(path + '.__{}'.format(cur), next_obj)
                cur += 1
        elif isinstance(obj, dict):
            for attr, next_obj in obj.items():
                self.__traverse(path + '.' + attr, next_obj)
    
    @staticmethod
    def __is_array(token):
        z = re.match(r'(__)(\d+)', token)
        if z:
            return int(z.groups()[1])
        return -1

    def __add_to_output(self, path, obj):
        tokens = path[1:].split('.')
        walker = self.__out
        for i in range(len(tokens)):
            token = tokens[i]
            index = self.__is_array(token)
            if index >= 0:
                while len(walker[tokens[i - 1]]) <= index:
                    walker[tokens[i - 1]].append({})
                if i + 1 >= len(tokens):
                    walker[tokens[i - 1]][index] = obj
                walker = walker[tokens[i - 1]][index]
            else:
                if i + 1 < len(tokens) and self.__is_array(tokens[i + 1]) >= 0:
                    if not token in walker:
                        walker[token] = []
                else:
                    if not token in walker:
                        walker[token] = {}
                    if i + 1 >= len(tokens):
                        walker[token] = obj
                    walker = walker[token]
            
    @staticmethod
    def merge(js_1, js_2):
        res = {}
        for key, value in js_2.items():
            if key in js_1:
                if isinstance(value, list):
                    if isinstance(js_1[key], list):
                        res[key] = js_1[key] + value
                    else:
                        res[key] = value
                elif isinstance(value, dict):
                    res[key] = JsonParser.merge(js_1[key], value)
                else:
                    res[key] = value
            else:
                res[key] = value
        for key, value in js_1.items():
            if not key in res:
                res[key] = value
        return res
