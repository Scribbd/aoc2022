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

    def __floordiv__(self, other):
        diff = self - other
        return max(abs(diff.x), abs(diff.y))
    
    def __str__(self):
        return f"({self.x},{self.y})"

class TailTable():
    right_tail = Location(1,0)
    left_tail = Location(-1,0)
    up_tail = Location(0,1)
    down_tail = Location(0,-1)
    
    right = frozenset([Location(2, -1), Location(2, 0), Location(2, 1)])
    left = frozenset([Location(-2, -1), Location(-2, 0), Location(-2, 1)])
    up = frozenset([Location(-1, 2), Location(0, 2), Location(1, 2)])
    down = frozenset([Location(-1, -2), Location(0, -2), Location(1, -2)])
    
    simple_dict = {right: left_tail, left: right_tail, up: down_tail, down: up_tail}
    
    edge = [Location(-2 , -2), Location(2, 2), Location(2, -2), Location(-2, 2)]
    edge_dict = {"R": right_tail, "L": left_tail, "U": down_tail, "D": up_tail}

class Body:
    def __init__(self, start: Location) -> None:
        self.head: Location = start
        self.tail: Location = start
        self.tail_history = [start]

    def move(self, direction: str) -> None:
        self.head += direction
        self.drag_tail(direction)
    
    def drag_tail(self, direction) -> None:
        if self.head // self.tail <= 1:
            print(f"No move: HEAD:{self.head} TAIL:{self.tail} DIFF:{self.head - self.tail}")
        else:
            vector = self.head - self.tail
            
            print(f"DO move: HEAD:{self.head} TAIL:{self.tail} DIFF:{self.head - self.tail}")

            if vector in TailTable.edge:
                print("EDGE")
                self.tail = self.head + TailTable.edge_dict[direction]
            # elif vector in TailTable.right:
            #     print("right")
            #     self.tail = self.head + TailTable.left_tail
            # elif vector in TailTable.left:
            #     print("left")
            #     self.tail = self.head + TailTable.right_tail
            # elif vector in TailTable.up:
            #     print("up")
            #     self.tail = self.head + TailTable.down_tail
            # elif vector in TailTable.down:
            #     print("down")
            #     self.tail = self.head + TailTable.up_tail
            else:
                for key, tail_diff in TailTable.simple_dict.items():
                    if vector in key:
                        print(key, tail_diff)
                        self.tail = self.head + tail_diff
            
            print(f"DID move: HEAD:{self.head} TAIL:{self.tail} DIFF:{self.head - self.tail}")
        print()

        self.tail_history.append(self.tail)

def main():
    start = Location(0,0)
    rope = Body(start)

    steps = 0
    for instruction in get_instructions():
        for step in list(instruction):
            rope.move(step)
            steps += 1
    
    print(steps)
    print(len(rope.tail_history))
    print(len(set(rope.tail_history)))

def get_instructions() -> list[Instruction]:
    with open("input/day_9", mode="r", encoding="UTF-8") as file:
        raw = file.readlines()
        lines = [line.rstrip() for line in raw]
    
    instructions = []
    for line in lines:
        comps = line.split(" ")
        instructions.append(Instruction(direction=comps[0],steps=int(comps[1])))

    return instructions

if __name__ == "__main__":
    main()