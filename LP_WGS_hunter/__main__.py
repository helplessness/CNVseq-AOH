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
app = typer.Typer(help='PGTA异倍体分析')

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
                print('确认文件是否为fq或bam')
        except Exception as e:
            logging.info(str(e))
            logging.info(sample_name+'\n')
            pass



@app.command()
def run(input_path: str = typer.Argument(help='输入文件的绝对路径', default=None),
        output_path: str = typer.Argument(help='输出文件夹的绝对路径', default=None),
        input_class: str = typer.Option(
        help='输入文件的类型是文件夹或者单个文件(one or mult)', default='one'),
        file_class: str = typer.Option(
        help='输入文件的类型fq文件或bam文件(fq or bam)', default='fq'),
        ref: str = typer.Option(
        help='基因组版本号', default='hg19'),
        debug: bool = typer.Option(help='输出debug信息', default=False),
        np: int = typer.Option(help='使用CPU核数量', default=32),
        sample_id: str = typer.Option(help='输出样本结果文件名，不指定使用fq/bam文件名（仅单文件分析模式适用）', default=None),
        include_x:bool = typer.Option(help='是否输出X染色体信息', default=False),
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
def run_file(
    sample_info: str = typer.Option(..., help='样本信息表格, TAB分割，"sample_id fq-path"'),
    result_dir: str = typer.Option(..., help='结果文件夹'),
    ref: str = typer.Option(help='基因组版本号', default='hg19'),
    debug: bool = typer.Option(help='输出debug信息', default=False),
    include_x:bool = typer.Option(help='是否输出X染色体信息', default=False),
):
    sample_df = pd.read_csv(sample_info, sep='\t', names=['sample_id', 'fq_path'])
    for idx, row in sample_df.iterrows():
        print(f'processing sample ({idx}):', row['sample_id'])
        run(
            input_path=row['fq_path'], output_path=result_dir, input_class='one',
            file_class='fq', debug=debug, sample_id=row['sample_id'], np=10,include_x=include_x,ref=ref
        )

@app.command()
def run_file_parallel(
    workers: int = typer.Option(help='使用CPU核数量', default=4),
    sample_info: str = typer.Option(..., help='样本信息表格, TAB分割，"sample_id fq-path"'),
    result_dir: str = typer.Option(..., help='结果文件夹'),
    debug: bool = typer.Option(help='输出debug信息', default=False),
    ref: str = typer.Option(help='基因组版本号', default='hg19'),
    include_x:bool = typer.Option(help='是否输出X染色体信息', default=False),
):
    debug_flag = '--debug' if debug else '--no-debug'
    include_x = '--include-x' if include_x else '--no-include-x'
    sample_df = pd.read_csv(sample_info, sep='\t', names=['sample_id', 'fq_path'])
    chunk_size = int(len(sample_df) / workers)
    task_li = []
    with tempfile.TemporaryDirectory(dir=result_dir) as tmp_dir:
        for idx, chunk in enumerate([sample_df[i:i+chunk_size] for i in range(0, len(sample_df), chunk_size)]):
            tmp_sample_info = os.path.join(tmp_dir, f'{idx}.tsv')
            chunk.to_csv(tmp_sample_info, sep='\t', index=False, header=False)
            task_li.append(
                sub.Popen([
                    "python", "-m", "heteroploidy_hunter", "run-file", "--sample-info",
                    tmp_sample_info, "--result-dir", result_dir,"--ref", ref, debug_flag,include_x
                    ])
                )
        for task in task_li:
            task.wait()
    print('finish all tasks')


@app.command()
def rnn_pre_loh(
    input_pkl: str = typer.Argument(help='pkl result file', default=None),
    output_dir: str = typer.Argument(help='output directory', default=None),
    thread_num: int = typer.Option(help='使用CPU核数量', default=22),
    interval: int = typer.Option(help='合并区域的间隔大小', default=2100000),
    length: int = typer.Option(help='筛选LOH的区域长度', default=3500000),
    deepth: bool = typer.Option(help='深度是否大于0.5', default=True),
    include_x:bool = typer.Option(help='是否输出X染色体信息', default=False)
):
    pre_loh.run_loh_pre(input_pkl,output_dir,thread_num,interval,length,deepth,include_x=include_x)


if __name__ == '__main__':
    app()
