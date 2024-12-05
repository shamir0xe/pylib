from typing import List


class FenwickTree:
    n: int
    data: List[int]

    def __init__(self, n: int) -> None:
        self.n = n
        self.data = [0 for _ in range(n)]

    def add(self, idx: int, x: int) -> None:
        assert 0 <= idx < self.n
        idx += 1
        while idx <= self.n:
            self.data[idx - 1] += x
            idx += idx & -idx

    def sum(self, left: int, right: int) -> int:
        assert 0 <= left <= right <= self.n
        return self.get(right) - self.get(left)

    def get(self, idx: int) -> int:
        res = 0
        while idx > 0:
            res += self.data[idx - 1]
            idx -= idx & -idx
        return res
