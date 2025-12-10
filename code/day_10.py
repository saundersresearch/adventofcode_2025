import heapq
import math

with open("inputs/day_10.txt") as f:
    lines = f.readlines()

### Part 1
print("\nPart 1")
print("======")

min_button_pushes = 0
for line in lines:
    line = line.strip().split(" ")

    # Get goal in binary
    goal_list = line[0][1:-1]
    goal_list = list(map(lambda x: '1' if x == '#' else '0', goal_list))[::-1]
    goal = int(''.join(goal_list), 2)

    # Get move_masks in binary so neighbors are just v ^ mask
    n_lights = len(goal_list)
    moves = line[1:-1]
    moves = [
        move[1:-1].split(',') 
        for move in moves
    ]
    move_masks = []
    for move in moves:
        move = [int(m) for m in move]
        mask = 0
        for m in move:
            mask |= (1 << m)
        move_masks.append(mask)

    # Use Djikstra's algorithm to find shortest path from 0 to goal
    def get_neighbors(v, move_masks):
        return [v ^ move for move in move_masks]

    source = 0
    dist = [math.inf]*2**n_lights
    prev = [None]*2**n_lights

    heap = []
    dist[source] = 0
    heapq.heappush(heap, (dist[source], source))

    while len(heap) > 0:
        _, u = heapq.heappop(heap)
        for v in get_neighbors(u, move_masks):
            alt = dist[u] + 1
            if alt < dist[v]:
                prev[v] = u
                dist[v] = alt
                heapq.heappush(heap, (alt, v))

    min_button_pushes += dist[goal]
print(f'Number of total button pushes: {min_button_pushes}')