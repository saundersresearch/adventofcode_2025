from functools import reduce

with open("inputs/day_6.txt") as f:
    block = f.readlines()

lines = [line.split() for line in block]

### Part 1
print("\nPart 1")
print("=======")

# Sample columns
operands = []
operations = lines[-1]
for i in range(len(lines[0])):
    operands.append([int(lines[line_num][i]) for line_num in range(len(lines) - 1)])


# Reduce columns given operation at bottom of column
result = 0
for operation, operand in zip(operations, operands):
    if operation == "+":
        func = int.__add__
    elif operation == "*":
        func = int.__mul__

    result += reduce(func, operand)

print(f'Total result is {result}')

### Part 2
print("\nPart 2")
print("=======")

lines = [line.strip("\n") for line in block]

result = 0
num_digits = len(lines) - 1
op_num = -1
operands = []
for col in range(len(lines[0])-1, -1, -1):
    # Sample column
    line = "".join([lines[i][col] for i in range(len(lines) - 1)])
    
    # Blank line --> select correct operation
    if line == " " * (num_digits):
        if operations[op_num] == "+":
            func = int.__add__
        elif operations[op_num] == "*":
            func = int.__mul__

        result += reduce(func, operands)
        operands = []
        op_num -= 1
    
    # Final column --> end as well
    elif col == 0:
        operands.append(int(line))
        if operations[op_num] == "+":
            func = int.__add__
        elif operations[op_num] == "*":
            func = int.__mul__

        result += reduce(func, operands)

    # Otherwise, just append integer to future operands to reduce
    else:
        operands.append(int(line))

print(f'Total result is {result}')
