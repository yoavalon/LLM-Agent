
t = eval(input())

for _ in range(t):
    n = eval(input())
    ans = n * (n + 1) / 2
    p = 1
    while p <= n:  # No further transformations possible while retaining semantics
        ans -= p * 2
        p *= 2
    print(ans)
