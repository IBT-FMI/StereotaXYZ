# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from os import path
from copy import deepcopy

def _implant_by_angle(angle, target, df,
	ax = False,
	color = 'c',
	plot_projections='best',
	display=False,
	):
	"""Calculate and print injection or implant entry pint and length required to each a specified target at a specified angle.

	Parameters
	----------

	angle: int
		The desired angle of the implant or injection in degrees. Note that the angle value is defined as 0 if the implant heads in posterior to anterior, and 180 if it heads in anterior to posterior.
	"""

	if not ax and display:
		plt.figure()
		plt.axis('equal')
		ax = plt.axes()

	real_angle = 180-angle
	df_ = deepcopy(df)
	resolution = 1000
	x_min = df['posteroanterior'].min()-1
	x_max = df['posteroanterior'].max()+1
	x = np.linspace(x_min,x_max,resolution)
	rad_angle = np.radians(real_angle)
	slope = np.tan(rad_angle)
	if isinstance(target, dict):
		x_offset = target['posteroanterior']
		y_offset = target['inferosuperior']
	else:
		x_offset = df_[df_['ID']==target]['posteroanterior'].values[0]
		y_offset = df_[df_['ID']==target]['inferosuperior'].values[0]
	intercept = -x_offset*slope + y_offset
	y = x*slope + intercept
	df_['inferosuperior '+str(angle)]=df_['posteroanterior']*slope + intercept
	if plot_projections == 'all':
		if display:
			ax.scatter(df_[df_['tissue']=='skull']['posteroanterior'], df_[df_['tissue']=='skull']['inferosuperior '+str(angle)], color=color)
	elif plot_projections == 'best':
		df_['projection distance'] = df_['inferosuperior '+str(angle)]-df_['inferosuperior']
		closest = df_[df_['tissue']=='skull']['projection distance'].abs().min()
		pa_in = df_[df_['projection distance'].abs()==closest]['posteroanterior'].values[0]
		is_in = df_[df_['projection distance'].abs()==closest]['inferosuperior '+str(angle)].values[0]
		is_in -= np.sin(rad_angle)*closest
		pa_in -= np.cos(rad_angle)*closest
		implant_length = ((is_in-y_offset)**2+(pa_in-x_offset)**2)**(1/2.)
		if display:
			ax.scatter(pa_in, is_in, color=color)
		print('For {}°:'.format(angle))
		print('Posteroanterior: {0:.2f}'.format(pa_in))
		print('Inferosuperior: {0:.2f}'.format(is_in))
		print('Implant Length: {0:.2f}'.format(implant_length))
	if display:
		ax.plot(x,y,color=color)
	return slope, intercept, pa_in, is_in

def implant_by_angle(target, df,
	stereotaxis_style_angle=True,
	resolution=1000,
	xz_angle=0.,
	yz_angle=0.,
	):
	"""Calculate and print injection or implant entry pint and length required to each a specified target at a specified angle.

	Parameters
	----------

	angle: int
		The desired angle of the implant or injection in degrees. Note that the angle value is defined as 0 if the implant heads in posterior to anterior, and 180 if it heads in anterior to posterior.
	"""

	if stereotaxys_style_angle:
		xz_angle = 90 + zx_angle
		yz_angle = 90 + zx_angle
	df_ = deepcopy(df)
	xz_angle = np.radians(yz_angle)
	yz_angle = np.radians(yz_angle)
	composite_angle = np.arctan((np.tan(xz_angle)**2+np.tan(yz_angle)**2)**(1/2))
	slope = np.tan(rad_angle)
	if isinstance(target, dict):
		x_offset = target['leftright']
		y_offset = target['posteroanterior']
		z_offset = target['inferosuperior']
	else:
		x_offset = df_[df_['ID']==target]['leftright'].values[0]
		y_offset = df_[df_['ID']==target]['posteroanterior'].values[0]
		z_offset = df_[df_['ID']==target]['inferosuperior'].values[0]
	increment = [
		np.tan(xz_angle)*np.cos(composite_angle),
		np.tan(yz_angle)*np.cos(composite_angle),
		np.cos(composite_angle),
		]
	df_['leftright (implant projection)']=(df_['leftright']-z_offset)*increment[0]
	df_['posteroanterior (implant projection)']=df_['posteroanterior']-z_offset*increment[1]
	df_['inferosuperior (implant projection)']=df_['inferosuperior']-z_offset*increment[2]
	closest = df_[df_['tissue']=='skull']['projection distance'].abs().min()
	pa_in = df_[df_['projection distance'].abs()==closest]['posteroanterior'].values[0]
	is_in = df_[df_['projection distance'].abs()==closest]['inferosuperior '+str(angle)].values[0]
	is_in -= np.sin(rad_angle)*closest
	pa_in -= np.cos(rad_angle)*closest
	implant_length = ((is_in-z_offset)**2+(pa_in-y_offset)**2)**(1/2.)
	return slope, intercept, pa_in, is_in

def draw_anatomy(df,):
	"""Draw skull and brain ROI locations listed in a `pandas.DataFrame` object.

	Parameters
	----------

	df : pandas.DataFrame
		A `pandas.DataFrame` object which contains columns named "tissue", "posteroanterior", and "inferosuperior".
	"""
	plt.figure()
	plt.axis('equal')
	ax = plt.axes()

	ax.scatter(df['posteroanterior'], df['inferosuperior'], color='0.5')
	ax.scatter(df[df['tissue']=='brain']['posteroanterior'], df[df['tissue']=='brain']['inferosuperior'], color='y')
	return ax

def load_data(df,
	ultimate_reference='bregma',
	):
	"""Load and process stereotactic and/or atlas data.

	Parameters
	----------
	origin : {"lambda", "bregma", interaural}
		Whether to make all coordinates relative to bregma, lambda, or the interaural midpoint.
		What value you can use is contingent on the data you input.

	Notes
	-----

	Interaural reference is not yet supported.
	"""
	if isinstance(df, str):
		df = path.abspath(path.expanduser(df))
		df = pd.read_csv(df)
	df_referenced = pd.DataFrame([])
	for index, row in df.iterrows():
		df_add = deepcopy(df.ix[index])
		reference = row['reference']
		superoinferior_measured = row['superoinferior']
		superoinferior_correction = 0
		posteroanterior_measured = row['posteroanterior']
		posteroanterior_correction = 0
		while reference != ultimate_reference:
			superoinferior_correction_step = df[df['ID']==reference]['superoinferior'].item()
			superoinferior_correction += superoinferior_correction_step
			posteroanterior_correction_step = df[df['ID']==reference]['posteroanterior'].item()
			posteroanterior_correction += posteroanterior_correction_step
			reference = df[df['ID']==reference]['reference'].item()
		df_add['reference'] = reference
		df_add['superoinferior'] = superoinferior_measured + superoinferior_correction
		df_add['posteroanterior'] = posteroanterior_measured + posteroanterior_correction
		df_referenced = df_referenced.append(df_add)

	df_referenced['inferosuperior'] = -df_referenced['superoinferior']

	return df_referenced


def design(data_file, target, angle,
	):
	df = load_data('~/data/stereotactic/skull_6465.csv')
	ax = draw_anatomy()
	implant(angle,target,df,ax,'orange','best')
	plt.show()

