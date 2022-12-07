import re
from dataclasses import dataclass, field

SIZE_THRESHOLD = 100000
MAX_SIZE = 70000000
MIN_NEED = 30000000
LS_REGEX_STRING = r"(?:(?:dir)|(?P<size>\d+))\s(?P<name>[\w\.]+)"

@dataclass
class Directory:
    name: str = field(compare=False)
    children: list = field(compare=False)
    parent: any = field(compare=False)
    size: int = field(default=0, compare=True)
    
    def visit_print(self, depth:int=0) -> None:
        indent = " " * depth
        print(f"{indent}{self.name} {self.size}")
        for child in self.children:
            child.visit_print(depth+1)
    
    def propagate_size(self) -> int:
        for child in self.children:
            self.size += child.propagate_size()
        return self.size
    
    def filter_size(self, threshold) -> int:
        filtered = 0
        if self.size < threshold:
            filtered += self.size
        for child in self.children:
            filtered += child.filter_size(threshold)
        return filtered
    
    def flatten(self) -> list:
        flat = []
        if self.children:
            flat.extend(self.children)
            for child in self.children:
                flat.extend(child.flatten())
        return flat

class DirVisitor:
    def __init__(self, root: Directory) -> None:
        self.root: Directory = root
        self.current: Directory = root
        
    def up(self) -> None:
        if not self.current.parent:
            raise RuntimeError(f"No parent found in {self.current.name}")
        self.current = self.current.parent
    
    def enter(self, dir_name: str) -> None:
        if not dir_name in [directory.name for directory in self.current.children]:
            raise RuntimeError(f"No child found with name {dir_name}")
        for directory in self.current.children:
            if directory.name == dir_name:
                self.current = directory


ls_regex = re.compile(LS_REGEX_STRING)

with open("input/day_7", mode="r", encoding="UTF-8") as file:
    lines = [line.rstrip() for line in file.readlines()]

tree = DirVisitor(Directory("/", [], None))

for line in lines[1:]:
    if line.startswith("$ cd"):
        if line.endswith(".."):
            tree.up()
        else:
            tree.enter(line[5:])
    elif line.startswith("$ ls"):
        continue
    else:
        reg_match = ls_regex.match(line)
        if reg_match:
            match_dict = reg_match.groupdict()
            if match_dict["size"]:
                tree.current.size += int(match_dict["size"])
            else:
                tree.current.children.append(Directory(name=match_dict["name"], children=[], parent=tree.current))
        else:
            print(f"Missed {line}")

tree.root.propagate_size()
# tree.root.visit_print()
print(tree.root.filter_size(SIZE_THRESHOLD))

free = MAX_SIZE - tree.root.size
needed = MIN_NEED - free

print(f"{needed = }")

applicable = {d.name:d.size for d in tree.root.flatten() if d.size > needed}

print(applicable)
