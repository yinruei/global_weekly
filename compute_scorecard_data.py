import os
import pandas as pd
import numpy as np
from compute_scorecard_wind_data import compute_windspeed_rmse_weekly_score, compute_windspeed_bias_weekly_score, compute_windspeed_pco_weekly_score
# FILENAME = 'HGT_P500_G2_2021102420211123.txt'
# 設定螢幕輸出格式
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', None)

# region
regions = ['G2', 'G2ASI', 'G2NHX', 'G2SHX', 'G2PNA', 'G2TRO']
# week
week = ['week1', 'week2']
# statistic name
cor_name = 'Anomaly Correlation'
rms_name = 'RMSE'
bias_name = 'Bias'

# vaiable name
cor_var = ['HGT', 'WIND', 'T', 'PMSL']
rms_var = ['HGT', 'WIND', 'T']
# rms_var = ['HGT', 'WIND', 'PMSL']
bias_var = ['HGT', 'WIND', 'PMSL']

# cor vaiable level
cor_HGT_level = ['P250', 'P500']
cor_T_level = ['P250', 'P500', 'P850']
# cor_U_level = ['P250', 'P500', 'P850']
# cor_V_level = ['P250', 'P500', 'P850']
cor_WIND_level = ['P250', 'P500', 'P850']
cor_PMSL_level = ['MSL']

# rms vaiable level
rms_HGT_level=['P250', 'P500']
# rms_U_level = ['P250', 'P500', 'P850']
# rms_V_level = ['P250', 'P500', 'P850']
rms_WIND_level=['P250', 'P500', 'P850']
rms_T_level=['P250', 'P500', 'P850']
rms_PMSL_level = ['MSL']

# bias vaiable level
bias_HGT_level=['P250', 'P500']
bias_WIND_level=['P250', 'P500', 'P850']
bias_T_level=['P250', 'P500', 'P850']
bias_PMSL_level = ['MSL']

start_time = '20211024'
end_time = '20211123'

def get_week():
    return week

def get_region():
    return regions

def read_file(FILENAME):
    # 讀取txt檔
    # print('FILENAME--->', FILENAME)
    df = pd.read_csv(FILENAME, sep="\s+", header=None, dtype=str)
    df = pd.DataFrame(df)
    # 刪除等號欄位
    del df[9]
    # 重新設定欄位名稱
    df.columns = ['version', 'model1', 'tau', 'valid_time', 'model2', 'resolution', 'anomaly', 'variable', 'level', 'grid', 'f', 'a', 'fa', 'f2', 'a2']
    # 去掉nan的資料
    df.dropna(axis=0, how='any', inplace=True)
    # 轉換成時間格式，進一步去計算init_time
    df['valid_time'] = pd.to_datetime(df['valid_time'], format='%Y%m%d%H')
    init_time = df['valid_time'] - pd.to_timedelta(df['tau'].astype(int), unit='hr')
    # 建立init_time欄位，將init_time insert進去
    df.insert(3, 'init_time', init_time)
    # 把所有可能需要計算的欄位資料型別改成數值型別才能計算
    df['tau'] = pd.to_numeric(df['tau'])
    df['f'] = pd.to_numeric(df['f'])
    df['a'] = pd.to_numeric(df['a'])
    df['fa'] = pd.to_numeric(df['fa'])
    df['f2'] = pd.to_numeric(df['f2'])
    df['a2'] = pd.to_numeric(df['a2'])

    return df

