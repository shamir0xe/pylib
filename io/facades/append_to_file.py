from io.buffer_writer import BufferWriter
from io.file_buffer import FileBuffer


class AppendToFile:
    @staticmethod
    def do(file_path: str, string: str) -> None:
        writer = BufferWriter(FileBuffer(file_path))
        writer.write_line(string)
        writer.close()
