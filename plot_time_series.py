import os
from tkinter import font
import pandas as pd
import numpy as np
import time
import seaborn as sns
# from datetime import datetime
from compute_scorecard_wind_data import (compute_windspeed_rmse_weekly_score,
                                         compute_windspeed_bias_weekly_score,
                                         compute_windspeed_pco_weekly_score,
                                         compute_windspeed_msess_weekly_score
                                        )
import matplotlib.pyplot as plt 
from compute_scorecard_data import (compute_rmse_weekly_score,
                                    compute_pco_weekly_score,
                                    compute_bias_weekly_score,
                                    compute_mean_squared_error,
                                    compute_msess,
                                    read_file, read_wind_file
                                    )
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
cor_name = 'Pattern Correlation'
rms_name = 'RMSE'
bias_name = 'Bias'
mess_name = 'Murphy MSE Skill Score'

# vaiable name
cor_var = ['HGT', 'WIND', 'T', 'PMSL']
rms_var = ['HGT', 'WIND', 'T']
# rms_var = ['HGT', 'WIND', 'PMSL']
bias_var = ['HGT', 'WIND', 'PMSL']
mess_var = ['HGT', 'WIND', 'T', 'PMSL']

# cor vaiable level
cor_HGT_level = ['P250', 'P500', 'P700']
cor_T_level = ['P250', 'P500', 'P850']
cor_U_level = ['P250', 'P500', 'P850']
cor_V_level = ['P250', 'P500', 'P850']
cor_WIND_level = ['P250', 'P500', 'P850']
cor_PMSL_level = ['MSL']

# rms vaiable level
rms_HGT_level=['P250', 'P500', 'P1000']
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

# mess vaiable level
mess_HGT_level = ['P250', 'P500']
mess_T_level = ['P250', 'P500', 'P850']
mess_U_level = ['P250', 'P500', 'P850']
mess_V_level = ['P250', 'P500', 'P850']
mess_WIND_level = ['P250', 'P500', 'P850']
mess_PMSL_level = ['MSL']

start_time = '20211024'
end_time = '20211123'

SOLID_COLOR_LIST = ['k-o', 'r-o', 'g-o', 'b-o']

