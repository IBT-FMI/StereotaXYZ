import matplotlib.pyplot as plt
from stereotaxyz import skullsweep
from stereotaxyz.plotting import make_nii
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

def template():
	plt.style.use('stereotaxyz.conf')
	plt.figure()
	plt.axis('equal')
	ax = plt.axes()
	display = plot_anat(
		anat_img='/home/chymera/ni_data/templates/DSURQEc_40micron_average.nii',
		display_mode='x',
		draw_cross=False,
		cut_coords=(0,),
		axes=ax,
		)

	skull_df = df[df['tissue']=='skull']
	skull_img = make_nii(skull_df, template='~/ni_data/templates/DSURQEc_200micron_average.nii')
	skullcolor = matplotlib.colors.ListedColormap(['#909090'], name='skullcolor')
	display.add_overlay(skull_img, cmap=skullcolor)

	target_df = df[df['ID']=='DR']
	try:
		target_x = target_df['posteroanterior'].item()
	except KeyError:
		target_x = 0
	try:
		target_y = target_df['leftright'].item()
	except KeyError:
		target_y = 0
	try:
		target_z = -target_df['superoinferior'].item()
	except KeyError:
		target_z = 0

	target_coords = [(target_y, target_x, target_z)]
	print(target_coords)
	display.add_markers(target_coords, marker_color='#E5E520', marker_size=200)

	slope, intercept, pa_in, is_in = skullsweep.implant(30, 'DR', df,
		ax = False,
		color = 'c',
		plot_projections='best',
		)
	insertion_site = [(0, pa_in, is_in)]
	display.add_markers(insertion_site, marker_color='#FFFFFF', marker_size=200)

	plt.show()

