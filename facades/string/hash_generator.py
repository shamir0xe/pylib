import random


class HashGenerator:
    mother_string = "abcdefghijklmnopqrstuvwxyz0123456789"
    mother_size = len(mother_string)

    @staticmethod
    def generate(length=5):
        res = ""
        while length > 0:
            length -= 1
            res += HashGenerator.mother_string[
                random.randint(0, HashGenerator.mother_size - 1)
            ]
        return res
