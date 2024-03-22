n=int(input())
a=list(map(int,input().split(' ')))
u=a.index(max(a))
v=a[::-1].index(min(a))
x=u+v
if x>=n: x-=1
print(x)