def plot_pco_line():
    for cor in cor_var:
        if cor == 'HGT':
            for HGT_level in cor_HGT_level:
                for region in regions:
                    filename = f'{cor}_{HGT_level}_{region}_{start_time}{end_time}.txt'
                    df = read_file(filename)
                    week1_avg, week2_avg, conflimit1, conflimit2 = compute_pco_weekly_score(df)
                    plot_data = []
                    for k, v in week1_avg.to_dict().items():
                        for a, b in week2_avg.to_dict().items():
                            if k == a:
                                plot_data.append({
                                    k: [v, b],
                                })
                    plot_fig(plot_data, cor_name, cor, region, HGT_level)
        elif cor == 'T':
            for T_level in cor_T_level:
                for region in regions:
                    filename = f'{cor}_{T_level}_{region}_{start_time}{end_time}.txt'
                    df = read_file(filename)
                    week1_avg, week2_avg, conflimit1, conflimit2 = compute_pco_weekly_score(df)
                    plot_data = []
                    for k, v in week1_avg.to_dict().items():
                        # print(k, v)
                        for a, b in week2_avg.to_dict().items():
                            if k == a:
                                plot_data.append({
                                    k: [v, b],
                                })
                    # print('plot_data--->', plot_data)
                    plot_fig(plot_data, cor_name, cor, region, T_level)

        elif cor == 'U':
            for U_level in cor_U_level:
                for region in regions:
                    filename = f'{cor}_{U_level}_{region}_{start_time}{end_time}.txt'
                    df = read_file(filename)
                    week1_avg, week2_avg, conflimit1, conflimit2 = compute_pco_weekly_score(df)
                    plot_data = []
                    for k, v in week1_avg.to_dict().items():
                        for a, b in week2_avg.to_dict().items():
                            if k == a:
                                plot_data.append({
                                    k: [v, b],
                                })
                    plot_fig(plot_data, cor_name, cor, region, U_level)
        elif cor == 'V':
            for V_level in cor_V_level:
                for region in regions:
                    filename = f'{cor}_{V_level}_{region}_{start_time}{end_time}.txt'
                    df = read_file(filename)
                    week1_avg, week2_avg, conflimit1, conflimit2 = compute_pco_weekly_score(df)
                    plot_data = []
                    for k, v in week1_avg.to_dict().items():
                        for a, b in week2_avg.to_dict().items():
                            if k == a:
                                plot_data.append({
                                    k: [v, b],
                                })
                    plot_fig(plot_data, cor_name, cor, region, V_level)
        elif cor == 'PMSL':
            for PMSL_level in cor_PMSL_level:
                for region in regions:
                    filename = f'{cor}_{PMSL_level}_{region}_{start_time}{end_time}.txt'
                    df = read_file(filename)
                    week1_avg, week2_avg, conflimit1, conflimit2 = compute_pco_weekly_score(df)
                    plot_data = []
                    for k, v in week1_avg.to_dict().items():
                        for a, b in week2_avg.to_dict().items():
                            if k == a:
                                plot_data.append({
                                    k: [v, b],
                                })
                    plot_fig(plot_data, cor_name, cor, region, PMSL_level)
        elif cor == 'WIND':
            # WIND 的txt內容跟其他的格式不同要注意!!!!
            for WIND_level in cor_WIND_level:
                for region in regions:
                    filename = f'{cor}_{WIND_level}_{region}_{start_time}{end_time}.txt'
                    df = read_wind_file(filename)
                    week1_avg, week2_avg, conflimit1, conflimit2 = compute_windspeed_pco_weekly_score(df)
                    plot_data = []
                    for k, v in week1_avg.to_dict().items():
                        for a, b in week2_avg.to_dict().items():
                            if k == a:
                                plot_data.append({
                                    k: [v, b],
                                })
                    plot_fig(plot_data, cor_name, cor, region, WIND_level)


