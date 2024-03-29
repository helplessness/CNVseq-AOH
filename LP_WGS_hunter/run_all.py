

# %%
import add_all
import os
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
from pathlib import Path
import pickle

sns.set()


# %%
control_dir = Path('/data2/LD-PGTA/control')
fq_file = Path(
    '/data2/LD-PGTA/cases/cnv-seq-test1/62')
output_dir = Path('/data2/LD-PGTA/cases/cnv-seq-test1/62')
sample_name = 'V350020055_L04_67'

# %%
if not output_dir.exists():
    output_dir.mkdir(parents=True)

pkl = add_all.run_aneuploidy_test(fq_file, output_dir, prefix=sample_name)
df = add_all.get_data(pkl_file=pkl)

# %%
li = []
for file in control_dir.rglob('*.pkl'):
    _df = add_all.get_data(pkl_file=file)
    if file.parent.name == 'pos':
        _df['karyotype'] = 'triploid'
    else:
        _df['karyotype'] = 'diploid'
    li.append(_df)
df_control = pd.concat(li)
df_control.reset_index(inplace=True, drop=True)

# %%
df['karyotype'] = 'V350020055_L04_67'
df.reset_index(inplace=True, drop=True)
# %%
df_all = pd.concat([df, df_control], ignore_index=True)
ax, fig = plt.subplots(figsize=(10, 5))

g = sns.lineplot(
    data=df_all, x='index', y='mean_of_mean', hue='karyotype'
)
g.set_xlabel('Chromosome')
g.set_xticks(range(1, 23))
g.set_xticklabels(range(1, 23))
g.set_ylabel('Likelihood')

plt.savefig(output_dir / 'aneuploidy.png')
#fig.savefig(output_dir / 'aneuploidy_test.png')

