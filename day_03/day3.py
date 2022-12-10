#!/bin/env python

import string

prio_list = list(string.ascii_letters)
score = 0

with open("input/day_3", mode="r", encoding="UTF-8") as file:
    for line in file.readlines():
        line = line.rstrip()
        first_half = line[0:len(line)//2]
        second_half = line[len(line)//2:]
        
        left_inv = set(first_half)
        right_inv = set(second_half)
        
        shared_item = list(left_inv & right_inv)
        
        score += prio_list.index(shared_item[0]) + 1
        
print(score)