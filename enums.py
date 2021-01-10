import enum

class Errors(enum.Enum):
    MissingParameters = 'MissingParameters'
    FileNotFound = 'FileNotFound'
    NotFound = '{}NotFound'
    BadParser = 'BadParser'
    PageNotFound = 'PageNotFound'
