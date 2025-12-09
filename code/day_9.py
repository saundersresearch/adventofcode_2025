from itertools import pairwise
from tqdm import trange, tqdm

with open("inputs/day_9_practice.txt", "r") as f:
    tiles = [
        tuple(int(x) for x in line.strip().split(","))
        for line in f
    ]

print(tiles)

### Part 1
print("\nPart 1")
print("======")

# Loop over tiles to get max area
largest_area = 0
for i in range(len(tiles)):
    for j in range(i + 1, len(tiles)):
        height = abs(tiles[j][0] - tiles[i][0]) + 1
        width = abs(tiles[j][1] - tiles[i][1]) + 1

        area = height*width
        largest_area = max(largest_area, area)

print(f'Largest area is {largest_area}')

### Part 2
print("\nPart 2")
print("======")

def line_line_col(v1, v2, v3, v4):
    # L1 from v1 to v2, L2 from v3 to v4
    y1, x1 = v1
    y2, x2 = v2
    y3, x3 = v3
    y4, x4 = v4

    # Need to handle collinear separately
    if len(set([x1,x2,x3,x4])) == 1:
        min_v1_y, max_v1_y = min(y1,y2), max(y1, y2)
        min_v2_y, max_v2_y = min(y3,y4), max(y3, y4)
        return any([l in range(min_v2_y, max_v2_y + 1) for l in list(range(min_v1_y, max_v1_y + 1))])
    elif len(set([y1,y2,y3,y4])) == 1:
        min_v1_x, max_v1_x = min(x1,x2), max(x1, x2)
        min_v2_x, max_v2_x = min(x3,x4), max(x3, x4)
        return any([l in range(min_v2_x, max_v2_x + 1) for l in list(range(min_v1_x, max_v1_x + 1))])

    denom = (y4-y3)*(x2-x1) - (x4-x3)*(y2-y1)
    u = (x4-x3)*(y1-y3) - (y4-y3)*(x1-x3)
    t = (x2-x1)*(y1-y3) - (y2-y1)*(x1-x3)

    # Colliding if 0 <= u <= denom and 0 <= t <= denom (if denom >= 0)
    if denom >= 0:
        return 0 <= u <= denom and 0 <= t <= denom
    else:
        return denom <= u <= 0 and denom <= t <= 0
    
def is_inside(v, points):
    # Check if v is inside polygon defined by points using ray casting
    # If arbitrary line to v crosses polygon even # of times: outside
    # If arbitrary line to v crosses polygon odd # of times: inside 

    # If v is any of the points, then it's inside
    if any([v == p for p in points]):
        return True

    line_segments = points.copy()
    line_segments.append(points[0])

    arbitrary_point = (0, v[0])
    num_crossings = 0
    for seg1, seg2 in pairwise(line_segments):
        # Does arbitrary line to v and line seg cross?
        if line_line_col(arbitrary_point, v, seg1, seg2):
            num_crossings += 1

    if num_crossings % 2 == 0:
        return False
    else:
        return True

largest_area = 0
line_segments = tiles.copy()
line_segments.append(tiles[0])
for i in trange(len(tiles)):
    for j in range(i + 1, len(tiles)):
        # Check if each of the 4 corners of the box are inside
        corner1 = tiles[i]
        corner2 = tiles[j]
        corner3 = tiles[i][0], tiles[j][1]
        corner4 = tiles[j][0], tiles[i][1]

        if not (is_inside(corner1, tiles) and is_inside(corner2, tiles)
            and is_inside(corner3, tiles) and is_inside(corner4, tiles)):
            continue
    
        height = abs(tiles[j][0] - tiles[i][0]) + 1
        width = abs(tiles[j][1] - tiles[i][1]) + 1

        area = height*width
        largest_area = max(largest_area, area)

print(f'Largest area within tiles is {largest_area}')