t = eval(input())

for _ in range(t):
	n = eval(input())
	ans = n * (n + 1) / 2
	p = 1
	while p <= n:
		ans -= p * 2
		p *= 2
	print(ans)