def read_wind_file(FILENAME):
    # 讀取txt檔
    # print('FILENAME--->', FILENAME)
    df = pd.read_csv(FILENAME, sep="\s+", header=None, dtype=str)
    df = pd.DataFrame(df)
    # 刪除等號欄位
    del df[9]
    # 重新設定欄位名稱
    df.columns = ['version', 'model1', 'tau', 'valid_time', 'model2', 'resolution', 'anomaly', 'variable', 'level', 'grid', 'uf', 'vf', 'ua', 'va', 'ufua_vfva', 'uf2_vf2', 'ua2_va2']
    # 去掉nan的資料
    df.dropna(axis=0, how='any', inplace=True)
    # 轉換成時間格式，進一步去計算init_time
    df['valid_time'] = pd.to_datetime(df['valid_time'], format='%Y%m%d%H')
    init_time = df['valid_time'] - pd.to_timedelta(df['tau'].astype(int), unit='hr')
    # 建立init_time欄位，將init_time insert進去
    df.insert(3, 'init_time', init_time)
    # 把所有可能需要計算的欄位資料型別改成數值型別才能計算
    df['tau'] = pd.to_numeric(df['tau'])
    df['uf'] = pd.to_numeric(df['uf'])
    df['vf'] = pd.to_numeric(df['vf'])
    df['ua'] = pd.to_numeric(df['ua'])
    df['va'] = pd.to_numeric(df['va'])
    df['ufua_vfva'] = pd.to_numeric(df['ufua_vfva'])
    df['uf2_vf2'] = pd.to_numeric(df['uf2_vf2'])
    df['ua2_va2'] = pd.to_numeric(df['ua2_va2'])

    return df

def compute_rms_week_ds(week1_avg, week2_avg, conflimit1, conflimit2, model1, model2):
    alpha1, alpha2, alpha3 = confidence_level()
    # 第一週的rms ds ds95 ds99 ds999
    ds = ( week1_avg[model1] - week1_avg[model2] ) / conflimit1[model1]
    ds95 = ds
    ds99 = ds * alpha1 / alpha2
    ds999 = ds * alpha1 / alpha3
    ds95 = round(ds95, 4)
    ds99 = round(ds99, 4)
    ds999 = round(ds999, 4)
    week1 = (ds95, ds99, ds999)

    # 第二週的rms ds ds95 ds99 ds999
    ds = ( week2_avg[model1] - week2_avg[model2] ) / conflimit2[model1]
    ds95 = ds
    ds99 = ds * alpha1 / alpha2
    ds999 = ds * alpha1 / alpha3
    ds95 = round(ds95, 4)
    ds99 = round(ds99, 4)
    ds999 = round(ds999, 4)
    week2 = (ds95, ds99, ds999)

    week = [week1, week2]

    return week

def compute_pco_week_ds(week1_avg, week2_avg, conflimit1, conflimit2, model1, model2):
    alpha1, alpha2, alpha3 = confidence_level()
    # 第一週的pco ds ds95 ds99 ds999
    ds = ( week1_avg[model2] - week1_avg[model1] ) / conflimit1[model1]
    ds95 = ds
    ds99 = ds * alpha1 / alpha2
    ds999 = ds * alpha1 / alpha3
    ds95 = round(ds95, 4)
    ds99 = round(ds99, 4)
    ds999 = round(ds999, 4)
    # print('--->', (ds95, ds99, ds999))
    week1 = (ds95, ds99, ds999)

    # 第二週的pco ds ds95 ds99 ds999
    ds = ( week2_avg[model2] - week2_avg[model1] ) / conflimit2[model1]
    ds95 = ds
    ds99 = ds * alpha1 / alpha2
    ds999 = ds * alpha1 / alpha3
    ds95 = round(ds95, 4)
    ds99 = round(ds99, 4)
    ds999 = round(ds999, 4)
    week2 = (ds95, ds99, ds999)

    week = [week1, week2]

    return week

