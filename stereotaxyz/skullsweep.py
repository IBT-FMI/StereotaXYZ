# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from os import path
from copy import deepcopy

def implant(angle, target, df,
	ax = False,
	color = 'c',
	plot_projections='all',
	):
	"""Calculate and print injection or implant entry pint and length rewuired to each a specified target at a specified angle.

	Parameters
	----------

	angle: int
		The desired angle of the implant or injection in degrees. Note that the angle value is defined as 0 if the implant heads in posterior to anterior, and 180 if it heads in anterior to posterior.
	"""

	real_angle = 180-angle
	df_ = deepcopy(df)
	resolution = 1000
	x_min = df['PA'].min()-1
	x_max = df['PA'].max()+1
	x = np.linspace(x_min,x_max,resolution)
	rad_angle = np.radians(real_angle)
	slope = np.tan(rad_angle)
	if isinstance(target, dict):
		x_offset = target['PA']
		y_offset = target['IS']
	else:
		x_offset = df_[df_['label']==target]['PA'].values[0]
		y_offset = df_[df_['label']==target]['IS'].values[0]
	intercept = -x_offset*slope + y_offset
	y = x*slope + intercept
	df_['IS '+str(angle)]=df_['PA']*slope + intercept
	if plot_projections == 'all':
		ax.scatter(df_[df_['tissue']=='skull']['PA'], df_[df_['tissue']=='skull']['IS '+str(angle)], color=color)
	elif plot_projections == 'best':
		df_['projection distance'] = df_['IS '+str(angle)]-df_['IS']
		closest = df_[df_['tissue']=='skull']['projection distance'].abs().min()
		pa_in = df_[df_['projection distance'].abs()==closest]['PA'].values[0]
		is_in = df_[df_['projection distance'].abs()==closest]['IS '+str(angle)].values[0]
		point_projection_hypothenuse = df_.loc[df_['projection distance'].abs()==closest, 'projection distance'].item()*np.sin(rad_angle)
		is_in -= np.sin(rad_angle)*point_projection_hypothenuse
		pa_in -= np.cos(rad_angle)*point_projection_hypothenuse
		implant_length = ((is_in-y_offset)**2+(pa_in-x_offset)**2)**(1/2.)
		ax.scatter(pa_in, is_in, color=color)
		print('For {}°:'.format(angle))
		print('Posteroanterior: {0:.2f}'.format(pa_in))
		print('Inferosuperior: {0:.2f}'.format(is_in))
		print('Implant Length: {0:.2f}'.format(implant_length))
	ax.plot(x,y,color=color)

def draw_anatomy(df,):
	"""Draw skull and brain ROI locations listed in a `pandas.DataFrame` object.

	Parameters
	----------

	df : pandas.DataFrame
		A `pandas.DataFrame` object which contains columns named "tissue", "PA", and "IS".
	"""
	plt.figure()
	plt.axis('equal')
	ax = plt.axes()

	ax.scatter(df['PA'], df['IS'], color='0.5')
	ax.scatter(df[df['tissue']=='brain']['PA'], df[df['tissue']=='brain']['IS'], color='y')
	return ax

def load_data(df,
	origin='bregma',
	):
	"""Load and process stereotactic and/or atlas data.

	Parameters
	----------
	origin : {"lambda", "bregma", interaural}
		Whether to make all coordinates relative to bregma, lambda, or the interaural midpoint.

	Notes
	-----

	Interaural reference is not yet supported.
	"""
	if isinstance(df, str):
		df = path.abspath(path.expanduser(df))
		df = pd.read_csv(df)
	if origin == 'bregma':
		df['PA, bregma'].fillna(df['PA, lambda']+df[df['ID']=='lambda']['PA, bregma'].values[0], inplace=True)
		df['IS, bregma'].fillna(df['IS, lambda']+df[df['ID']=='lambda']['IS, bregma'].values[0], inplace=True)
		df['PA'] = df['PA, bregma']
		df['IS'] = df['IS, bregma']
	elif origin == 'lambda':
		df['PA, lambda'].fillna(df['PA, bregma']+df[df['ID']=='bregma']['PA, lambda'].values[0], inplace=True)
		df['IS, lambda'].fillna(df['IS, bregma']+df[df['ID']=='bregma']['IS, lambda'].values[0], inplace=True)
		df['PA'] = df['PA, lambda']
		df['IS'] = df['IS, lambda']

	return df


df = load_data('~/data/stereotactic/skull_6465.csv', origin='bregma')
ax = draw_anatomy(df)
#implant(30,'VTA',df,ax,'b','best')
#implant(45,'VTA',df,ax,'c','best')
#implant(30,'DR',df,ax,'red','best')
implant(45,'DR',df,ax,'orange','best')

plt.show()

