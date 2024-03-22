
n, w = tuple(int(s) for s in input().strip().split(' '))
a = list(int(s) for s in input().strip().split(' '))  # Use list comprehension for consistency
a = sorted(a)
print(min(w, 3 * n * a[n] / 2.0, 3 * n * a[0]))  # Adapt calculation for consistency
