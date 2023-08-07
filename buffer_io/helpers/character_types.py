from enum import Enum


class CharacterTypes(Enum):
    Alphabet = "alphabet"
    Digit = "digit"
    Parenthesis = "parenthesis"
    Operator = "operator"
    Separator = "separator"
    Unknown = "unknown"
