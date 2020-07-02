import numpy as np
np.set_printoptions(suppress=True)
np.seterr(divide='ignore',invalid='ignore')
import scipy.io as scio
from ints_Q_normal import *
from acbi_hist import *

FOV_X = 5  
FOV_Y = 4  
CYCLE_NUM = 25  
FOV_NUM = FOV_X * FOV_Y

if __name__ == "__main__":

    data_path = 'F://wd/Ecoli/GMM_input.mat'
    data = scio.loadmat(data_path)
    acgtIndex = data.get('acgtIndex')
    data_after_pre_call = data.get('data_afterNorma')  # the data just for test
    data_needDeal = data_after_pre_call[acgtIndex[:,0] != 6]
    q_mean_T,q_mean_A = np.zeros(4),np.zeros(4)
    acbi_T,acbi_A = np.zeros(acgtIndex.shape[0]),np.zeros(acgtIndex.shape[0])
    count_T,count_A = np.zeros(acgtIndex.shape[0]),np.zeros(acgtIndex.shape[0])
    validDNB = np.ones(acgtIndex.shape[0])

    # for i in range(FOV_NUM):
    for j in range(CYCLE_NUM):
        # 调用pre_call

        nor_ints_T,nor_q_T = ints_Q_normal(data_after_pre_call,acgtIndex,2,0)   # 获得T碱基的H通道的Q值
        nor_ints_A,nor_q_A = ints_Q_normal(data_after_pre_call,acgtIndex,1,1)   # 获得A碱基的L通道的Q值
        q_mean_T += nor_q_T
        q_mean_A += nor_q_A
        count_T += np.where(acgtIndex[:,0] == 2,1,0)
        count_A += np.where(acgtIndex[:,0] == 1,1,0)
        acbi_T += data_after_pre_call[:,0] * np.where(acgtIndex[:,0] == 2,1,0)
        acbi_A += data_after_pre_call[:,1] * np.where(acgtIndex[:,0] == 1,1,0)
    q_mean_T = q_mean_T/CYCLE_NUM
    q_mean_A = q_mean_A/CYCLE_NUM
    acbi_T = acbi_T/count_T
    acbi_A = acbi_A/count_A
    acbi_T[np.isnan(acbi_T)] = 0
    acbi_A[np.isnan(acbi_A)] = 0
    acbi_T[np.where(acbi_T > q_mean_T[3])] = 0
    acbi_A[np.where(acbi_A > q_mean_A[3])] = 0
    validDNB[np.logical_and(acbi_T,acbi_A) == 0] = 0
    # np.savetxt('test.txt',np.logical_and(acbi_T,acbi_A),fmt = '%f')
    acbi_hist(acbi_A)

    