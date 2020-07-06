import numpy as np
np.set_printoptions(suppress=True)
np.seterr(divide='ignore',invalid='ignore')
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import scipy.io as scio

FOV_C = 4  
FOV_R = 5  
CYCLE_NUM = 1
FOV_NUM = FOV_C * FOV_R


def data_pre_deal(signalH,signalL,acgtIndex):
    # 把存放H通道和L通道亮度值的 N * M 的数组拼接成 DNB_num * 2 的二维数组
    # 把存放acgt标签的 N * M 的数组变形为 DNB_num * 1 的二维数组
    
    signalH = np.reshape(signalH,[-1,1])
    signalL = np.reshape(signalL,(-1,1))
    acgtIndex = np.reshape(acgtIndex,(-1,1))
    signal_H_L = np.stack((signalH[:,0],signalL[:,0]),axis=1)

    return signal_H_L,acgtIndex


def split_fov(image_c_num,image_r_num):
    # 将image划分为 FOV_X * FOV_Y 个FOV
    # 返回值为每个FOV的左右分界线，以便在原image二维数组上切片

    fov_c_num = np.zeros(FOV_C)
    fov_r_num = np.zeros(FOV_R)
    fov_c_single_num = int(image_c_num / FOV_C)
    fov_r_single_num = int(image_r_num / FOV_R)
    fov_c_num_ex = image_c_num % FOV_C
    fov_r_num_ex = image_r_num % FOV_R
    fov_c_num = fov_c_num + fov_c_single_num
    fov_r_num = fov_r_num + fov_r_single_num
    for i in range(fov_c_num_ex):
        fov_c_num[i] = fov_c_num[i] + 1
    for i in range(fov_r_num_ex):
        fov_r_num[i] = fov_r_num[i] + 1

    fov_c_limits = fov_c_num.copy()
    fov_r_limits = fov_r_num.copy()
    fov_c_limits = np.insert(fov_c_limits,0,0)
    fov_r_limits = np.insert(fov_r_limits,0,0)
    for i in range(FOV_C):
        fov_c_limits[i+1] = fov_c_limits[i+1] + fov_c_limits[i] 
    for i in range(FOV_R):
        fov_r_limits[i+1] = fov_r_limits[i+1] + fov_r_limits[i] 
    
    return fov_c_num,fov_r_num,fov_c_limits,fov_r_limits


def ints_Q_normal(data_after_pre_call,acgtIndex,index,H_or_L):
    # 对想处理的N碱基的H or L通道的亮度值以及Q值进行归一化
    # index 代表碱基N： G = 0, A = 1, T = 2, C = 3
    # H_or_L： H通道 = 0, L通道 = 1
    # Q值： 容量为4的一维数组，为通道亮度值排序后的四分位点
    
    q = np.percentile(np.sort(data_after_pre_call[:,H_or_L][acgtIndex[:,0] == index]),(25,50,75))
    q4 = q[2] + 3*(q[2] - q[0])
    q = np.append(q,q4)
    nor_ints = data_after_pre_call[:,H_or_L][acgtIndex[:,0] == index]/q[1]
    nor_q = q/q[1]

    return nor_ints,nor_q


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



if __name__ == "__main__":

    data_path = 'F://wd/Ecoli/1.mat'
    data = scio.loadmat(data_path)

    dataH_image = data.get('dataH')
    dataL_image = data.get('dataL')
    acgtIndex_image = data.get('acgtIndex1')

    acbi = np.zeros([acgtIndex_image.shape[0],acgtIndex_image.shape[1]])
    validDNB = np.ones([acgtIndex_image.shape[0],acgtIndex_image.shape[1]])

    for i in range(FOV_NUM):

        fov_c_num,fov_r_num,fov_c_limits,fov_r_limits = split_fov(dataH_image.shape[1],dataH_image.shape[0])
        
        r_seq = int(i / FOV_C)     # 确定该FOV在几行几列
        c_seq = int(i % FOV_C)
       
        dataH_image_copy = dataH_image.copy()
        dataL_image_copy = dataL_image.copy()
        acgtIndex_image_copy = acgtIndex_image.copy()
        dataH_slice = dataH_image_copy[int(fov_r_limits[r_seq]):int(fov_r_limits[r_seq + 1]),int(fov_c_limits[c_seq]):int(fov_c_limits[c_seq + 1])]      # 将原图的H,L通道值以及acgt标签切片成20个FOV
        dataL_slice = dataL_image_copy[int(fov_r_limits[r_seq]):int(fov_r_limits[r_seq + 1]),int(fov_c_limits[c_seq]):int(fov_c_limits[c_seq + 1])]
        acgtIndex_slice = acgtIndex_image_copy[int(fov_r_limits[r_seq]):int(fov_r_limits[r_seq + 1]),int(fov_c_limits[c_seq]):int(fov_c_limits[c_seq + 1])]
        
        data_H_L,acgtIndex = data_pre_deal(dataH_slice,dataL_slice,acgtIndex_slice)

        q_mean = np.zeros(4)
        count = np.zeros(acgtIndex.shape[0])
        acbi_fov = np.zeros(acgtIndex.shape[0])
        validDNB_fov = np.ones(acgtIndex.shape[0])
        
        for j in range(CYCLE_NUM):
            # 调用pre_call

            nor_ints_T,nor_q_T = ints_Q_normal(data_H_L,acgtIndex,2,0)   # 获得T碱基的H通道的Q值
            nor_ints_A,nor_q_A = ints_Q_normal(data_H_L,acgtIndex,1,1)   # 获得A碱基的L通道的Q值
            q_mean = q_mean + nor_q_T + nor_q_A        # 累加所有cycle的碱基T的H通道和碱基A的L通道的Q值，最后得到Q1,Q2,Q3和Q4四个值。循环结束后会将Q值除以cycle_num进行归一化
            count = count + np.where(acgtIndex[:,0] == 2,1,0) + np.where(acgtIndex[:,0] == 1,1,0)       # 累加所有cycle上的A碱基的L通道的值和T碱基的H通道的值，得到ACBI（size为DNB个数），并记录累加的点的个数为count
            acbi_fov = acbi_fov + data_H_L[:,0] * np.where(acgtIndex[:,0] == 2,1,0) + data_H_L[:,1] * np.where(acgtIndex[:,0] == 1,1,0)
            
        q_mean = q_mean/CYCLE_NUM
        acbi_fov = acbi_fov/count            # 如果count = 0，则validDNB = false，如果count != 0，则计算ACBI= ACBI/count；
        acbi_fov[np.isnan(acbi_fov)] = 0
        acbi_fov[np.where(acbi_fov > q_mean[3])] = 0       
        validDNB_fov[acbi_fov == 0] = 0        # 如果ACBI > Q4，则validDNB = false
        acbi_re = acbi_fov.reshape([int(fov_r_num[r_seq]),int(fov_c_num[c_seq])])                # 将acbi_fov和validDNB_fov reshape为原本形状,并更新acbi和validDNB
        validDNB_re = validDNB_fov.reshape([int(fov_r_num[r_seq]),int(fov_c_num[c_seq])])        
        acbi[int(fov_r_limits[r_seq]):int(fov_r_limits[r_seq + 1]),int(fov_c_limits[c_seq]):int(fov_c_limits[c_seq + 1])] = acbi_re
        validDNB[int(fov_r_limits[r_seq]):int(fov_r_limits[r_seq + 1]),int(fov_c_limits[c_seq]):int(fov_c_limits[c_seq + 1])] = validDNB_re

    print(acbi.shape)
    print(validDNB.shape)

        # frequency,bins_limits,patches = acbi_hist(acbi)     # hist处理

    


