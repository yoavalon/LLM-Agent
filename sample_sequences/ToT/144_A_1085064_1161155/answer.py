## Expert 1
Program A is syntactically transformed to express all the input operations in just one line, just like Program B.

```python
#Intermediate Program A1
n, N = eval(input()), list(map(int,input().split()))
a=N[::-1].index(min(N))
b=N.index(max(N))
print(a+b-(0 if b<n-1-a else 1))
```

## Expert 2
Program A is modified by moving the maximum value to the front of the list, similar to Program B.

```python
#Intermediate Program A2
n=eval(input());N=list(map(int,input().split()))
mx=max(N)
b=N.index(mx)
N.remove(mx)
N = [mx] + N
a=N[::-1].index(min(N))
print(a+b-(0 if b<n-1-a else 1))
```

## Expert 3
Program A is transformed by using `int()` function to cast the input to an integer instead of `eval()`, just like program B.

```python
#Intermediate Program A3
n=int(input());N=list(map(int,input().split()))
a=N[::-1].index(min(N))
b=N.index(max(N))
print(a+b-(0 if b<n-1-a else 1))
```

## Expert 1
Program A1 is modified to use the `int()` function to cast the input to an integer, and the operation of identifying the maximum value and moving it to the beginning of the sequence is also added.

```python
#Intermediate Program A1
n, N = int(input()), list(map(int,input().split()))
mx=max(N)
b=N.index(mx)
N.remove(mx)
N = [mx] + N
a=N[::-1].index(min(N))
print(a+b-(0 if b<n-1-a else 1))
```

## Expert 2
Program A2 is modified by replacing `eval()` with `int()` for casting user input to an integer, the same as Program B.

```python
#Intermediate Program A2
n=int(input());N=list(map(int,input().split()))
mx=max(N)
b=N.index(mx)
N.remove(mx)
N = [mx] + N
a=N[::-1].index(min(N))
print(a+b-(0 if b<n-1-a else 1))
```

## Expert 3
Program A3 is modified by moving the maximum value to the front of the list, similar to Program B.

```python
#Intermediate Program A3
n=int(input());N=list(map(int,input().split()))
mx=max(N)
b=N.index(mx)
N.remove(mx)
N = [mx] + N
a=N[::-1].index(min(N))
print(a+b-(0 if b<n-1-a else 1))
```

At this point there is no Expert left who thinks they can make a transformation without breaking the program's semantics. This means that there will be no more transformations from now. This is the final Program A:

```python
n=int(input());N=list(map(int,input().split()))
mx=max(N)
b=N.index(mx)
N.remove(mx)
N = [mx] + N
a=N[::-1].index(min(N))
print(a+b-(0 if b<n-1-a else 1))
```