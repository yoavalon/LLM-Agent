n = eval(input())
a = list(map(int,input().split()))
mx = a.index(max(a))
a.reverse()
mn = a.index(min(a))
ans = mn+mx
print(ans - (ans >= n))