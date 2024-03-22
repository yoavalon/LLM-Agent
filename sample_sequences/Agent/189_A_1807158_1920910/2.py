l=list(map(int,input().split()))
n=l[0]
l=l[1:]
dp=(n+1)*[-1]
dp[0]=1
for i in range(0,n+1):
    for j in l:
        if i-j>=0 and dp[i-j]!=-1:
            dp[i]=max(dp[i],dp[i-j]+1)
print(dp[n]-1)