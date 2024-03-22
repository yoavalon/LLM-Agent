
l = list(map(int, input().split(' ')))
n, v = l[0], l[1:]
dp = [1] * (n + 1)
for i in range(1, n + 1):
    if i not in v:
        dp[i] = -2**64  # Use consistent negative value
for i in range(1, n + 1):
    for j in v:
        if i > j:
            dp[i] = max(dp[i], dp[j] + dp[i - j])
print(dp[n])