def plot_rmse_line():
    for cor in rms_var:
        if cor == 'HGT':
            for HGT_level in cor_HGT_level:
                for region in regions:
                    filename = f'{cor}_{HGT_level}_{region}_{start_time}{end_time}.txt'
                    df = read_file(filename)
                    week1_avg, week2_avg, conflimit1, conflimit2 = compute_rmse_weekly_score(df)
                    plot_data = []
                    for k, v in week1_avg.to_dict().items():
                        for a, b in week2_avg.to_dict().items():
                            if k == a:
                                plot_data.append({
                                    k: [v, b],
                                })
                    plot_fig(plot_data, rms_name, cor, region, HGT_level)
        elif cor == 'T':
            for T_level in cor_T_level:
                for region in regions:
                    filename = f'{cor}_{T_level}_{region}_{start_time}{end_time}.txt'
                    df = read_file(filename)
                    week1_avg, week2_avg, conflimit1, conflimit2 = compute_rmse_weekly_score(df)
                    plot_data = []
                    for k, v in week1_avg.to_dict().items():
                        # print(k, v)
                        for a, b in week2_avg.to_dict().items():
                            if k == a:
                                plot_data.append({
                                    k: [v, b],
                                })
                    # print('plot_data--->', plot_data)
                    plot_fig(plot_data, rms_name, cor, region, T_level)

        elif cor == 'U':
            for U_level in cor_U_level:
                for region in regions:
                    filename = f'{cor}_{U_level}_{region}_{start_time}{end_time}.txt'
                    df = read_file(filename)
                    week1_avg, week2_avg, conflimit1, conflimit2 = compute_rmse_weekly_score(df)
                    plot_data = []
                    for k, v in week1_avg.to_dict().items():
                        for a, b in week2_avg.to_dict().items():
                            if k == a:
                                plot_data.append({
                                    k: [v, b],
                                })
                    plot_fig(plot_data, rms_name, cor, region, U_level)
        elif cor == 'V':
            for V_level in cor_V_level:
                for region in regions:
                    filename = f'{cor}_{V_level}_{region}_{start_time}{end_time}.txt'
                    df = read_file(filename)
                    week1_avg, week2_avg, conflimit1, conflimit2 = compute_rmse_weekly_score(df)
                    plot_data = []
                    for k, v in week1_avg.to_dict().items():
                        for a, b in week2_avg.to_dict().items():
                            if k == a:
                                plot_data.append({
                                    k: [v, b],
                                })
                    plot_fig(plot_data, rms_name, cor, region, V_level)
        elif cor == 'PMSL':
            for PMSL_level in cor_PMSL_level:
                for region in regions:
                    filename = f'{cor}_{PMSL_level}_{region}_{start_time}{end_time}.txt'
                    df = read_file(filename)
                    week1_avg, week2_avg, conflimit1, conflimit2 = compute_rmse_weekly_score(df)
                    plot_data = []
                    for k, v in week1_avg.to_dict().items():
                        for a, b in week2_avg.to_dict().items():
                            if k == a:
                                plot_data.append({
                                    k: [v, b],
                                })
                    plot_fig(plot_data, rms_name, cor, region, PMSL_level)
        elif cor == 'WIND':
            # WIND 的txt內容跟其他的格式不同要注意!!!!
            for WIND_level in cor_WIND_level:
                for region in regions:
                    filename = f'{cor}_{WIND_level}_{region}_{start_time}{end_time}.txt'
                    df = read_wind_file(filename)
                    week1_avg, week2_avg, conflimit1, conflimit2 = compute_windspeed_rmse_weekly_score(df)
                    plot_data = []
                    for k, v in week1_avg.to_dict().items():
                        for a, b in week2_avg.to_dict().items():
                            if k == a:
                                plot_data.append({
                                    k: [v, b],
                                })
                    plot_fig(plot_data, rms_name, cor, region, WIND_level)

