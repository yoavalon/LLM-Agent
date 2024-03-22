n=eval(input());N=list(map(int,input().split()))
a=N[::-1].index(min(N))
b=N.index(max(N))
print(a+b-(0 if b<n-1-a else 1))