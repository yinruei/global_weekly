from flask import Flask, render_template
from compute_scorecard_data import convert_rmse_weekly_score, convert_pco_weekly_score, convert_bias_weekly_score
from compute_scorecard_data import get_region, get_week
app = Flask(__name__)

@app.route("/")
def index():
    model1 = 'JMA_GFS_JG06' #CWB_GFS_GH0D
    model2 = 'EC_GFS_EC05' # EC_GFS_EC05, NCEP_GFS_NA05, JMA_GFS_JG06
    rmse_data_list = convert_rmse_weekly_score(model1, model2)
    pco_data_list = convert_pco_weekly_score(model1, model2)
    bias_data_list = convert_bias_weekly_score(model1, model2)
    # model1 名字簡化
    if model1 == 'CWB_GFS_GH0D':
        model1 = 'CWB'
    elif model1 == 'EC_GFS_EC05':
        model1 = 'EC'
    elif model1 == 'JMA_GFS_JG06':
        model1 = 'JMA'
    elif model1 == 'NCEP_GFS_NA05':
        model1 = 'NCEP'
    # model2 名字簡化
    if model2 == 'NCEP_GFS_NA05':
        model2 = 'NCEP'
    elif model2 == 'EC_GFS_EC05':
        model2 = 'EC'
    elif model2 == 'JMA_GFS_JG06':
        model2 = 'JMA'
    elif model2 == 'CWB_GFS_GH0D':
        model2 = 'CWB'
    # print('rmse_data_list-->', rmse_data_list)
    # print('pco_data_list-->', pco_data_list)
    # print('bias_data_list-->', bias_data_list)
    tmp = {}
    bias_score_data = []
    for datas in bias_data_list:
        for key, value in datas.items():
            # print(key, datas.keys())
            if key in tmp.keys():
                tmp[key].extend(value)
                # print('key', key)
                # print('jjjj', value)
                # print(tmp['key'])
                # tmp[key].append(value)
            else:
                # print('nononon')
                # tmp[key] = list()
                value_list = [value]
                tmp[key] = value
                # tmp[key] = list()
                # tmp[key].append(value)
            # print('tmp--->', tmp)
            bias_score_data.append(tmp)

    # print('_list----------', _list, len(_list))
    # print('bias_score_data', bias_score_data)

    tmp = {}
    pco_score_data = []
    for datas in pco_data_list:
        for key, value in datas.items():
            # print(key, datas.keys())
            if key in tmp.keys():
                tmp[key].extend(value)
                # print('key', key)
                # print('jjjj', value)
                # print(tmp['key'])
                # tmp[key].append(value)
            else:
                # print('nononon')
                # tmp[key] = list()
                value_list = [value]
                tmp[key] = value
                # tmp[key] = list()
                # tmp[key].append(value)
            # print('tmp--->', tmp)
            pco_score_data.append(tmp)

    # print('_list----------', _list, len(_list))
    # print('pco_score_data', pco_score_data)
    tmp = {}
    rms_score_data = []
    for datas in rmse_data_list:
        for key, value in datas.items():
            # print(key, datas.keys())
            if key in tmp.keys():
                tmp[key].extend(value)
                # print('key', key)
                # print('jjjj', value)
                # print(tmp['key'])
                # tmp[key].append(value)
            else:
                # print('nononon')
                # tmp[key] = list()
                value_list = [value]
                tmp[key] = value
                # tmp[key] = list()
                # tmp[key].append(value)
            # print('tmp--->', tmp)
            rms_score_data.append(tmp)

    # print('rms_score_data', rms_score_data)

    rms_rowspan = len(rms_score_data[0]) + 1
    pco_rowspan = len(pco_score_data[0]) + 1
    bias_rowspan = len(bias_score_data[0]) + 1

    start_time = '2021102300'
    end_time = '2021112400'
    region_colspan = len(get_week())

    data = {
            'start_time': start_time,
            'end_time': end_time,
            'region': get_region(),
            'region_colspan': region_colspan,
            'week': get_week(),
            'model1': model1,
            'model2': model2,
            'rms_rowspan': rms_rowspan,
            'pco_rowspan': pco_rowspan,
            'bias_rowspan': bias_rowspan,
            'rms_score_data': [rms_score_data[0]],
            'pco_score_data' : [pco_score_data[0]],
            'bias_score_data' : [bias_score_data[0]]
        }
    
    return render_template('mainindex.html', data=data)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port='5000',debug=True)