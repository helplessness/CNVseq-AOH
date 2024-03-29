

from LP_WGS_hunter import PLOT_PANEL
import pathlib
'''
[('BPH', 'SPH'), ('disomy', 'monosomy'), ('BPH', 'disomy'), ('disomy', 'SPH'), ('SPH', 'monosomy')]
'''

def merge_obs(name, work_dir,include_x:False):
    work_dir = pathlib.Path(work_dir)
    result_file = work_dir / f'{name}.pkl'
    PLOT_PANEL.wrap_panel_plot_for_single_indv(
        name, bin_size=4000000, pairs=(('BPH', 'SPH'),('BPH', 'disomy'),('SPH', 'disomy')),
        save=name, work_dir=work_dir.as_posix(), save_file=result_file,include_x=include_x
    )
    if result_file.exists():
        return result_file
    raise Exception('failed to merge obs files')


# if __name__ == '__main__':
# 	name = 'V350101898_L03_41'
# 	work_dir = pathlib.Path('/data1/ceshi/1009/result/V350101898_L03_41')
# 	a = merge_obs(name,work_dir)