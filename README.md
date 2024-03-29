# 低深度WGS异倍体检测流程

## 依赖工具
- bwa
- samtools

## 安装python 依赖 (建议使用独立python环境)

```bash
pip install -r requirements.txt
```
## 数据库文件准备
以下文件需要放在heteroploidy_hunter/data目录下
```bash
╰─$ ll data
total 29M
-rw-rw-r-- 1 phoenix phoenix 2.3M  4月 27 09:43 BGRU.model.125_at.h5
-rw-rw-r-- 1 phoenix phoenix 997K  4月 27 09:43 BGRU.model.50_at.h5
-rw-rw-r-- 1 phoenix phoenix 7.6M  2月  7  2023 bluefuse_by_chrom.txt
drwxr-xr-x 4 phoenix phoenix 4.0K  2月  7  2023 control
-rw-rw-r-- 1 phoenix phoenix 786K  2月  7  2023 GRU.model.h5
-rw-rw-r-- 1 phoenix phoenix 669K  2月  7  2023 igsr_samples.tsv
-rw-rw-r-- 1 phoenix phoenix  17M  2月  7  2023 ldpgta_by_chrom.txt
drwxrwxr-x 2 phoenix phoenix 4.0K  2月  7  2023 MODELS
-rw-rw-r-- 1 phoenix phoenix 2.3K  2月  7  2023 README.md
drwxrwxr-x 4 phoenix phoenix 4.0K 10月 10 09:55 ref_panel
drwxrwxr-x 4 phoenix phoenix 4.0K 10月 10 09:54 ref_path
-rw-rw-r-- 1 phoenix phoenix  48K 10月 10 16:01 upd-disease.xls
drwxrwxr-x 2 phoenix phoenix 4.0K  2月 28  2023 zscore
```

## 使用方法
- 异倍体分析流程运行
    ```bash
    ╰─$ python -m heteroploidy_hunter run --help
	Usage: python -m heteroploidy_hunter run [OPTIONS] [INPUT_PATH] [OUTPUT_PATH]

	Arguments:
	[INPUT_PATH]   输入文件的绝对路径
	[OUTPUT_PATH]  输出文件夹的绝对路径

	Options:
	--input-class TEXT            输入文件的类型是文件夹或者单个文件(one or mult)  [default: one]
	--file-class TEXT             输入文件的类型fq文件或bam文件(fq or bam)  [default: fq]
	--ref TEXT                    基因组版本号  [default: hg19]
	--debug / --no-debug          输出debug信息  [default: no-debug]
	--np INTEGER                  使用CPU核数量  [default: 32]
	--sample-id TEXT              输出样本结果文件名，不指定使用fq/bam文件名（仅单文件分析模式适用）
	--include-x / --no-include-x  是否输出X染色体信息  [default: no-include-x]
	--help                        Show this message and exit.
    ```
- 根据样本编号、fq路径配置文件单线程执行
  样本编号、fq路径配置文件格式(**TAB分割，无表头**，"sample_id fq-path")

    |          |             |
    | -------- | ----------- |
    | sample-1 | /path/to/fq |
    | sample-2 | /path/to/fq |


    ```bash
    ╰─$ python -m heteroploidy_hunter run-file --help
    Usage: python -m heteroploidy_hunter run-file [OPTIONS]

    Options:
    --sample-info TEXT    样本信息表格, TAB分割，"sample_id fq-path"  [required]
    --result-dir TEXT     结果文件夹  [required]
    --debug / --no-debug  输出debug信息  [default: no-debug]
    --help                Show this message and exit.
  ```

- 根据样本编号、fq路径配置文件多线程执行
    ```bash
    ╰─$ python -m heteroploidy_hunter run-file-parallel --help
    Usage: python -m heteroploidy_hunter run-file-parallel [OPTIONS]

    Options:
    --workers INTEGER     使用CPU核数量  [default: 4]
    --sample-info TEXT    样本信息表格, TAB分割，"sample_id fq-path"  [required]
    --result-dir TEXT     结果文件夹  [required]
    --debug / --no-debug  输出debug信息  [default: no-debug]
    --help                Show this message and exit.
    ```
- 分析结果统计
    ```bash
    ╰─$ python -m heteroploidy_hunter zscore --help
    Usage: python -m heteroploidy_hunter zscore [OPTIONS] [INPUT_DIR]
                                            [OUTPUT_FILE] [FQ_DIR]

	Arguments:
	[INPUT_DIR]    pkl result directory
	[OUTPUT_FILE]  output directory
	[FQ_DIR]       directory containing all fq files

	Options:
  	--help  Show this message and exit.
  	```
- LOH分析
	```bash
	╰─$ python -m heteroploidy_hunter rnn-pre-loh --help
	Usage: python -m heteroploidy_hunter rnn-pre-loh [OPTIONS] [INPUT_PKL]
                                                 [OUTPUT_DIR]

	Arguments:
	[INPUT_PKL]   pkl result file
	[OUTPUT_DIR]  output directory

	Options:
	--thread-num INTEGER          使用CPU核数量  [default: 22]
	--interval INTEGER            合并区域的间隔大小  [default: 2100000]
	--length INTEGER              筛选LOH的区域长度  [default: 3500000]
	--deepth / --no-deepth        深度是否大于0.5  [default: deepth]
	--include-x / --no-include-x  是否输出X染色体信息  [default: no-include-x]
	--help                        Show this message and exit.
	```
- LOH注释
	```bash
	╰─$ python -m heteroploidy_hunter anno --help
	Usage: python -m heteroploidy_hunter anno [OPTIONS] [INPUT_TXT] [OUTPUT_DIR]

	Arguments:
	[INPUT_TXT]   loh的输出txt文件
	[OUTPUT_DIR]  output directory

	Options:
	--help  Show this message and exit.
	```