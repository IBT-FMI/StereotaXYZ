import matplotlib.pyplot as plt
from stereotaxyz import skullsweep
from stereotaxyz import plotting
from nilearn.plotting import plot_stat_map, plot_roi, plot_anat
from os import path
import matplotlib

data_dir = path.join(path.dirname(path.realpath(__file__)),"../example_data")
data_file = path.join(data_dir,'skull_6465.csv')
df = skullsweep.load_data(data_file)

def basic():
	ax = skullsweep.draw_anatomy(df)
	skullsweep.implant(30,'VTA',df,ax,'orange','best')
	plt.show()

def old():
	plt.style.use('stereotaxyz.conf')
	plt.figure()
	plt.axis('equal')
	ax = plt.axes()
	skull_df = df[df['tissue']=='skull']
	skull_img = make_nii(skull_df, template='~/ni_data/templates/DSURQEc_200micron_average.nii')
	skullcolor = matplotlib.colors.ListedColormap(['#FFFFFF'], name='skullcolor')
	plot_roi(skull_img,
		bg_img='/home/chymera/ni_data/templates/DSURQEc_40micron_average.nii',
		cut_coords=(0,),
		display_mode='x',
		draw_cross=False,
		cmap=skullcolor,
		axes=ax,
		alpha=1.0,
		)
	plt.show()

def demo():
	plotting.co_plot('DR',data_file, angle=30,)
