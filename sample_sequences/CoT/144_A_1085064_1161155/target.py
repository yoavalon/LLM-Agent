n, m = (int)(input()), list(map(int, input().split()))
mx = max(m)
res = m.index(mx)
m.remove(mx)
m = [mx] + m
print(res + m[::-1].index(min(m)))