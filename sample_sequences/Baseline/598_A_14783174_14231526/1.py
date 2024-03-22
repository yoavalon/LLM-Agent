
t = eval(input())

for _ in range(t):  # Replace while loop with for loop
    n = eval(input())
    x = n.bit_length()  # Keep calculation for consistency
    ans = ((n * (n + 1)) / 2) - (2 * ((2 ** x) - 1))
    print(ans)
