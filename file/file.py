import json
from ..io.buffer_reader import BufferReader
from ..io.file_buffer import FileBuffer
from ..io.buffer_writer import BufferWriter


class File:
    @staticmethod
    def read_file(path: str) -> str:
        res = ''
        reader = BufferReader(FileBuffer(path))
        while not reader.end_of_buffer():
            res += reader.next_line()
        reader.close()
        return res
    
    @staticmethod
    def write_file(file_path: str, data: str) -> None:
        BufferWriter(FileBuffer(file_path=file_path, mode='w+')) \
            .write(data) \
            .close()

    @staticmethod
    def read_json(path: str) -> dict:
        return json.loads(File.read_file(path=path))
