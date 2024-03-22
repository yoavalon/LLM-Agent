
l = list(map(int, input().split(' ')))
n, a, b, c = l[0], l[1], l[2], l[3]  # Reintroduce individual variables
dp = [1] * (n + 1)
for i in range(1, n + 1):
    if i not in (a, b, c):  # Retain check for allowed values
        dp[i] = -2**64
for i in range(1, n + 1):
    for j in (a, b, c):  # Iterate through allowed values explicitly
        if i > j:
            dp[i] = max(dp[i], dp[j] + dp[i - j])
print(dp[n])
