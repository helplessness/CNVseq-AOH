FROM ubuntu:20.04

RUN apt-get update \
      && apt-get install -y git wget python3.8 python3-distutils pip build-essential libncurses5-dev zlib1g-dev libbz2-dev liblzma-dev libcurl3-dev


ADD requirements.txt ./
RUN pip3 install -r requirements.txt

RUN git clone https://github.com/lh3/bwa.git \
	  && cd bwa \
	  && make \
	  && cp bwa /usr/local/bin

RUN wget https://github.com/samtools/samtools/releases/download/1.9/samtools-1.9.tar.bz2 \
	&& tar jxf samtools-1.9.tar.bz2 \
	&& rm samtools-1.9.tar.bz2 \
	&& cd samtools-1.9 \
	&& make \
	&& cp samtools /usr/local/bin



# docker run -v /LP_WGS_hunter:/LP_WGS_hunter -v your_input_dir:/input_dir -v your_output_dir:/output_dir --rm -e PYTHONPATH=/LP_WGS_hunter docker_imageId python3 -m LP_WGS_hunter --help