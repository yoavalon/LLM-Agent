L=eval(input());m=list(map(int,input().split()))
p=m.index(max(m))
q=m[::-1].index(min(m))
print(p+q-(p+q>=L))
