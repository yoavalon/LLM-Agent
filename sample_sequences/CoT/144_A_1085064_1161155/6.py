n = (int)(input())
m = list(map(int, input().split()))
mx = max(m)
res = m.index(mx)
m.remove(mx)
m = [mx] + m
print(res + m[::-1].index(min(m))-(0 if res<n-1-m[::-1].index(min(m)) else 1))