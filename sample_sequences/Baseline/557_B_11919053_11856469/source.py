R=lambda:list(map(int,input().split()))
n,w=R()
a=sorted(R())
print(min(w,3*n*a[0],1.5*n*a[n]))