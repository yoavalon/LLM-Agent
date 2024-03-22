
n = int(input())
x = input().split(" ")
count = 0
curr = 0

for i in x:
    count += abs(int(i) - curr)
    curr = int(i)
print(count)
