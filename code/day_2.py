from textwrap import wrap

### Part 1
print("Part 1")
print("======")

with open("inputs/day_2.txt", "r") as f:
    id_range_list = list(f.readline().split(","))

total = 0
for id_range in id_range_list:
    low, high = id_range.split("-")
    low, high = int(low), int(high)

    for id in range(low, high+1):
        id_str = str(id)

        # Only even length strings can be repeats
        if len(id_str) % 2 == 0:
            if id_str[:len(id_str)//2] == id_str[len(id_str)//2:]:
                total += id

print(f'Total is {total}\n')

### Part 1
print("Part 2")
print("======")

with open("inputs/day_2.txt", "r") as f:
    id_range_list = list(f.readline().split(","))

total = 0
for id_range in id_range_list:
    low, high = id_range.split("-")
    low, high = int(low), int(high)

    for id in range(low, high+1):
        id_str = str(id)

        # Now, need to consider strings from length 1 to len(id_str)//2
        for repeat_len in range(1, len(id_str)//2+1):
            if len(id_str) % repeat_len == 0:
                segments = wrap(id_str, repeat_len)

                # Are all the segments equal?
                if len(set(segments)) == 1:
                    total += id
                    break

print(f'Total is {total}')
