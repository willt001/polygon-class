from typing import List

class Point:
    "Object to represent a coordinate in 2D space"
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y
    
    def __eq__(self, other: "Point") -> bool:
        return (self.x == other.x) and (self.y == other.y)
    
    def __str__(self) -> str:
        return f'({self.x}, {self.y})'

class Line:
    """Object to represent a line between two points as ax + by = c"""
    def __init__(self, p1: Point, p2: Point, is_infinite: bool = False) -> None:
        if p1 == p2:
            raise AssertionError
        if not is_infinite:
            self.boundaries = (p1, p2)
        else:
            self.boundaries = None
        if p1.x == p2.x:
            self.a = 1
            self.b = 0
            self.c = p1.x
        elif p1.y == p2.y:
            self.a = 0
            self.b = 1
            self.c = p1.y
        else:
            self.a = (p2.y - p1.y) / (p1.x - p2.x)
            self.b = 1
            self.c = self.a * p1.x + self.b * p1.y
    
    def __eq__(self, other: "Line") -> bool:
        return (self.a == other.a) and (self.b == other.b) and (self.c == other.c)
    
    def intersection_point(self, other: "Line", starting_point: Point=None) -> Point:
        if self.a * other.b == self.b * other.a:
            # Lines are parallel
            return None
        y = (other.c * self.a - self.c * other.a) / (self.a * other.b - self.b * other.a)
        try:
            x = (self.c - self.b * y) / self.a
        except:
            x = (other.c - other.b * y) / other.a
        if self.boundaries:
            p1, p2 = self.boundaries
            min_x = min(p1.x, p2.x)
            max_x = max(p1.x, p2.x)
            min_y = min(p1.y, p2.y)
            max_y = max(p1.y, p2.y)
            if x >= min_x and x <= max_x and y >= min_y and y <= max_y:
                on_self = True
            else:
                on_self = False
        else:
            on_self = True
        if other.boundaries:
            p1, p2 = other.boundaries
            min_x = min(p1.x, p2.x)
            max_x = max(p1.x, p2.x)
            min_y = min(p1.y, p2.y)
            max_y = max(p1.y, p2.y)
            if x >= min_x and x <= max_x and y >= min_y and y <= max_y:
                on_other = True
            else:
                on_other = False
        else:
            on_other = True
        if on_self and on_other:
            if not starting_point or x > starting_point.x:
                return Point(x, y)
        return None
    
    def __str__(self) -> str:
        return f'{self.boundaries[0]}, {self.boundaries[1]}'

class Polygon:
    """Object to represent a polygon as an ordered collection of vertices"""
    def __init__(self, vertexes: List[Point]) -> None:
        if vertexes[0] != vertexes[-1]:
            raise AssertionError
        self.vertexes = vertexes
        self.edges = []
        for i in range(len(vertexes) - 1):
            edge = Line(vertexes[i], vertexes[i + 1])
            self.edges.append(edge)

    def __str__(self) -> str:
        min_x = min([point.x for point in self.vertexes])
        max_x = max([point.x for point in self.vertexes])
        min_y = min([point.y for point in self.vertexes])
        max_y = max([point.y for point in self.vertexes])
        grid = [['.'] * (max_x - min_x + 1) for _ in range(max_y - min_y + 1)]
        for point in self.vertexes:
            grid[point.y - min_y][point.x - min_x] = 'X'
        rows = [''.join(row)[::-1] for row in grid]
        return '\n'.join(rows)[::-1]
    
    def contains_point(self, point: Point) -> bool:
        '''Implemented using the raycasting algorithm.'''
        arbitrary_line = Line(point, Point(point.x + 1, point.y + 1), is_infinite=True)
        intersections = set()
        for edge in self.edges:
            intersection = edge.intersection_point(arbitrary_line, starting_point=point)
            if intersection is not None:
                intersections.add((intersection.x, intersection.y))
        if len(intersections) % 2 == 0:
            return False
        return True


if __name__ == "__main__":
    square = Polygon([Point(0, 0), Point(0, 3), Point(3, 3), Point(3, 0), Point(0, 0)])
    print(square)
    print(square.contains_point(Point(0, 0)))
    print(square.contains_point(Point(2, 1)))
    print(square.contains_point(Point(-1, 1)))