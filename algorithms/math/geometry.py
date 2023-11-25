from __future__ import annotations
import math
import random
from ...buffer_io.string_buffer import StringBuffer
from ...buffer_io.buffer_reader import BufferReader


class Geometry:
    """
    a library for 2D geometry problems
    """

    EPS = 1e-9

    @staticmethod
    def translate(expression, *points):
        """
        . dot
        * cross
        *. scalar product
        + sum
        - subtract
        """
        operators = [".", "*", "*.", "+", "-"]

        def parse_point(p):
            if isinstance(p, str):
                index = "".join("".join(p.split("[")).split("]"))
                index = int(index)
                return points[index]
            return p

        string_buffer = BufferReader(StringBuffer(expression))
        stack = []
        while not string_buffer.end_of_buffer():
            token = string_buffer.next_string()
            stack.append(token)
            if token in operators:
                stack.pop()
                if token == ".":
                    b = parse_point(stack.pop())
                    a = parse_point(stack.pop())
                    stack.append(Geometry.dot(a, b))
                elif token == "*":
                    b = parse_point(stack.pop())
                    a = parse_point(stack.pop())
                    stack.append(None)  # cross not implemented
                elif token == "*.":
                    b = float(parse_point(stack.pop()))
                    a = parse_point(stack.pop())
                    stack.append(Geometry.Point.times(a, b))
                elif token == "+":
                    b = parse_point(stack.pop())
                    a = parse_point(stack.pop())
                    stack.append(Geometry.Point.add(a, b))
                elif token == "-":
                    b = parse_point(stack.pop())
                    a = parse_point(stack.pop())
                    stack.append(Geometry.Point.sub(a, b))

        return stack.pop()

    @staticmethod
    def side_sign(p1, p2, p3):
        """
        returns: 1 left, 0 on, -1 right
        """
        sign = (p1.x - p3.x) * (p2.y - p3.y) - (p1.y - p3.y) * (p2.x - p3.x)
        if math.fabs(sign) < Geometry.EPS:
            return 0
        if sign > 0:
            return +1
        return -1

    @staticmethod
    def dot(p1, p2):
        return p1.x * p2.x + p1.y * p2.y

    @staticmethod
    def inside_polygon(points, p):
        """
        returns:
                1 - inside
                2 - on the border
                3 - outside
        of the polygon.
        points are ordered clockwise or counter-clockwise

        """
        sz = len(points)
        for x in range(sz):
            y = (x + 1) % sz
            if Geometry.in_between(points[x], p, points[y]):
                return 2

        ray = Geometry.Line(
            p,
            Geometry.Point(
                random.randint(123456, 789123), random.randint(123456, 789123)
            ),
        )
        counter = 0
        for x in range(sz):
            y = (x + 1) % sz
            intersection = Geometry.segment_intersection(
                ray, Geometry.Line(points[x], points[y])
            )
            if intersection is None:
                continue
            counter += 1

        if counter % 2 is 0:
            return 3
        return 1

    @staticmethod
    def in_between(p1, intersection, p2):
        """
        check wether intersection is in the middle of p1-p2 segment or not
        """
        return (
            math.fabs(
                Geometry.dist(p1, intersection)
                + Geometry.dist(intersection, p2)
                - Geometry.dist(p1, p2)
            )
            < Geometry.EPS
        )

    @staticmethod
    def dist(p1, p2):
        return Geometry.translate("[0] [1] -", p1, p2).length()

    @staticmethod
    def segment_intersection(l1, l2):
        """
        returns the intersection of the 2 segments, l1 and l2
        """
        intersection = Geometry.intersection(l1, l2)
        if intersection is None:
            return None

        if Geometry.in_between(l1.p1, intersection, l1.p2) and Geometry.in_between(
            l2.p1, intersection, l2.p2
        ):
            return intersection
        return None

    @staticmethod
    def intersection(l1, l2):
        p1 = l1.p1
        p2 = l1.p2
        p3 = l2.p1
        p4 = l2.p2

        d = (p4.y - p3.y) * (p2.x - p1.x) - (p4.x - p3.x) * (p2.y - p1.y)
        if d < Geometry.EPS:
            return None

        ua = (p4.x - p3.x) * (p1.y - p3.y) - (p4.y - p3.y) * (p1.x - p3.x)
        ua /= d

        point = Geometry.Point.add(
            p1, Geometry.Point.times(Geometry.Point.sub(p2, p1), ua)
        )
        return point

    class Point:
        def __init__(self, x, y):
            self.x = x
            self.y = y

        def __str__(self):
            return "({:.02f}, {:.02f})".format(self.x, self.y)

        def length(self):
            return math.sqrt(self.x * self.x + self.y * self.y)

        def normalize(self):
            length = self.length()
            if length < Geometry.EPS:
                return -1
            self.x /= length
            self.y /= length
            return 0

        def __lt__(self, other):
            if math.fabs(self.x - other.x) < Geometry.EPS:
                return self.y + Geometry.EPS < other.y
            return self.x + Geometry.EPS < other.x

        def __eq__(self, other):
            return (
                math.fabs(self.x - other.x) < Geometry.EPS
                and math.fabs(self.y - other.y) < Geometry.EPS
            )

        def sin(self) -> float:
            return self.y / self.length()

        def cos(self) -> float:
            return self.x / self.length()

        def subtract(self, p) -> Geometry.Point:
            return Geometry.Point.sub(self, p)

        def addition(self, p) -> Geometry.Point:
            return Geometry.Point.add(self, p)

        def cross(self, p) -> float:
            return p.y * self.x - p.x * self.y

        @staticmethod
        def sub(p1, p2):
            return Geometry.Point(p1.x - p2.x, p1.y - p2.y)

        @staticmethod
        def add(p1, p2):
            return Geometry.Point(p1.x + p2.x, p1.y + p2.y)

        @staticmethod
        def times(p1, sc):
            return Geometry.Point(p1.x * sc, p1.y * sc)

        @staticmethod
        def is_lower(p1, p2):
            if p1.x - p2.x < Geometry.EPS:
                if p1.y - p2.y < Geometry.EPS:
                    return 0
                return p1.y < p2.y
            return p1.x < p2.y

        @staticmethod
        def is_equal(p1, p2):
            return (
                math.fabs(p1.x - p2.x) < Geometry.EPS
                and math.fabs(p1.y - p2.y) < Geometry.EPS
            )

    class Line:
        def __init__(self, p1, p2):
            self.p1 = p1
            self.p2 = p2

        def __str__(self) -> str:
            return "{} -> {}".format(self.p1, self.p2)
