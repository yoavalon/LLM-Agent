n=eval(input())
a=list(map(int,input().split()))
u=a.index(max(a))
v=a[::-1].index(min(a))
x=u+v  # equivalent to the calculation of n-v+u in Program B
if x>=n: x-=1  # equivalent to the if statement in Program B (if u>v: v+=1)
print(x)