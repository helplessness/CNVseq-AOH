import os
import typer
import logging
from pathlib import Path
from LP_WGS_hunter import config
from LP_WGS_hunter import run_all_piliang
from LP_WGS_hunter import run_from_bam
import collections
import pandas as pd
import math
from concurrent.futures import ProcessPoolExecutor as Pool
from multiprocessing import current_process
import subprocess as sub
import tempfile
from LP_WGS_hunter import pre_loh

LOG_FORMAT = '%(asctime)s-%(levelname)s-%(filename)s(%(lineno)s)-%(message)s'
app = typer.Typer(help='Recurrent neural network for predicting absence of heterozygosity from low pass WGS with ultra-low depth')

# Encodes the rows of the legend table
leg_tuple = collections.namedtuple(
    'leg_tuple', ('chr_id', 'pos', 'ref', 'alt'))
# Encodes the rows of the samples table
sam_tuple = collections.namedtuple(
    'sam_tuple', ('sample_id', 'group1', 'group2', 'sex'))
# Encodes the rows of the observations table
obs_tuple = collections.namedtuple('obs_tuple', ('pos', 'read_id', 'base'))


def mult_file(output_origin_dir, origin_path, control_dir, file_class, debug, np=32,include_x=False,ref='hg19'):
    log_level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(filename=os.path.join(
        output_origin_dir, 'output.log'), format=LOG_FORMAT, level=log_level, filemode='w')
    if file_class == 'fq':
        for file_name in origin_path.rglob('*.fq.gz'):
            if '_unmap' not in file_name.name:
                sample_name = file_name.name.split('.')[0]
                output_dir = os.path.join(output_origin_dir, sample_name)
                if not os.path.exists(output_dir):
                    os.mkdir(output_dir)
                try:
                    run_all_piliang.run_main(
                        file_name, output_dir, sample_name, control_dir, np=np,include_x=include_x,ref=ref)
                except Exception as e:
                    logging.info('skip', sample_name, str(e))
    elif file_class == 'bam':
        for file_name in origin_path.rglob('*.bam'):
            sample_name = file_name.name.split('.')[0]
            output_dir = os.path.join(output_origin_dir, sample_name)
            if not os.path.exists(output_dir):
                os.mkdir(output_dir)
            try:
                run_from_bam.run_main_bam(
                    file_name.as_posix(), output_dir,
                    sample_name, control_dir, np=np,include_x=include_x,ref=ref
                )
            except Exception as e:
                logging.info('skip', sample_name, str(e))
    else:
        raise('invalid file class, should be fq or bam')


def one_file(output_origin_dir, origin_path, control_dir, file_class, debug, sample_name=None, np=32,include_x=False,ref='hg19'):
    log_level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(filename=os.path.join(
        output_origin_dir, 'output.log'), format=LOG_FORMAT, level=log_level, filemode='w')
    file_name = Path(origin_path)
    if '_unmap' not in file_name.name:
        sample_name = file_name.name.split('.')[0] if sample_name is None else sample_name
        output_dir = os.path.join(output_origin_dir, sample_name)
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)
        try:
            if file_class == 'fq':
                run_all_piliang.run_main(
                    file_name, output_dir, sample_name, control_dir, np=np,include_x=include_x,ref=ref)
            elif file_class == 'bam':
                run_from_bam.run_main_bam(file_name.as_posix(
                ), output_dir, sample_name, control_dir, np=np,include_x=include_x,ref=ref)
            else:
                print('Verify that the file is fq or bam')
        except Exception as e:
            logging.info(str(e))
            logging.info(sample_name+'\n')
            pass



@app.command()
def run(input_path: str = typer.Argument(help='the absolute path to the input file', default=None),
        output_path: str = typer.Argument(help='The absolute path to the output folder', default=None),
        input_class: str = typer.Option(
        help='The type of input file is a folder or a single file (one or mult).', default='one'),
        file_class: str = typer.Option(
        help='Type of input file fq file or bam file (fq or bam)', default='fq'),
        ref: str = typer.Option(
        help='Genome version number', default='hg19'),
        debug: bool = typer.Option(help='Output debugging information', default=False),
        np: int = typer.Option(help='Number of CPU cores used', default=32),
        sample_id: str = typer.Option(help='Output sample result file name, fq/bam file name is not specified (single file analysis mode only applies)', default=None),
        include_x:bool = typer.Option(help='Whether to output X chromosome information', default=False),
        ):

    control_dir = Path(config.CONREOL_DIR)
    origin_path = Path(input_path)
    output_origin_dir = Path(output_path)
    if not os.path.exists(output_origin_dir):
        os.mkdir(output_origin_dir)
    if input_class == 'one':
        one_file(output_origin_dir, origin_path,
                 control_dir, file_class, debug, np=np, sample_name=sample_id,include_x=include_x,ref=ref)
    elif input_class == 'mult':
        mult_file(output_origin_dir, origin_path,
                  control_dir, file_class, debug, np=np,include_x=include_x,ref=ref)
    # if not debug:
    #     print('cleaning workspace, rm tmp files ...')
    #     os.system(f'rm {output_origin_dir}/*/*.sam')
    #     os.system(f'rm {output_origin_dir}/*/*.bwa')


@app.command()
def rnn_pre_loh(
    input_pkl: str = typer.Argument(help='pkl result file', default=None),
    output_dir: str = typer.Argument(help='output directory', default=None),
    thread_num: int = typer.Option(help='Number of CPU cores used', default=22),
    interval: int = typer.Option(help='The interval size of the merge area', default=2100000),
    length: int = typer.Option(help='Filter the area length of the LOH', default=3500000),
    deepth: bool = typer.Option(help='The depth is greater than 0.5X,used to select a different model, the default is 125KB model', default=True),
    include_x:bool = typer.Option(help='Whether to output X chromosome information', default=False)
):
    pre_loh.run_loh_pre(input_pkl,output_dir,thread_num,interval,length,deepth,include_x=include_x)


if __name__ == '__main__':
    app()
