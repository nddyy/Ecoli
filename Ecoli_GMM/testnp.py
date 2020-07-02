import numpy as np
np.set_printoptions(suppress=True)
import scipy.io as scio

data1_path = 'F://wd/Ecoli/1.mat'
data2_path = 'F://wd/Ecoli/2.mat'
data1 = scio.loadmat(data1_path)
data2 = scio.loadmat(data2_path)

signalH1 = data1.get('dataH')
signalL1 = data1.get('dataL')
acgtIndex = data1.get('acgtIndex1')

signalH1 = np.reshape(signalH1,[-1,1])
signalL1 = np.reshape(signalL1,(-1,1))
acgtIndex = np.reshape(acgtIndex,(-1,1))
signal_H_L = np.stack((signalH1[:,0],signalL1[:,0]),axis=1)
# print(signal_H_L)
# print(acgtIndex)
print(data2)
# print(signalH1,'\n',signalL1,'\n',acgtIndex)

# # print(acgtIndex.shape[1])
# b = np.where(acgtIndex[:,0] == 1,1,0)
# print(b)

# a = np.zeros(acgtIndex.shape[0])

# for i in range(2):
#     a += data_after_pre_call[:,1] * b    
# print(a)
# # print(np.diag(sigma_square))


