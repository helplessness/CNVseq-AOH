


import os
import subprocess
import pathlib as pl
import os

def get_reads_by_num(num, fastq,out_dir):
    '''
    获取指定数量的reads
    '''
    fastq = pl.Path(fastq)
    output_name = fastq.name.split('.')[0]+'.fq'
    output_file = pl.Path(out_dir)/output_name
    cmd1 = 'seqtk sample -s 100 {} {}> {}'.format(fastq, num, output_file)
    cmd2 = 'gzip {}'.format(output_file)
    cmd_list = [cmd1,cmd2]
    for cmd in cmd_list:
        if subprocess.call(cmd, shell=True):
            raise Exception("{} 执行失败".format(cmd))
    print('{} 执行成功'.format(fastq))


def get_ratio_by_bam(random_seed,num, bam_file,out_dir):
    '''
    获取指定数量的reads
    '''
    bam_file = pl.Path(bam_file)
    output_name = bam_file.name.split('.')[0]

    output_file_dir = pl.Path(out_dir)/str(random_seed).replace('.','')/'bam'
    if not output_file_dir.exists():
        output_file_dir.mkdir(parents=True)
    result_dir = pl.Path(out_dir)/str(random_seed).replace('.','')/'result'
    if not result_dir.exists():
        result_dir.mkdir(parents=True)
    output_file_choutiname= os.path.join(output_file_dir,str(output_name)+'_'+str(random_seed).replace('.','')+'_chouti.bam')
    output_file_name= os.path.join(output_file_dir,str(output_name)+'_'+str(random_seed).replace('.','')+'.bam')
    output_file_name_bai= os.path.join(output_file_dir,str(output_name)+'_'+str(random_seed).replace('.','')+'.bai')
    cmd1 = 'java -jar /home/phoenix/workspace/tf_data/software/picard.jar DownsampleSam -I {} -O {} -R {} -P {}'.format(bam_file.as_posix(),output_file_choutiname,random_seed ,num)
    cmd2 = 'samtools sort -@ 10 -o {} {}'.format(output_file_name,output_file_choutiname)
    cmd3 = 'samtools index {} {}'.format(output_file_name,output_file_name_bai)
    for cmd in [cmd1,cmd2,cmd3]:
        if subprocess.call(cmd, shell=True):
            raise Exception("{} 执行失败".format(cmd))
    print('{} 执行成功'.format(bam_file))
    return output_file_name,result_dir.as_posix()

# num = 0.1
# bam_file = '/data1/LOH_result/origin/CNR0104885/CNR0104885.bam'
# out_dir = '/data1/LOH_result'
# a,b = get_ratio_by_bam(num,bam_file,out_dir)
# print(a,b)