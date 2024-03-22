
l = list(map(int, input().split(' ')))
n, v = l[0], l[1:]  # Store allowed values in variable v for consistency
dp = [1] * (n + 1)
for i in range(1, n + 1):
    if i not in v:
        dp[i] = -2**64
for i in range(1, n + 1):
    for j in v:  # Use variable v for consistency
        if i > j:
            dp[i] = max(dp[i], dp[j] + dp[i - j])
print(dp[n])
