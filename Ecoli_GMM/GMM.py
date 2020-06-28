import numpy as np
np.set_printoptions(suppress=True)
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
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
    print(miu,'\n',sigma_square,'\n',alpha)

    W = E_step.update_W(data_needDeal,miu,sigma_square,alpha)
    # print(W)
    # print(np.argmax(W,axis=1))

    
    # fig = plt.figure(figsize=(20,10))
    # ax1 = fig.add_subplot(121)
    # ax2 = fig.add_subplot(122)
    # colors = ['b','g','r','gold']
    # ax1.set_title('NO_GMM')
    # ax2.set_title('GMM')
    # plt.xlabel('H')
    # plt.ylabel('L')
    # for i in range(4):
    #     ax1.scatter(x=data_afterNorma[:,0][acgtIndex[:,0] == i],y=data_afterNorma[:,1][acgtIndex[:,0] == i],s = 0.0005,c = colors[i])
    #     ax2.scatter(x=data_needDeal[:,0][np.argmax(W,axis=1) == i],y=data_needDeal[:,1][np.argmax(W,axis=1) == i],s = 0.0005,c = colors[i])
    # plt.show()


   