def compute_bias_week_ds(week1_avg, week2_avg, conflimit1, conflimit2, model1, model2):
    alpha1, alpha2, alpha3 = confidence_level()
    # 第一週的bias ds ds95 ds99 ds999
    # 計算bias特別要注意
    # let ds="abs($score1 - $score2) / $conf1"
    # let sss="(abs($score1) - abs($score2))"
    # if (( $sss <  0 )); then let ds="-$ds"; fi
    ds = ( abs(week1_avg[model1] - week1_avg[model2] )) / conflimit1[model1]
    sss = (abs(week1_avg[model1]) - abs(week1_avg[model2]))
    if sss < 0 :
        ds = -ds
    ds95 = ds
    ds99 = ds * alpha1 / alpha2
    ds999 = ds * alpha1 / alpha3
    ds95 = round(ds95, 4)
    ds99 = round(ds99, 4)
    ds999 = round(ds999, 4)
    # print('--->', (ds95, ds99, ds999))
    week1 = (ds95, ds99, ds999)

    # 第二週的bias ds ds95 ds99 ds999
    # 計算bias特別要注意
    # let ds="abs($score1 - $score2) / $conf1"
    # let sss="(abs($score1) - abs($score2))"
    # if (( $sss <  0 )); then let ds="-$ds"; fi
    ds = ( abs(week2_avg[model1] - week2_avg[model2] )) / conflimit2[model1]
    sss = (abs(week2_avg[model1]) - abs(week1_avg[model2]))
    if sss < 0 :
        ds = -ds
    ds95 = ds
    ds99 = ds * alpha1 / alpha2
    ds999 = ds * alpha1 / alpha3
    ds95 = round(ds95, 4)
    ds99 = round(ds99, 4)
    ds999 = round(ds999, 4)
    week2 = (ds95, ds99, ds999)

    week = [week1, week2]

    return week

def convert_rmse_weekly_score(model1, model2):
    data_list = []
    for rms in rms_var:
        if rms == 'HGT':
            for HGT_level in rms_HGT_level:
                for region in regions:
                    filename = f'{rms}_{HGT_level}_{region}_{start_time}{end_time}.txt'
                    df = read_file(filename)
                    week1_avg, week2_avg, conflimit1, conflimit2 = compute_rmse_weekly_score(df)
                    week = compute_rms_week_ds(week1_avg, week2_avg, conflimit1, conflimit2, model1, model2)
                    data_list.append({
                        f'{rms}_{HGT_level}':  week,
                    })

        elif rms == 'T':
            for T_level in rms_T_level:
                for region in regions:
                    filename = f'{rms}_{T_level}_{region}_{start_time}{end_time}.txt'
                    df = read_file(filename)
                    week1_avg, week2_avg, conflimit1, conflimit2 = compute_rmse_weekly_score(df)
                    week = compute_rms_week_ds(week1_avg, week2_avg, conflimit1, conflimit2, model1, model2)
                    data_list.append({
                        f'{rms}_{T_level}':  week,
                    })
        elif rms == 'WIND':
            # WIND 的txt內容跟其他的格式不同要注意!!!!
            for WIND_level in rms_WIND_level:
                for region in regions:
                    filename = f'{rms}_{WIND_level}_{region}_{start_time}{end_time}.txt'
                    # wind讀檔方式不同須注意
                    df = read_wind_file(filename)
                    # wind計算方式不同須注意
                    week1_avg, week2_avg, conflimit1, conflimit2 = compute_windspeed_rmse_weekly_score(df)
                    week = compute_rms_week_ds(week1_avg, week2_avg, conflimit1, conflimit2, model1, model2)
                    data_list.append({
                        f'{rms}_{WIND_level}':  week,
                    })
    print('rmse data_list-->', data_list)

    return data_list
    
