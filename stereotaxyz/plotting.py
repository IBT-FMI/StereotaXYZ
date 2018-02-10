# coding: utf-8

import matplotlib
import matplotlib.pyplot as plt
import nibabel as nib
import numpy as np
import pandas as pd
from copy import deepcopy
from matplotlib import rcParams
from matplotlib import patches
from os import makedirs, path
from stereotaxyz import skullsweep

THIS_PATH = path.dirname(path.realpath(__file__))

def yz(df,
	target="",
	incision=[],
	angle=0.,
	resolution=1000,
	stereotaxis_style_angle=True,
	color_skull='gray',
	color_target='orange',
	color_insertion='c',
	color_incision='r',
	color_projection='',
	custom_style=False,
	insertion_axis=True,
	save_as='',
	reference='',
	):
	"""Create a 2D plot (along the YZ plane) containing structures of interest recorded in a StereotaXYZ-style (e.g. `stereotaxyz.skullsweep`-outputted) DataFrame.

	Parameters
	----------

	df : pandas.DataFrame
		A Pandas DataFrame object containing columns named 'posteroanterior', 'inferosuperior', and 'ID'.
	target : str or dict or listi, optional
		Either a string giving the 'ID' column in the `df` input which denotes the target structure row; or a dictionary containing keys named 'posteroanterior' or 'inferosuperior'; or a list of lengtht 2 containing in the first position the posteroanterior and on the second position the inferosuperior coordinates.
	incision : dict or list, optional
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
	color_insertion : str, optional
		Color with which the insertion and insertion axis are to be drawn (this has to be a Matplotlib interpretable string).
		Setting this to an empty string will disable plotting of respective feature.
	color_incision : str, optional
		Color with which the incison point is to be drawn (this has to be a Matplotlib interpretable string).
		Setting this to an empty string will disable plotting of respective feature.
	color_projection : str, optional
		Color with which the skull projection points on the insertion axis are to be drawn (this has to be a Matplotlib interpretable string).
		Setting this to an empty string will disable plotting of respective feature.
		This is mainly a debugging feature.
	insertion_axis : bool, optional
		Whether to plot the insertion axis.
	save_as : str
		Path under which to save the output image.
	reference : string, optional
		Referenc epoint relative to which to compute the coordinate specifications displayed int the figure legend.
		This value must be present once and only once on the 'ID' column of the dataframe passed to the `df` parameter.
	"""

	# Set References
	internal_references = df['reference'].unique()
	internal_reference = internal_references[0]
	if len(internal_references) > 1:
		print(
			'WARNING: The DataFrame you have passed to `stereotaxyz.plotting.yz()` contains rows referenced to multiple values, namely: "{}". '
			'We will assume that all values are referenced to {}. '
			'This means that some of the computations and/or the reference specification for the output may be wrong. '
			.format(references, reference)
		)

	if not reference:
		reference = internal_reference

	if reference != internal_reference:
		x_reference = df[df['ID']==reference]['posteroanterior'].item()
		y_reference = df[df['ID']==reference]['inferosuperior'].item()
	else:
		x_reference = 0
		y_reference = 0

	# Check LeftRight integrity
	leftrights = df['leftright'].unique()
	leftright = leftrights[0]
	if len(leftrights) > 1:
		print(
			'WARNING: The DataFrame you have passed to `stereotaxyz.plotting.yz()` contains multiple leftright axis specifications, namely: "{}". '
			'We will assume that all values are aligned leftright at {}mm. '
			'This means that some of the computations and/or the leftright specification for the output may be wrong.'
			.format(leftrights, leftright)
		)

	# Start actual plotting:
	if not custom_style:
		plt.style.use(path.join(THIS_PATH,'stereotaxyz.conf'))

	plt.figure()
	plt.axis('equal')
	ax = plt.axes()

	x_min = df['posteroanterior'].min()-1
	x_max = df['posteroanterior'].max()+1

	input_angle = angle
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

	if incision:
		try:
			x_incision = incision['posteroanterior']
			y_incision = incision['inferosuperior']
		except TypeError:
			x_incision, y_incision = incision
	else:
		x_incision = df[df['ID']=='incision']['posteroanterior'].values[0]
		y_incision = df[df['ID']=='incision']['inferosuperior'].values[0]


	legend_handles = []
	legend_names = []
	if color_skull:
		skull_plot = ax.scatter(df[df['tissue']=='skull']['posteroanterior'], df[df['tissue']=='skull']['inferosuperior'], color=color_skull)
		legend_handles.append(skull_plot)
		legend_names.append("Skull")
	if target:
		if color_insertion and insertion_axis:
			insertion_axis_plot, = ax.plot(x, y, color=color_insertion, linewidth=rcParams['lines.linewidth']*0.5, label='Insertion Axis')
		if color_projection:
			skull_projection_plot = ax.scatter(df[df['tissue']=='skull']['posteroanterior (insertion projection)'], df[df['tissue']=='skull']['inferosuperior (insertion projection)'], color=color_projection)
			legend_handles.append(skull_projection_plot)
			legend_names.append("Skull Projection")
		if color_target:
			target_plot = ax.scatter(x_offset, y_offset, color=color_target)
			legend_handles.append(target_plot)
			legend_names.append("Target")
	if (x_incision and y_incision) and color_incision:
		incision_plot = ax.scatter(x_incision, y_incision, color=color_incision, marker='D')
		legend_handles.append(incision_plot)
		if reference != internal_reference:
			legend_names.append("Incision [PA/IS={:.2f}/{:.2f}mm]\n\t(relative to {})"
				.format(x_incision-x_reference, y_incision-y_reference, reference)
				.expandtabs()
			)
		else:
			legend_names.append("Incision [PA/IS={:.2f}/{:.2f}mm]".format(x_incision-x_reference, y_incision-y_reference))
	if (x_incision and y_incision) and target and color_insertion:
		insertion_plot, = ax.plot([x_incision, x_offset],[y_incision,y_offset],  color=color_insertion, linewidth=rcParams['lines.linewidth']*2.)
		legend_handles.append(insertion_plot)
		insertion_length = np.abs(df[df['ID']=='incision']['projection t'].item())
		legend_names.append("Insertion [{:.2f}mm]".format(insertion_length))

	# These (less important) items should be at the end of the legend, though they should also be plotted underneath (i.e. before) all others.
	try:
		legend_handles.append(insertion_axis_plot)
		legend_names.append("Insertion Axis")
	except NameError:
		pass
	legend = ax.legend(legend_handles, legend_names)


	ax.set_xlabel('Posteroanterior({}) [mm]'.format(internal_reference))
	ax.set_ylabel('Inferosuperior({}) [mm]'.format(internal_reference))

	ax.set_title(u'{:.0f}° Insertion | Leftright({}) = {:.2f}mm'.format(
		input_angle,
		internal_reference,
		leftright,
		))

	if save_as:
		save_as = path.abspath(path.expanduser(save_as))
		plt.savefig(save_as)

