### Part 1
print("\nPart 1")
print("======")

with open("inputs/day_3.txt", "r") as f:
    banks = f.readlines()

total = 0
for bank in banks:
    bank_list = list(map(int, bank.strip()))

    max_joltage = max(bank_list)
    max_joltage_id = bank_list.index(max_joltage)

    rest = bank_list[max_joltage_id+1:]

    if len(rest) > 0:
        second_max_joltage = max(rest)
    else:
        second_max_joltage = max_joltage
        max_joltage = max(bank_list[:-1])

    total += int(str(f'{max_joltage}{second_max_joltage}'))

print(f'The total joltage is {total}')

### Part 2
print("\nPart 2")
print("======")

with open("inputs/day_3.txt", "r") as f:
    banks = f.readlines()

total = 0
n = 12
for bank in banks:
    bank_list = list(map(int, bank.strip()))

    subset_idx = []
    start_idx = 0

    # The next number must be the leftmost largest number in the subset that has n-1 to the right of it
    # (starting at the previous number's index)
    for i in range(n):
        subset = bank_list[start_idx:len(bank_list) -(n-i-1)]
        if len(subset) > 0:
            max_val = max(subset)
            for j, val in enumerate(subset):
                j += start_idx
                if val == max_val and j not in subset_idx:
                    subset_idx.append(j)
                    start_idx = j + 1
                    break
    
    total += int("".join(map(str, [bank_list[b] for b in subset_idx])))

print(f'The total joltage is {total}')