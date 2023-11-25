import unittest
import random
from ..data.data_transfer_object import DataTransferObject
from ..string.hash_generator import HashGenerator
from dataclasses import dataclass


@dataclass
class DTO(DataTransferObject):
    p1: int
    p2: str = "Hallo"


@dataclass
class DTO_With_Mapper(DataTransferObject):
    p1: int
    p2: DTO
    p3: str

    def p3_mapper(self, data) -> str:
        return data + "-dto"


class TestDataTransferObject(unittest.TestCase):
    def test_inheritance_variables_assignment(self) -> None:
        p1 = random.randint(0, 12345)
        dto = DTO.from_dict({"p1": p1})
        self.assertEqual(dto.p1, p1)
        self.assertEqual(dto.p2, "Hallo")

    def test_mapper_functioning(self) -> None:
        p1: int = random.randint(0, 12345)
        p2: DTO = DTO.from_dict({"p1": p1})
        p3: str = HashGenerator.generate()
        dto = DTO_With_Mapper.from_dict({"p1": p1, "p2": p2, "p3": p3, "p4": 1.23})

        self.assertEqual(dto.p1, p1)
        self.assertEqual(dto.p2, p2)
        self.assertEqual(dto.p3, p3 + "-dto")


if __name__ == "__main__":
    unittest.main()
