
t = eval(input())

for _ in range(t):
    n = eval(input())
    ans = n * (n + 1) / 2  # Initialize ans like the second program
    x = n.bit_length()
    while p <= n:  # Introduce inner while loop for consistency
        ans -= p * 2
        p *= 2
    print(ans)
