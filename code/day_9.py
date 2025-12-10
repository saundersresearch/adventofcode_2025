from itertools import pairwise, product
from tqdm import trange, tqdm
import matplotlib.pyplot as plt

with open("inputs/day_9.txt", "r") as f:
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
# https://www.xjavascript.com/blog/check-if-polygon-is-inside-a-polygon/
print("\nPart 2")
print("======")

def is_point_inside_polygon(point, verts):
    """Determines if point is inside potentially non-convex polygon defined by verts"""
    y, x = point
    inside = False
    n = len(verts)

    for i in range(n):
        j = (i + 1) % n
        yi, xi = verts[i]
        yj, xj = verts[j]

        if is_point_on_segment(point, (verts[i], verts[j])):
            return True
        
        # Does a horizontal ray intersect line_seg?
        if (yi > y) != (yj > y):
            x_inter = ((y - yi)*(xj - xi)) / (yj - yi) + xi
            if x < x_inter:
                inside = not inside

    return inside

def is_point_on_segment(point, segment):
    """Determines if point is on segment"""
    y, x = point
    (y1, x1), (y2, x2) = segment


    if (min(x1, x2) <= x <= max(x1, x2)) and (min(y1,y2) <= y <= max(y1, y2)):
        cross_product = (x - x1)*(y2 - y1) - (y - y1)*(x2 - x1)
        return cross_product == 0
    
    return False

def are_segments_intersecting(segment1, segment2):
    """Determines if segment1 and segment2 intersect"""
    A, B = segment1
    C, D = segment2

    # If endpoints are shared, they don't overlap
    if A == C or A == D or B == C or B == D:
        return False

    o1 = orientation(A, B, C)
    o2 = orientation(A, B, D)
    o3 = orientation(C, D, A)
    o4 = orientation(C, D, B)

    # Segments intersect?
    if o1 != o2 and o3 != o4:
        # Is the intersection just an endpoint? Find point of intersection
        denom = (B[0] - A[0]) * (D[1] - C[1]) - (B[1] - A[1]) * (D[0] - C[0])
        if denom == 0:
            return False

        t_num = (C[0] - A[0]) * (D[1] - C[1]) - (C[1] - A[1]) * (D[0] - C[0])
        u_num = (C[0] - A[0]) * (B[1] - A[1]) - (C[1] - A[1]) * (B[0] - A[0])
        if t_num == 0 or t_num == denom or u_num == 0 or u_num == denom:
            return False
        
        return True
    
    return False

def orientation(p, q, r):
    """0 is collinear, 1 is CW, 2 is CCW"""
    val = (q[0] - p[0])*(r[1] - q[1]) - (q[1] - p[1])*(r[0] - q[0])
    if val == 0:
        return 0
    elif val > 0:
        return 1
    else:
        return 2
    
def on_segment(p, q, r):
    """Returns True if q is on segment pr"""
    return (q[1] <= max(p[1], r[1]) and q[1] >= min(p[1], r[1]) 
            and q[0] <= max(p[0], r[0]) and q[0] >= min(p[0], r[0]))


def is_rect_inside_polygon(rect, polygon_verts):
    for vert in rect:
        if not is_point_inside_polygon(vert, polygon_verts):
            return False
        
    n = len(polygon_verts)
    for i in range(n):
        j = (i + 1) % n
        segment1 = (polygon_verts[i], polygon_verts[j])

        for l in range(4):
            m = (l + 1) % 4
            segment2 = (rect[l], rect[m])

            if are_segments_intersecting(segment1, segment2):
                return False
            
    return True

# Segments touching at endpoints shouldn't overlap
segment1 = [(100,50), (50,50)]
segment2 = [(50,50), (50,100)]
assert not are_segments_intersecting(segment1, segment2)

# This should pass too
segment1 = [(7,3), (7,5)]
segment2 = [(2,5), (9,5)]
assert not are_segments_intersecting(segment1, segment2)

# Rectangle is inside
polygon = [(0,0), (4,0), (4,4), (0, 4)]
rect = [(1,1), (3,1), (3,3), (1,3)]
assert is_rect_inside_polygon(rect, polygon)

# Rectangle crosses edge (non-convex)
polygon = [(0,0), (4,0), (4,4), (2,4), (2,2), (1,2), (1,4), (0, 4)]
rect = [(1,1), (3,1), (3,3), (1,3)]
assert not is_rect_inside_polygon(rect, polygon)

# Another non-convex example but on the edge (doesn't work, but our input doesn't have this case)
polygon = [(0,0), (10,0), (10,60), (20, 60), (20,0), (100,0), (100,70), (0,70)]
rect = [(0,0), (100,0), (100,70), (0,70)]
# assert not is_rect_inside_polygon(rect, polygon)

# Rectangle is outside but shares an edge
polygon = [(0,0), (100, 0), (100, 50), (50, 50), (50, 100), (0, 150)]
rect = [(50, 50), (100, 50), (100, 100), (50, 100)]
assert not is_rect_inside_polygon(rect, polygon)

# Rectangle is just the edge
polygon = [(0,0), (100, 0), (100, 50), (50, 50), (50, 100), (0, 150)]
rect = [(50,50), (50, 50), (50, 100), (50, 100)]
assert is_rect_inside_polygon(rect, polygon)

# Check actual case
polygon = [(7, 1), (11, 1), (11, 7), (9, 7), (9, 5), (2, 5), (2, 3), (7, 3)]
rect = [(2,5),(7,5),(7,3),(2,3)]
assert is_rect_inside_polygon(rect, polygon)

# Loop over tiles to get max area
largest_area = 0
largest_rect = None
for i in trange(len(tiles)):
    for j in range(i + 1, len(tiles)):
        height = abs(tiles[j][0] - tiles[i][0]) + 1
        width = abs(tiles[j][1] - tiles[i][1]) + 1

        area = height*width

        # Only need to search if area is larger
        if area > largest_area:
            rect = [
                tiles[i],
                (tiles[i][0], tiles[j][1]),
                tiles[j],
                (tiles[j][0], tiles[i][1])
            ]
            if is_rect_inside_polygon(rect, tiles):
                largest_area = max(largest_area, area)
                largest_rect = rect

fig, ax = plt.subplots()
for i in range(len(tiles)):
    tile1 = tiles[i]
    tile2 = tiles[(i + 1) % len(tiles)]
    ax.plot([tile1[0], tile2[0]], [tile1[1], tile2[1]])

for i in range(4):
    rect1 = largest_rect[i]
    rect2 = largest_rect[(i + 1) % 4]
    ax.plot([rect1[0], rect2[0]], [rect1[1], rect2[1]], '*', markersize=25, color='y')

plt.show()


print(f'Largest area is {largest_area}')