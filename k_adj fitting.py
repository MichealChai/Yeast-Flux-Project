import matplotlib.pyplot as plt
import numpy as np
import math
import pandas as pd 
from scipy.optimize import curve_fit

# 获取当前工作目录
#current_dir = os.getcwd()
#print("当前工作目录：", current_dir)

# 设置当前工作目录
#new_dir = "D:\Desktop\code\Python"
#os.chdir(new_dir)

# 再次获取当前工作目录
#updated_dir = os.getcwd()
#print("更新后的工作目录：", updated_dir)

#定义函数,T为Total
def func1(x,k1):
    return (1-(math.e)**(-k1*x))

def func2(x,k1,k2):
    return (1+k2/(k1-k2)*(math.e)**(-k1*x)-k1/(k1-k2)*(math.e)**(-k2*x))

#将数据放于fitting.csv文件中
data = pd.read_csv(r'k_value_fitting.csv')

#读取表头
head = data.columns.values.tolist()
#print(head)

#忽略除以0的警告
np.seterr(divide='ignore', invalid='ignore')

n = 3           #每组平行的数量
m = 1
col = 0         #计数，有多少代谢物
len_col = len(data.iloc[0])         #读取有多少列
ms_mtx = pd.DataFrame()
column = []
while m < len_col:
    if m % n == 1:
        mean = pd.DataFrame(np.mean(data.iloc[:,m:m+3] , axis= 1))      #平均值计算
        std = pd.DataFrame(np.std(data.iloc[:,m:m+3] , axis=1))         #标准差计算
        column.append((head[m] , "mean"))
        column.append((head[m] , "std"))
        mtx = pd.concat([mean , std] , axis = 1)
        ms_mtx = pd.concat([ms_mtx , mtx] , axis = 1)
        col += 1
    m += 1
ms_mtx.columns = pd.MultiIndex.from_tuples(column)
ms_mtx.insert(loc=0, column='time(h)', value=data.iloc[:,0])            #插入时间x轴
outputpath = 'result_mean_std.csv'
ms_mtx.to_csv(outputpath , sep=',' , index=True,header=True)

x = np.append(np.arange(0.001 , 0.5 , 0.01) , np.arange(0.6 , 12 , 0.1))
i = 1
time_len = len(ms_mtx.iloc[:,0])     #读取时间点数量
time_n = np.arange(1,time_len)
k_value = pd.DataFrame()
head_m_s = ms_mtx.columns.values.tolist()
head_m_s = np.array(head_m_s)
head_k = []
while i < col+1:
    popt1, pcov1 = curve_fit(func1, ms_mtx['time(h)'] , ms_mtx.iloc[:,2*i-1] , maxfev = 1000000 , method = 'lm')       #拟合参数,pcov对角线上元素为对应参数方差，最大调用数改为1000000
    bounds = ([popt1[0] , 0] , [popt1[0]+0.00001 , np.inf])                                                            #固定上游代谢物的k value,并用其计算下游代谢物的k value
    popt2, pcov2 = curve_fit(func1, ms_mtx['time(h)'] , ms_mtx.iloc[:,2*i+1] , maxfev = 1000000 , method = 'lm')
    popt3, pcov3 = curve_fit(func2, ms_mtx['time(h)'] , ms_mtx.iloc[:,2*i+1] , bounds = bounds , maxfev = 1000000)
    calc = pd.DataFrame([popt1[0] , popt2[0] , popt3[1]])
    head_k.append((head_m_s[2*i-1,0] , head_m_s[2*i+1,0]))
    k_value = pd.concat([k_value , calc] , axis = 1)
    i += 2
k_value.columns = pd.MultiIndex.from_tuples(head_k)
k_value.rename(index={0:"k_for" , 1:"k_lat_ori" , 2:"k_lat_cor"} , inplace = True)              #k_for:k_value_former   k_lat_ori:k_value_latter_original   k_lat_cor:k_value_latter_correctional
k_value.to_csv('real_k_value.csv' , sep=',' , index=True,header=True)
