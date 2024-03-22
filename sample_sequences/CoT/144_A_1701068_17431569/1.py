n=eval(input())
a=list(map(int,input().split()))
max_position=a.index(max(a))
min_position_reverse=a[::-1].index(min(a))
x=max_position+min_position_reverse
print(x-(x>=n))