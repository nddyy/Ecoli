import numpy as np



def ints_Q_normal(data_after_pre_call,acgtIndex,index,H_or_L):
    # 对想处理的N碱基的H or L通道的亮度值以及Q值进行归一化
    # index 代表碱基N： G = 0, A = 1, T = 2, C = 3
    # H_or_L： H通道 = 0, L通道 = 1
    # Q值： 容量为4的一维数组，为通道亮度值排序后的四分位点
    
    q = np.percentile(np.sort(data_after_pre_call[:,H_or_L][acgtIndex[:,0] == index]),(25,50,75))
    q4 = q[2] + 3*(q[2] - q[0])
    q = np.append(q,q4)
    nor_ints = data_after_pre_call[:,H_or_L][acgtIndex[:,0] == index]/q[1]
    nor_q = q/q[1]
    return nor_ints,nor_q
    