from __future__ import annotations

from dataclasses import dataclass
from copy import copy

@dataclass
class Instruction:
    direction:str
    steps:int
    
    def __iter__(self):
        return copy(self)
    
    def __len__(self):
        return self.steps
    
    def __next__(self):
        if self.steps < 1:
            raise StopIteration
        self.steps -= 1
        return self.direction

@dataclass(frozen=True)
class Location:
    x: int
    y: int
    
    def __sub__(self, other):
        return Location(self.x - other.x, self.y - other.y)
    
    def __iadd__(self, other):
        return self.__add__(other)
    
    def __add__(self, other):
        if type(other) != str:
            return Location(self.x + other.x, self.y + other.y)    
        match other:
            case "R":
                return Location(self.x+1, self.y)
            case "L":
                return Location(self.x-1, self.y)
            case "U":
                return Location(self.x, self.y+1)
            case "D":
                return Location(self.x, self.y-1)
            
    def to_tuple(self) -> tuple[int,int]:
        return tuple([self.x, self.y])

    def __floordiv__(self, other):
        diff = self - other
        return max(abs(diff.x), abs(diff.y))
    
    def __str__(self):
        return f"({self.x},{self.y})"
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __iter__(self):
        yield self.x
        yield self.y

class MoveTable:
    right_tail = Location(1,0)
    left_tail = Location(-1,0)
    up_tail = Location(0,1)
    down_tail = Location(0,-1)
    
    right = frozenset([Location(2, -1), Location(2, 0), Location(2, 1)])
    left = frozenset([Location(-2, -1), Location(-2, 0), Location(-2, 1)])
    up = frozenset([Location(-1, 2), Location(0, 2), Location(1, 2)])
    down = frozenset([Location(-1, -2), Location(0, -2), Location(1, -2)])
    
    simple_dict = {right: left_tail, left: right_tail, up: down_tail, down: up_tail}
    
    edge_dict = {Location(-2 , -2): Location(1,1), Location(2, 2): Location(-1, -1), Location(2, -2): Location(-1,1), Location(-2, 2): Location(1,-1)}

class Body:
    def __init__(self, start: Location, size: int) -> None:
        self.body: list[Location] = []
        for _ in range(size):
            self.body.append(start)
        self.tail_history = [start]

    def move_head(self, direction: str) -> None:
        self.body[0] += direction
        self.drag_body()
        graph(self.body)
    
    def drag_body(self) -> None:
        for part in range(1, len(self.body)):
            diff = self.body[part-1] // self.body[part] 
            if diff <= 1:
                continue
                # print(f"{part} NO Move")
            elif diff >= 3:
                print(part, self.body)
                # print(f"ALLERT")
                exit()
            else:
                self.drag_part(part)
                # graph(self.body)
                # print()

        self.tail_history.append(self.body[-1])

    def drag_part(self, part:int):
        vector = self.body[part-1] - self.body[part]
        print(f"{part} DO move: {part-1}:{self.body[part-1]} {part}:{self.body[part]} VEC:{vector}")
        if vector in MoveTable.edge_dict.keys():
            # print("EDGE")
            self.body[part] = self.body[part-1] + MoveTable.edge_dict[vector]
        else:
            for key, tail_diff in MoveTable.simple_dict.items():
                if vector in key:
                    self.body[part] = self.body[part-1] + tail_diff
                    break
        print(f"{part} DID move: {part-1}:{self.body[part-1]} {part}:{self.body[part]} VEC:{self.body[part-1] - self.body[part]}")


def main():
    start = Location(0,0)
    rope = Body(start, 10)

    steps = 0
    for instruction in get_instructions():
        print(instruction)
        for step in list(instruction):
            rope.move_head(step)
            steps += 1
            print()
    
    print()
    
    print(steps)
    print(len(rope.tail_history))
    print(len(set(rope.tail_history)))
    graph(set(rope.tail_history))

def get_instructions() -> list[Instruction]:
    with open("input/day_9", mode="r", encoding="UTF-8") as file:
        raw = file.readlines()
        lines = [line.rstrip() for line in raw]
    
    instructions = []
    for line in lines:
        comps = line.split(" ")
        instructions.append(Instruction(direction=comps[0],steps=int(comps[1])))

    return instructions

def graph(coords):
    # get the x and y coordinates
    x, y = zip(*coords)
    labels = [str(i) for i in range(len(coords)-1,0,-1)] + ["H"]

    # find the range of x and y coordinates
    xmin, xmax = min(x), max(x)
    ymin, ymax = min(y), max(y)
    # xmin, xmax = 0, 6
    # ymin, ymax = 0, 6

    # create an empty grid with the same size as the x and y ranges
    grid = []
    for i in range(ymax - ymin + 1):
        grid.append(["."] * (xmax - xmin + 1))

    # fill in the grid with the coordinates
    for i, coord in enumerate(reversed(list(coords))):
        x, y = coord
        grid[y - ymin][x - xmin] = labels[i][0]

    # print the grid
    for row in reversed(grid):
        print("".join(row))

if __name__ == "__main__":
    main()
    

