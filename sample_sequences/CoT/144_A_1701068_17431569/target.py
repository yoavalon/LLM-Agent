n=eval(input())
a=list(map(int,input().split(' ')))
u=0
v=0
for x in range(n):
    if a[u]<a[x]:u=x
    elif a[v]>=a[x]:v=x
if u>v: v+=1
print(n-v+u-1)