def plot_bias_line():
    for cor in bias_var:
        if cor == 'HGT':
            for HGT_level in cor_HGT_level:
                for region in regions:
                    filename = f'{cor}_{HGT_level}_{region}_{start_time}{end_time}.txt'
                    df = read_file(filename)
                    week1_avg, week2_avg, conflimit1, conflimit2 = compute_bias_weekly_score(df)
                    # print('week1_avg-->', week1_avg[1], type(week1_avg))
                    # print('week2_avg-->', week2_avg.to_dict())
                    plot_data = []
                    for k, v in week1_avg.to_dict().items():
                        for a, b in week2_avg.to_dict().items():
                            if k == a:
                                plot_data.append({
                                    k: [v, b],
                                })
                    plot_fig(plot_data, bias_name, cor, region, HGT_level)
        elif cor == 'T':
            for T_level in cor_T_level:
                for region in regions:
                    filename = f'{cor}_{T_level}_{region}_{start_time}{end_time}.txt'
                    df = read_file(filename)
                    week1_avg, week2_avg, conflimit1, conflimit2 = compute_bias_weekly_score(df)
                    plot_data = []
                    for k, v in week1_avg.to_dict().items():
                        # print(k, v)
                        for a, b in week2_avg.to_dict().items():
                            if k == a:
                                plot_data.append({
                                    k: [v, b],
                                })
                    # print('plot_data--->', plot_data)
                    plot_fig(plot_data, bias_name, cor, region, T_level)

        elif cor == 'U':
            for U_level in cor_U_level:
                for region in regions:
                    filename = f'{cor}_{U_level}_{region}_{start_time}{end_time}.txt'
                    df = read_file(filename)
                    week1_avg, week2_avg, conflimit1, conflimit2 = compute_bias_weekly_score(df)
                    plot_data = []
                    for k, v in week1_avg.to_dict().items():
                        for a, b in week2_avg.to_dict().items():
                            if k == a:
                                plot_data.append({
                                    k: [v, b],
                                })
                    plot_fig(plot_data, bias_name, cor, region, U_level)
        elif cor == 'V':
            for V_level in cor_V_level:
                for region in regions:
                    filename = f'{cor}_{V_level}_{region}_{start_time}{end_time}.txt'
                    df = read_file(filename)
                    week1_avg, week2_avg, conflimit1, conflimit2 = compute_bias_weekly_score(df)
                    plot_data = []
                    for k, v in week1_avg.to_dict().items():
                        for a, b in week2_avg.to_dict().items():
                            if k == a:
                                plot_data.append({
                                    k: [v, b],
                                })
                    plot_fig(plot_data, bias_name, cor, region, V_level)
        elif cor == 'PMSL':
            for PMSL_level in cor_PMSL_level:
                for region in regions:
                    filename = f'{cor}_{PMSL_level}_{region}_{start_time}{end_time}.txt'
                    df = read_file(filename)
                    week1_avg, week2_avg, conflimit1, conflimit2 = compute_bias_weekly_score(df)
                    plot_data = []
                    # print('week1_avg-->', week1_avg[0], type(week1_avg))
                    # print('week2_avg-->', week2_avg.to_dict())

                    for k, v in week1_avg.to_dict().items():
                        for a, b in week2_avg.to_dict().items():
                            if k == a:
                                plot_data.append({
                                    k: [v, b],
                                })
                    plot_fig(plot_data, bias_name, cor, region, PMSL_level)
        elif cor == 'WIND':
            # WIND 的txt內容跟其他的格式不同要注意!!!!
            for WIND_level in cor_WIND_level:
                for region in regions:
                    filename = f'{cor}_{WIND_level}_{region}_{start_time}{end_time}.txt'
                    df = read_wind_file(filename)
                    week1_avg, week2_avg, conflimit1, conflimit2 = compute_windspeed_bias_weekly_score(df)
                    plot_data = []
                    for k, v in week1_avg.to_dict().items():
                        for a, b in week2_avg.to_dict().items():
                            if k == a:
                                plot_data.append({
                                    k: [v, b],
                                })
                    plot_fig(plot_data, bias_name, cor, region, WIND_level)

