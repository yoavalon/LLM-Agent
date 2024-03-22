n=eval(input())
a=list(map(int,input().split()))
x=a.index(max(a))+a[::-1].index(min(a))
print(x-(x>=n))

