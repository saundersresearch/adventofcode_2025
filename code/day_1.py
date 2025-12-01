### Part 1
print('Part 1')
print('======')
dial = 50
num_dial = 100
num_zero = 0
with open('inputs/day_1.txt') as f:
    for line in f:
        instructions = line.strip()
        direction = instructions[0]
        distance = int(instructions[1:])
        
        if direction == 'L':
            dial = (dial - distance) % num_dial
        elif direction == 'R':
            dial = (dial + distance) % num_dial
        
        if dial == 0:
            num_zero += 1

print(f'Number of zero hits: {num_zero}\n')

### Part 2
print('Part 2')
print('======')
dial = 50
num_zero = 0
with open('inputs/day_1.txt') as f:
    for line in f:
        instructions = line.strip()
        direction = instructions[0]
        distance = int(instructions[1:])

        # Brute force method checking each dial motion
        for i in range(distance):
            if direction == 'L':
                dial -= 1
            elif direction == 'R':
                dial += 1

            if dial == 100:
                dial = 0
            elif dial == -1:
                dial = 99

            if dial == 0:
                num_zero += 1

print(f'Number of zero hits: {num_zero}\n')