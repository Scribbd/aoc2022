import re

STACKS = 9
STACK_DEPTH = 8
STACK_FIRST = 1
STACK_WIDTH = 4

MOVE_START = 10
INSTRUCT_REGEX = r"move (?P<n>.*) from (?P<s>.*) to (?P<d>.*)"

with open("input/day_5", mode="r", encoding="UTF-8") as file:
    lines = file.readlines()

stacks:list[list] = [ [] for _ in range(STACKS) ]

container_lines = lines[:STACK_DEPTH]
container_lines.reverse()

for line in container_lines:
    for i, stack in enumerate(stacks):
        container = line[STACK_FIRST+i*STACK_WIDTH]
        if container.strip():
            stack.append(container)

move_lines = lines[MOVE_START:]
instruct = re.compile(INSTRUCT_REGEX)

for line in move_lines:
    instruct_dict = instruct.match(line).groupdict()
    count = int(instruct_dict["n"])
    source = int(instruct_dict["s"]) - 1
    dest = int(instruct_dict["d"]) - 1
    grabbed = stacks[source][-count:]
    del stacks[source][-count:]
    stacks[dest].extend(grabbed)
    
        
for stack in stacks:
    print(stack[-1], end="")