from functools import cache

with open("inputs/day_7.txt", "r") as f:
    lines = f.readlines()
    lines = [list(line.strip()) for line in lines]

manifold = {}

for row, line in enumerate(lines):
    for col, char in enumerate(line):
        manifold[row, col] = char
        if char == "S":
            start_pos = (row, col)

### Part 1
print("\nPart 1")
print("=======")

num_rows = len(lines)
num_cols = len(lines[0])

# Make a set with the ends of paths, add one every time it splits
path_ends = set()
path_ends.add(start_pos)

split_indices = set()
while len(path_ends) > 0:
    path_end = path_ends.pop()

    # Is there a next path?
    if 0 <= path_end[0] < num_rows - 1:
        next_char = manifold[path_end[0] + 1, path_end[1]]

        # If next_char is ^, split and add both to stack
        if next_char == "^":
            # Do any of the paths need combined?
            if (path_end[0] + 1, path_end[1] + 1) not in path_ends:
                path_ends.add((path_end[0] + 1, path_end[1] + 1))
            if (path_end[0] + 1, path_end[1] - 1) not in path_ends:
                path_ends.add((path_end[0] + 1, path_end[1] - 1))

            split_indices.add((path_end[0] + 1, path_end[1]))
        # Otherwise, push back onto stack as is
        else:
            path_ends.add((path_end[0] + 1, path_end[1]))

total_splits = len(split_indices)
print(f'There are {total_splits} beam splits')

### Part 2
print("\nPart 2")
print("=======")

# Here, use a DFS with memoization to count all potential paths
@cache
def count_paths(s):
    # Are we at the end?
    if s[0] >= num_rows:
        return 1
    else:
        # Run for each child of s
        if manifold[s] == "^":
            # Split and produce two children
            child1 = s[0] + 1, s[1] + 1
            child2 = s[0] + 1, s[1] - 1
            return count_paths(child1) + count_paths(child2)
        else: 
            # Child is directly below
            child = s[0] + 1, s[1]
            return count_paths(child)


total_paths = count_paths(start_pos)
print(f'There are {total_paths} potential paths')