def convert_pco_weekly_score(model1, model2):
    data_list = []
    for cor in cor_var:
        if cor == 'HGT':
            for HGT_level in cor_HGT_level:
                for region in regions:
                    filename = f'{cor}_{HGT_level}_{region}_{start_time}{end_time}.txt'
                    df = read_file(filename)
                    week1_avg, week2_avg, conflimit1, conflimit2 = compute_pco_weekly_score(df)
                    week = compute_pco_week_ds(week1_avg, week2_avg, conflimit1, conflimit2, model1, model2)
                    data_list.append({
                        f'{cor}_{HGT_level}':  week,
                    })

        elif cor == 'T':
            for T_level in cor_T_level:
                for region in regions:
                    filename = f'{cor}_{T_level}_{region}_{start_time}{end_time}.txt'
                    df = read_file(filename)
                    week1_avg, week2_avg, conflimit1, conflimit2 = compute_pco_weekly_score(df)
                    week = compute_pco_week_ds(week1_avg, week2_avg, conflimit1, conflimit2, model1, model2)
                    data_list.append({
                        f'{cor}_{T_level}':  week,
                    })

        elif cor == 'U':
            for U_level in cor_U_level:
                for region in regions:
                    filename = f'{cor}_{U_level}_{region}_{start_time}{end_time}.txt'
                    df = read_file(filename)
                    week1_avg, week2_avg, conflimit1, conflimit2 = compute_pco_weekly_score(df)
                    week = compute_pco_week_ds(week1_avg, week2_avg, conflimit1, conflimit2, model1, model2)
                    data_list.append({
                        f'{cor}_{U_level}':  week,
                    })
        elif cor == 'V':
            for V_level in cor_V_level:
                for region in regions:
                    filename = f'{cor}_{V_level}_{region}_{start_time}{end_time}.txt'
                    df = read_file(filename)
                    week1_avg, week2_avg, conflimit1, conflimit2 = compute_pco_weekly_score(df)
                    week = compute_pco_week_ds(week1_avg, week2_avg, conflimit1, conflimit2, model1, model2)
                    data_list.append({
                        f'{cor}_{V_level}':  week,
                    })          
        elif cor == 'PMSL':
            for PMSL_level in cor_PMSL_level:
                for region in regions:
                    filename = f'{cor}_{PMSL_level}_{region}_{start_time}{end_time}.txt'
                    df = read_file(filename)
                    week1_avg, week2_avg, conflimit1, conflimit2 = compute_pco_weekly_score(df)
                    week = compute_pco_week_ds(week1_avg, week2_avg, conflimit1, conflimit2, model1, model2)
                    data_list.append({
                        f'{PMSL_level}P':  week,
                    })
            
        elif cor == 'WIND':
            # WIND 的txt內容跟其他的格式不同要注意!!!!
             for WIND_level in cor_WIND_level:
                for region in regions:
                    filename = f'{cor}_{WIND_level}_{region}_{start_time}{end_time}.txt'
                    # wind讀檔方式不同須注意
                    df = read_wind_file(filename)
                    # wind計算方式不同須注意
                    week1_avg, week2_avg, conflimit1, conflimit2 = compute_windspeed_pco_weekly_score(df)
                    week = compute_pco_week_ds(week1_avg, week2_avg, conflimit1, conflimit2, model1, model2)
                    data_list.append({
                        f'{cor}_{WIND_level}':  week,
                    })

    return data_list

def convert_bias_weekly_score(model1, model2):
    data_list = []
    for bias in bias_var:
        if bias == 'HGT':
            for HGT_level in bias_HGT_level:
                for region in regions:
                    filename = f'{bias}_{HGT_level}_{region}_{start_time}{end_time}.txt'
                    df = read_file(filename)
                    week1_avg, week2_avg, conflimit1, conflimit2 = compute_bias_weekly_score(df)
                    week = compute_bias_week_ds(week1_avg, week2_avg, conflimit1, conflimit2, model1, model2)
                    data_list.append({
                        f'{bias}_{HGT_level}':  week,
                    })

        elif bias == 'T':
            for T_level in cor_T_level:
                for region in regions:
                    filename = f'{bias}_{T_level}_{region}_{start_time}{end_time}.txt'
                    df = read_file(filename)
                    week1_avg, week2_avg, conflimit1, conflimit2 = compute_bias_weekly_score(df)
                    week = compute_bias_week_ds(week1_avg, week2_avg, conflimit1, conflimit2, model1, model2)
                    data_list.append({
                        f'{bias}_{T_level}':  week,
                    })
        elif bias == 'WIND':
            # WIND 的txt內容跟其他的格式不同要注意!!!!
            for WIND_level in bias_WIND_level:
                for region in regions:
                    filename = f'{bias}_{WIND_level}_{region}_{start_time}{end_time}.txt'
                    # wind讀檔方式不同須注意
                    df = read_wind_file(filename)
                    # wind計算方式不同須注意
                    week1_avg, week2_avg, conflimit1, conflimit2 = compute_windspeed_bias_weekly_score(df)
                    week = compute_bias_week_ds(week1_avg, week2_avg, conflimit1, conflimit2, model1, model2)
                    data_list.append({
                        f'{bias}_{WIND_level}':  week,
                    })
    # print('bias data_list-->', data_list)

    return data_list

