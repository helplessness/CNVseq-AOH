'''
0:1.96,1.29
1:1.29.0.85
'''

#%%
import pandas as pd
import pathlib
import plotly
import plotly.express as px
import pickle
from sklearn.preprocessing import StandardScaler
import joblib
import plotly.express as px
import plotly

#%%
def get_data(pkl_file,chr_name = None):
    '''
    获取pkl文件中的平均值，可选按照染色体输出结果
    '''
    _data = pickle.load(open(pkl_file, 'rb'))
    _json = pd.DataFrame(
        [
            pd.Series(
                v['statistics']['LLRs_per_chromosome'][('BPH', 'SPH')]['mean_of_mean'],
                name=int(v['chr_id'])
            )
            for k, v in _data.items()
        ] + [
            pd.Series(pkl_file.name.split('/')[-1].split('.')[0])
        ]
    ).T
    _json.columns = [i for i in range(22)]+['sample_name']
    if chr_name is not None:
        return _json[chr_name-1]
    else:
        return _json

#%%

def build_model(build=False):
    '''
    build model for each chromosome,默认不在输出
    需要输入文件，同时生成csv文件，用于绘图和计算'''
    # all_data_path = pathlib.Path('/data2/LD-PGTA/cases/guangxiu/0801_result_1M/result')
    all_data_path = pathlib.Path('/data3/guangxiu1125/result/')
    all_data = pd.DataFrame()

    for file_name in all_data_path.rglob('*.pkl'):
        if file_name.parent.name.endswith('_unmap'):
            continue
        else:
            all_data = all_data.append(get_data(file_name))
    all_data.to_csv('all_guangxiu_1125.csv', index=False)
    if build:
        for chr_name in all_data.columns:
            if chr_name != 'sample_name':
                ss = StandardScaler()
                model = ss.fit_transform(all_data[chr_name].values.reshape(-1, 1))
                joblib.dump(ss, '/home/tf/pro/inherance/chr_z_score/origin/%s.sav' % str(chr_name+1))


build_model()
#%%
data = pd.read_csv('all_guangxiu_1125.csv', header=0)

def done_row(row:pd.Series):
    for i in [j for j in range(0,22)]:
        model = joblib.load('/home/tf/pro/inherance/chr_z_score/origin/%s.sav' % str(i+1))
        row[i] = model.transform([[row[i]]])[0][0]
    return row
new_data = data.apply(done_row, axis=1)

# %%
#### 绘图和生成最后zscore之后的结果文件
polt_data = pd.DataFrame()
final_0801_data = pd.DataFrame()
for idx,rows in new_data.iterrows():
    danti_num = 0 
    dantihuiqu_num = 0
    normal_num = 0
    santihuiqu_num = 0
    santi_num = 0
    for i in [j for j in range(0,22)]:
        if rows[i] > 1.29:
            santi_num += 1
        elif rows[i] > 0.85 and rows[i] <= 1.29:
            santihuiqu_num += 1
        elif rows[i] > -1.96 and rows[i] <= 1.29:
            normal_num += 1
        elif rows[i] > -2.56 and rows[i] <= -1.96:
            dantihuiqu_num += 1
        else:
            danti_num += 1
    final_0801_data = final_0801_data.append(pd.Series([rows['sample_name'],danti_num,dantihuiqu_num,normal_num,santihuiqu_num,santi_num],
                    index=['sample_name','Haploidy','Haploidy_greyarea','Normal','Trisomy_greyarea','Trisomy']),ignore_index=True)
    polt_data = polt_data.append({'sample':rows['sample_name'],'classes':'Haploidy','num':danti_num},ignore_index=True)
    polt_data = polt_data.append({'sample':rows['sample_name'],'classes':'Haploidy_greyarea','num':dantihuiqu_num},ignore_index=True)
    polt_data = polt_data.append({'sample':rows['sample_name'],'classes':'Normal','num':normal_num},ignore_index=True)
    polt_data = polt_data.append({'sample':rows['sample_name'],'classes':'Trisomy_greyarea','num':santihuiqu_num},ignore_index=True)
    polt_data = polt_data.append({'sample':rows['sample_name'],'classes':'Trisomy','num':santi_num},ignore_index=True)

fig = px.bar(polt_data, x="sample", y="num", color="classes", title="不同类别的样本数量")
final_0801_data.to_csv('all_guangxiu_1125_final.csv', index=False)
plotly.offline.plot(fig,filename="all_guangxiu_1125.html")
# %%
