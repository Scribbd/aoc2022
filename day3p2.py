#!/bin/env python

import string

prio_list = list(string.ascii_letters)
score = 0

with open("input/day_3", mode="r", encoding="UTF-8") as file:
    lines = file.readlines()

while lines:
    elf = []
    for i in range(3):
        elf.append(set(lines.pop().rstrip()))
    
    shared_item = list(elf[0] & elf[1] & elf[2])
    
    score += prio_list.index(shared_item[0]) + 1
        
print(score)