n = eval(input())
a = list(map(int, input().split()))
mx, mn = a.index(max(a)), len(a) - a[::-1].index(min(a)) - 1
ans = mn + mx
print(ans if ans >= n else ans - 1)