import os
from .io import FileReader, BufferReader, StringBuffer
import json

class File:
    def __init__(self):
        pass

    @staticmethod
    def get_all_files(directory='.', ext=None, suffix=None):
        """return all files of the directory with .{ext}
        """
        _, _, filenames = next(os.walk(directory))
        if ext is not None:
            filenames = [name for name in filenames if '{}'.format(ext) in name]
        if suffix is not None:
            filenames = [name for name in filenames if '{}.'.format(suffix) in name]
        return filenames
    
    @staticmethod
    def read_json(directory):
        reader = FileReader(directory)
        string = ''
        while not reader.end_of_file():
            string += reader.next_line()
        return json.loads(string)

    @staticmethod
    def is_file(directory):
        return os.path.isfile(directory)

    def get_all_folders(self):
        pass

    @staticmethod
    def read_csv(directory, delimiter=','):
        reader = FileReader(directory)
        first = True
        res, keys = [], []
        while not reader.end_of_file():
            line = reader.next_line()
            line = line.replace(',', ', ')
            line_reader = BufferReader(
                StringBuffer(line), 
                delimiters=delimiter, 
                exclude_delimiters=' \n\r'
            )
            items = []
            while not line_reader.end_of_buffer():
                items.append(line_reader.next_string().strip())
            if first:
                first = False
                keys = items
            else:
                items.extend([None] * (len(keys) - len(items)))
                row_items = {}
                for i in range(len(keys)):
                    row_items[keys[i]] = items[i]
                res.append(row_items)
        return res


        

