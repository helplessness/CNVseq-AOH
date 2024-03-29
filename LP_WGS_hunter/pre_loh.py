import multiprocessing
from LP_WGS_hunter import config
from keras.models import load_model
import numpy as np
import pickle
import os
import matplotlib.pyplot as plt


def get_right_area(a,b,interval):
    idx_list = []
    for idx,i in enumerate(a):
        if i >=0.85:
            idx_list.append(idx)
    if idx_list != []:
        duandian_list = []
        start = 0
        for idx,j in enumerate(idx_list):
            if idx < len(idx_list)-1:
                if b[idx_list[idx+1]] - b[j] > interval:
                    if duandian_list == []:
                        duandian_list.append((idx_list[0],j))
                        start = idx_list[idx+1]
                    else:
                        duandian_list.append((start,j))
                        start = idx_list[idx+1]
            else:
                if start != 0:
                    duandian_list.append((start,j))
                else:
                    duandian_list.append((idx_list[0],j))
    else:
        duandian_list = []
    return duandian_list



def new_RNN_get_loh_new(pkl_path,chr_num,output_dir,interval,length,deepth):
    plt.figure()
    with open(pkl_path,'rb') as f:
        data = pickle.load(f)
    a = data[list(data.keys())[chr_num-1]]['statistics']['LLRs_per_genomic_window'][('disomy', 'monosomy')]
    weizhi_list = []
    disomy_list = []
    monosomy_list = []
    x_list = []
    num_list = []
    for idx,i in enumerate(a):
        num_list.append(idx)
        weizhi_list.append(i)
        x_list.append(i[1])
        disomy_list.append(a[i][0])
        monosomy_list.append(a[i][1])
    plt.scatter(x_list, disomy_list,marker='.',s=3)
    plt.title('chr%s'%str(chr_num))
    
    feature_list_all = []
    new_weizhi = []
    if deepth:
        for j in num_list:
            if j >= 125 and j < len(num_list)-125:
                feature_list = []
                one_feature_list = []
                one_feature_list_1 = []
                for num in range(-125,125,1):
                    one_feature_list.append(disomy_list[j+num])
                    one_feature_list_1.append(monosomy_list[j+num])
                feature_list.append(one_feature_list)
                feature_list.append(one_feature_list_1)
                feature_list_all.append(feature_list)
                new_weizhi.append(weizhi_list[j][0])

        x_train= np.array(feature_list_all)
        model = load_model(config.LOH_MODEL_high)
        predict_test = model.predict(x_train)
        pre_score_list = predict_test.reshape(1,-1).tolist()[0]
    else:
        for j in num_list:
            if j >= 50 and j < len(num_list)-50:
                feature_list = []
                one_feature_list = []
                one_feature_list_1 = []
                for num in range(-50,50,1):
                    one_feature_list.append(disomy_list[j+num])
                    one_feature_list_1.append(monosomy_list[j+num])
                feature_list.append(one_feature_list)
                feature_list.append(one_feature_list_1)
                feature_list_all.append(feature_list)
                new_weizhi.append(weizhi_list[j][0])

        x_train= np.array(feature_list_all)
        model = load_model(config.LOH_MODEL_low)
        predict_test = model.predict(x_train)
        pre_score_list = predict_test.reshape(1,-1).tolist()[0]

    final_list = get_right_area(pre_score_list,new_weizhi,interval)
    no_select_list = []
    return_list = []
    for one_distance in final_list:
        no_select_list.append((chr_num,new_weizhi[one_distance[0]],new_weizhi[one_distance[1]]))
        if new_weizhi[one_distance[1]]-new_weizhi[one_distance[0]] >= length:
            return_list.append((chr_num,new_weizhi[one_distance[0]],new_weizhi[one_distance[1]]))
            plt.axvspan(new_weizhi[one_distance[0]],new_weizhi[one_distance[1]], alpha=0.4, color='lightcoral')
    plt.savefig(os.path.join(output_dir,'chr' + str(chr_num)+'-loh.png'))
    return no_select_list, return_list


def run_loh_pre(input_pkl,output_dir,thread_num,interval=2100000,length=3500000,deepth=True,include_x=False):
    base_name = os.path.basename(input_pkl).split('.')[0]
    max_chr = 24 if include_x else 23
    with open(os.path.join(output_dir,'%s_chr_real.txt'%(base_name)),'w') as f:
        with open(os.path.join(output_dir,'%s_chr_final.txt'%(base_name)),'w') as g:
            pool = multiprocessing.Pool(thread_num)
            duilie_list = []
            for chr_num in range(1,max_chr):
                result = pool.apply_async(new_RNN_get_loh_new,(input_pkl,chr_num,output_dir,interval,length,deepth))
                duilie_list.append(result)
            pool.close()
            pool.join()
            for real_pos,final_pos in zip([i.get()[0] for i in duilie_list],[i.get()[1] for i in duilie_list]):
                f.write(str(real_pos)+'\n')
                g.write(str(final_pos)+'\n')
        

if __name__ == '__main__':
    sample_name = 'HG00096'   ####NA19728
    num = '3'
    pkl_path = '/data4/1kg_data/data/all_group_result/%s_%s/%s_%s.pkl'%(sample_name,num,sample_name,num)
    output_dir = '/home/phoenix/workspace/tf_data/data/tes/'
    run_loh_pre(pkl_path,output_dir,24,deepth=False)