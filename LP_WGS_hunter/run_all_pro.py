


# %%
from LP_WGS_hunter import add_all
import os
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
from pathlib import Path
from LP_WGS_hunter import merge_obs
import collections


sns.set()

CHROMS = ['chr' + str(i) for i in range(1, 23)]

leg_tuple = collections.namedtuple('leg_tuple', ('chr_id', 'pos', 'ref', 'alt')) #Encodes the rows of the legend table
sam_tuple = collections.namedtuple('sam_tuple', ('sample_id', 'group1', 'group2', 'sex')) #Encodes the rows of the samples table
obs_tuple = collections.namedtuple('obs_tuple', ('pos', 'read_id', 'base')) #Encodes the rows of the observations table

def run_main(file,output_dir, sample_name,control_dir, np=32):
    fq_file = Path(file)
    pkl = add_all.run_aneuploidy_test(fq_file, output_dir, prefix=sample_name, np=np)
    # pkl = merge_obs.merge_obs(sample_name, output_dir)
    # print('done merge obs')
    # df = add_all.get_data(pkl_file=pkl)

    # li = []
    # for file in control_dir.rglob('*.pkl'):
    #     _df = add_all.get_data(pkl_file=file)
    #     if file.parent.name == 'pos':
    #         _df['karyotype'] = 'triploid'
    #     else:
    #         _df['karyotype'] = 'diploid'
    #     li.append(_df)
    # df_control = pd.concat(li)
    # df_control.reset_index(inplace=True, drop=True)

    # df['karyotype'] = sample_name
    # df.reset_index(inplace=True, drop=True)

    # df_all = pd.concat([df, df_control], ignore_index=True)

    # ax, fig = plt.subplots(figsize=(10, 5))

    # g = sns.lineplot(
    #     data=df_all, x='index', y='mean_of_mean', hue='karyotype'
    # )
    # g.set_xlabel('Chromosome')
    # g.set_xticks(range(1, 23))
    # g.set_xticklabels(range(1, 23))
    # g.set_ylabel('Likelihood')

    # df.to_csv(os.path.join(output_dir,sample_name+'_aneuploidy.csv'),index=False)
    # plt.savefig(os.path.join(output_dir,sample_name+'_aneuploidy.png'))


if __name__ == '__main__':
    control_dir = Path('/data2/LD-PGTA/control')
    origin_path = Path('/data4/cnvseq/cases/fq/V350132481_L02_49.fq.gz')
    output_origin_dir = '/data4/cnvseq/cases/49/'
    # for file in origin_path.rglob('*.fq.gz'):
    # 	sample_name = file.name.split('.')[0]
    # 	output_dir = output_origin_dir / sample_name
    sample_name = 'V350135343_L01_95'
    if not os.path.exists(output_origin_dir):
        os.mkdir(output_origin_dir)
    try:
        run_main(origin_path, output_origin_dir, sample_name,control_dir)
    except Exception as e:
        print(e)