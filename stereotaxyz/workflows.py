# coding: utf-8

import matplotlib.pyplot as plt
from os import path
from stereotaxyz import plotting, skullsweep

def plot2d(data, target,
	angle=0,
	reference='bregma',
	resolution=1000,
	color_skull='gray',
	color_target='orange',
	color_insertion='c',
	color_incision='r',
	color_projection='',
	insertion_axis=True,
	save_as='',
	):

	data_file = path.abspath(path.expanduser(data))
	df = skullsweep.load_data(data_file, ultimate_reference=reference)

	increment, df = skullsweep.insert_by_angle(target, df, yz_angle=angle,)

	plotting.yz(df, target,
		angle=angle,
		save_as=save_as,
		resolution=resolution,
		color_skull=color_skull,
		color_target=color_target,
		color_insertion=color_insertion,
		color_incision=color_incision,
		color_projection=color_projection,
		insertion_axis=insertion_axis,
		)
	if not save_as:
		plt.show()

def plot3d(data, target,
	yz_angle=0,
	xz_angle=0,
	view='x',
	reference='bregma',
	save_as='',
	insertion_resolution=0.05,
	color_projection='',
	color_skull='#DDDDDD',
	color_incision='#FE2244',
	color_target='#FE9911',
	skull_point_size=0.2,
	marker_size=0.2,
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
	yz_angle : float
		Desired angle of entry in the yz-plane (relative to the -z-axis).
	xz_angle : float
		Desired angle of entry in the xz-plane (relative to the -z-axis).
	view : {'x','yx'}
		Specify the axes perpendicularly to which the image should be cut for display.
	save_as : str
		Path under which to save the output image.

	Notes
	-----
	Some functions are imported in local scope to allow 2D plotting to function with minimal dependencies.
	"""

	data_file = path.abspath(path.expanduser(data))
	df = skullsweep.load_data(data_file, ultimate_reference=reference)

	increment, df = skullsweep.insert_by_angle(target, df, yz_angle=yz_angle,)

	plotting.xyz(df, target,
		xz_angle=xz_angle,
		yz_angle=yz_angle,
		axis_cut=view,
		save_as=save_as,
		color_projection=color_projection,
		color_skull=color_skull,
		color_incision=color_incision,
		color_target=color_target,
		insertion_resolution=insertion_resolution,
		skull_point_size=skull_point_size,
		marker_size=marker_size,
		)
	if not save_as:
		plt.show()

def text(data, target,
	yz_angle=0,
	xz_angle=0,
	reference='bregma',
	):

	data_file = path.abspath(path.expanduser(data))
	df = skullsweep.load_data(data_file, ultimate_reference=reference)

	increment, df = skullsweep.insert_by_angle(target, df, yz_angle=yz_angle, xz_angle=xz_angle)

	x_target = df[df['ID']==target]['leftright'].item()
	y_target = df[df['ID']==target]['posteroanterior'].item()
	z_target = df[df['ID']==target]['inferosuperior'].item()

	x_incision = df[df['ID']=='incision']['leftright'].item()
	y_incision = df[df['ID']=='incision']['posteroanterior'].item()
	z_incision = df[df['ID']=='incision']['inferosuperior'].item()

	insertion_length = ((x_incision-x_target)**2+(y_incision-y_target)**2+(z_incision-z_target)**2)**(1/2.)
	print('You have selected:\n')
	print('\tTarget: "{}"'.format(target))
	print('\t\tLeftRight({}): \t\t{:.2f}'.format(reference, x_target))
	print('\t\tPosteroAnterior({}): \t{:.2f}'.format(reference, y_target))
	print('\t\tInferoSuperior({}): \t{:.2f}'.format(reference, z_target))
	print('\tEntry Angles:')
	print(u'\t\tXZ(from Posteroanterior axis): \t{:.0f}°'.format(xz_angle).encode('utf-8'))
	print(u'\t\tYZ(from Posteroanterior axis): \t{:.0f}°'.format(yz_angle).encode('utf-8'))
	print('')
	print('Given your skull points, you can best reach the target at the desired angle with:\n')
	print('\tIcision Site:')
	print('\t\tLeftRight({}): \t\t{:.2f}'.format(reference, x_incision))
	print('\t\tPosteroAnterior({}): \t{:.2f}'.format(reference, y_incision))
	print('\t\tInferoSuperior({}): \t{:.2f}'.format(reference, z_incision))
	print('\tInsertion Length: {:.2f}mm'.format(insertion_length))
