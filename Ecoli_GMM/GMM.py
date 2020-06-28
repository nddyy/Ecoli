import numpy as np
np.set_printoptions(suppress=True)
import matplotlib.pyplot as plt
# import pandas as pd
import scipy.io as scio
import get_miu_sigma_alpha
import E_step


if __name__ == '__main__':
    
    data_path = 'F://wd/Ecoli/GMM_input.mat'
    data = scio.loadmat(data_path)
    acgtIndex = data.get('acgtIndex')
    data_afterNorma = data.get('data_afterNorma')
    data_needDeal = data_afterNorma[acgtIndex[:,0] != 6]
    # 标签为6的数据为噪音点，剔除掉

    miu,sigma_square,alpha = get_miu_sigma_alpha.get_miu_sigma_alpha(data_afterNorma,acgtIndex)
    # print(miu,'\n',sigma_square,'\n',alpha)

    W = E_step.update_W(data_needDeal,miu,sigma_square,alpha)
    print(len(W))

   