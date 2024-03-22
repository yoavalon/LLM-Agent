n = int(input())
a = list(map(int,input().split()))
i = a.index(max(a))
a = [a[i]]+a[:i]+a[i+1:]
j = a[::-1].index(min(a))
print(i + j)