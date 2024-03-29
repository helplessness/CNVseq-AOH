# 低深度WGS异倍体检测流程

## 依赖工具
- bwa
- samtools

## 安装python 依赖 (建议使用独立python环境)

```bash
pip install -r requirements.txt
```
## 数据库文件准备
以下文件需要放在LP_WGS_hunter/data目录下

特征提取参考[LD-PGTA](https://github.com/mccoy-lab/LD-PGTA)

[数据下载链接](https://drive.google.com/drive/folders/1oPje84IvxaD54kRCg78lywJFo6Q9n0L0?usp=drive_link)
```bash
╰─$ ll data
total 29M
-rw-rw-r-- 1 phoenix phoenix 2.3M  4月 27 09:43 BGRU.model.125_at.h5
-rw-rw-r-- 1 phoenix phoenix 997K  4月 27 09:43 BGRU.model.50_at.h5
drwxrwxr-x 2 phoenix phoenix 4.0K  2月  7  2023 MODELS
drwxrwxr-x 4 phoenix phoenix 4.0K 10月 10 09:55 ref_panel
drwxrwxr-x 4 phoenix phoenix 4.0K 10月 10 09:54 ref_path
```

```
ref_path
├── hg19
│   ├── hg19.fa
│   ├── hg19.fa.amb
│   ├── hg19.fa.ann
│   ├── hg19.fa.bwt
│   ├── hg19.fa.fai
│   ├── hg19.fa.pac
│   └── hg19.fa.sa
└── hg38
    ├── hg38bwaidx.amb
    ├── hg38bwaidx.ann
    ├── hg38bwaidx.bwt
    ├── hg38bwaidx.pac
    ├── hg38bwaidx.sa
    ├── hg38.fa
    └── hg38.fa.fai
```


## 使用方法
- 特征提取流程
    ```bash
    ╰─$ python -m LP_WGS_hunter run --help
	Usage: python -m LP_WGS_hunter run [OPTIONS] [INPUT_PATH] [OUTPUT_PATH]

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

- LOH分析
	```bash
	╰─$ python -m LP_WGS_hunter rnn-pre-loh --help
	Usage: python -m LP_WGS_hunter rnn-pre-loh [OPTIONS] [INPUT_PKL]
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
