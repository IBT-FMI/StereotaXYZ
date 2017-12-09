# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from os import path
from copy import deepcopy

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
	if stereotaxis_style_angle:
		xz_angle = xz_angle
		yz_angle = 90 + yz_angle
	df_ = deepcopy(df)
	xz_angle = np.radians(xz_angle)
	yz_angle = np.radians(yz_angle)
	composite_angle = np.arctan((np.tan(xz_angle)**2+np.tan(yz_angle)**2)**(1/2))
	if isinstance(target, dict):
		x_offset = target['leftright']
		y_offset = target['posteroanterior']
		z_offset = target['inferosuperior']
	else:
		x_offset = df_[df_['ID']==target]['leftright'].values[0]
		y_offset = df_[df_['ID']==target]['posteroanterior'].values[0]
		z_offset = df_[df_['ID']==target]['inferosuperior'].values[0]
	increment = [
		np.sin(xz_angle),
		np.sin(yz_angle),
		np.cos(xz_angle)*np.cos(yz_angle),
		]
	df_['projection t'] = (df_['leftright']-x_offset)*float(increment[0]) + (df_['posteroanterior']-y_offset)*float(increment[1]) + (df_['inferosuperior']-z_offset)*float(increment[2])
	df_['leftright (implant projection)'] = df_['projection t']*increment[0] + x_offset
	df_['posteroanterior (implant projection)'] = df_['projection t']*increment[1] + y_offset
	df_['inferosuperior (implant projection)'] = df_['projection t']*increment[2] + z_offset
	df_['projection distance'] = ((df_['leftright']-x_offset)**2 + (df_['posteroanterior']-y_offset)**2 + (df_['inferosuperior']-z_offset)**2 - df_['projection t']**2)**(1./2)
	closest = df_[df_['tissue']=='skull']['projection distance'].abs().min()
	posteroanterior = df_[df_['projection distance'].abs()==closest]['posteroanterior (implant projection)'].values[0]
	inferosuperior = df_[df_['projection distance'].abs()==closest]['inferosuperior (implant projection)'].values[0]
	leftright = df_[df_['projection distance'].abs()==closest]['leftright (implant projection)'].values[0]
	t = df_[df_['projection distance'].abs()==closest]['projection t'].values[0]
	references = df_['reference'].tolist()
	# Select the most frequent reference:
	reference = max(set(references), key=references.count)
	df_ = df_.append({
			'ID' : 'incision',
			'reference' : reference,
			'leftright' : leftright,
			'posteroanterior' : posteroanterior,
			'inferosuperior' : inferosuperior,
			'projection t' : t,
			},
		ignore_index=True)
	return increment, df_

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
	if not 'leftright' in df_referenced.columns:
		df_referenced['leftright'] = 0

	return df_referenced


def design(data_file, target, angle,
	):
	df = load_data('~/data/stereotactic/skull_6465.csv')
	ax = draw_anatomy()
	implant(angle,target,df,ax,'orange','best')
	plt.show()

