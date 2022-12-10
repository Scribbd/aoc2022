score = 0

with open("input/day_4", mode="r", encoding="UTF-8") as file:
    for line in file.readlines():
        assignments = line.rstrip().split(",")
        sets: set = []
        for assignment in assignments:
            start, end = assignment.split("-")
            sets.append(set(range(int(start), int(end)+1)))
        
        if sets[0].issubset(sets[1]) or sets[1].issubset(sets[0]):
            score += 1


print(score)