import pandas as pd
import os 
from collections import Counter 


public = pd.read_csv('D:\coder\M_projects_Python\Mikhail_Shugai\public_clones.txt', sep='\t', index_col = False)
met_data = pd.read_csv('D:\coder\M_projects_Python\Mikhail_Shugai\metadata.txt', sep='\t', index_col = False)

pub_lst = list(public['cdr3aa'])
met_dict = dict(zip(list(met_data['file_name']), list(met_data['cmv'])))

def read_col(file, n):                                                         #открывает файл, генерирует список из данных n-ого столбца    
    result = []                                     
    with open(file) as infile:
        for line in infile:
            result.append((line.split()[n]))
    return result        

f_plus = []
f_min = []
nf_plus = []
nf_min = []
    

def IntersLst(first, second):                                                   #возвращиет пересечение двух списков
    in_lst =  list(set(first) & set(second))
    return in_lst

def DifLst(first, second):                                                     #разница двух списков
    dif_lst = list(set(first) - set(second))
    return dif_lst
    
for filename in os.listdir():
    sample = read_col(filename, 3)
    found = IntersLst(pub_lst, sample)
    not_found = DifLst(pub_lst, found)            
    if met_dict[os.path.basename(filename)]== '+':
        f_plus.extend(found)
        nf_plus.extend(not_found)
    elif met_dict[os.path.basename(filename)]== '-':
        f_min.extend(found) 
        nf_min.extend(not_found)
             
     
pub_dict = dict(zip(pub_lst, [0]*len(pub_lst)))
f_plus_d = { **pub_dict, **Counter(f_plus)}
f_min_d = { **pub_dict, **Counter(f_min)}
nf_plus_d = { **pub_dict, **Counter(nf_plus)}
nf_min_d  = { **pub_dict, **Counter(nf_min)}       

fmin, nfmin, fplus, nfplus = pd.Series(f_min_d), pd.Series(nf_min_d), pd.Series(f_plus_d), pd.Series(nf_plus_d)    

df = pd.concat([fmin.rename('fmin'), nfmin.rename('nfmin'), fplus.rename('fplus'), nfplus.rename('nfplus')], axis = 1)
df = df.rename_axis('cdr3aa')
df.to_csv('cmv_clones_.txt')















    