def xyz(df,
	axis_cut='x',
	color_projection='',
	color_skull='#E0E0E0',
	color_incision='#FE2244',
	color_insertion='#22FE11',
	color_target='#FE9911',
	custom_style=False,
	incision=[],
	insertion_resolution=0.1,
	figure_title=u'YZ/XY={:.0f}/{:.0f}° Insertion',
	marker_size=0.2,
	reference='',
	save_as='',
	skull_point_size=0.2,
	target="",
	template='~/ni_data/templates/DSURQEc_40micron_average.nii',
	text_output=False,
	xz_angle=0.,
	yz_angle=0.,
	):
	"""Co-plot of skullsweep data points together with target and incision coordinates (as computed based on the skullsweep data and the angle of entry).

	Parameters
	----------

	df : pandas.DataFrame
		StereotaXYZ-style `pandas.DataFrame` object, best obtained from `stereotaxyz.skulsweep.load_data()`.
	axis_cut : {'x','yx'}
		Specify the axes perpendicularly to which the image should be cut for display.
	custom_style : bool
		Whether to forego the application of a default style.
	figure_title : string, optional
		Title to be  applied to the figure.
		Substitution characters, e.g. `{0}` and `{1}` will be formatted with the yz and xz angle values respectively.
	incision : dict or list, optional
		Either a dictionary containing keys named 'posteroanterior' or 'inferosuperior'; or a list of lengtht 2 containing in the first position the posteroanterior and on the second position the inferosuperior coordinates.
	reference : string, optional
		Referenc epoint relative to which to compute the coordinate specifications displayed int the figure legend.
		This value must be present once and only once on the 'ID' column of the dataframe passed to the `df` parameter.
	save_as : str
		Path under which to save the output image.
	skullsweep_data : str or pandas.DataFrame
		Path to a CSV file or `pandas.DataFrame` object containing skullsweep and optionally target coordinates.
		The data should include columns named 'ID', 'posteroanterior', 'superoinferior', 'reference', and 'tissue'.
	target : str or list or tuple
		Target identifier. Can either be a string (identifying a row via the 'ID' column of the skullsweep_data DataFrame) or a list or tuple of exactly 3 floats giving the y (leftright), x (posteroanterior), and z (superoinferior) coordinates of the target, in this order.
	template : str
		Path to template (generally an anatomical image) to be used as background.
	text_output : bool
		Whether to print relevant output (computed enrty point coordinates and recommended insertion length) to the command line.
	xz_angle : float
		Desired angle of entry in the xz-plane (relative to the -z-axis).
	yz_angle : float
		Desired angle of entry in the yz-plane (relative to the -z-axis).

	Notes
	-----
	Some functions are imported in local scope to allow 2D plotting to function with minimal dependencies.
	"""

	try:
		from nilearn.plotting import plot_anat
	except ImportError:
		print(
			'You seem to be lacking “nilearn”, a module which we require for 3D plotting on top of a reference image - or one of its dependencies. '
			'Please make this package and its full dependency stack available, or use our background-less 2D plotting functionality instead.'
		)
		return False

	# Set References
	internal_references = df['reference'].unique()
	internal_reference = internal_references[0]
	if len(internal_references) > 1:
		print(
			'WARNING: The DataFrame you have passed to `stereotaxyz.plotting.yz()` contains rows referenced to multiple values, namely: "{}". '
			'We will assume that all values are referenced to {}. '
			'This means that some of the computations and/or the reference specification for the output may be wrong. '
			.format(references, reference)
		)
	if not reference:
		reference = internal_reference

	if reference != internal_reference:
		x_reference = df[df['ID']==reference]['leftright'].item()
		y_reference = df[df['ID']==reference]['posteroanterior'].item()
		z_reference = df[df['ID']==reference]['inferosuperior'].item()
	else:
		x_reference = 0
		y_reference = 0
		z_reference = 0

	template = path.abspath(path.expanduser(template))
	if not path.isfile(template) and 'DSURQEc_40micron_average.nii' in template:
		ni_data_dir = path.abspath(path.expanduser('~/.ni_data'))
		templates_dir = path.join(ni_data_dir,'templates')
		template = path.join(templates_dir,'DSURQEc_40micron_average.nii')
		if not path.isfile(template):
			print('The template you have specified cannot be found on your system. '
				'Luckily, we know where to get it from.\n'
				'We are currently trying to download it '
				'(this may take 2-3 minutes, but it only needs to be done once).')
			if not path.exists(ni_data_dir):
				makedirs(ni_data_dir)
			if not path.exists(templates_dir):
				makedirs(templates_dir)
			import urllib
			# Python 3/2 compatibility
			try:
				urllib.request.urlretrieve ("http://chymera.eu/ni_data/templates/DSURQEc_40micron_average.nii", template)
			except AttributeError:
				urllib.urlretrieve ("http://chymera.eu/ni_data/templates/DSURQEc_40micron_average.nii", template)

	if target:
		if type(target) is [tuple, list] and len(target) == 3:
			x_target, y_target, z_target = target
		elif isinstance(target, dict):
			x_target = target['leftright']
			y_target = target['posteroanterior']
			z_target = target['inferosuperior']
		else:
			x_target = df[df['ID']==target]['leftright'].item()
			y_target = df[df['ID']==target]['posteroanterior'].item()
			z_target = df[df['ID']==target]['inferosuperior'].item()
			target_coords = [(x_target, y_target, z_target)]

	if incision:
		try:
			x_incisison = incision['leftright']
			y_incisison = incision['posteroanterior']
			z_incisison = incision['inferosuperior']
		except TypeError:
			x_incision, y_incision, z_incision = incision
	else:
		x_incision = df[df['ID']=='incision']['leftright'].item()
		y_incision = df[df['ID']=='incision']['posteroanterior'].item()
		z_incision = df[df['ID']=='incision']['inferosuperior'].item()

	incision_coords = [(x_incision, y_incision, z_incision)]

	# Start actual plotting:
	if not custom_style:
		plt.style.use(path.join(THIS_PATH,'stereotaxyz.conf'))

	fig = plt.figure()
	plt.axis('equal')
	ax = plt.axes()

	# Plot Anatomy
	if axis_cut == 'x':
		display = plot_anat(
			anat_img=template,
			annotate=False,
			display_mode=axis_cut,
			draw_cross=False,
			cut_coords=(target_coords[0][0],),
			axes=ax,
			alpha=1.0,
			dim=0,
			black_bg=False,
			)
	elif axis_cut == 'yx':
		display = plot_anat(
			anat_img=template,
			annotate=False,
			display_mode=axis_cut,
			draw_cross=False,
			cut_coords=(target_coords[0][0],target_coords[0][1]),
			axes=ax,
			alpha=1.0,
			dim=0,
			black_bg=False,
			)

	# Calculate Screen-to-Anatomy resolution
	bbox = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
	width, height = bbox.width, bbox.height
	width *= fig.dpi
	height *= fig.dpi
	template_img = nib.load(template)
	template_x_resolution = template_img.shape[0]
	template_x_affine = template_img.affine[0,0]
	px_per_template_unit = abs(width/(template_x_resolution*template_x_affine))
	adjusted_marker_size = marker_size * px_per_template_unit

	# Create and Plot Skull Sweep Points
	skull_df = df[df['tissue']=='skull']
	skull_img = make_nii(skull_df, template=template, resolution=skull_point_size, target_coords=target_coords)
	skull_color = matplotlib.colors.ListedColormap([color_skull], name='skull_color')
	display.add_overlay(skull_img, cmap=skull_color)
	skull_legend = plt.scatter([],[], marker="s", color=color_skull, label='Skull')

	# Plot Target
	if target:
		display.add_markers(target_coords, marker_color=color_target, marker_size=adjusted_marker_size**1.8)
		target_legend = plt.scatter([],[], marker="o", color=color_target, label='Target')

	# Plot Incision
	display.add_markers(incision_coords, marker_color=color_incision, marker_size=adjusted_marker_size**1.8, marker="D")
	if reference != internal_reference:
		format_list = incision_coords[0]
		format_list = np.subtract(format_list, (x_reference, y_reference, z_reference))
		format_list = list(format_list)
		format_list.append(reference)
		incision_legend = plt.scatter([],[], marker="D", color=color_incision, label="Incision [LR/PA/IS={:.2f}/{:.2f}/{:.2f}mm]\n\t(relative to {})"
			.format(*format_list)
			.expandtabs()
			)
	else:
		incision_legend = plt.scatter([],[], marker="D", color=color_incision, label="Incision [LR/PA/IS={:.2f}/{:.2f}/{:.2f}mm]".format(*incision_coords[0]))

	# Create and Plot Inserion
	insertion_length = ((x_incision-x_target)**2+(y_incision-y_target)**2+(z_incision-z_target)**2)**(1/2.)
	x_increment = (x_incision-x_target)/float(insertion_length)
	y_increment = (y_incision-y_target)/float(insertion_length)
	z_increment = (z_incision-z_target)/float(insertion_length)
	insertion_t_resolution = 100
	insertion_t = np.linspace(0, insertion_length, insertion_t_resolution)
	insertion_df = pd.DataFrame(
			np.column_stack([
				insertion_t*x_increment+x_target,
				insertion_t*y_increment+y_target,
				insertion_t*z_increment+z_target,
				]),
                        columns=[
				'leftright',
				'posteroanterior',
				'inferosuperior',
				])
	insertion_img = make_nii(insertion_df, template=template, resolution=insertion_resolution, target_coords=target_coords)
	insertion_color = matplotlib.colors.ListedColormap([color_insertion], name='insertion_color')
	display.add_overlay(insertion_img, cmap=insertion_color)
	insertion_legend, = plt.plot([],[], color=color_insertion ,label='Insertion [{:.2f}mm]'.format(insertion_length),)

	#Create and Plot Skull Sweep Projection Points
	if color_projection:
		skull_df_ = deepcopy(skull_df)
		skull_df_['posteroanterior'] = skull_df_['posteroanterior (insertion projection)']
		skull_df_['inferosuperior'] = skull_df_['inferosuperior (insertion projection)']
		skull_df_['leftright'] = skull_df_['leftright (insertion projection)']
		projection_img = make_nii(skull_df_, template=template, resolution=skull_point_size)
		projection_color = matplotlib.colors.ListedColormap([color_projection], name='projection_color')
		display.add_overlay(projection_img, cmap=projection_color)

	# We create and place the legend.
	# The positioning may be fragile
	plt.legend(loc='lower right',bbox_to_anchor=(0.995, 0.005))
	plt.suptitle(figure_title.format(yz_angle,xz_angle), y=0.9)

	if save_as:
		save_as = path.abspath(path.expanduser(save_as))
		plt.savefig(save_as)