def compute_rmse_weekly_score(df):
    # 計算rmse
    # RMSE:  rms= sqrt( X4 + X5 - 2*X3 )
    df['rmse'] = np.sqrt(df['f2'] + df['a2'] - 2*df['fa'])
    # 為了乾淨，清掉不需要的欄位
    df = df.drop(columns=['model2', 'grid', 'version', 'resolution', 'anomaly', 'variable', 'level', 'grid', 'f', 'a', 'fa', 'f2', 'a2'])
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

    # 再篩出符合第三週的值
    # df_week3 = df[ (df['tau'] >= 336)  & (df['tau'] < 504 ) ]
    # week3 = df_week3.groupby(['model1', 'init_time'])[['rmse']].mean()
    # week.insert(3, 'week3', week3)
    # 刪掉rmse欄位，week1, week2都是rmse的值了
    week = week.drop(columns=['rmse'])

    # 攤平column 值
    week = week.reset_index()
    week1_avg = week.groupby(['model1'])['week1'].mean()
    week1_std = week.groupby(['model1'])['week1'].std()

    week2_avg = week.groupby(['model1'])['week2'].mean()
    week2_std = week.groupby(['model1'])['week2'].std()

    # week3_avg = week.groupby(['model1'])['week3'].mean()
    # week3_std = week.groupby(['model1'])['week3'].std()

    week_std = [week1_std, week2_std]
    conflimit = []
    for std in week_std:
        conflimit.append(compute_conflimit(std))

    return week1_avg, week2_avg, conflimit[0], conflimit[1]

def compute_bias_weekly_score(df):
    # df = read_file(FILENAME)
    # 計算bias
    # Mean biases: bias= ( X1 - X2 )
    df['bias'] = df['f'] - df['a']
    # 為了乾淨，清掉不需要的欄位
    df = df.drop(columns=['model2', 'grid', 'version', 'resolution', 'anomaly', 'variable', 'level', 'grid', 'f', 'a', 'fa', 'f2', 'a2'])
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

def compute_pco_weekly_score(df):
    # df = read_file(FILENAME)
    # 計算pattern orrelation
    #  Pattern correlation : R=( X3 - X1*X2 ) / sqrt{var(f)*var(a)}
    #    where var(f)={ X4 - X1*X1 } 
    #          var(a)={ X5 - X2*X2 } 
    df['pco'] = ( df['fa'] -  (df['f'] * df['a']) ) /  np.sqrt( ( df['f2'] - df['f']**2 )  * ( df['a2'] -df['a']** 2 ) ) 
    # 為了乾淨，清掉不需要的欄位
    df = df.drop(columns=['model2', 'grid', 'version', 'resolution', 'anomaly', 'variable', 'level', 'grid', 'f', 'a', 'fa', 'f2', 'a2'])
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

def confidence_level():
    ndays = 30
    if ndays > 80:
        alpha1=1.960  ; #95% confidence level
        alpha2=2.576  ; #99% confidence level
        alpha3=3.291  ; #99.9% confidence level
    elif ndays > 40 & ndays < 80:
        alpha1=2.0    ; #95% confidence level
        alpha2=2.66   ; #99% confidence level
        alpha3=3.46   ; #99.9% confidence level
    elif ndays > 20 & ndays < 40:
        alpha1=2.042  ; #95% confidence level
        alpha2=2.75   ; #99% confidence level
        alpha3=3.646  ; #99.9% confidence level
    elif ndays < 20:
        alpha1=2.228  ; #95% confidence level
        alpha2=3.169  ; #99% confidence level
        alpha3=4.587  ; #99.9% confidence level
    
    return alpha1, alpha2, alpha3
