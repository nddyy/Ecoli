import numpy as np
from scipy.stats import multivariate_normal

def update_W(acgt_data, miu, sigma_square, alpha):
    # clusters_num 是GMM模型中聚类的个数，也就是子高斯分布的个数。该项目数据明确要分为ACGT四簇，所以直接定义为4
    # points_num 是样本点的个数
    # miu 是每个高斯分布的均值
    # sigma_square 是每个高斯分布的方差
    # pdf为概率密度函数
    # W 是每个样本属于每一簇的概率，是个 clusters_num * points_num 大小的矩阵。一个子高斯分布就是一簇
    # alpha 是每一簇的比重

    points_num = len(acgt_data)
    clusters_num = 4   
    pdfs = np.zeros([points_num, clusters_num])     
    for i in range(clusters_num):
        pdfs[:,i] = alpha[i] * multivariate_normal.pdf(acgt_data,miu[i],np.diag(sigma_square[i]))
    W = pdfs / pdfs.sum(axis=1).reshape(-1, 1)

    return W

# def update_Pi(W):
#     Pi = W.sum(axis=0) / W.sum()
#     return Pi