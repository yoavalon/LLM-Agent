import sys
n = int(input())
a = list(map(int, input().split()))
a.sort()
if a[-1] == 1:
    for x in a[:-1] + [2]:
        print(x),
else:
    for x in [1] + a[:-1]:
        print(x),