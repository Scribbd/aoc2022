#!/bin/env python
elfs_inventory = [0]

def nmax(values: list, n: int) -> list:
    final_list = []
    for _ in range(0, n):
        max_val = max(values)
        final_list.append(max_val)
        values.remove(max_val)
    
    return final_list

with open("./input/day_1", mode="r", encoding="UTF-8") as file:
    i = 0
    for line in file.readlines():
        if line.strip():
            elfs_inventory[i] += int(line.strip())
        else:
            i += 1
            elfs_inventory.append(0)
    
print(f"Elf with most: {max(elfs_inventory)}")

print(f"Top three func: {sum(nmax(elfs_inventory.copy(), 3))}")

elfs_inventory.sort(reverse=True)

print(f"Sort top {elfs_inventory[0]}")
print(f"Sort top 3 {sum(elfs_inventory[:3])}")