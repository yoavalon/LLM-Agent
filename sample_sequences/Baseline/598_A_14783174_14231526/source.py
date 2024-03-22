import math
t=eval(input())
while t:
    t-=1
    n=eval(input())
    ##x= math.log(n,2)
    x=n.bit_length()
    s= ((n*(n+1))/2)- (2*((2**x)-1))
    print(s)
