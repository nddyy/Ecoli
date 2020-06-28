import numpy as np
import matplotlib.pyplot as plt
import scipy.io as scio
import get_miu_sigma_alpha
import E_step


if __name__ == '__main__':
    
    # 输入为三个 N X M 的ndarray，分别为 signalH,signalL,acgtIndex

    # miu,sigma_square,alpha = get_miu_sigma_alpha.get_miu_sigma_alpha(signalH,signalL,acgtIndex)
    # # print(miu,'\n',sigma_square,'\n',alpha)

    # acgt_data = np.stack((signalH.ravel(),signalL.ravel()),axis=1)

    # W = E_step.update_W(acgt_data,miu,sigma_square,alpha)

    # print(W)