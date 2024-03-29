from LP_WGS_hunter import add_all
import os
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
from pathlib import Path
from LP_WGS_hunter import merge_obs
import collections

sns.set()

# CHROMS = ['chr' + str(i) for i in range(1, 23)]

leg_tuple = collections.namedtuple('leg_tuple', ('chr_id', 'pos', 'ref', 'alt')) #Encodes the rows of the legend table
sam_tuple = collections.namedtuple('sam_tuple', ('sample_id', 'group1', 'group2', 'sex')) #Encodes the rows of the samples table
obs_tuple = collections.namedtuple('obs_tuple', ('pos', 'read_id', 'base')) #Encodes the rows of the observations table

def run_main_bam(bam_file:str, output_dir:str, sample_name,control_dir,include_x,np=32,ref='hg19'):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    pkl = add_all.run_aneuploidy_test_bam(bam_file, output_dir, prefix=sample_name, np=np,include_x=include_x,ref=ref)


if __name__ == '__main__':
    control_dir = Path('/data2/LD-PGTA/control')
    origin_path = Path('/data4/1kg_data/data1/')
    output_origin_dir = Path('/data4/1kg_data/data/result/')
    for file_name in origin_path.rglob('*.bam'):
        try:
            sample_name = '.'.join(file_name.name.split('.')[:-1])
            output_dir = os.path.join(output_origin_dir, sample_name)
            if not os.path.exists(output_dir):
                os.mkdir(output_dir)
            print('start bos')
            run_main_bam(file_name.as_posix(), output_dir, sample_name,control_dir)
        except:
            pass

    # file_name = '/data3/1kg/sample/NA12889/3/NA12889_1.bam'
    # output = '/data3/1kg/sample/NA12889/3/result'
    # run_main_bam(file_name,output,'NA12889_1',control_dir)


