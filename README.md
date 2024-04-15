# LP_WGS_hunter
 We developed a method for predicting the absence of heterozygosity using LP GS data, which overcomes the sparse nature of typical LP GS by combing population-based haplotype information, adjustable sliding windows, and RNN.

Data and results described in the manuscript can be found here：

A tutorial and description of the software can be found here：
# Docker image run

```
docker build Dockerfile -t ldwgs:v1

docker run -it --rm -v /home/phoenix/data/:/data ldwgs:v1

docker run -v /LP_WGS_hunter:/LP_WGS_hunter -v your_input_dir:/input_dir -v your_output_dir:/output_dir --rm -e PYTHONPATH=/LP_WGS_hunter ldwgs:v1 python3 -m LP_WGS_hunter --help
```

# Localized installation

## Dependency tools
- bwa
- samtools

## Install python dependencies (astandalone python environment is recommended)

```bash
pip install -r requirements.txt
```
## Database file preparation
The following files need to be stored in the LP_WGS_hunter/data directory

Feature Extraction Reference [LD-PGTA](https://github.com/mccoy-lab/LD-PGTA)

[Data download link](https://drive.google.com/drive/folders/1oPje84IvxaD54kRCg78lywJFo6Q9n0L0?usp=drive_link)
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


## How to use?
- Feature extraction process
    ```bash
    ╰─$ python -m LP_WGS_hunter run --help
	Usage: python -m LP_WGS_hunter run [OPTIONS] [INPUT_PATH] [OUTPUT_PATH]

	Arguments:
		[INPUT_PATH]   the absolute path to the input file
		[OUTPUT_PATH]  The absolute path to the output folder

	Options:
		--input-class TEXT            The type of input file is a folder or a single
										file (one or mult).  [default: one]
		--file-class TEXT             Type of input file fq file or bam file (fq or
										bam)  [default: fq]
		--ref TEXT                    Genome version number  [default: hg19]
		--debug / --no-debug          Output debugging information  [default: no-
										debug]
		--np INTEGER                  Number of CPU cores used  [default: 32]
		--sample-id TEXT              Output sample result file name, fq/bam file
										name is not specified (single file analysis
										mode only applies)
		--include-x / --no-include-x  Whether to output X chromosome information
										[default: no-include-x]
		--help                        Show this message and exit.
    ```

- LOH analysis
	```bash
	╰─$ python -m LP_WGS_hunter rnn-pre-loh --help
	Usage: python -m LP_WGS_hunter rnn-pre-loh [OPTIONS] [INPUT_PKL]
                                                 [OUTPUT_DIR]

	Arguments:
		[INPUT_PKL]   pkl result file
		[OUTPUT_DIR]  output directory

	Options:
		--thread-num INTEGER          Number of CPU cores used  [default: 22]
		--interval INTEGER            The interval size of the merge area  [default:
										2100000]
		--length INTEGER              Filter the area length of the LOH  [default:
										3500000]
		--deepth / --no-deepth        The depth is greater than 0.5X,used to select
										a different model, the default is 125KB model
										[default: deepth]
		--include-x / --no-include-x  Whether to output X chromosome information
										[default: no-include-x]
		--help                        Show this message and exit.
	```
