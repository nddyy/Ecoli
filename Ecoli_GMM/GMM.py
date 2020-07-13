import numpy as np
np.set_printoptions(suppress=True)
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import scipy.io as scio
import get_miu_sigma_alpha
import E_step
import time


if __name__ == '__main__':
    
    data_path = 'F://wd/Ecoli/GMM_input.mat'
    data = scio.loadmat(data_path)
    acgtIndex = data.get('acgtIndex')
    data_afterNorma = data.get('data_afterNorma')

    # time_start=time.time()

    miu,cov,alpha = get_miu_sigma_alpha.get_miu_sigma_alpha(data_afterNorma,acgtIndex)

    data_deal_index6 = data_afterNorma.copy()
    data_deal_index6[np.where((data_deal_index6[:,0] == 65504) | (data_deal_index6[:,1] == 65504))] = [0,0]

    W = E_step.update_W(data_deal_index6,miu,cov,alpha)
    W[np.where((data_afterNorma[:,0] == 65504) | (data_afterNorma[:,1] == 65504))] = [0.25,0.25,0.25,0.25]

    # time_end=time.time()
    # print('time cost',time_end-time_start,'s')
    
    fig = plt.figure(figsize=(10,5))
    ax1 = fig.add_subplot(121)
    ax2 = fig.add_subplot(122)
    colors = ['b','g','r','y','g','r','k']
    ax1.set_title('NO_GMM')
    ax2.set_title('GMM')
    plt.xlabel('H')
    plt.ylabel('L')
    for i in range(7):
        ax1.scatter(x=data_deal_index6[:,0][acgtIndex[:,0] == i],y=data_deal_index6[:,1][acgtIndex[:,0] == i],s = 0.0005,c = colors[i])
        ax2.scatter(x=data_deal_index6[:,0][np.argmax(W,axis=1) == i],y=data_deal_index6[:,1][np.argmax(W,axis=1) == i],s = 0.0005,c = colors[i])
    plt.show()


   