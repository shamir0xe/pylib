import json
import os
from ..buffer_io.buffer_reader import BufferReader
from ..buffer_io.file_buffer import FileBuffer
from ..buffer_io.buffer_writer import BufferWriter
from ..buffer_io.string_buffer import StringBuffer


class File:
    @staticmethod
    def read_file(path: str) -> str:
        res = ""
        reader = BufferReader(FileBuffer(path))
        while not reader.end_of_buffer():
            res += reader.next_line()
        reader.close()
        return res

    @staticmethod
    def write_file(file_path: str, data: str) -> None:
        BufferWriter(FileBuffer(file_path=file_path, mode="w+")).write(data).close()

    @staticmethod
    def is_file(directory):
        return os.path.isfile(directory)

    @staticmethod
    def read_json(path: str) -> dict:
        return json.loads(File.read_file(path=path))

    @staticmethod
    def read_csv(directory, delimiter=","):
        reader = BufferReader(FileBuffer(directory))
        first = True
        res, keys = [], []
        while not reader.end_of_buffer():
            line = reader.next_line()
            line = line.replace(",", ", ")
            line_reader = BufferReader(
                StringBuffer(line), delimiters=delimiter, exclude_delimiters=" \n\r"
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

    @staticmethod
    def append_to_file(file_path: str, string: str) -> None:
        writer = BufferWriter(FileBuffer(file_path))
        writer.write_line(string)
        writer.close()

    @staticmethod
    def get_all_files(directory=".", ext=None):
        """return all files of the directory with .{ext}"""
        _, _, filenames = next(os.walk(directory))
        if ext is not None:
            filenames = [name for name in filenames if "{}".format(ext) in name]
        return filenames
