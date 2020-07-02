import numpy as np
import scipy.io as scio

# data_path = 'F://wd/Ecoli/GMM_input.mat'
# data = scio.loadmat(data_path)
# acgtIndex = data.get('acgtIndex')
# data_after_pre_call = data.get('data_afterNorma')  # the data just for test
# data_needDeal = data_after_pre_call[acgtIndex[:,0] != 6]

# # print(acgtIndex.shape[1])
# b = np.where(acgtIndex[:,0] == 1,1,0)
# print(b)

# a = np.zeros(acgtIndex.shape[0])

# for i in range(2):
#     a += data_after_pre_call[:,1] * b    
# print(a)
# # print(np.diag(sigma_square))

a = [[1,2],[3,4],[1,2],[3,4]]

print(np.diag(a))
