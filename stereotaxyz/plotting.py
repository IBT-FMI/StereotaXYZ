import matplotlib
import matplotlib.pyplot as plt
import nibabel as nib
import numpy as np
import nibabel as nib
import numpy as np
from copy import deepcopy
from matplotlib import rcParams
from nilearn.plotting import plot_stat_map, plot_roi, plot_anat
from os import path
from stereotaxyz import skullsweep

THIS_PATH = path.dirname(path.realpath(__file__))

def plot_yz(df,
	target="",
	entry=[],
	angle=0.,
	resolution=1000,
	stereotaxis_style_angle=True,
	color_skull='gray',
	color_target='orange',
	color_implant='c',
	color_entry='r',
	color_projection='',
	custom_style=False,
	implant_axis=True,
	):
	"""Create a 2D plot (along the YZ plane) containing structures of interest recorded in a StereotaXYZ-style (e.g. `stereotaxyz.skullsweep`-outputted) DataFrame.

	Parameters
	----------

	df : pandas.DataFrame
		A Pandas DataFrame object containing columns named 'posteroanterior', 'inferosuperior', and 'ID'.
	target : str or dict or listi, optional
		Either a string giving the 'ID' column in the `df` input which denotes the target structure row; or a dictionary containing keys named 'posteroanterior' or 'inferosuperior'; or a list of lengtht 2 containing in the first position the posteroanterior and on the second position the inferosuperior coordinates.
	entry : dict or list, optional
		Either a dictionary containing keys named 'posteroanterior' or 'inferosuperior'; or a list of lengtht 2 containing in the first position the posteroanterior and on the second position the inferosuperior coordinates.
	angle : float, optional
		Angle in the YZ-plane.
		The angle can be given with respect to the posterioanterior axis (set `stereotaxis_style_angle` to `False`) or with respect to the inferosuperior axis (set `stereotaxis_style_angle` to `True`).
	resolution : int, optional
		Resolution at which to sample the coordinate space.
	stereotaxis_style_angle : bool, optional
		Whether to set the angle reative to the inferosuperior axis (the other alternative - corresponding to this variable being set to `False` - is that the angle is interpreted as relative to the posteroanterior axis).
	color_skull : str, optional
		Color with which the skull points are to be drawn (this has to be a Matplotlib interpretable string).
		Setting this to an empty string will disable plotting of respective feature.
	color_target : str, optional
		Color with which the target point is to be drawn (this has to be a Matplotlib interpretable string).
		Setting this to an empty string will disable plotting of respective feature.
	color_implant : str, optional
		Color with which the implant and implant axis are to be drawn (this has to be a Matplotlib interpretable string).
		Setting this to an empty string will disable plotting of respective feature.
	color_entry : str, optional
		Color with which the implant entry point is to be drawn (this has to be a Matplotlib interpretable string).
		Setting this to an empty string will disable plotting of respective feature.
	color_entry : str, optional
		Color with which the skull projection points on the implant axis are to be drawn (this has to be a Matplotlib interpretable string).
		Setting this to an empty string will disable plotting of respective feature.
		This is mainly a debugging feature.
	implant_axis : bool, optional
		Whether to plot the implant axis.
	"""

	# Start actual plotting:
	if not custom_style:
		plt.style.use(path.join(THIS_PATH,'stereotaxyz.conf'))

	plt.figure()
	plt.axis('equal')
	ax = plt.axes()

	x_min = df['posteroanterior'].min()-1
	x_max = df['posteroanterior'].max()+1

	if stereotaxis_style_angle:
		angle += 90
	angle = np.radians(angle)
        slope = np.tan(angle)

	if target:
		if isinstance(target, dict):
			x_offset = target['posteroanterior']
			y_offset = target['inferosuperior']
		try:
			x_offset = df[df['ID']==target]['posteroanterior'].values[0]
			y_offset = df[df['ID']==target]['inferosuperior'].values[0]
		except KeyError:
			x_offset, y_offset = target
		intercept = -x_offset*slope + y_offset
		x = np.linspace(x_min,x_max,resolution)
		y = x*slope + intercept

	if entry:
		try:
			x_entry = entry['posteroanterior']
			y_entry = entry['inferosuperior']
		except TypeError:
			x_entry, y_entry = entry

	legend_handles = []
	legend_names = []
	if color_skull:
		skull_plot = ax.scatter(df[df['tissue']=='skull']['posteroanterior'], df[df['tissue']=='skull']['inferosuperior'], color=color_skull)
		legend_handles.append(skull_plot)
		legend_names.append("Skull")
	if target:
		if color_implant and implant_axis:
			implant_axis_plot, = ax.plot(x, y, color=color_implant, linewidth=rcParams['lines.linewidth']*0.5, label='Implant Axis')
		if color_target:
			target_plot = ax.scatter(x_offset, y_offset, color=color_target)
			legend_handles.append(target_plot)
			legend_names.append("Target")
		if color_projection:
			skull_projection_plot = ax.scatter(df[df['tissue']=='skull']['posteroanterior (implant projection)'], df[df['tissue']=='skull']['inferosuperior (implant projection)'], color=color_projection)
			legend_handles.append(skull_projection_plot)
			legend_names.append("Skull Projection")
	if entry and color_entry:
		entry_plot = ax.scatter(x_entry, y_entry, color=color_entry, marker='D')
		legend_handles.append(entry_plot)
		legend_names.append("Entry Point")
	if entry and target and color_implant:
		implant_plot, = ax.plot([x_entry, x_offset],[y_entry,y_offset],  color=color_implant, linewidth=rcParams['lines.linewidth']*2.)
		legend_handles.append(implant_plot)
		legend_names.append("Implant")
	# These (less important) items should be at the end of the legend, though they should also be plotted underneath (i.e. before) all others.
	try:
		legend_handles.append(implant_axis_plot)
		legend_names.append("Implant Axis")
	except NameError:
		pass
	legend = ax.legend(legend_handles, legend_names)

def co_plot(target, skullsweep_data,
	yz_angle=0,
	xz_angle=0,
	angle_axis='x',
	custom_style=False,
	template='~/ni_data/templates/DSURQEc_40micron_average.nii',
	text_output=False,
	projection_color='',
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
			target_z = target_df['inferosuperior'].item()
		except KeyError:
			target_z = 0
		target_coords = [(target_y, target_x, target_z)]
	if text_output:
		print(target_coords)

	t, posteroanterior, inferosuperior, leftright, df_ = skullsweep.implant_by_angle(target, animal_df,
		yz_angle=yz_angle,
		)
	insertion_site = [(leftright, posteroanterior, inferosuperior)]

	if projection_color:
		projection_df = deepcopy(df_)
		projection_df['posteroanterior'] = projection_df['posteroanterior (implant projection)']
		projection_df['inferosuperior'] = projection_df['inferosuperior (implant projection)']
		projection_df['leftright'] = projection_df['leftright (implant projection)']
		projection_img = make_nii(projection_df, template='~/ni_data/templates/DSURQEc_200micron_average.nii')
		projection_color = matplotlib.colors.ListedColormap([projection_color], name='projection_color')

	# Start actual plotting:
	if not custom_style:
		try:
			plt.style.use('stereotaxyz.conf')
		except IOError:
			pass
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
	if projection_color:
		display.add_overlay(projection_img, cmap=projection_color)
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


