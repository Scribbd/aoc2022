import math
from enum import Enum, auto


class Directions(Enum):
    north = auto()
    east = auto()
    south = auto()
    west = auto()

def main():
    max_score = 0
    
    grid = get_grid()

    # Iterate
    for x, _ in enumerate(grid):
        for y, _ in enumerate(grid[x]):
            scenic_scores = scenic(grid, x, y)
            score = math.prod(scenic_scores)
            if score <= 1:
                continue
            if max_score < score:
                print(f"{x, y, scenic_scores, score = }")
            max_score = max(max_score, score)

    print(max_score)

def get_grid():
    with open("input/day_8", mode="r", encoding="UTF-8") as file:
        lines = file.readlines()

    grid:list[list[int]] = []

    # Populate
    for i, line in enumerate(lines):
        grid.append([])
        for tree in line.rstrip():
            grid[i].append(int(tree))
    return grid

def scenic(grid, x, y) -> list[int]:
    tree = grid[x][y]
    scores = []
    
    if tree == 0:
        return [0]
    
    for d in Directions:
        score = 0
        trees = find(d, x, y, grid)
        for other in trees:
            score += 1
            if other >= tree:
                break
        scores.append(score)
    
    return scores
        

def find(direction, x_target, y_target, grid) -> list[int]:
    x_range = [x_target]
    y_range = [y_target]
    match direction:
        case Directions.north:
            y_range = range(y_target-1, -1, -1)
        case Directions.east:
            x_range = range(x_target-1, -1, -1)
        case Directions.south:
            y_range = range(y_target+1, len(grid))
        case Directions.west:
            x_range = range(x_target+1, len(grid[x_target]))
    trees = []
    for x in x_range:
        for y in y_range:
            trees.append(grid[x][y])
    
    return trees

if __name__ == "__main__":
    main()