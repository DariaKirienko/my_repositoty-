
import pandas as pd
import scipy.stats as stats
import statsmodels.stats.multitest as smt


cmv = pd.read_csv('D:\coder\M_projects_Python\Mikhail_Shugai\cmv_clones_.txt', sep=',')
cmv.columns = ['cdr3aa','f+CMV-', 'n_f+CMV-', 'f+CMV+', 'n_f+CMV+' ]
cmv = cmv.set_index('cdr3aa')


cdr3 = list(cmv.index) 


df_col = [0]*len(cdr3)
df_pv = pd.DataFrame({'odds_ratio' : df_col, 'p-value' : df_col, 'p-value_adjust' : df_col}, index = cdr3)


for item in cdr3:                                                              #Odds ratio, Fisher test
    a =  cmv.loc[item, 'f+CMV+']
    b = cmv.loc[item, 'f+CMV-']
    c = cmv.loc[item, 'n_f+CMV+']
    d = cmv.loc[item, 'n_f+CMV-']
    lst = [[a,b],[c,d]]
    oddsratio, pvalue = stats.fisher_exact(lst)
    df_pv.loc[item, 'odds_ratio'] = oddsratio
    df_pv.loc[item, 'p-value'] =  pvalue

  


df = df_pv.drop(df_pv[df_pv.odds_ratio < 1.1].index)                           #Drop Oddds ratio < 1.1


r, pc, aS, aB =  smt.multipletests(list(df['p-value']), alpha=0.05,            #p-value adjustment
         method='fdr_bh', is_sorted=False, returnsorted=False)  
df['p-value_adjust'] = pc


df_finish = df.sort_values('p-value', kind='mergesort')
df_finish.index.name = 'cdr3aa'
#df_finish = df_finish.round(8)
#df_finish = df_finish.set_index('cdr3aa')

#df_finish.to_csv('cmv_pv(2).txt')


print('Whoaaaaa!')
