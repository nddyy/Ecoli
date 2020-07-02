import numpy as np
np.set_printoptions(suppress=True)
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse


def acbi_hist(acbi):

    p1,p99 =  np.percentile(np.sort(acbi),(1,99))
    p1_p99_acbi = np.sort(acbi[np.where((acbi >= p1) & (acbi <= p99))])
    # print(p1_p99_acbi)
    # print(p99)
    # plt.rcParams['font.family']='SimHei'
    # plt.rcParams['font.size']=20
    # plt.axis([0,0.2,0,2000])
    n, bins_limits, patches = plt.hist(p1_p99_acbi,bins=300,color='k')
    print(np.array(patches))
    # np.savetxt('patches.txt',patches)
    # print(bins_limits)
    # plt.show()