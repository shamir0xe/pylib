import os
import threading
from functools import wraps
import math
import random
from datetime import (datetime, timedelta)
import time
from .buffer_io import (FileReader, FileWriter, BufferReader, StringBuffer)


def delay(delay=0.):
    """
    Decorator delaying the execution of a function for a while.
    """
    def wrap(f):
        @wraps(f)
        def delayed(*args, **kwargs):
            timer = threading.Timer(delay, f, args=args, kwargs=kwargs)
            timer.start()

        return delayed

    return wrap

def binary_search(bounds, condition, callable_obj, dest):
     start, end = bounds
     # debug_text('dest is: %', dest)
     # debug_text('type dest is: %', type(dest))
     # debug_text('arguments: %', callable_obj.get_arguments())
     while not condition((start, end)):
         mid = (end + start) / 2
         pivot, order = callable_obj.call(mid)
         # debug_text('calling for [%]s --> [%]', mid, pivot)
         if pivot * order < dest * order:
             start = mid
         else:
             end = mid
     return start

def debug_text(*texts):
    """"
    the function for printing text
    just use % for extra arguments inside the string
    """
    debug = True
    if debug:
        arr = []
        sz = len(texts)
        i = 0
        while i < sz:
            if type(texts[i]) is str:
                res = ''
                count = 0
                args = []
                for char in texts[i]:
                    if char == '%':
                        res += '{}'
                        count += 1
                    else:
                        res += char
                if count > 0:
                    while count > 0:
                        i += 1
                        args.append(texts[i])
                        count -= 1
                    res = res.format(*args)
                arr.append(res)
            else:
                arr.append(texts[i])
            i += 1
        sz = len(arr)
        res = ''
        for i in range(sz):
            if i > 0:
                res += ', '
            res += '[{}]'
        print(res.format(*arr), end='\r\n', flush=True)


def check_server_response(server, response, message):
    if not server.check_success_response(response):
        raise Exception(message)


class RandomIndexGenerator:
    """
    generating random index derived from weihgt"""
    def __init__(self, weights):
        weights = [math.fabs(x) for x in weights]
        s = sum(weights)
        self.cummulative_sum = []
        self.n = len(weights)

        cur = 0
        for weight in weights:
            cur += weight
            self.cummulative_sum.append(cur / s)

    def get_index(self):
        rnd = random.random()
        for i in range(self.n):
            if self.cummulative_sum[i] >= rnd:
                return i
        return -1


class TimeManager:
    @staticmethod
    def get_date(days_offset=0):
        desire_date = datetime.now() + timedelta(days=days_offset)
        # return str(desire_date.strftime("%Y-%m-%d %H:%M:%S"))
        return str(desire_date.strftime("%Y-%m-%d"))

    @staticmethod
    def get_date_time(days_offset=0):
        now = datetime.now()
        return now + timedelta(days=days_offset) - timedelta(
            hours=now.hour,
            minutes=now.minute,
            seconds=now.second,
            microseconds=now.microsecond)

    @staticmethod
    def get_hours_timestamp():
        return str(datetime.now().strftime("%H-%M-%S"))

    @staticmethod
    def get_time(string_time):
        return datetime.strptime(string_time, "%Y-%m-%d")

    @staticmethod
    def get_time_diff(t_1, t_2, input_format="seconds"):
        diff = t_1 - t_2
        seconds = diff.total_seconds()
        if input_format == "seconds":
            return seconds
        if input_format == "days":
            return round(seconds / 60 / 60 / 24)
        return False

    @staticmethod
    def get_string_time_diff(str_t_1, str_t_2):
        return TimeManager.get_time_diff(TimeManager.get_time(str_t_1),
                                         TimeManager.get_time(str_t_2))


class HashGenerator:
    mother_string = "abcdefghijklmnopqrstuvwxyz0123456789"
    mother_size = len(mother_string)

    @staticmethod
    def generate(length=5):
        res = ""
        while length > 0:
            length -= 1
            res += HashGenerator.mother_string[random.randint(
                0, HashGenerator.mother_size - 1)]
        return res


class Timer:
    def __init__(self, name="timer"):
        self.start = time.time()
        self.name = name

    def start_task(self):
        self.start = time.time()

    def get_elapsed_time(self):
        """
        returns elapsed time in milliseconds
        """
        return (time.time() - self.start) * 1000

    def time_stamp(self):
        debug_text("{}: {:.02f}ms elapsed".format(self.name,
                                                  self.get_elapsed_time()))


