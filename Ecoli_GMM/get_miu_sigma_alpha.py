import numpy as np


def get_miu_sigma_alpha(data_afterNorma,acgtIndex):
    # 计算agct各自的μ，σ和α，也就是均值，方差和该类数据占全部数据的比重

    miu = np.zeros([4,2]) 
    sigma_square = np.zeros([4,2]) 
    # alpha = np.zeros(4)
    alpha = np.array([0.25,0.25,0.25,0.25])
    # total_num = acgtIndex.shape[0]

    for i in range(4):
        miu[i,0] = np.mean(data_afterNorma[:,0][acgtIndex[:,0] == i])
        miu[i,1] = np.mean(data_afterNorma[:,1][acgtIndex[:,0] == i])
        sigma_square[i,0] = np.var(data_afterNorma[:,0][acgtIndex[:,0] == i])
        sigma_square[i,1] = np.var(data_afterNorma[:,1][acgtIndex[:,0] == i])
        # alpha[i] = np.sum(acgtIndex == i)/total_num

    return miu,sigma_square,alpha