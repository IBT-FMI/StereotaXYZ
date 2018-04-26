# coding: utf-8

import matplotlib.pyplot as plt
from os import path
from stereotaxyz import plotting, skullsweep

def plot2d(data, target,
	pitch=0,
	internal_reference='bregma',
	resolution=1000,
	color_skull='gray',
	color_target='orange',
	color_insertion='c',
	color_incision='r',
	color_projection='',
	insertion_axis=True,
	save_as='',
	reference='',
	):

	data_file = path.abspath(path.expanduser(data))
	df = skullsweep.load_data(data_file, ultimate_reference=internal_reference)

	increment, df = skullsweep.insert_by_angle(target, df, pitch=angle,)

	plotting.yz(df, target,
		pitch=pitch,
		save_as=save_as,
		resolution=resolution,
		color_skull=color_skull,
		color_target=color_target,
		color_insertion=color_insertion,
		color_incision=color_incision,
		color_projection=color_projection,
		insertion_axis=insertion_axis,
		reference=reference,
		)
	if not save_as:
		plt.show()

def plot3d(data, target,
	pitch=0,
	yaw=0,
	view='x',
	internal_reference='bregma',
	save_as='',
	insertion_resolution=0.05,
	color_projection='',
	color_skull='#DDDDDD',
	color_incision='#FE2244',
	color_target='#FE9911',
	skull_point_size=0.2,
	marker_size=0.2,
	reference='',
	template='~/ni_data/templates/DSURQEc_40micron_average.nii',
	):
	"""Load StereotaXYZ-formatted skullsweep data and co-plot skull points together with target, implant, and incision coordinates.

	Parameters
	----------

	data : str
		Path to a StereotaXYZ-formatted skullsweep file.
	target : str or list or tuple
		Target identifier. Can either be a string (identifying a row via the 'ID' column of the skullsweep_data DataFrame) or a list or tuple of exactly 3 floats giving the y (leftright), x (posteroanterior), and z (superoinferior) coordinates of the target, in this order.
	skullsweep_data : str or pandas.DataFrame
		Path to a CSV file or `pandas.DataFrame` object containing skullsweep and optionally target coordinates.
		The data should include columns named 'ID', 'posteroanterior', 'superoinferior', 'reference', and 'tissue'.
	pitch : float
		Desired implant pitch (relative to the -z-axis).
	yaw : float
		Desired implatn yaw (relative to the -z-axis).
	view : {'x','yx'}
		Specify the axes perpendicularly to which the image should be cut for display.
	save_as : str
		Path under which to save the output image.
	reference : string, optional
		Referenc epoint relative to which to compute the coordinate specifications displayed int the figure legend.
		This value must be present once and only once on the 'ID' column of the dataframe passed to the `df` parameter.

	Notes
	-----
	Some functions are imported in local scope to allow 2D plotting to function with minimal dependencies.
	"""

	data_file = path.abspath(path.expanduser(data))
	df = skullsweep.load_data(data_file, ultimate_reference=internal_reference)

	increment, df = skullsweep.insert_by_angle(target, df, pitch=pitch,)

	plotting.xyz(df,
		axis_cut=view,
		color_projection=color_projection,
		color_skull=color_skull,
		color_incision=color_incision,
		color_target=color_target,
		insertion_resolution=insertion_resolution,
		marker_size=marker_size,
		reference=reference,
		save_as=save_as,
		skull_point_size=skull_point_size,
		target=target,
		yaw=yaw,
		pitch=pitch,
		template=template,
		)
	if not save_as:
		plt.show()

def text(data, target,
	pitch=0,
	yaw=0,
	internal_reference='bregma',
	reference='',
	):
	"""Return a text summary of the user-specified constraints for insertion and the computed best insertion length and incision site.

	Parameters
	----------

	data : str
		Path to a StereotaXYZ-formatted skullsweep file.
	reference : string, optional
		Referenc epoint relative to which to compute the coordinate specifications displayed int the figure legend.
		This value must be present once and only once on the 'ID' column of the dataframe passed to the `df` parameter.
	"""


	if not reference:
		reference = internal_reference

	data_file = path.abspath(path.expanduser(data))
	df = skullsweep.load_data(data_file, ultimate_reference=internal_reference)

	increment, df = skullsweep.insert_by_angle(target, df, pitch=pitch, yaw=yaw)

	if reference != internal_reference:
		x_reference = df[df['ID']==reference]['leftright'].item()
		y_reference = df[df['ID']==reference]['posteroanterior'].item()
		z_reference = df[df['ID']==reference]['inferosuperior'].item()
	else:
		x_reference = 0
		y_reference = 0
		z_reference = 0

	x_target = df[df['ID']==target]['leftright'].item() - x_reference
	y_target = df[df['ID']==target]['posteroanterior'].item() - y_reference
	z_target = df[df['ID']==target]['inferosuperior'].item() - z_reference

	x_incision = df[df['ID']=='incision']['leftright'].item() - x_reference
	y_incision = df[df['ID']=='incision']['posteroanterior'].item() - y_reference
	z_incision = df[df['ID']=='incision']['inferosuperior'].item() - z_reference

	insertion_length = ((x_incision-x_target)**2+(y_incision-y_target)**2+(z_incision-z_target)**2)**(1/2.)
	print('You have selected:\n')
	print('\tTarget: "{}"'.format(target))
	print('\t\tLeftRight({}): \t\t{:.2f}'.format(reference, x_target))
	print('\t\tPosteroAnterior({}): \t{:.2f}'.format(reference, y_target))
	print('\t\tInferoSuperior({}): \t{:.2f}'.format(reference, z_target))
	print('\tEntry Angles:')
	print(u'\t\tXZ(from Posteroanterior axis): \t{:.0f}°'.format(yaw).encode('utf-8'))
	print(u'\t\tYZ(from Posteroanterior axis): \t{:.0f}°'.format(pitch).encode('utf-8'))
	print('')
	print('Given your skull points, you can best reach the target at the desired angle with:\n')
	print('\tIcision Site:')
	print('\t\tLeftRight({}): \t\t{:.2f}'.format(reference, x_incision))
	print('\t\tPosteroAnterior({}): \t{:.2f}'.format(reference, y_incision))
	print('\t\tInferoSuperior({}): \t{:.2f}'.format(reference, z_incision))
	print('\tInsertion Length: {:.2f}mm'.format(insertion_length))
