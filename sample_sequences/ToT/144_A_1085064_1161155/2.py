#Intermediate Program A2
n=eval(input());N=list(map(int,input().split()))
mx=max(N)
b=N.index(mx)
N.remove(mx)
N = [mx] + N
a=N[::-1].index(min(N))
print(a+b-(0 if b<n-1-a else 1))