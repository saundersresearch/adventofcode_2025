from collections import deque

with open('inputs/day_5.txt') as f:
    blocks = f.read().strip().split("\n\n")

fresh_ranges = blocks[0].splitlines()
available_ingredients = blocks[1].splitlines()

fresh_ranges = [list(map(int, r.split("-"))) for r in fresh_ranges]
available_ingredients = list(map(int, available_ingredients))

print(fresh_ranges)
print(available_ingredients)

### Part 1
print("\nPart 1")
print("======")

# Loop through ranges and check if ingredient ID is within range
num_fresh = 0
for ingredient in available_ingredients:
    for low, high in fresh_ranges:
        if ingredient >= low and ingredient <= high:
            num_fresh += 1
            break
    
print(f'There are {num_fresh} fresh ingredients available.')

### Part 2
print("\nPart 2")
print("======")

# Sort ranges by first item
sorted_ranges = sorted(fresh_ranges, key=lambda r: r[0])
sorted_ranges = deque(sorted_ranges)
exclusive_ranges = deque([])

# Pop off top two ranges
while len(sorted_ranges) > 1:
    first = sorted_ranges.popleft()
    second = sorted_ranges.popleft()

    # Do they overlap? If so, fix and append to sorted_ranges
    if second[0] <= first[1]:
        sorted_ranges.appendleft([min(first[0], second[0]), max(first[1], second[1])])
    else:
        # If they don't overlap, then the first will be mutually exclusive
        exclusive_ranges.append(first)
        sorted_ranges.appendleft(second)

exclusive_ranges.append(sorted_ranges.pop())

# Count how many are in each range
total_fresh = 0
for fresh_range in exclusive_ranges:
    total_fresh += fresh_range[1] - fresh_range[0] + 1

print(f'There are {total_fresh} total fresh ingredients.')