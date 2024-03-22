The program B separates the tasks which are performed in program A in a single line of code to multiple lines and uses different variable names. The variables `u` and `v` in program B represent the same concept found in program A where `a.index(max(a))` and `a[::-1].index(min(a))` are calculated. Here is how we can transform Program A step by step to make it look more like the syntax of Program B.

**Intermediate Program 1**

Splitting the calculation of `x` into two steps and replacing variable names:

```python
n=eval(input())
a=list(map(int,input().split()))
max_position=a.index(max(a))
min_position_reverse=a[::-1].index(min(a))
x=max_position+min_position_reverse
print(x-(x>=n))
```


**Intermediate Program 2**
Simplify the last print line by separating the calculation into two lines and introduce variables to make it similar to Program B.

```python
n=eval(input())
a=list(map(int,input().split()))
u=a.index(max(a))
v=a[::-1].index(min(a))
x=u+v  # equivalent to the calculation of n-v+u in Program B
if x>=n: x-=1  # equivalent to the if statement in Program B (if u>v: v+=1)
print(x)
```


**Intermediate Program 3**

Remove the `eval()` function used in Program A for consistency with Program B:

```python
n=int(input())
a=list(map(int,input().split()))
u=a.index(max(a))
v=a[::-1].index(min(a))
x=u+v
if x>=n: x-=1
print(x)
```

**Intermediate Program 4**

Use `input().split(' ')` instead of `input().split()` like in Program B:
```python
n=int(input())
a=list(map(int,input().split(' ')))
u=a.index(max(a))
v=a[::-1].index(min(a))
x=u+v
if x>=n: x-=1
print(x)
```
Now the program A is structurally very similar to program B.

Final Note: The semantic equivalence between these two programs presumes that the input values are distinct. If there are duplicated min or max numbers, the original programs actually have different behaviours due to how `index` function or loop iteration treats duplicates.