

from cmath import log
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

def run_main(fq_file,output_dir, sample_name,control_dir):
    fq_file = Path(fq_file)
    pkl = add_all.run_aneuploidy_test(fq_file, output_dir, prefix=sample_name)

if __name__ == '__main__':
    control_dir = Path('/data2/LD-PGTA/control')
    # origin_path = Path(sys.argv[1])
    # output_origin_dir = Path(sys.argv[2])
    origin_path = Path('/data2/LD-PGTA/cases/ceshi/1109/fq/')
    output_origin_dir = Path('/data2/LD-PGTA/cases/ceshi/1109/result')
    with open('log_1.log','w') as f:
        for file_name in origin_path.rglob('*.fq.gz'):
            # sample_name = file_name.parent.name
            sample_name = file_name.name.split('.')[0]
            output_dir = os.path.join(output_origin_dir, sample_name)
            if not os.path.exists(output_dir):
                os.mkdir(output_dir)
            print('start bos')
            # add_all.run_aneuploidy_test(fq_file, output_dir, prefix=sample_name)
            try:
                run_main(file_name,output_dir, sample_name,control_dir)
            except Exception as e:
                f.writelines(sample_name+'\n')
                pass
