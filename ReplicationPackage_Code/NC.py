import sys

def ND_Compute(a,b):
    A = set(a)
    B = set(b)
    return 1 - len(A.intersection(B)) / float(len(A.union(B)))


def SD_Compute(a,b):
    count=0
    total=0
    invalid=0
    min_num=-sys.maxsize-1
    for i in range(len(a)):
        total+=1
        if a[i]==min_num:
            invalid+=1
            continue
        if a[i]==b[i]:
            count+=1
    if total==invalid:
        return 1
    sd=1-(count/(total))
    return sd

def BD_Compute(c_s,c_f):
    count = 0
    for i in c_s:
        if c_s[i] == c_f[i] and c_s[i]!=1:
            count += 1
    return 1 - count / len(c_s)

def TD_Compute(a,b,k=1,l=1):
    count=0
    for i in range(len(a)):
        if a[i]==b[i]:
            count+=1
    return 1-count/(k*l)

