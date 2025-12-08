from collections import deque
import heapq

with open("inputs/day_8.txt", "r") as f:
    lines = [
        [int(x) for x in line.strip().split(",")]
        for line in f
    ]

n_connections = 1000
n_largest_sizes = 3

### Part 1
print("\nPart 1")
print("======")

# Get n shortest connections using a heap
heap = []
for i in range(len(lines)):
    for j in range(i+1, len(lines)):
        pos1 = lines[i]
        pos2 = lines[j]
        distance_sq = (pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2 + (pos1[2] - pos2[2])**2
        heapq.heappush(heap, (distance_sq, (i, j)))

# Fill adjacency matrix by connecting the shortest connections
adj_matrix = [[0]*len(lines) for _ in range(len(lines))]
for n in range(n_connections):
    distance_sq, (i, j) = heapq.heappop(heap)
    adj_matrix[i][j] = 1
    adj_matrix[j][i] = 1

# Count number of connected components
visited = [False]*len(adj_matrix)
num_components = 0
component_sizes = []

for i in range(len(adj_matrix)):
    if visited[i]:
        continue

    to_visit = deque([i])
    component_size = 0

    while len(to_visit) > 0:
        vertex = to_visit.pop()
        if not visited[vertex]:
            component_size += 1
            visited[vertex] = True
            neighbors = [i for i, adj in enumerate(adj_matrix[vertex]) if adj == 1]
            for neighbor in neighbors:
                to_visit.appendleft(neighbor)

    num_components += 1
    component_sizes.append(component_size)

# Now get n largest component sizes
total = 1
for i in range(n_largest_sizes):
    next_largest_size = max(component_sizes)
    next_largest_idx = component_sizes.index(next_largest_size)
    
    total *= next_largest_size
    component_sizes[next_largest_idx] = 0

print(f'Multiplying the top {n_largest_sizes} circuit sizes gives {total} ')

### Part 2
print("\nPart 2")
print("======")

# Loop over all shortest connections using a heap
heap = []
for i in range(len(lines)):
    for j in range(i+1, len(lines)):
        pos1 = lines[i]
        pos2 = lines[j]
        distance_sq = (pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2 + (pos1[2] - pos2[2])**2
        heapq.heappush(heap, (distance_sq, (i, j), (pos1, pos2)))

# Fill adjacency matrix by connecting the shortest connections
adj_matrix = [[0]*len(lines) for _ in range(len(lines))]
degrees = [0]*len(lines)
max_heap = len(heap)
while len(heap) > 0:
    distance_sq, (i, j), (pos1, pos2) = heapq.heappop(heap)
    degrees[i] += 1
    degrees[j] += 1
    adj_matrix[i][j] = 1
    adj_matrix[j][i] = 1

    # Don't even bother checking if there are unconnected nodes
    if not all(d >= 1 for d in degrees):
        continue

    # Is number of connected components 1?
    visited = [False]*len(adj_matrix)
    num_components = 0

    for i in range(len(adj_matrix)):
        if visited[i]:
            continue

        to_visit = deque([i])

        while len(to_visit) > 0:
            vertex = to_visit.pop()
            if not visited[vertex]:
                visited[vertex] = True
                neighbors = [i for i, adj in enumerate(adj_matrix[vertex]) if adj == 1]
                for neighbor in neighbors:
                    to_visit.appendleft(neighbor)

        num_components += 1
    
    if num_components == 1:
        print(f'Connecting {pos1} and {pos2} resulted in 1 circuit: {pos1[0]*pos2[0]}')
        break