import collections
from scipy.stats import norm
import matplotlib.pyplot as plt
import numpy as np

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
    # main.save()
    import numpy as np

    a = np.random.normal(size=1000)

    bins = np.arange(-8, 9)
    # bins = np.array([-1.2,2.3,3.1,3.3,4.2,4.5,4.7,5])
    print(a)
    print(bins)

    histogram = np.histogram(a, bins=bins, normed=True)[0]

    bins = 0.5*(bins[1:] + bins[:-1])

    from scipy import stats

    b = stats.norm.pdf(bins)  # norm是正态分布
    import matplotlib.pyplot as plt
    plt.plot(bins, b)
    plt.show()
    print(b)
    #plt.plot(bins, histogram)
    plt.plot(bins, b)
    plt.show()
def _calc_ent(probs):
    """
    计算信息熵
    :param probs: numpy结构
    :return: 返回probs的信息熵
    """
    ent = - probs.dot(np.log2(probs))
    return ent

def gauss_function(data=np.array([1,2,3,4,5,6,7,8])):
    random_sample=data

    # Generate an array of 200 random sample from a normal dist with
    # mean 0 and stdv 1
    #random_sample = norm.rvs(loc=0,scale=1,size=200)
    sample=data
    from scipy import stats
    import numpy as np
    from scipy.stats import norm
    mu, std = norm.fit(data)
    print(mu)
    print(std)

if __name__ == '__main__':
    t=np.array([1,2,3,4,5])
    for i in range(0,3):
        print(i)