n=eval(input())
a = list(map(int, input().split()))
ans = a.index(max(a)) + a[::-1].index(min(a))
print(ans - (ans >= n))