def make_nii(df_slice,
	template='/home/chymera/ni_data/templates/DSURQEc_40micron_average.nii',
	resolution=0.1,
	target_coords=False):
	"""Create a NIfTI based on a dataframe containing bregma-relative skullsweep points, and a bregma-origin template.
	"""

	template = nib.load(path.abspath(path.expanduser(template)))
	affine = template.affine
	affine_factor = [
		np.abs(affine[0,0]/float(resolution)),
		np.abs(affine[1,1]/float(resolution)),
		np.abs(affine[2,2]/float(resolution)),
		]
	affine[0,0] = affine[1,1] = affine[2,2] = resolution
	shape = [
		int(round(template.shape[0]*affine_factor[0])),
		int(round(template.shape[1]*affine_factor[1])),
		int(round(template.shape[2]*affine_factor[2])),
		]
	data = np.zeros(shape=tuple(shape))
	for ix, point in df_slice.iterrows():
		try:
			y = point['posteroanterior']
		except KeyError:
			try:
				y = -point['anteroposterior']
			except KeyError:
				y = 0
		try:
			x = point['leftright']
		except KeyError:
			try:
				x = -point['rightleft']
			except KeyError:
				x = 0
		try:
			z = point['inferosuperior']
		except KeyError:
			try:
				z = -point['superoinferior']
			except KeyError:
				z = 0
		new_x = (x-affine[0,3])/affine[0,0]
		new_x = int(round(new_x))
		new_y = (y-affine[1,3])/affine[1,1]
		new_y = int(round(new_y))
		new_z = (z-affine[2,3])/affine[2,2]
		new_z = int(round(new_z))
		# Awkward hack to get around nileaarn issue 1605:
		# https://github.com/nilearn/nilearn/issues/1605
		if target_coords:
			if not target_coords[0][1]*1.05 <= y <= target_coords[0][1]*0.95:
				data[new_x,new_y,new_z] = 1
		else:
			data[new_x,new_y,new_z] = 1

	new_image = nib.Nifti1Image(data, affine=affine)
	nib.save(new_image, '/home/chymera/lla.nii.gz')
	return new_image


