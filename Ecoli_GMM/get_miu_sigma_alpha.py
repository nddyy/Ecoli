import numpy as np

def get_miu_sigma_alpha(signalH,signalL,acgtIndex):
    # 计算agct各自的μ，σ和α，也就是均值，方差和该类数据占全部数据的比重

    miu = np.zeros([4,2]) 
    sigma_square = np.zeros([4,2]) 
    alpha = np.zeros(4)
    total_num = acgtIndex.shape[0] * acgtIndex.shape[1]    

    # group_G = np.dstack((signalH[acgtIndex == 0],signalL[acgtIndex == 0]))
    # group_A = np.dstack((signalH[acgtIndex == 1],signalL[acgtIndex == 1]))
    # group_C = np.dstack((signalH[acgtIndex == 2],signalL[acgtIndex == 2]))
    # group_T = np.dstack((signalH[acgtIndex == 3],signalL[acgtIndex == 3]))

    for i in range(4):
        miu[i,0] = np.sum(signalH[acgtIndex == i])/len(signalH[acgtIndex == i])
        miu[i,1] = np.sum(signalL[acgtIndex == i])/len(signalL[acgtIndex == i])


    for i in range(4):
        total_Dvalue_H = 0
        total_Dvalue_L = 0
        for j in range(len(signalH[acgtIndex == i])):
            total_Dvalue_H = total_Dvalue_H + np.square(signalH[acgtIndex == i][j] - miu[i,0])
            total_Dvalue_L = total_Dvalue_L + np.square(signalL[acgtIndex == i][j] - miu[i,1])
        sigma_square[i,0] = total_Dvalue_H/len(signalH[acgtIndex == i])
        sigma_square[i,1] = total_Dvalue_L/len(signalL[acgtIndex == i])

    for i in range(4):
        alpha[i] = len(signalH[acgtIndex == i])/total_num

    return miu,sigma_square,alpha