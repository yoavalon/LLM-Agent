n = input()
a = list(map(int,input().split()))
i = a.index(max(a))
a = [a[i]]+a[:i]+a[i+1:]
a = a.reverse()
j = a.index(min(a))
print(i + j)