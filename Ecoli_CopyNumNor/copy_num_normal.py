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

    # data1_path = 'F://wd/Ecoli/1.mat'
    # data2_path = 'F://wd/Ecoli/2.mat'
    # data1 = scio.loadmat(data1_path)
    # data2 = scio.loadmat(data2_path)
    # signalH1 = data1.get('dataH')
    # signalL1 = data1.get('dataL')
    # acgtIndex1 = data1.get('acgtIndex1')
    # signalH2 = data2.get('dataH')
    # signalL2 = data2.get('dataL')
    # acgtIndex2 = data2.get('acgtIndex1')

    

    q_mean = np.zeros(4)
    acbi = np.zeros(acgtIndex.shape[0])
    count = np.zeros(acgtIndex.shape[0])
    validDNB = np.ones([FOV_NUM,acgtIndex.shape[0]])

    for i in range(FOV_NUM):
        for j in range(CYCLE_NUM):
            # 调用pre_call

            nor_ints_T,nor_q_T = ints_Q_normal(data_after_pre_call,acgtIndex,2,0)   # 获得T碱基的H通道的Q值
            nor_ints_A,nor_q_A = ints_Q_normal(data_after_pre_call,acgtIndex,1,1)   # 获得A碱基的L通道的Q值
            q_mean = q_mean + nor_q_T + nor_q_A
            count = count + np.where(acgtIndex[:,0] == 2,1,0) + np.where(acgtIndex[:,0] == 1,1,0)
            acbi = acbi + data_after_pre_call[:,0] * np.where(acgtIndex[:,0] == 2,1,0) + data_after_pre_call[:,1] * np.where(acgtIndex[:,0] == 1,1,0)
        q_mean = q_mean/CYCLE_NUM
        acbi = acbi/count
        acbi[np.isnan(acbi)] = 0
        acbi[np.where(acbi > q_mean[3])] = 0
        validDNB[i,:][acbi == 0] = 0
        print(validDNB[i])
        # data_after_pre_call[:,0] = data_after_pre_call[:,0]
        # frequency,bins_limits,patches = acbi_hist(acbi)

    

def data_pre_deal(signalH,signalL,acgtIndex):
    # 把存放H通道和L通道亮度值的 N X M 的数组拼接成 DNB_num X 2 的二维数组
    # 把存放acgt标签的 N X M 的数组变形为 DNB_num X 1 的二维数组
    
    signalH = np.reshape(signalH,[-1,1])
    signalL = np.reshape(signalL,(-1,1))
    acgtIndex = np.reshape(acgtIndex,(-1,1))
    signal_H_L = np.stack((signalH[:,0],signalL[:,0]),axis=1)

    return signal_H_L,acgtIndex