n = eval(input())
a = list(map(int, input().split()))
mx = a.index(max(a))
mn = len(a) - a[::-1].index(min(a)) - 1
print(mn + mx if mn + mx >= n else mn + mx - 1)