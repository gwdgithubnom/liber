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
    from context import resource_manager

    from cluster.dbscan import dbscan_chrisjmccormick
    f = input()
    r = f.split(' ')
    filename = ''
    if len(r) > 1:
        n = int(r[1])
    else:
        n = int(input())
    filename = str(r[0])
    result = readFile(file=filename)
    for k in result:
        if result[k] <= n:
            continue
        else:
            print(k + " " + str(result[k]))
    return r


if __name__ == '__main__':
    # main.save()
    from pandas import Series
    index_id=Series(['1','2','3','4'],index=['1','2','3','4'])
    ll=index_id.values
    id_index=Series(ll,index=index_id.index)
    print(id_index)
    index_id[1]=333

    id_index.drop(labels=['1'],axis=0)
    print(index_id)
    print(id_index)
