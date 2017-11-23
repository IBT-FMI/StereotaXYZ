import matplotlib.pyplot as plt
from stereotaxyz import skullsweep
from stereotaxyz.plotting import make_nii
from nilearn.plotting import plot_stat_map, plot_roi
from os import path
from matplotlib import cm

data_dir = path.join(path.dirname(path.realpath(__file__)),"../example_data")
data_file = path.join(data_dir,'skull_6465.csv')
df = skullsweep.load_data(data_file)

df_slice = df[df['tissue']=='skull']
img = make_nii(df_slice, template='~/ni_data/templates/DSURQEc_200micron_average.nii')

plot_roi(img, bg_img='/home/chymera/ni_data/templates/DSURQEc_40micron_average.nii', draw_cross=False, cmap=cm.Pastel1)
plt.show()