class TerminalProcess:
    def __init__(self, 
        total_loops, 
        prefix = '', 
        suffix = '', 
        decimals = 1, 
        length = 100, 
        fill = '█', 
        print_end = "\r"
    ):
        """
        Call in a loop to create terminal progress bar
        @params:
            iteration   - Required  : current iteration (Int)
            total       - Required  : total iterations (Int)
            prefix      - Optional  : prefix string (Str)
            suffix      - Optional  : suffix string (Str)
            decimals    - Optional  : positive number of decimals in percent complete (Int)
            length      - Optional  : character length of bar (Int)
            fill        - Optional  : bar fill character (Str)
            printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
        """
        self.total = total_loops
        self.iteration = 0
        self.prefix = prefix
        self.suffix = suffix
        self.decimals = decimals
        self.length = length
        self.fill = fill
        self.print_end = print_end

    def hit(self):
        """
        hit the progress iteration, and update it
        """
        self.iteration += 1
        percent = ("{0:." + str(self.decimals) + "f}").format(100 * (self.iteration / float(self.total)))
        filledLength = int(self.length * self.iteration // self.total)
        bar = self.fill * filledLength + '-' * (self.length - filledLength)
        print(f'\r{self.prefix} |{bar}| {percent}% {self.suffix}', end = self.print_end)
        # Print New Line on Complete
        if self.iteration == self.total: 
            print()

    def clear(self):
        self.iteration = 0


class ArrayTools:
    @staticmethod
    def range(begin, end, step=1):
        res = []
        index = 0
        while True:
            res.append(begin + step * index)
            index += 1
            if begin + step * index >= end:
                break
        return res

class FileHandler:
    @staticmethod
    def get_filenames(path=".", file_type=""):
        if not os.path.isdir(path):
            raise Exception('{} is not a directory'.format(path))
        type_len = len(file_type)
        files = [
            f for f in os.listdir(os.path.abspath(path))
            if type_len == 0 or f[-type_len:] == file_type
        ]
        return files

    @staticmethod
    def get_file_number(path=".", file_type="", delimiters="[]()-"):
        files = FileHandler.get_filenames(path=path, file_type=file_type)
        res = -1
        for f in files:
            buffer_reader = BufferReader(StringBuffer(f),
                                            delimiters=delimiters)
            number = None
            while not buffer_reader.end_of_buffer():
                ss = buffer_reader.read()
                try:
                    number = int(ss)
                    break
                except ValueError:
                    pass
            if not number is None:
                res = max(res, number)
        res += 1
        # debug_text('big_boy number is: [%]', res)
        return res


class Callable:
    input_index = HashGenerator.generate()
    def __init__(self, func, *args):
        self.func = func
        self.__args = args

    def call(self, *args):
        new_args = []
        index = 0
        for argument in self.__args:
            if argument is Callable.input_index:
                new_args.append(args[index])
                index += 1
            else:
                new_args.append(argument)
        # debug_text('going to call f width %', new_args)
        return self.func(*new_args)

    def get_arguments(self):
        return self.__args


class Logger:
    def __init__(self, task_name, time_threshold=-1):
        """
        time_threshold should be given in seconds
        """
        self.__task_name = task_name
        self.__timer = Timer("logger")
        self.__stream_timer = Timer("stream")
        self.__whole_timer = None
        self.__map = {}
        self.__time_threshold = time_threshold

    def __check_active(self):
        if self.__whole_timer is None:
            self.__whole_timer = Timer("task")

    def get_total_time(self):
        self.__check_active()
        return self.__whole_timer.get_elapsed_time()

    def start_timer(self):
        self.__check_active()
        self.__timer.start_task()

    def get_timestamp(self):
        self.__check_active()
        return self.__timer.get_elapsed_time()

    def add_log(self, key, *values, timestamp=False, stream=False):
        self.__check_active()
        if stream and not self.__need_log():
            return None
        if not key in self.__map:
            self.__map[key] = []
        values = [
            value.call() if isinstance(value, Callable) else value
            for value in values
        ]
        tup = (*values, )
        if timestamp:
            tup = (round(self.get_timestamp()) / 1000., *values)
        debug_text('[{:>22}]: [{}]'.format(key, tup))
        self.__map[key].append(tup)
        return tup

    def __need_log(self):
        """
        when streaming the logs, check if you need more log to meet the threshold or not
        """
        flag = self.__stream_timer.get_elapsed_time(
        ) > self.__time_threshold * 1000
        if flag:
            self.__stream_timer.start_task()
        return flag

    def write_to_file(self, file_name):
        self.__check_active()
        file_writer = FileWriter(file_name)
        file_writer.write_line('[{:>22}] task logs'.format(self.__task_name))
        file_writer.write_line('[{:>22}]: {:02f}s'.format(
            'total time taken',
            self.get_total_time() / 1000))
        for key in self.__map:
            file_writer.write('[{:>22}]: ['.format(key))
            values = self.__map[key]
            first = True
            for tup in values:
                if first:
                    first = False
                else:
                    file_writer.write(', ')
                file_writer.write('{}'.format(tup))
            file_writer.write_line(']')
        file_writer.close()
