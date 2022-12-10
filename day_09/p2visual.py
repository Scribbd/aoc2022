# list of coordinate pairs
coords = [(1, 2), (3, 4), (5, 6)]


# get the x and y coordinates
x, y = zip(*coords)

# find the range of x and y coordinates
xmin, xmax = min(x), max(x)
ymin, ymax = min(y), max(y)

# create an empty grid with the same size as the x and y ranges
grid = []
for i in range(ymax - ymin + 1):
    grid.append([" "] * (xmax - xmin + 1))

# fill in the grid with the coordinates
for i, coord in enumerate(coords):
    x, y = coord
    grid[y - ymin][x - xmin] = str(i)

# print the grid
for row in reversed(grid):
    print("".join(row))
