n = int(input())
a = list(map(int, input().split()))
a = sorted(a)
if a[-1] == 1:
    for i in a[:-1] + [2]:
        print(i),
else:
    for i in [1] + a[:-1]:
        print(i),