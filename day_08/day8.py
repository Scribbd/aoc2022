from enum import Enum, auto

class Directions(Enum):
    north = auto()
    east = auto()
    south = auto()
    west = auto()

def main():
    score = 0
    
    with open("input/day_8", mode="r", encoding="UTF-8") as file:
        lines = file.readlines()

    grid:list[list[int]] = []

    # Populate
    for i, line in enumerate(lines):
        grid.append([])
        for tree in line.rstrip():
            grid[i].append(int(tree))

    # Iterate
    for x, _ in enumerate(grid):
        for y, _ in enumerate(grid[x]):
            if x <= 0 or x >= len(grid)-1:
                score += 1
            elif y <= 0 or y >= len(grid[x])-1:
                score += 1
            elif see(grid, x, y):
                score += 1

            # print(f"{x, y, score = }")

    print(score)

def see(grid, x, y) -> bool:
    tree = grid[x][y]
    
    if tree == 0:
        # print(f"0 HIDDEN {x, y = }")
        return False
    
    for d in Directions:
        # print(f"{x, y, d.name = }")
        trees = find(d, x, y, grid)
        for i, other in enumerate(trees):
            # print(f"{x, y, d.name, tree, other, other >= tree = }")
            if other >= tree:
                # print(f"{d.name} HIDDEN")
                break
            if i == len(trees) - 1:
                return True
    
    return False
    
def find(direction, x_target, y_target, grid) -> list[int]:
    x_range = [x_target]
    y_range = [y_target]
    match direction:
        case Directions.north:
            y_range = range(y_target)
        case Directions.east:
            x_range = range(x_target)
        case Directions.south:
            y_range = range(y_target+1, len(grid))
        case Directions.west:
            x_range = range(x_target+1, len(grid[x_target]))
    trees = []
    for x in x_range:
        for y in y_range:
            trees.append(grid[x][y])
    # print(f"{x_target, y_target, direction.name, trees = }")
    return trees

if __name__ == "__main__":
    main()