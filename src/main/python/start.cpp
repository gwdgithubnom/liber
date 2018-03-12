import collections

def readFile(file="input.txt"):
    try:
        f=open(file)
    except:
        print("file not found, in current directory.")
    data=[]
    for line in f:
        line=f.readline()
        line=line+" "+line[:-1]
    data=line.split(' ')
    r = collections.Counter(data)
    return r


if __name__ == '__main__':
    # main.save()

    f=input()
    r=f.split(' ')
    filename=''
    if len(r)>1:
        n=int(r[1])
    else:
        n=int(input())
    filename = str(r[0])
    result=readFile(file=filename)
    for k in result:
        if result[k]<=n:
            continue
        else:
            print(k+" "+str(result[k]))
