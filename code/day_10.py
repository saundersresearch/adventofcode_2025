import heapq
import math
from scipy.optimize import linprog
import numpy as np

with open("inputs/day_10.txt") as f:
    lines = f.readlines()

### Part 1
print("\nPart 1")
print("======")

total_button_pushes = 0
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

    total_button_pushes += dist[goal]
print(f'Number of total button pushes: {total_button_pushes}')

### Part 2
print("\nPart 2")
print("======")

total_button_pushes = 0
for line in lines:
    line = line.strip().split(" ")

    # Get goal
    goal_list = line[-1][1:-1]
    goal_list = goal_list.split(',')
    goal_list = [int(g) for g in goal_list]

    # This time, move_masks needs to describe which buttons are pushed
    # (need to reverse order)
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
        move_masks.append([int(d) for d in f'{mask:0{n_lights}b}'][::-1])

    # Equivalent to solving the following integer programming problem:
    # min c @ x s.t. A_eq @ x = b_eq
    # If c is ones, c @ x is the total # of button pushes
    # Then set up so A_eq @ x produces total number
    c = np.array([1]*len(move_masks))
    A_eq = np.array(move_masks).T
    b_eq = np.array(goal_list)

    
    res = linprog(
        c=c,
        A_eq=A_eq,
        b_eq=b_eq,
        integrality=1,
    )
    total_button_pushes += int(round(sum(res.x)))

print(f'Number of total button pushes: {total_button_pushes}')
