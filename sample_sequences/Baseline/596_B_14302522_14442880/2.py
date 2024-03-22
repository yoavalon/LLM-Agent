
n = int(input())
x = list(map(int, input().split(" ")))
count = 0
curr = 0

for i in x:
    count += abs(i - curr)
    curr = i
print(count)
