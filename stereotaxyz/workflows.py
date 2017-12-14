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

	data_file = path.abspath(path.expanduser(data))
	df = skullsweep.load_data(data_file, ultimate_reference=reference)

	increment, df = skullsweep.insert_by_angle(target, df, yz_angle=yz_angle,)

	plotting.xyz(df, target,
		xz_angle=xz_angle,
		yz_angle=yz_angle,
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
	print(u'\t\tXZ(from Posteroanterior axis): \t{:.0f}°'.format(xz_angle))
	print(u'\t\tYZ(from Posteroanterior axis): \t{:.0f}°'.format(yz_angle))
	print('')
	print('Given your skull points, you can best reach the target at the desired angle with:\n')
	print('\tIcision Site:')
	print('\t\tLeftRight({}): \t\t{:.2f}'.format(reference, x_incision))
	print('\t\tPosteroAnterior({}): \t{:.2f}'.format(reference, y_incision))
	print('\t\tInferoSuperior({}): \t{:.2f}'.format(reference, z_incision))
	print('\tInsertion Length: {:.2f}mm'.format(insertion_length))
