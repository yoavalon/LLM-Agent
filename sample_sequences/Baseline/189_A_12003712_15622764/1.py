
l = list(map(int, input().split(' ')))  # Read input like the second program
n, a, b, c = l[0], l[1], l[2], l[3]
dp = [1] * (n + 1)  # Initialize dp like the second program
for i in range(1, n + 1):
    if i not in (a, b, c):  # Check for allowed values like the second program
        dp[i] = -2**64
for i in range(1, n + 1):
    for j in (a, b, c):  # Iterate through allowed values
        if i > j:
            dp[i] = max(dp[i], dp[j] + dp[i - j])
print(dp[n])
