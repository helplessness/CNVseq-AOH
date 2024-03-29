


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