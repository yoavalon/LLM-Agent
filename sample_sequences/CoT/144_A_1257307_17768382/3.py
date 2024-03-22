n = eval(input())
a = list(map(int, input().split()))
mx, mn = a.index(max(a)), len(a) - a[::-1].index(min(a)) - 1
print(mn + mx if mn + mx >= n else mn + mx - 1)