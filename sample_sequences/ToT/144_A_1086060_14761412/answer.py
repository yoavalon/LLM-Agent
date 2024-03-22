Expert 1:
```
L=eval(input())
a=list(map(int,input().split()))
ma=max(a)
mi=min(a)
ima= a.index(ma)
imi= a[-1::-1].index(mi)
q=ima + imi 
print(q - 1 if ima >= L - imi else q)
```

Expert 2:
```
n =eval(input())
m=list(map(int,input().split()))
ma=max(m)
ima= m.index(ma)
imi= m[::-1].index(mi)
q = ima + imi 
print(q - 1 if ima >= n - imi else q)
```

Expert 3:
```
n =eval(input())
a=list(map(int,input().split()))
ma=max(a)
imi=a[::-1].index(min(a))
ima= a.index(ma)
q= ima + imi 
print(q - 1 if ima >= n - imi else q)
```

 Expert 1:
```
n = eval(input())
a = list(map(int, input().split()))
ma = max(a)
mi = min(a)
ima = a.index(ma)
imi = a[::-1].index(mi)
c = ima + imi
print(c - 1 if ima >= n - imi else c)
```

Expert 2:
```
n = eval(input())
a = list(map(int, input().split()))
ma = max(a)
mi = min(a)
ima = a.index(ma)
imi = a[-1::-1].index(mi)
c = ima + imi
print(c - 1 if ima >= n - imi  else c)
```

Expert 3:
```
n = eval(input())
a = list(map(int, input().split()))
ma = max(a)
mi = min(a)
ima = a.index(ma)
imi = a[::-1].index(mi)
c = ima + imi 
print(c - 1 if ima >= n - imi else c)
```