
n, w = tuple(int(s) for s in input().strip().split(' '))  # Read input as tuple for consistency
a = sorted(list(map(int, input().strip().split(' '))))  # Keep list for consistency
print(min(w, 3 * n * a[0], 1.5 * n * a[n]))