def plot_msess_line():
    for cor in mess_var:
        if cor == 'HGT':
            for HGT_level in mess_HGT_level:
                for region in regions:
                    filename = f'{cor}_{HGT_level}_{region}_{start_time}{end_time}.txt'
                    df = read_file(filename)
                    week1_avg, week2_avg = compute_msess(df)
                    plot_data = []
                    for k, v in week1_avg.to_dict().items():
                        for a, b in week2_avg.to_dict().items():
                            if k == a:
                                plot_data.append({
                                    k: [v, b],
                                })
                    plot_fig(plot_data, mess_name, cor, region, HGT_level)
        elif cor == 'T':
            for T_level in mess_T_level:
                for region in regions:
                    filename = f'{cor}_{T_level}_{region}_{start_time}{end_time}.txt'
                    df = read_file(filename)
                    week1_avg, week2_avg = compute_msess(df)
                    plot_data = []
                    for k, v in week1_avg.to_dict().items():
                        # print(k, v)
                        for a, b in week2_avg.to_dict().items():
                            if k == a:
                                plot_data.append({
                                    k: [v, b],
                                })
                    # print('plot_data--->', plot_data)
                    plot_fig(plot_data, mess_name, cor, region, T_level)

        elif cor == 'U':
            for U_level in mses_U_level:
                for region in regions:
                    filename = f'{cor}_{U_level}_{region}_{start_time}{end_time}.txt'
                    df = read_file(filename)
                    week1_avg, week2_avg = compute_msess(df)
                    plot_data = []
                    for k, v in week1_avg.to_dict().items():
                        for a, b in week2_avg.to_dict().items():
                            if k == a:
                                plot_data.append({
                                    k: [v, b],
                                })
                    plot_fig(plot_data, mess_name, cor, region, U_level)
        elif cor == 'V':
            for V_level in mess_V_level:
                for region in regions:
                    filename = f'{cor}_{V_level}_{region}_{start_time}{end_time}.txt'
                    df = read_file(filename)
                    week1_avg, week2_avg = compute_msess(df)
                    plot_data = []
                    for k, v in week1_avg.to_dict().items():
                        for a, b in week2_avg.to_dict().items():
                            if k == a:
                                plot_data.append({
                                    k: [v, b],
                                })
                    plot_fig(plot_data, mess_name, cor, region, V_level)
        elif cor == 'PMSL':
            for PMSL_level in mess_PMSL_level:
                for region in regions:
                    filename = f'{cor}_{PMSL_level}_{region}_{start_time}{end_time}.txt'
                    df = read_file(filename)
                    week1_avg, week2_avg = compute_msess(df)
                    plot_data = []
                    for k, v in week1_avg.to_dict().items():
                        for a, b in week2_avg.to_dict().items():
                            if k == a:
                                plot_data.append({
                                    k: [v, b],
                                })
                    plot_fig(plot_data, mess_name, cor, region, PMSL_level)
        elif cor == 'WIND':
            # WIND 的txt內容跟其他的格式不同要注意!!!!
            for WIND_level in mess_WIND_level:
                for region in regions:
                    filename = f'{cor}_{WIND_level}_{region}_{start_time}{end_time}.txt'
                    df = read_wind_file(filename)
                    week1_avg, week2_avg = compute_windspeed_msess_weekly_score(df)
                    plot_data = []
                    for k, v in week1_avg.to_dict().items():
                        for a, b in week2_avg.to_dict().items():
                            if k == a:
                                plot_data.append({
                                    k: [v, b],
                                })
                    plot_fig(plot_data, mess_name, cor, region, WIND_level)

def plot_fig(plot_data, score_name, param_type, region, level_type):
    sns.set_style("darkgrid")
    # sns.set_context("poster")
    if score_name == 'Pattern Correlation':
        fig_filename = 'pco'
    elif score_name == 'RMSE':
        fig_filename = 'rms'
    elif score_name == 'Bias':
        fig_filename = 'bias'
    elif score_name == 'Murphy MSE Skill Score':
        fig_filename = 'msess'
    cnt=0
    plt.figure(figsize=(8, 6), dpi=300)
    for i in plot_data:
        for k, v in i.items():
            plt.plot(['week1', 'week2'], v, SOLID_COLOR_LIST[cnt], label=f'{k}')
            cnt+=1
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.xlabel('week', fontsize=16)
    plt.legend(loc='best')

    if param_type == 'PMSL':
        plt.title(f'{score_name}_{param_type}_{region}\n{start_time}_{end_time} Mean', fontsize=14)                   
        plt.savefig(f'{fig_filename}_{param_type}_{region}.png')

    else:
        plt.title(f'{score_name}_{param_type}_{level_type}_{region}\n{start_time}_{end_time} Mean', fontsize=14)                   
        plt.savefig(f'{fig_filename}_{param_type}_{level_type}_{region}.png')
    plt.close()



if __name__ == '__main__':
    start = time.process_time()
    print('start plot pco mean')
    plot_pco_line()
    print('end plot pco mean')
    print('------------------------------')
    print('start plot rmse mean')
    plot_rmse_line()
    print('end plot rmse mean')
    print('------------------------------')
    print('start plot bias mean')
    plot_bias_line()
    print('end plot bias mean')
    print('------------------------------')
    print('start plot msess mean')
    plot_msess_line()
    print('end plot msess mean')
    end = time.process_time()
    print(f'cost time: {end-start} s')
