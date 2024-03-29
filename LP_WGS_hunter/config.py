import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR,'data')
MODEL_DIR = os.path.join(DATA_DIR,'MODELS')
REF_DIR_19 =os.path.join(os.path.join(DATA_DIR,'ref_path'),'hg19')
REF_DIR_38 =os.path.join(os.path.join(DATA_DIR,'ref_path'),'hg38')
REF_PANEL_DIR_19 = os.path.join(os.path.join(DATA_DIR,'ref_panel'),'hg19')
REF_PANEL_DIR_38 = os.path.join(os.path.join(DATA_DIR,'ref_panel'),'hg38')
CONREOL_DIR = os.path.join(DATA_DIR,'control')
ZSCORE_DIR = os.path.join(DATA_DIR,'zscore')
LOH_MODEL_high = os.path.join(DATA_DIR,'BGRU.model.125_at.h5')
LOH_MODEL_low = os.path.join(DATA_DIR,'BGRU.model.50_at.h5')
UPD_FILE = os.path.join(DATA_DIR,'upd-disease.tsv')