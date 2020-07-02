import numpy as np
np.set_printoptions(suppress=True)
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse


def acbi_hist(acbi):
    # 用acbi的p1到p99的数据进行300段的hist计算
    # frequency：分组区间对应的频率，也就是每个分组中有多少个数据
    # bins_limits：分组时的分隔值，也就是每组的左右边界线,有bins+1个值
    # patches：直方图中列表对象 

    p1,p99 =  np.percentile(np.sort(acbi),(1,99))
    p1_p99_acbi = np.sort(acbi[np.where((acbi >= p1) & (acbi <= p99))])
    plt.axis([0,0.2,0,3])
    frequency,bins_limits,patches = plt.hist(p1_p99_acbi,bins=300,density=1)
    plt.show()

    return frequency,bins_limits,patches