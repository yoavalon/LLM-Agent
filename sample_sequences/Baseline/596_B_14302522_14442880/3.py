
n = 5
x = [1, 3, 4, 2, 5]
count = 0
curr = x[0]

for i in x[1:]:
    count += abs(i - curr)
    curr = i

print(count)
