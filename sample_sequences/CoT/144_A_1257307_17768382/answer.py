Firstly, I'll reformat Program A a bit (adding spaces around binary operators and equals sign, rearranging the expressions in if-else condition to match with Program B) and for further transformation: 

```python
n = eval(input())
a = list(map(int, input().split()))
mx = a.index(max(a))
a.reverse()
mn = a.index(min(a))
print(mn + mx if mn + mx >= n else mn + mx - 1)
```
Secondly, I'll replace the `a.reverse()` and related parsing in `mn` variable with index calculation from reversed array to match the one line logic in Program B - this will remove the need for reversing the array:

```python
n = eval(input())
a = list(map(int, input().split()))
mx = a.index(max(a))
mn = len(a) - a[::-1].index(min(a)) - 1
print(mn + mx if mn + mx >= n else mn + mx - 1)
```

The third transformation entails merging variable assignments `mx` and `mn` in one line as Program B does with `ans`. Note that the values of `mx` and `mn` are used in an expression for the `print` statement. Therefore, the values needs to be calculated before they're used. The transformation results in:

```python
n = eval(input())
a = list(map(int, input().split()))
mx, mn = a.index(max(a)), len(a) - a[::-1].index(min(a)) - 1
print(mn + mx if mn + mx >= n else mn + mx - 1)
```
The fourth transformation entails merging the calculation in the print statement into a single line like Program B:

```python
n = eval(input())
a = list(map(int, input().split()))
mx, mn = a.index(max(a)), len(a) - a[::-1].index(min(a)) - 1
ans = mn + mx
print(ans if ans >= n else ans - 1)
```

With the above transition, now Program A is syntactically similar to Program B and semantic is same as before.