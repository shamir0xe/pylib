import random


class HashGenerator:
    mother_string = "abcdefghijklmnopqrstuvwxyz0123456789"
    mother_size = len(mother_string)

    @staticmethod
    def generate(length: int = 5, upper_case_probability: float = 0.5):
        res = ""
        while length > 0:
            length -= 1
            char = HashGenerator.mother_string[
                random.randint(0, HashGenerator.mother_size - 1)
            ]
            if random.random() < upper_case_probability:
                char = char.upper()
            res += char
        return res
