
n, w = map(int, input().strip().split())  # Use map for input like the second program
a = list(int(s) for s in input().strip().split(' '))

a = sorted(a)

print(min(w, 3 * n * a[n] / 2.0, 3 * n * a[0]))
