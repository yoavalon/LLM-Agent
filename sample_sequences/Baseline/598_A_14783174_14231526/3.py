
t = eval(input())

for _ in range(t):
    n = eval(input())
    ans = n * (n + 1) / 2
    p = 1  # Initialize p like the second program
    while p <= n:
        ans -= p * 2
        p *= 2
    print(ans)
