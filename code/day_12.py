from itertools import product
from tqdm import tqdm

with open("inputs/day_12.txt", "r") as f:
    blocks = f.read().split("\n\n")
    lines = [block.split("\n") for block in blocks]

shape_len = 3
shapes = []
for line in lines[:-1]:
    shape = []
    for row, chars in enumerate(line[1:]):
        for col, char in enumerate(chars):
            if char == "#":
                shape.append((row - shape_len // 2, col - shape_len // 2))

    shapes.append(tuple(shape))

# Precompute transforms for shapes
shape_transforms = {}
for i, shape in enumerate(shapes):
    shape_transforms[shape] = []
    for rotations, flips in product(range(4), range(2)):
        p = shape
        for F in range(flips):
            p = [(q[0], -q[1]) for q in p]
        for R in range(rotations):
            p = [(q[1], -q[0]) for q in p]
        shape_transforms[shape].append(p)

def dfs(pieces, board, board_size, i=0):
    if i == len(pieces):
        return True
    
    # Do we even have room to fit the rest?
    if sum([v == 0 for v in board.values()]) < sum([len(piece) for piece in pieces[i:]]):
        return False
    
    p = pieces[i]
    piece_transforms = shape_transforms[p]
    for p in piece_transforms:
        for pos in product(range(board_size[0]), range(board_size[1])):
            # Does it fit on board?
            new_placement_idx = [(pos[0] + row, pos[1] + col) for row, col in p]
            if all(0 <= r < board_size[0] and
                0 <= c < board_size[1] and
                board[r, c] == 0
                for (r, c) in new_placement_idx):
                # Place on board
                for idx in new_placement_idx:
                    board[idx] = 1
                if dfs(pieces, board, board_size, i+1):
                    return True
                    
                # Remove from board
                for idx in new_placement_idx:
                    board[idx] = 0
    return False

num_fit = 0
for region in tqdm(lines[-1]):
    region_size, present_list = region.split(": ")
    region_size = tuple(int(x) for x in region_size.split('x'))
    present_list = [int(x) for x in present_list.split(' ')]

    presents = []
    for r, num_present in enumerate(present_list):
        presents.extend([shapes[r]]* num_present)

    board = dict(zip(product(range(region_size[0]), range(region_size[1])), [0]*(region_size[0]*region_size[1])))

    if dfs(presents, board, region_size):
        num_fit += 1

print(f'Total that can fit: {num_fit}')