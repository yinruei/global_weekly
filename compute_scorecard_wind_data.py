import numpy as np
import pandas as pd

def compute_conflimit(std):
    # if(nsz>=80);            'define intvl=1.960*std/sqrt(nsz-1)'  ;endif
    # if(nsz>=40 & nsz <80);  'define intvl=2.000*std/sqrt(nsz-1)'  ;endif
    # if(nsz>=20 & nsz <40);  'define intvl=2.042*std/sqrt(nsz-1)'  ;endif
    # if(nsz<20);             'define intvl=2.228*std/sqrt(nsz-1)'  ;endif
    nsz = 30
    if nsz > 80:
        intvl = 1.960*std/np.sqrt(nsz-1)
    elif nsz >= 40 & nsz <80 :
        intvl = 2.000*std/np.sqrt(nsz-1)
    elif nsz >= 20 & nsz < 40:
        intvl = 2.042*std/np.sqrt(nsz-1)
    elif nsz < 20:
        intvl = 2.228*std/np.sqrt(nsz-1)

    return intvl

def compute_windspeed_rmse_weekly_score(df):
    # 計算rmse
    # RMSE:  rmse = sqrt( X6 + X7 - 2*X5 )
    df['rmse'] = np.sqrt(df['uf2_vf2'] + df['ua2_va2'] - 2*df['ufua_vfva'])
    # 為了乾淨，清掉不需要的欄位
    # print('df-->', df)
    df = df.drop(columns=['model2', 'grid', 'version', 'resolution', 'anomaly', 'variable', 'level', 'grid','uf', 'vf', 'ua', 'va', 'ufua_vfva', 'uf2_vf2', 'ua2_va2'])
    # print('before df', df)
    # 先篩出符合第一週的值
    df_week1 = df[(df['tau'] < 168)]
    # 將篩出來的值 用groupby將model1跟init_time分群 算出第一週rmse的平均
    week = df_week1.groupby(['model1', 'init_time'])[['rmse']].mean()
    
    # print(df_week1)
    week.insert(1, 'week1', week)
    # 再篩出符合第二週的值
    df_week2 = df[ (df['tau'] >= 168)  & (df['tau'] < 336 ) ]
    week2 = df_week2.groupby(['model1', 'init_time'])[['rmse']].mean()
    week.insert(2, 'week2', week2)
    # 刪掉rmse欄位，week1, week2都是rmse的值了
    week = week.drop(columns=['rmse'])

    # 攤平column 值
    week = week.reset_index()
    week1_avg = week.groupby(['model1'])['week1'].mean()
    week1_std = week.groupby(['model1'])['week1'].std()

    week2_avg = week.groupby(['model1'])['week2'].mean()
    week2_std = week.groupby(['model1'])['week2'].std()

    week_std = [week1_std, week2_std]
    conflimit = []
    for std in week_std:
        conflimit.append(compute_conflimit(std))

    return week1_avg, week2_avg, conflimit[0], conflimit[1]

def compute_windspeed_bias_weekly_score(df):
    # df = read_file(FILENAME)
    # 計算bias
    #  Mean biases: sqrt[ X6 ] - sqrt[ X7 ]
    df['bias'] = df['uf2_vf2'] - df['ua2_va2']
    # 為了乾淨，清掉不需要的欄位
    df = df.drop(columns=['model2', 'grid', 'version', 'resolution', 'anomaly', 'variable', 'level', 'grid', 'uf', 'vf', 'ua', 'va', 'ufua_vfva', 'uf2_vf2', 'ua2_va2'])
    # print('before df', df)
    # 先篩出符合第一週的值
    df_week1 = df[(df['tau'] < 168)]
    # 將篩出來的值 用groupby將model1跟init_time分群 算出第一週bias的平均
    week = df_week1.groupby(['model1', 'init_time'])[['bias']].mean()
    # print(df_week1)
    week.insert(1, 'week1', week)
    # 再篩出符合第二週的值
    df_week2 = df[ (df['tau'] >= 168)  & (df['tau'] < 336 ) ]
    week2 = df_week2.groupby(['model1', 'init_time'])[['bias']].mean()
    week.insert(2, 'week2', week2)
    # 刪掉bias欄位，week1, week2都是bias的值了
    week = week.drop(columns=['bias'])

    # 攤平column 值
    week = week.reset_index()
    # print(week)
    week1_avg = week.groupby(['model1'])['week1'].mean()
    week1_std = week.groupby(['model1'])['week1'].std()
    week2_avg = week.groupby(['model1'])['week2'].mean()
    week2_std = week.groupby(['model1'])['week2'].std()

    week_std = [week1_std, week2_std]
    conflimit = []
    for std in week_std:
        conflimit.append(compute_conflimit(std))

    return week1_avg, week2_avg, conflimit[0], conflimit[1]

def compute_windspeed_pco_weekly_score(df):
    # df = read_file(FILENAME)
    #  Pattern correlation: R=( X5 - X1*X3 - X2*X4 ) / sqrt{var(V_f)*var(V_a)}
    #    where var(V_f)=( X6 - X1*X1 - X2*X2 )
    #          var(V_a)=( X7 - X3*X3 - X4*X4 )
    #          V_f and V_a are vector winds, V_f=uf(i)+vf(j), V_a=ua(i)+va(j).
    df['pco'] = ( df['ufua_vfva'] -  ( df['uf'] * df['ua'] - df['vf'] * df['va']) ) /  np.sqrt( ( df['uf2_vf2'] - df['uf']**2 - df['uf']**2 )  * ( df['ua2_va2'] - df['ua']** 2 - df['va']** 2 ) ) 
    # 為了乾淨，清掉不需要的欄位
    df = df.drop(columns=['model2', 'grid', 'version', 'resolution', 'anomaly', 'variable', 'level', 'grid', 'uf', 'vf', 'ua', 'va', 'ufua_vfva', 'uf2_vf2', 'ua2_va2'])
    # print('before df', df)
    # 先篩出符合第一週的值
    df_week1 = df[(df['tau'] < 168)]
    # 將篩出來的值 用groupby將model1跟init_time分群 算出第一週pco的平均
    week = df_week1.groupby(['model1', 'init_time'])[['pco']].mean()
    # print(df_week1)
    week.insert(1, 'week1', week)
    # 再篩出符合第二週的值
    df_week2 = df[ (df['tau'] >= 168)  & (df['tau'] < 336 ) ]
    week2 = df_week2.groupby(['model1', 'init_time'])[['pco']].mean()
    week.insert(2, 'week2', week2)
    # 刪掉rmse欄位，week1, pco
    week = week.drop(columns=['pco'])

    # 攤平column 值
    week = week.reset_index()
    # print('week1', week.groupby(['model1'])['week1'].mean())
    # print('week2', week.groupby(['model1'])['week2'].mean())
    week1_avg = week.groupby(['model1'])['week1'].mean()
    week1_std = week.groupby(['model1'])['week1'].std()

    week2_avg = week.groupby(['model1'])['week2'].mean()
    week2_std = week.groupby(['model1'])['week2'].std()

    week_std = [week1_std, week2_std]
    conflimit = []
    for std in week_std:
        conflimit.append(compute_conflimit(std))

    return week1_avg, week2_avg, conflimit[0], conflimit[1]