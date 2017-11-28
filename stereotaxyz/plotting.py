import matplotlib
import matplotlib.pyplot as plt
import nibabel as nib
import numpy as np
import nibabel as nib
import numpy as np
from nilearn.plotting import plot_stat_map, plot_roi, plot_anat
from os import path
from stereotaxyz import skullsweep

def co_plot(target, skullsweep_data,
	angle=0,
	angle_axis='x',
	custom_style=False,
	template='~/ni_data/templates/DSURQEc_40micron_average.nii',
	text_output=False,
	save_as='',
	):
	"""Co-plot of skullsweep data points together with target and best entry point coordinates (as computed based on the skullsweep data and the angle of entry).

	Parameters
	----------

	target : str or list or tuple
		Target identifier. Can either be a string (identifying a row via the 'ID' column of the skullsweep_data DataFrame) or a list or tuple of exactly 3 floats giving the y (leftright), x (posteroanterior), and z (superoinferior) coordinates of the target, in this order.
	skullsweep_data : str or pandas.DataFrame
		Path to a CSV file or `pandas.DataFrame` object containing skullsweep and optionally target coordinates.
		The data should include columns named 'ID', 'posteroanterior', 'superoinferior', 'reference', and 'tissue'.
	angle : float
		Desired angle of entry.
	angle_axis : {'x', 'y'}
		Along which axis the angle should be applied.
		Currently only 'x' is supported.
	custom_style : bool
		Whether to forego the application of a default style.
	template : str
		Path to template (generally an anatomical image) to be used as background.
	text_output : bool
		Whether to print relevant output (computed enrty point coordinates and recommended implant length) to the command line.
	save_as : str
		Path under which to save the output image.
	"""


	template = path.abspath(path.expanduser(template))
	animal_df = skullsweep.load_data(skullsweep_data)

	skull_df = animal_df[animal_df['tissue']=='skull']
	skull_img = make_nii(skull_df, template='~/ni_data/templates/DSURQEc_200micron_average.nii')
	skull_color = matplotlib.colors.ListedColormap(['#909090'], name='skull_color')

	if type(target) is tuple and len(target) == 3:
		target_coords = [target]
	elif type(target) is list and len(target) == 3:
		target_coords = [tuple(target)]
	else:
		target_df = animal_df[animal_df['ID']==target]
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
	if text_output:
		print(target_coords)

	slope, intercept, pa_in, is_in = skullsweep.implant(angle, 'DR', animal_df,
		ax = False,
		color = 'c',
		plot_projections='best',
		)
	insertion_site = [(0, pa_in, is_in)]

	# Start actual plotting:
	if not custom_style:
		plt.style.use('stereotaxyz.conf')
	plt.figure()
	plt.axis('equal')
	ax = plt.axes()
	display = plot_anat(
		anat_img='/home/chymera/ni_data/templates/DSURQEc_40micron_average.nii',
		display_mode=angle_axis,
		draw_cross=False,
		cut_coords=(0,),
		axes=ax,
		alpha=1.0,
		)
	display.add_overlay(skull_img, cmap=skull_color)
	display.add_markers(target_coords, marker_color='#E5E520', marker_size=200)
	display.add_markers(insertion_site, marker_color='#FFFFFF', marker_size=200)
	if not save_as:
		plt.show()

def make_nii(df_slice,
	template='/home/chymera/ni_data/templates/DSURQEc_200micron_average.nii',
	):
	"""Create a NIfTI based on a dataframe containing bregma-relative skullsweep points, and a bregma-origin template.
	"""
	template = nib.load(path.abspath(path.expanduser(template)))
	affine = template.affine
	data = np.zeros(shape=template.shape)
	for ix, point in df_slice.iterrows():
		try:
			x = point['posteroanterior']
		except KeyError:
			try:
				x = -point['anteroposterior']
			except KeyError:
				x = 0
		try:
			y = point['leftright']
		except KeyError:
			try:
				y = -point['rightleft']
			except KeyError:
				y = 0
		try:
			z = point['inferosuperior']
		except KeyError:
			try:
				z = -point['superoinferior']
			except KeyError:
				z = 0
		new_y = (-y-affine[0,3])/affine[0,0]
		new_y = int(round(new_y))
		new_x = (x-affine[1,3])/affine[1,1]
		new_x = int(round(new_x))
		new_z = (z-affine[2,3])/affine[2,2]
		new_z = int(round(new_z))
		data[new_y,new_x,new_z] = 1

	new_image = nib.Nifti1Image(data, affine=affine)
	return new_image


