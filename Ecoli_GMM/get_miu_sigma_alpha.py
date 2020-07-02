import numpy as np


def get_miu_sigma_alpha(data_afterNorma,acgtIndex):
    # 计算agct各自的μ，cov和α，也就是均值，协方差和该类数据占有效数据的比重
    # alpha默认为[0.25,0.25,0.25,0.25]在实测中有较好效果

    miu = np.zeros([4,2]) 
    cov = np.zeros([4,2,2])
    alpha = np.array([0.25,0.25,0.25,0.25])

    for i in range(4):
        miu[i,0] = np.mean(data_afterNorma[:,0][acgtIndex[:,0] == i])
        miu[i,1] = np.mean(data_afterNorma[:,1][acgtIndex[:,0] == i])
        cov[i] = np.cov((data_afterNorma[:,0][acgtIndex[:,0] == i]),(data_afterNorma[:,1][acgtIndex[:,0] == i]))

    return miu,cov,alpha