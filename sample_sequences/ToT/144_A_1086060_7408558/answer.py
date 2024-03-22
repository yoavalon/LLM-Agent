Expert 1:


    #Step 1: Change variable name L to n to match Program B
    n = eval(input())
    m = list(map(int, input().split()))
    q = m.index(max(m)) + m[::-1].index(min(m))
    print(q - (q >= n))


Expert 2:


    #Step 1: Rename variable m to a
    n=eval(input())
    a=list(map(int,input().split()))
    q=a.index(max(a))+a[::-1].index(min(a))
    print(q-(q>=n))


Expert 3:


    #Step 1: Break down the complex line of code into smaller parts for clarity, similar to Program B
    n = eval(input())
    a = list(map(int, input().split()))

    i = a.index(max(a))
    a.reverse()

    j = a.index(min(a))
    q = i + j

    print(q - (q >= n))



Expert 1:


    #Step 2: Change variable name m to a to match Program B
    n = eval(input())
    a = list(map(int, input().split()))
    q = a.index(max(a)) + a[::-1].index(min(a))
    print(q - (q >= n))


Expert 2:


    #Step 2: Split the complex formula into multiple line 
    n=eval(input())
    a=list(map(int,input().split()))
    i=a.index(max(a))
    a.reverse()
    j=a.index(min(a))
    q=i+j
    print(q-(q>=n))


Expert 3:


    #Step 2: Replace the inequality operator with a conditional statement, like in Program B
    n = eval(input())
    a = list(map(int, input().split()))
    i = a.index(max(a))
    a.reverse()
    j = a.index(min(a))
    q = i + j
    if q < n: 
        print(q)
    else: 
        print(q - 1)


Expert 1:


    #Step 3: Replace the inequality operator with a conditional statement
    n = eval(input())
    a = list(map(int, input().split()))
    q = a.index(max(a)) + a[::-1].index(min(a))
    if q < n:
        print(q)
    else:
        print(q - 1)


Expert 2:


    #Step 3: Replace the print statement with a conditional statement
    n=eval(input())
    a=list(map(int,input().split()))
    i=a.index(max(a))
    a.reverse()
    j=a.index(min(a))
    q=i+j
    if q < n:
        print(q)
    else:
        print(q-1)


Expert 3:


    #Step 3: There are no more transformations that keep the semantics of the program intact while making it syntactically more similar to Program B
    n = eval(input())
    a = list(map(int, input().split()))
    i = a.index(max(a))
    a.reverse()
    j = a.index(min(a))
    q = i + j
    if q < n: 
        print(q)
    else: 
        print(q - 1)