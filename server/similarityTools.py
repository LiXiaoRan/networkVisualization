import numpy as np
import scipy.spatial.distance as dist



def cosine_similarity(x1, y1, norm=False):
    """ 计算两个向量x和y的余弦相似度 """
    x=[]
    y=[]

    for arr in x1:
        x.append(arr['value'])
    for arr in y1:
        y.append(arr['value'])

    assert len(x) == len(y), "len(x) != len(y)"
    zero_list = [0] * len(x)
    if x == zero_list or y == zero_list:
        return float(1) if x == y else float(0)

    # method 1
    res = np.array([[x[i] * y[i], x[i] * x[i], y[i] * y[i]] for i in range(len(x))])
    cos = sum(res[:, 0]) / (np.sqrt(sum(res[:, 1])) * np.sqrt(sum(res[:, 2])))
    return 0.5 * cos + 0.5 if norm else cos  # 归一化到[0, 1]区间内


def jaccardSimilarity(arr1,arr2):
    arr_list1=[]
    arr_list2=[]
    for arr in arr1:
        arr_list1.append(strtoASCII(arr['value']))
    for arr in arr2:
        arr_list2.append(strtoASCII(arr['value']))
    
    v1=np.array(arr_list1)
    v2=np.array(arr_list2)
    matv=np.array([v1,v2])
    ds=dist.pdist(matv,'jaccard')
    return ds;



def strtoASCII(string):
    '''将字符串转成数字的和'''
    sum=0;
    string=str(string)
    if len(string) == 1:
        return ord(str(string))
    else:
        for i in range(len(string)):
            sum=sum+(ord(str(string[i])))
        return sum
