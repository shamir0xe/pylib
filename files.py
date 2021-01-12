from os import walk
from PythonLibrary.buffer_io import FileReader
import json

class File:
    def __init__(self):
        pass

    @staticmethod
    def get_all_files(directory='.', ext=None, suffix=None):
        """return all files of the directory with .{ext}
        """
        _, _, filenames = next(walk(directory))
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

    def get_all_folders(self):
        pass

