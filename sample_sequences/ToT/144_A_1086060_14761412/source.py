L=eval(input());m=list(map(int,input().split()))
q=m.index(max(m))+m[::-1].index(min(m))
print(q-(q>=L))