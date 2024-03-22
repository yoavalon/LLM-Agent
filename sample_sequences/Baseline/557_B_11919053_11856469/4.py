
n, w = tuple(map(int, input().strip().split()))  # Store input as tuple for consistency
a = list(int(s) for s in input().strip().split(' '))

a = sorted(a)

print(min(w, 3 * n * a[n] / 2.0, 3 * n * a[0]))
