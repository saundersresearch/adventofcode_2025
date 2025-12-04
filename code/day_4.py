grid_map = {}
with open("inputs/day_4.txt", "r") as f:
    grid = f.readlines()
    grid = [line.strip() for line in grid]
    grid = [list(line) for line in grid]

for i, line in enumerate(grid):
    for j, char in enumerate(line):
        grid_map[i, j] = char

### Part 1
print("\nPart 1")
print("======")

# Loop through each spot and count the number of 'x' neighbors
total_accessible = 0
relative_neighbors = [
    (-1, -1), (0,-1), (1,-1), 
    (-1, 0), (1, 0), 
    (-1, 1), (0, 1), (1, 1)
]
for (i, j), char in grid_map.items():
    num_neighbors = 0
    if char != "@":
        continue

    for relative_i, relative_j in relative_neighbors:
        if ((i + relative_i, j + relative_j) in grid_map.keys() and
            grid_map[i + relative_i, j + relative_j] == '@'):
            num_neighbors += 1

    if num_neighbors < 4:
        total_accessible += 1

print(f'There are {total_accessible} accessible positions.')

### Part 2
print("\nPart 2")
print("======")

# This time, we need to add each accessible index to a list for removal, then try again
accessible_indices = set()
while True:
    rolls_to_remove = set()
    for (i, j), char in grid_map.items():
        num_neighbors = 0
        if char != "@":
            continue

        for relative_i, relative_j in relative_neighbors:
            if ((i + relative_i, j + relative_j) in grid_map.keys() and
                grid_map[i + relative_i, j + relative_j] == '@'):
                num_neighbors += 1
            
        if num_neighbors < 4 and (i, j) not in accessible_indices:
            accessible_indices.add((i,j))
            rolls_to_remove.add((i,j))
        
    for roll in rolls_to_remove:
        grid_map[*roll] = '.'
    
    if len(rolls_to_remove) == 0:
        break

print(f'There are {len(accessible_indices)} accessible positions with removal.')