

# %%
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

from LP_WGS_hunter import data_prep
from LP_WGS_hunter import merge_obs
import pickle
import os
from LP_WGS_hunter import make_obs_tab
from LP_WGS_hunter import ANEUPLOIDY_TEST
import collections
from multiprocessing import current_process, Pool
# from concurrent.futures import ProcessPoolExecutor as Pool
from LP_WGS_hunter import config


CHROMS = ['chr' + str(i) for i in range(1, 23)]
CHROMS_X = CHROMS + ['chrX']

# Encodes the rows of the legend table
leg_tuple = collections.namedtuple(
    'leg_tuple', ('chr_id', 'pos', 'ref', 'alt'))
# Encodes the rows of the samples table
sam_tuple = collections.namedtuple(
    'sam_tuple', ('sample_id', 'group1', 'group2', 'sex'))
# Encodes the rows of the observations table
obs_tuple = collections.namedtuple('obs_tuple', ('pos', 'read_id', 'base'))

# %%


def get_panel(chrom: str,ref='hg19'):
    """
    return legend, sample and hap file of the specified chromosome
    """
    ref_panel_dir = Path(config.REF_PANEL_DIR_19 if ref == 'hg19' else config.REF_PANEL_DIR_38)
    chrom_no = ''.join(chrom[3:])
    legend = os.path.join(ref_panel_dir, os.path.join(
        chrom, chrom_no+'_eas.legend.gz'))
    sample_file = os.path.join(
        ref_panel_dir, os.path.join(chrom, 'eas.sample.gz'))
    hap = os.path.join(ref_panel_dir, os.path.join(
        chrom, chrom_no+'_eas.hap.gz'))
    return (
        legend,
        sample_file,
        hap
    )


def make_chrom_obs(bam, chrom, obs_dir,ref):
    legend_file, sample_file, hap_file = get_panel(chrom,ref=ref)
    # retrive_bases(bam, legend_file, sample_file, obs_dir)
    # 更改最下映射质量和基本质量
    make_obs_tab.retrive_bases(
        bam_filename=bam,
        legend_filename=legend_file,
        sample_filename=sample_file,
        output_filename='',
        output_dir=obs_dir,
        fasta_filename='',
        handle_multiple_observations='all',
        min_bq=30,
        min_mq=30,
        max_depth=0,
        compress='unc',
    )


def aneuploidy_chrom_test(obs_file, chrom, output_dir,ref='hg19'):
    legend_file, sample_file, hap_file = get_panel(chrom,ref=ref)
    # 更改    ####--min-score 4
    ANEUPLOIDY_TEST.aneuploidy_test(obs_filename=obs_file,
                                    leg_filename=legend_file,
                                    hap_filename=hap_file,
                                    ancestral_makeup=('EAS',),
                                    window_size=0,
                                    subsamples=32,
                                    offset=0,
                                    min_reads=6,  # 更改 6
                                    max_reads=4,  # 更改4
                                    min_score=2,
                                    min_HF=0.05,
                                    output_filename='',
                                    output_dir=output_dir,
                                    compress='bz2')


def run_two_pro(bam_file, an_input_dir, chrom, out_path,ref='hg19'):
    # try:
    make_chrom_obs(bam_file, chrom, out_path,ref=ref)
    all_name = an_input_dir+'.'+''.join(chrom[3:])+'.obs.p'
    aneuploidy_chrom_test(all_name, chrom, out_path,ref=ref)
    # except:P
    # 	pass


def run_aneuploidy_test(fq_file: Path, output_dir: str, prefix: str,include_x:bool, np=32,debug=False,ref='hg19'):
    bam_file = data_prep.align(fq_file, output_dir, prefix, np=np,debug=debug,ref=ref)
    an_input_dir = os.path.join(output_dir, prefix)
    pool = Pool(np)
    chroms = CHROMS_X if include_x else CHROMS
    for chrom in chroms:
        t1 = pool.apply_async(
            run_two_pro, (bam_file, an_input_dir, chrom, output_dir,ref))
        # make_chrom_obs(bam_file,chrom,output_dir)
    pool.close()
    pool.join()
    pkl_file = merge_obs.merge_obs(prefix, output_dir,include_x=include_x)
    return pkl_file


def run_aneuploidy_test_pe(
        fq_file1: Path, fq_file2: Path, output_dir: str,
        prefix: str,include_x:bool, np=32,debug=False,ref='hg19'
):
    bam_file = data_prep.align_pe(fq_file1, fq_file2, output_dir, prefix,debug,ref=ref)
    an_input_dir = os.path.join(output_dir, prefix)
    pool = Pool(np)
    chroms = CHROMS_X if include_x else CHROMS

    for chrom in chroms:
        t1 = pool.apply_async(
            run_two_pro, (bam_file, an_input_dir, chrom, output_dir,ref))
        # make_chrom_obs(bam_file,chrom,output_dir)
    pool.close()
    pool.join()
    pkl_file = merge_obs.merge_obs(prefix, output_dir,include_x=include_x)
    return pkl_file


def run_aneuploidy_test_bam(bam_file, output_dir: str, prefix: str,include_x:bool, np=32,ref='hg19'):
    an_input_dir = os.path.join(output_dir, prefix)
    pool = Pool(np)
    chroms = CHROMS_X if include_x else CHROMS
    for chrom in chroms:
        t1 = pool.apply_async(
            run_two_pro, (bam_file, an_input_dir, chrom, output_dir,ref))
        # make_chrom_obs(bam_file,chrom,output_dir)
    pool.close()
    pool.join()
    pkl_file = merge_obs.merge_obs(prefix, output_dir,include_x=include_x)
    return pkl_file


def get_data(pkl_file):
    _data = pickle.load(open(pkl_file, 'rb'))
    _json = pd.DataFrame(
        [
            pd.Series(
                v['statistics']['LLRs_per_chromosome'][('BPH', 'SPH')],
                # v['statistics']['LLRs_per_chromosome'][('disomy', 'monosomy')],
                name=v['chr_id']
            )
            for k, v in _data.items()
        ]
    )
    _json.reset_index(inplace=True)
    return _json


if __name__ == '__main__':
    # origin_path = '/data4/1kg_data/data/1kg/HG00096/HG00096_005.bam'
    # output_origin_dir = '/home/phoenix/workspace/tf_data/data/tes'
    # # run_two_pro(origin_path,output_origin_dir,'chr1',output_origin_dir)
    # a = run_aneuploidy_test_bam(
    #     origin_path, output_origin_dir, 'HG00096_005')
    # print(a)
	pkl_path = '/data1/tf_data/test/HG00096_005/HG00096_005.pkl'
	print(get_data(pkl_path))

'''
python ANEUPLOIDY_TEST.py /data2/LD-PGTA/cases/guangxiu/GX_result1/CL100190295_L02_12/CL100190295_L02_12.X.obs.p /data2/LD-PGTA/ref_panel/chrX/X_eas.legend.gz /data2/LD-PGTA/ref_panel/chrX/X_eas.hap.gz EAS --window-size 0 --min-reads 6 --max-reads 4 --compress bz2 --output-dir /data2/LD-PGTA/cases/guangxiu/GX_result1
'''
