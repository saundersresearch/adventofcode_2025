import math
from collections import deque
from functools import cache
import copy

with open("inputs/day_11.txt") as f:
    lines = f.readlines()
    lines = [line.strip().split(": ") for line in lines]

# Represent DAG as a dict
graph = {}
for line in lines:
    graph[line[0]] = line[1].split(" ")

# Are there any missing keys?
keys = set(graph.keys())
values = set((v for values in graph.values() for v in values))
if set(graph.keys()) != set((v for values in graph.values() for v in values)):
    missing_keys = values - keys
    for missing_key in missing_keys:
        graph[missing_key] = []

print(graph)

### Part 1
print("\nPart 1")
print("======")

# Use DFS to count all possible paths
def get_num_paths(s, t):
    if (s == t):
        return 1
    else:
        path_count = 0
        for neighbor in graph[s]:
            path_count += get_num_paths(neighbor, t)

    return path_count

print(get_num_paths('you', 'out'))

### Part 2
print("\nPart 2")
print("======")

# DFS is too slow, so we'll use a topological sort.
# First, create topological sort of graph
nodes = list(graph.keys())
topological_sort = deque()
visited = dict(zip(nodes, [False]*len(nodes)))

def visit(n):
    if n not in graph:
        pass
    elif visited[n]:
        return
    else:
        for neighbor in graph[n]:
            visit(neighbor)

    topological_sort.appendleft(n)
    visited[n] = True

for node in visited.keys():
    if not visited[node]:
        visit(node)

topological_sort = list(topological_sort)

def is_topological_sort(sort):
    for node1, values in graph.items():
        for node2 in values:
            if sort.index(node1) > sort.index(node2):
                return False
            
    return True
        
assert is_topological_sort(topological_sort)

# Which comes first, fft or dac?
fft_index = topological_sort.index('fft')
dac_index = topological_sort.index('dac')

first_stop = 'fft' if fft_index < dac_index else 'dac'
second_stop = 'dac' if first_stop == 'fft' else 'fft'

def get_num_paths(s, t):
    paths = dict(zip(nodes, [0]*len(nodes)))
    paths[s] = 1
    for u in topological_sort:
        for v in graph[u]:
            paths[v] += paths[u]

    return paths[t]

# Count paths from s to first_stop, first_stop to second_stop, second_stop to end
total_paths = (get_num_paths('svr', first_stop) * 
    get_num_paths(first_stop, second_stop) * 
    get_num_paths(second_stop, 'out'))
print(f'There are {total_paths} that pass through dac and fft')