# %%
from pathlib import Path
import subprocess as sp
import os
from LP_WGS_hunter import config

# ref_path =  os.path.join(config.REF_DIR, 'hg38bwaidx')
# ref_path =  os.path.join(config.REF_DIR,'hg19.fa')
# ref_path = '/data2/hg38/hg38bwaidx'

# %%


def align(fq_file: Path, result_dir: str, prefix, np=5,debug=False,ref='hg19') -> str:
    # ref_path =  os.path.join(config.REF_DIR, 'hg38bwaidx')
    ref_path =  os.path.join(config.REF_DIR_19,'hg19.fa') if ref=='hg19' else os.path.join(config.REF_DIR_38, 'hg38bwaidx')
    bam_file = os.path.join(result_dir,prefix+'.bam')
    if os.path.exists(bam_file):
        return bam_file
    bwa_cmd = f'bwa aln -t {np} {ref_path} {fq_file.as_posix()} > {result_dir}/{prefix}.bwa'
    samse_cmd = f'bwa samse {ref_path} {result_dir}/{prefix}.bwa {fq_file.as_posix()} > {result_dir}/{prefix}.sam'

    sam2bam_cmd = f'samtools view -bS -F 4 {result_dir}/{prefix}.sam | samtools sort -@ 10 -o {bam_file}'
    idx_cmd = f'samtools index {result_dir}/{prefix}.bam {result_dir}/{prefix}.bai'
    print('run: ', bwa_cmd)
    code, status = sp.getstatusoutput(bwa_cmd)
    print(code, status)
    print('run: ', samse_cmd)
    code, status = sp.getstatusoutput(samse_cmd)
    print(code, status)
    print('run: ', sam2bam_cmd)
    code, status = sp.getstatusoutput(sam2bam_cmd)
    print(code, status)
    print('run: ', idx_cmd)
    code, status = sp.getstatusoutput(idx_cmd)
    print(code, status)
    if not debug:
        print('cleaning workspace, rm tmp files ...')
        os.system(f'rm {result_dir}/{prefix}.bwa')
        os.system(f'rm {result_dir}/{prefix}.sam')
    if os.path.exists(bam_file):
        return bam_file
    raise Exception('failed to align fq to bam')


def align_pe(fq_file1: Path,fq_file2:Path, result_dir: str, prefix, np=5,debug = False,ref='hg19') -> str:
    ref_path =  os.path.join(config.REF_DIR_19,'hg19.fa') if ref=='hg19' else os.path.join(config.REF_DIR_38, 'hg38bwaidx')
    bam_file = os.path.join(result_dir,prefix+'.bam')
    if os.path.exists(bam_file):
        return bam_file
    bwa_cmd = f'bwa mem -t {np} {ref_path} {fq_file1.as_posix()} {fq_file2.as_posix()} > {result_dir}/{prefix}.sam'
    # samse_cmd = f'bwa samse {ref_path} {result_dir}/{prefix}.bwa {fq_file.as_posix()} > {result_dir}/{prefix}.sam'
    sam2bam_cmd = f'samtools view -bS -F 4 {result_dir}/{prefix}.sam | samtools sort -@ 10 -o {bam_file}'
    idx_cmd = f'samtools index {result_dir}/{prefix}.bam {result_dir}/{prefix}.bai'

    code, status = sp.getstatusoutput(bwa_cmd)
    print(code, status)
    code, status = sp.getstatusoutput(sam2bam_cmd)
    print(code, status)
    code, status = sp.getstatusoutput(idx_cmd)
    print(code, status)
    if not debug:
        os.system(f'rm {result_dir}/{prefix}.bwa')
        os.system(f'rm {result_dir}/{prefix}.sam')
    if os.path.exists(bam_file):
        return bam_file
    raise Exception('failed to align fq to bam')



# bwa mem ref.fa read1.fq read2.fq > mem-pe.sam