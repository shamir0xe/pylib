import json
import re


class JsonHelper:
    @staticmethod
    def merge(js_1, js_2):
        """merging two jsons together, overwriting common fields in js_1 with
        values provided with js_2
        """
        res = {}
        for key, value in js_2.items():
            if key in js_1:
                if isinstance(value, list):
                    if isinstance(js_1[key], list):
                        res[key] = js_1[key] + value
                    else:
                        res[key] = value
                elif isinstance(value, dict):
                    res[key] = JsonHelper.merge(js_1[key], value)
                else:
                    res[key] = value
            else:
                res[key] = value
            if key not in res:
                res[key] = value
        return res

    @staticmethod
    def selector_get_value(js, selector):
        if selector == "":
            return js
        token = selector.split(".")[0]
        array_index = JsonHelper.__selector_array_index(token)
        index = len(token) + 1
        next_selector = selector[index:] if index < len(selector) else ""
        if array_index == -2:
            # merging all of the answers
            res = []
            for element in js:
                res.append(JsonHelper.selector_get_value(element, next_selector))
            return res
        elif array_index >= 0:
            # element of an array
            next_js = js[array_index] if array_index < len(js) else {}
            return JsonHelper.selector_get_value(next_js, next_selector)
        else:
            # element of the object
            next_js = js[token] if token in js else {}
            return JsonHelper.selector_get_value(next_js, next_selector)

    @staticmethod
    def selector_set_value(js, selector, value):
        if selector == "":
            return value

        token = selector.split(".")[0]
        array_index = JsonHelper.__selector_array_index(token)
        index = len(token) + 1
        next_selector = selector[index:] if index < len(selector) else ""
        if array_index == -2:
            # merging all of the answers
            res = []
            for element in js:
                res.append(JsonHelper.selector_set_value(element, next_selector, value))
            js = res
        elif array_index >= 0:
            # element of an array
            next_js = js[array_index] if array_index < len(js) else {}
            js[array_index] = JsonHelper.selector_set_value(
                next_js, next_selector, value
            )
        else:
            # element of the object
            next_js = js[token] if token in js else {}
            js[token] = JsonHelper.selector_set_value(next_js, next_selector, value)
        return js

    @staticmethod
    def apply_stucture(js, structure):
        """applying structure to the fields of the json"""
        res = json.loads(json.dumps(js))
        for selector, value in structure.items():
            js_value = JsonHelper.selector_get_value(res, selector)
            if type(value) != type(js_value):
                if isinstance(value, list):
                    res = JsonHelper.selector_set_value(res, selector, [js_value])
                elif isinstance(value, dict):
                    # TODO
                    pass
        return res

    @staticmethod
    def __selector_array_index(token):
        if token == "*":
            return -2
        z = re.match(r"(__)(\d+)", token)
        if z:
            return int(z.groups()[1])
        return -1


class JsonParser:
    def __init__(self, json_file):
        self.json = json_file

    def parse(self, selectors):
        rev_map = {}
        for (
            key,
            value,
        ) in selectors.items():
            rev_map["." + value] = key
        self.__selectors = rev_map
        self.__out = {}
        self.__traverse("", self.json)
        return self.__out

    def __currected_path(self, path):
        if len(path) < 2:
            return ""
        path = re.sub(r"(\.__\d+)(\.|$)+", ".*.", path)
        path = path[:-1] if path[-1] == "." else path
        return path

    def __check_path(self, path):
        return self.__currected_path(path) in self.__selectors

    def __traverse(self, path, obj):
        if self.__check_path(path):
            self.__add_to_output(path, obj)
        if isinstance(obj, list):
            cur = 0
            for next_obj in obj:
                self.__traverse(path + ".__{}".format(cur), next_obj)
                cur += 1
        elif isinstance(obj, dict):
            for attr, next_obj in obj.items():
                self.__traverse(path + "." + attr, next_obj)

    @staticmethod
    def __is_array(token):
        z = re.match(r"(__)(\d+)", token)
        if z:
            return int(z.groups()[1])
        return -1

    def __add_to_output(self, path, obj):
        tokens = path[1:].split(".")
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
                    if token not in walker:
                        walker[token] = []
                else:
                    if token not in walker:
                        walker[token] = {}
                    if i + 1 >= len(tokens):
                        walker[token] = obj
                    walker = walker[token]
