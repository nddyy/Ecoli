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

FOV_C = 4  
FOV_R = 5  
# split_FOV

image_r = signalH1.shape[0]
image_c = signalH1.shape[1]
fov_r_num = np.zeros(FOV_R)
fov_c_num = np.zeros(FOV_C)
fov_r_single_num = int(image_r / FOV_R)
fov_c_single_num = int(image_c / FOV_C)
fov_r_num_ex = image_r % FOV_R
fov_c_num_ex = image_c % FOV_C
fov_r_num = fov_r_num + fov_r_single_num
fov_c_num = fov_c_num + fov_c_single_num
for i in range(fov_r_num_ex):
    fov_r_num[i] = fov_r_num[i] + 1
for i in range(fov_c_num_ex):
    fov_c_num[i] = fov_c_num[i] + 1

fov_r_limits = fov_r_num.copy()
fov_c_limits = fov_c_num.copy()

fov_r_limits = np.insert(fov_r_limits,0,0)
fov_c_limits = np.insert(fov_c_limits,0,0)

for i in range(FOV_C):
    fov_c_limits[i+1] = fov_c_limits[i+1] + fov_c_limits[i] 
for i in range(FOV_R):
    fov_r_limits[i+1] = fov_r_limits[i+1] + fov_r_limits[i] 

print(fov_c_limits)
print(fov_r_limits)



