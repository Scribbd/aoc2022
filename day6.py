MARKER_LENGTH = 14


with open("input/day_6", mode="r", encoding="UTF-8") as file:
    line = file.readline()

for i in range(MARKER_LENGTH-1, len(line)):
    chunk = set(line[i-MARKER_LENGTH:i])
    if len(chunk) == MARKER_LENGTH:
        print(i)
        break